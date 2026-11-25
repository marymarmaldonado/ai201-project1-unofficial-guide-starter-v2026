#!/usr/bin/env python3
"""
The Unofficial Guide — the same pipeline, over HTTP.

    python serve.py                          run it locally on port 5000
    gunicorn serve:app                       run it the way a host runs it

Nothing new happens in this file. It is a wrapper: a request comes in, it
hands the question to `app.py::ask_pipeline` — the exact function the command
line uses — and hands the answer back as JSON. Retrieval, the relevance gate
and the grounded prompt all still live where they lived. If you change how
your system answers, you change it in those files and this one follows.

Two routes:

    POST /ask       {"question": "..."} in, the answer and its sources out
    GET  /health    is the service up, and is there an index to search

Why this exists: `app.py` runs once and exits, which is fine on your laptop
and impossible to deploy. A hosted service has to stay up and wait for
requests. This is the smallest thing that does that.

Capstone (unit 9): every /ask request now writes one structured record to
logs/requests.jsonl via runlog.py — timestamp, question, answer, status,
duration and per-stage timing, and the tokens the request used. Failures
(bad input, exceptions) are logged too, not just successes.
"""

import os
import time

from flask import Flask, jsonify, request

import config

app = Flask(__name__)


@app.get("/health")
def health():
    """Is the service up, and is there an index to search?

    Two different questions, and the second one is the one that bites. A
    freshly deployed service answers this route happily while every /ask
    returns "no index" — hosts give you no disk that survives a restart, so
    the index has to be built as part of getting the service up. Checking
    here means you find that out in one request instead of five.
    """
    from store import index_exists

    ready = index_exists(config.CORPUS)
    return jsonify(
        {
            "status": "ok",
            "corpus": config.CORPUS,
            "index_ready": ready,
            "detail": (
                "ready"
                if ready
                else "no index for this corpus — run `python app.py index`"
            ),
        }
    )


@app.post("/ask")
def ask():
    """One question in, one grounded answer out — and one log record.

    A refused question is a 200, not an error. The gate refusing is your
    system working — it is an answer, and the JSON says so with
    `"refused": true` so whatever calls this can tell the two apart.

    Capstone: every path through this function writes exactly one record to
    the run log (runlog.py) — answered, refused, bad input, or a crash — with
    how long it took and how many tokens it used. The response carries the
    same request_id so a reply can be matched to its log line.
    """
    import generate
    import runlog
    from app import ask_pipeline

    started = time.perf_counter()
    request_id = runlog.new_request_id()
    calls_before = generate.call_count()
    tokens_before = generate.token_counts()
    cache_before = generate.cache_hit_count()

    base = {
        "request_id": request_id,
        "route": "/ask",
        "corpus": config.CORPUS,
        "model": config.MODEL,
        "threshold": config.THRESHOLD,
        "top_k": config.TOP_K,
    }

    def usage_since_start():
        after = generate.token_counts()
        return {
            "model_calls": generate.call_count() - calls_before,
            "prompt_tokens": after["prompt"] - tokens_before["prompt"],
            "output_tokens": after["output"] - tokens_before["output"],
            "total_tokens": after["total"] - tokens_before["total"],
            "cache_hits": generate.cache_hit_count() - cache_before,
        }

    def elapsed_ms():
        return round((time.perf_counter() - started) * 1000, 1)

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        payload = {}
    raw_question = payload.get("question")
    question = raw_question.strip() if isinstance(raw_question, str) else ""

    if not question:
        message = (
            "Send JSON with a question in it, like "
            '{"question": "is the housing lottery random?"}'
        )
        runlog.write(
            {
                **base,
                "status": "bad_request",
                "http_status": 400,
                "question": None,
                "answer": None,
                "error": message,
                "raw_body": request.get_data(as_text=True)[:200],
                "duration_ms": elapsed_ms(),
            }
        )
        return jsonify({"error": message, "request_id": request_id}), 400

    try:
        outcome = ask_pipeline(question, corpus=config.CORPUS)
    except Exception as exc:  # noqa: BLE001 — a reader gets this, not a traceback
        runlog.write(
            {
                **base,
                "status": "error",
                "http_status": 500,
                "question": question,
                "answer": None,
                "error_type": type(exc).__name__,
                "error": str(exc)[:500],
                "duration_ms": elapsed_ms(),
                **usage_since_start(),
            }
        )
        return (
            jsonify(
                {"error": f"{type(exc).__name__}: {exc}", "request_id": request_id}
            ),
            500,
        )

    timings = outcome.get("timings") or {}
    runlog.write(
        {
            **base,
            "status": "refused" if outcome["refused"] else "answered",
            "http_status": 200,
            "question": question,
            "answer": outcome["answer"],
            "sources": outcome["sources"],
            "best_distance": round(outcome["best_distance"], 4),
            "retrieval_ms": timings.get("retrieval_ms"),
            "generation_ms": timings.get("generation_ms"),
            "duration_ms": elapsed_ms(),
            **usage_since_start(),
        }
    )

    return jsonify(
        {
            "request_id": request_id,
            "question": question,
            "answer": outcome["answer"],
            "refused": outcome["refused"],
            "sources": outcome["sources"],
            "best_distance": round(outcome["best_distance"], 4),
            "threshold": outcome["threshold"],
            "corpus": config.CORPUS,
        }
    )


def main():
    # Hosts tell you which port to listen on through PORT, and they expect you
    # on 0.0.0.0. Binding 127.0.0.1 instead works perfectly on your laptop and
    # then answers nothing at all once deployed, because the host's router
    # can't reach a socket that only accepts connections from inside the
    # container. It is the single most common way a first deploy "succeeds"
    # and is unreachable.
    port = int(os.getenv("PORT", "5000"))

    # Debug mode reloads on save, which is handy, and prints a console that
    # runs arbitrary code, which is not something to leave switched on where
    # strangers can reach it. Off unless you ask for it.
    debug = os.getenv("AI201_DEBUG", "0") == "1"

    print(f"Serving The Unofficial Guide on http://localhost:{port}")
    print(f"Corpus: {config.CORPUS}    (Ctrl-C to stop)\n")
    print("Try it from another terminal:\n")
    print(f"  curl http://localhost:{port}/health")
    print(
        f"  curl -X POST http://localhost:{port}/ask \\\n"
        f"    -H 'Content-Type: application/json' \\\n"
        f"    -d '{{\"question\": \"is the housing lottery random?\"}}'\n"
    )

    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
