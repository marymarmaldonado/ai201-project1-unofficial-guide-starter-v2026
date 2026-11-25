#!/usr/bin/env python3
"""
Measure what one request costs, from real requests rather than a pricing page.

Start the service in one terminal WITH THE CACHE OFF (a cached answer costs
nothing and would make the number meaningless):

    Windows:      $env:AI201_CACHE="0"; python serve.py
    macOS/Linux:  AI201_CACHE=0 python serve.py

Then in a second terminal:

    python tools/measure_cost.py                 10 requests, the default
    python tools/measure_cost.py -n 20
    python tools/measure_cost.py --price-in 0.10 --price-out 0.40
                                                 also convert tokens to dollars,
                                                 using $ per 1M tokens you looked up

It sends your five in-corpus questions from questions.py (cycled to reach -n)
to POST /ask, then reads back the log records those requests wrote — matched
by request_id — and averages tokens and latency. Tokens come from the
service's own usage report on each response (generate.py::_record_tokens),
so they are measured, not estimated.
"""

import argparse
import json
import statistics
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import runlog  # noqa: E402
from questions import answered  # noqa: E402


def post(url, question, timeout):
    body = json.dumps({"question": question}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            status = resp.status
    except urllib.error.HTTPError as exc:
        data = json.loads(exc.read().decode("utf-8") or "{}")
        status = exc.code
    return status, data, (time.perf_counter() - started) * 1000


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-n", type=int, default=10, help="how many requests (default 10)")
    ap.add_argument("--url", default="http://localhost:5000")
    ap.add_argument("--timeout", type=float, default=120)
    ap.add_argument("--price-in", type=float, help="$ per 1M input tokens")
    ap.add_argument("--price-out", type=float, help="$ per 1M output tokens")
    args = ap.parse_args()

    questions = [q["question"] for q in answered()]
    if not questions:
        sys.exit("questions.py has no questions filled in.")

    ids = []
    print(f"Sending {args.n} requests to {args.url}/ask ...\n")
    for i in range(args.n):
        q = questions[i % len(questions)]
        status, data, client_ms = post(args.url + "/ask", q, args.timeout)
        rid = data.get("request_id")
        ids.append(rid)
        print(f"  {i + 1:>2}. {status}  {client_ms:7.0f} ms  [{rid}]  {q}")

    time.sleep(0.2)
    by_id = {r.get("request_id"): r for r in runlog.read()}
    recs = [by_id[i] for i in ids if i in by_id]
    missing = len(ids) - len(recs)

    answered_recs = [r for r in recs if r.get("status") == "answered"]
    cached = [r for r in answered_recs if r.get("cache_hits")]
    real = [r for r in answered_recs if not r.get("cache_hits")]

    print(f"\n{len(recs)} of {len(ids)} requests found in the log ({missing} missing).")
    print("status: " + ", ".join(
        f"{s}={sum(1 for r in recs if r.get('status') == s)}"
        for s in sorted({r.get('status') for r in recs})
    ))
    if cached:
        print(f"WARNING: {len(cached)} answer(s) came from the cache. Restart serve.py with AI201_CACHE=0.")
    if not real:
        sys.exit("No real (uncached) answered requests to measure.")

    p = [r["prompt_tokens"] for r in real]
    o = [r["output_tokens"] for r in real]
    t = [r["total_tokens"] for r in real]
    d = [r["duration_ms"] for r in real]
    calls = [r["model_calls"] for r in real]

    print(f"\nPer answered request, mean over n={len(real)} uncached requests:")
    print(f"  model calls    {statistics.mean(calls):.2f}")
    print(f"  prompt tokens  {statistics.mean(p):,.1f}   (min {min(p)}, max {max(p)})")
    print(f"  output tokens  {statistics.mean(o):,.1f}   (min {min(o)}, max {max(o)})")
    print(f"  total tokens   {statistics.mean(t):,.1f}")
    print(f"  server time    {statistics.mean(d):,.0f} ms (median {statistics.median(d):,.0f} ms)")

    if args.price_in is not None and args.price_out is not None:
        per = statistics.mean(p) / 1e6 * args.price_in + statistics.mean(o) / 1e6 * args.price_out
        print(f"\n  at ${args.price_in}/1M in and ${args.price_out}/1M out: ${per:.6f} per request")
        print(f"  100 people x 1 question/day: ${per * 100:.4f}/day, ${per * 100 * 30:.2f}/30 days")


if __name__ == "__main__":
    main()
