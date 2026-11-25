#!/usr/bin/env python3
"""
Read the run log back and summarise it — no new code needed to ask questions
about a run that already happened.

    python tools/read_log.py                    summary of the whole log
    python tools/read_log.py --last 12          only the last 12 records
    python tools/read_log.py --since 2026-11-25T16:00
    python tools/read_log.py --tail 10          print the raw last 10 lines
    python tools/read_log.py --status error     only one kind of record

The summary is what the README's Instrumentation and What It Costs sections
are built from: counts by status, latency percentiles, tokens per answered
request.
"""

import argparse
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import runlog  # noqa: E402


def pct(values, p):
    if not values:
        return None
    values = sorted(values)
    k = max(0, min(len(values) - 1, round(p / 100 * (len(values) - 1))))
    return values[k]


def fmt(x, unit=""):
    return "—" if x is None else f"{x:,.1f}{unit}"


def select(records, args):
    if args.since:
        records = [r for r in records if str(r.get("ts", "")) >= args.since]
    if args.status:
        records = [r for r in records if r.get("status") == args.status]
    if args.last:
        records = records[-args.last:]
    return records


def summarise(records):
    print(f"log file: {runlog.LOG_PATH}")
    print(f"records:  {len(records)}")
    if not records:
        return
    print(f"from {records[0].get('ts')}  to  {records[-1].get('ts')}\n")

    by_status = {}
    for r in records:
        by_status[r.get("status", "?")] = by_status.get(r.get("status", "?"), 0) + 1
    print("by status: " + ", ".join(f"{k}={v}" for k, v in sorted(by_status.items())))

    for label, group in [
        ("all requests", records),
        ("answered", [r for r in records if r.get("status") == "answered"]),
        ("refused", [r for r in records if r.get("status") == "refused"]),
    ]:
        d = [r["duration_ms"] for r in group if isinstance(r.get("duration_ms"), (int, float))]
        if not d:
            continue
        print(
            f"\nlatency, {label} (n={len(d)}): "
            f"mean {fmt(statistics.mean(d), ' ms')}, "
            f"median {fmt(pct(d, 50), ' ms')}, "
            f"p90 {fmt(pct(d, 90), ' ms')}, "
            f"max {fmt(max(d), ' ms')}"
        )

    answered = [r for r in records if r.get("status") == "answered"]
    if answered:
        ret = [r["retrieval_ms"] for r in answered if isinstance(r.get("retrieval_ms"), (int, float))]
        gen = [r["generation_ms"] for r in answered if isinstance(r.get("generation_ms"), (int, float))]
        tot = [r["duration_ms"] for r in answered if isinstance(r.get("duration_ms"), (int, float))]
        if ret and gen and tot:
            mr, mg, mt = statistics.mean(ret), statistics.mean(gen), statistics.mean(tot)
            print(
                f"\nwhere the time goes, answered (mean): retrieval {fmt(mr, ' ms')} "
                f"({mr / mt:.0%}), generation {fmt(mg, ' ms')} ({mg / mt:.0%}), "
                f"other {fmt(mt - mr - mg, ' ms')} ({(mt - mr - mg) / mt:.0%})"
            )

        real = [r for r in answered if not r.get("cache_hits")]
        cached = len(answered) - len(real)
        if real:
            p = [r.get("prompt_tokens", 0) for r in real]
            o = [r.get("output_tokens", 0) for r in real]
            print(
                f"\ntokens per answered request (n={len(real)}, cache misses only): "
                f"prompt mean {statistics.mean(p):,.1f}, output mean {statistics.mean(o):,.1f}, "
                f"total mean {statistics.mean([a + b for a, b in zip(p, o)]):,.1f}"
            )
        if cached:
            print(f"  ({cached} answered request(s) came from the cache and cost no tokens — excluded)")

    errors = [r for r in records if r.get("status") == "error"]
    for r in errors[-5:]:
        print(f"\nerror {r.get('request_id')}: {r.get('error_type')}: {str(r.get('error'))[:160]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--last", type=int)
    ap.add_argument("--since", help="ISO timestamp prefix, e.g. 2026-11-25T16:00")
    ap.add_argument("--status")
    ap.add_argument("--tail", type=int, help="print the raw JSON of the last N selected records")
    args = ap.parse_args()

    records = select(runlog.read(), args)
    if args.tail:
        for r in records[-args.tail:]:
            print(json.dumps(r, ensure_ascii=False))
        return
    summarise(records)


if __name__ == "__main__":
    main()
