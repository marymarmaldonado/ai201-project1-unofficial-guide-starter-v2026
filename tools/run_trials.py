#!/usr/bin/env python3
"""
Capstone trials: run the same battery of requests through the service three
times, changing nothing in between, and write what happened to results/.

    python tools/run_trials.py --label before
    python tools/run_trials.py --label after --trials 3

Runs IN-PROCESS through serve.py's real /ask handler (Flask's test client), so
every request takes the same path a real HTTP request does — handler, pipeline,
gate, Gemini, run log — without needing a second terminal. The response cache
is forced off: three trials are three real sets of answers.

Each trial sends four groups of requests:

    in_corpus      the five QUESTIONS in questions.py        (real Gemini calls)
    out_of_scope   the five OUT_OF_SCOPE in questions.py     (should be refused)
    bad_input      five malformed requests                    (should be 400s)
    injected       three generation failures forced on purpose: an invalid
                   key, a 503 "model overloaded", and a timeout — the model
                   client is swapped for one that raises, for these three only

For every request it records the HTTP status, the response, and whether a log
record with the same request_id was written. Trial log records go to
logs/trials_<label>.jsonl so they don't mix with the session log.

The output file is raw measurements per trial. Which of these numbers your
criteria use, and what counts as MET, is decided in criteria.md — not here.
"""

import argparse
import json
import os
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

BAD_INPUTS = [
    ("empty object", {"json": {}}),
    ("empty question", {"json": {"question": ""}}),
    ("whitespace question", {"json": {"question": "   "}}),
    ("question is a number", {"json": {"question": 42}}),
    ("body is not JSON", {"data": "this is not json", "content_type": "application/json"}),
]

INJECTED = [
    ("invalid API key", lambda: RuntimeError("400 INVALID_ARGUMENT. API key not valid. (injected by run_trials)")),
    ("503 model overloaded", lambda: RuntimeError("503 UNAVAILABLE. This model is currently experiencing high demand. (injected by run_trials)")),
    ("timeout", lambda: TimeoutError("The read operation timed out (injected by run_trials)")),
]


class _Raiser:
    """Stands in for the Gemini client and raises the error it was given."""

    def __init__(self, make_exc):
        self.models = self
        self._make = make_exc

    def generate_content(self, **_):
        raise self._make()


def run_trial(client, generate, questions, out_of_scope, log_ids_before):
    rows = []

    def send(group, label, expects=None, **kw):
        kw.setdefault("json", None)
        if kw["json"] is None:
            kw.pop("json")
        started = time.perf_counter()
        resp = client.post("/ask", **kw)
        client_ms = (time.perf_counter() - started) * 1000
        try:
            body = resp.get_json(silent=True) or {}
        except Exception:  # noqa: BLE001
            body = {}
        rows.append(
            {
                "group": group,
                "label": label,
                "http_status": resp.status_code,
                "request_id": body.get("request_id"),
                "refused": body.get("refused"),
                "answer": body.get("answer"),
                "error": body.get("error"),
                "sources": body.get("sources"),
                "best_distance": body.get("best_distance"),
                "expects": expects,
                "client_ms": round(client_ms, 1),
            }
        )

    for q in questions:
        send("in_corpus", q["question"], expects=q.get("expects"), json={"question": q["question"]})
    for q in out_of_scope:
        send("out_of_scope", q, json={"question": q})
    for label, kw in BAD_INPUTS:
        send("bad_input", label, **kw)

    real_get_client = generate._get_client
    try:
        for (label, make_exc), q in zip(INJECTED, questions):
            generate._get_client = lambda make_exc=make_exc: _Raiser(make_exc)
            send("injected", f"{label} — {q['question']}", json={"question": q["question"]})
    finally:
        generate._get_client = real_get_client

    return rows


def attach_log(rows, records):
    by_id = {r.get("request_id"): r for r in records}
    for row in rows:
        rec = by_id.get(row["request_id"])
        row["logged"] = rec is not None
        row["log_status"] = rec.get("status") if rec else None
        for k in ("duration_ms", "retrieval_ms", "generation_ms", "prompt_tokens", "output_tokens", "total_tokens", "error_type"):
            row[k] = rec.get(k) if rec else None
        if row["expects"]:
            row["expects_found"] = bool(row["answer"]) and row["expects"].lower() in row["answer"].lower()
    return rows


def summary(rows):
    def grp(g):
        return [r for r in rows if r["group"] == g]

    out = {}
    out["log_records_written"] = f"{sum(r['logged'] for r in rows)}/{len(rows)}"
    ic = grp("in_corpus")
    out["in_corpus_200"] = f"{sum(r['http_status'] == 200 and not r['refused'] for r in ic)}/{len(ic)}"
    out["in_corpus_expects_found"] = f"{sum(bool(r.get('expects_found')) for r in ic)}/{len(ic)}"
    out["in_corpus_has_sources"] = f"{sum(bool(r['sources']) for r in ic)}/{len(ic)}"
    d = [r["duration_ms"] for r in ic if isinstance(r.get("duration_ms"), (int, float)) and r["log_status"] == "answered"]
    if d:
        out["in_corpus_ms_median"] = round(statistics.median(d))
        out["in_corpus_ms_max"] = round(max(d))
        for s in (2000, 3000, 5000, 10000):
            out[f"in_corpus_under_{s // 1000}s"] = f"{sum(x < s for x in d)}/{len(ic)}"
    t = [r["total_tokens"] for r in ic if r["log_status"] == "answered" and r.get("total_tokens")]
    if t:
        out["in_corpus_tokens_mean"] = round(statistics.mean(t), 1)
        out["in_corpus_tokens_max"] = max(t)
    oos = grp("out_of_scope")
    out["out_of_scope_refused"] = f"{sum(bool(r['refused']) for r in oos)}/{len(oos)}"
    od = [r["duration_ms"] for r in oos if isinstance(r.get("duration_ms"), (int, float))]
    if od:
        out["out_of_scope_ms_max"] = round(max(od))
    out["out_of_scope_zero_tokens"] = f"{sum((r.get('total_tokens') or 0) == 0 for r in oos)}/{len(oos)}"
    bi = grp("bad_input")
    out["bad_input_400"] = f"{sum(r['http_status'] == 400 for r in bi)}/{len(bi)}"
    out["bad_input_500"] = f"{sum(r['http_status'] == 500 for r in bi)}/{len(bi)}"
    out["bad_input_logged"] = f"{sum(r['logged'] for r in bi)}/{len(bi)}"
    inj = grp("injected")
    out["injected_logged_as_error"] = f"{sum(r['log_status'] == 'error' for r in inj)}/{len(inj)}"
    out["injected_status_codes"] = ",".join(str(r["http_status"]) for r in inj)
    out["injected_has_error_message"] = f"{sum(bool(r['error']) for r in inj)}/{len(inj)}"
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--label", required=True, help="before / after — goes in the file names")
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--pause", type=float, default=5.0, help="seconds between trials")
    args = ap.parse_args()

    log_path = ROOT / "logs" / f"trials_{args.label}.jsonl"
    os.environ["AI201_LOG_PATH"] = str(log_path)
    os.environ["AI201_CACHE"] = "0"

    import config

    config.CACHE_ENABLED = False
    import generate
    import runlog
    import serve
    from questions import OUT_OF_SCOPE, answered
    from store import index_exists

    if not index_exists(config.CORPUS):
        sys.exit("No index yet. Run `python serve.py` once (it builds it), or `python app.py index`.")

    questions = answered()
    client = serve.app.test_client()
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    all_rows = []

    for t in range(1, args.trials + 1):
        print(f"\n=== trial {t} of {args.trials} ===")
        rows = run_trial(client, generate, questions, OUT_OF_SCOPE, None)
        for r in rows:
            r["trial"] = t
            print(f"  {r['group']:<13} {r['http_status']}  {r['client_ms']:>8.0f} ms  {r['label'][:60]}")
        all_rows.extend(rows)
        if t < args.trials:
            time.sleep(args.pause)

    time.sleep(0.2)
    attach_log(all_rows, runlog.read(log_path))

    summaries = {t: summary([r for r in all_rows if r["trial"] == t]) for t in range(1, args.trials + 1)}
    keys = list(summaries[1].keys())
    for s in summaries.values():
        for k in s:
            if k not in keys:
                keys.append(k)

    lines = [
        f"# Capstone trials — {args.label}",
        "",
        f"Run {stamp}, {args.trials} trials, cache off, model `{config.MODEL}`, threshold `{config.THRESHOLD}`.",
        f"Produced by `tools/run_trials.py::main`; log records in `{log_path.relative_to(ROOT).as_posix()}`.",
        "",
        "## Measurements per trial",
        "",
        "| Measure | " + " | ".join(f"Trial {t}" for t in summaries) + " |",
        "|---|" + "---|" * len(summaries),
    ]
    for k in keys:
        lines.append(f"| `{k}` | " + " | ".join(str(summaries[t].get(k, "—")) for t in summaries) + " |")
    lines += ["", "## Every request", ""]
    lines += ["| Trial | Group | Request | HTTP | Logged as | ms | Tokens | Detail |", "|---|---|---|---|---|---|---|---|"]
    for r in all_rows:
        detail = r.get("error") or (r.get("answer") or "")
        detail = str(detail).replace("|", "/").replace("\n", " ")[:120]
        lines.append(
            f"| {r['trial']} | {r['group']} | {r['label'][:55]} | {r['http_status']} | {r['log_status']} | "
            f"{r.get('duration_ms') if r.get('duration_ms') is not None else '—'} | {r.get('total_tokens') or 0} | {detail} |"
        )
    out = ROOT / "results" / f"capstone_{stamp}_{args.label}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ROOT / "results" / f"capstone_{stamp}_{args.label}.json").write_text(
        json.dumps({"summaries": summaries, "rows": all_rows}, indent=2, default=str), encoding="utf-8"
    )

    print("\n" + "\n".join(lines[7:7 + 2 + len(keys)]))
    print(f"\nWrote {out.relative_to(ROOT)}")
    print(generate.usage())


if __name__ == "__main__":
    main()
