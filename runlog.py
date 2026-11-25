"""
Structured run log for The Unofficial Guide (capstone, Shape A).

Every request the service handles becomes ONE line in a JSON-lines file:
one JSON object per line, with named fields, so a run can be read back and
counted later without re-running anything.

    logs/requests.jsonl      (override with AI201_LOG_PATH)

Fields every record carries:

    ts             ISO-8601 UTC timestamp, when the request finished
    request_id     short random id, also returned to the caller
    route          which endpoint ("/ask")
    status         "answered" | "refused" | "bad_request" | "error"
    http_status    the status code the caller got
    question       what came in (None if there wasn't one)
    answer         what went out (truncated to ANSWER_MAX chars)
    duration_ms    wall-clock time for the whole request, end to end

Plus, when they apply: best_distance, threshold, sources, retrieval_ms,
generation_ms, model_calls, prompt_tokens, output_tokens, total_tokens,
cache_hits, model, corpus, error_type, error, raw_body.

Read it back with:   python tools/read_log.py
"""

import json
import os
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

import config

LOG_PATH = Path(os.getenv("AI201_LOG_PATH", str(config.ROOT / "logs" / "requests.jsonl")))
ANSWER_MAX = 600

_lock = threading.Lock()


def new_request_id() -> str:
    return uuid.uuid4().hex[:8]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def write(record: dict) -> None:
    """Append one record. Never raises: logging must not take the service down.

    If the write itself fails, the failure goes to stderr so it is at least
    visible in the terminal — a log that silently stops is the one failure a
    log can't record about itself.
    """
    rec = {"ts": now_iso(), **record}
    answer = rec.get("answer")
    if isinstance(answer, str) and len(answer) > ANSWER_MAX:
        rec["answer"] = answer[:ANSWER_MAX] + "…"
    try:
        line = json.dumps(rec, ensure_ascii=False, default=str)
        with _lock:
            LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with LOG_PATH.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
                f.flush()
    except Exception as exc:  # noqa: BLE001
        import sys

        print(f"[runlog] could not write log record: {exc!r}", file=sys.stderr, flush=True)


def read(path: Path | None = None) -> list[dict]:
    """Every record in the log, oldest first. Skips (and counts) bad lines."""
    path = path or LOG_PATH
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            records.append({"status": "corrupt_line", "raw": line[:200]})
    return records
