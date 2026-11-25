# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This project is a retrieval-augmented question answering system built around the `city_guides` corpus. The corpus contains structured Markdown travel guides for different towns and regional topics (transportation, accessibility, food, and seasonal travel). The system retrieves the most relevant guide sections for a question, checks whether the retrieved information is relevant enough to answer, and then generates a grounded response using only those documents. It can answer specific questions about places in the guides.

## Chunking Strategy

**Chunk size: One Markdown section per chunk**
**Overlap: None**

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->
     
     I chose a structure-based chunking strategy because the City Guides are long Markdown documents organized into labeled sections such as getting there, getting around, where to eat, and when to go. The starter's fixed-size chunker split sentences, words, and sections in the middle. My chunker instead splits each document at its `##` Markdown headings, merges the document introduction with the first section, and includes the document title in each later chunk so the place name is not lost during retrieval. I did not use overlap because each section is intended to represent a complete topic on its own.


## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

## Straightforward

**Thornby Wells** is the easiest town in the region. It is flat, compact, and
everything is within three minutes of everything else. Parking is free for two
hours anywhere in town and the station is central. The pump room and gardens
are level throughout.

**Marchwood** has a modern tram network with level boarding on all four lines,
running every 8 minutes on weekdays. The city museum and covered market are both
step-free. The distances between districts are the main consideration.

**Brightwater** is level along the river and through the centre. The mill museum
is step-free. The station is a 15-minute walk from campus on flat ground, or the
shuttle meets the four busiest arrivals.
```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
# Corry Vale

## When to go

May to September. Outside those months the pub in the third village closes, the farm shop reduces its hours, and several footpaths become genuinely boggy rather than merely wet. The road is not gritted above the second village and is impassable in snow.

```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
# Givens Mill

## Eat and drink

A tearoom attached to the mill, open 10 to 4 daily except Tuesdays, which sells bread made from the flour ground twenty metresaway and is the reason most people come. One pub, food served lunchtimes and Thursday to Saturday evenings.

```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
# Kestrelford

## Where to stay

Two inns on the square and a handful of rooms above the pubs. Booking ahead matters between May and September and not at all otherwise. There is no accommodation of any kind within four miles of the town in either direction.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
# Pellew Sands

## Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** Is the seafood at Halden Bay fresh?

**Answer:**

```
Yes, Halden Bay's seafood is genuinely fresh because the two harbour restaurants buy directly from boats that land in the early morning.

This comes from *guide_eating.md* and *guide_halden_bay.md*.

Sources retrieved: guide_eating.md, guide_halden_bay.md
```

**My relevance cutoff:** 0.65

I chose a cutoff of 0.65 because my five in-corpus questions had best distances from 0.2679 to 0.6003, while the five out-of-scope questions ranged from 0.8350 to 0.9968. This leaves a clear gap between supported and unsupported questions.

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
| What cities are the most accessible or walkable? | Yes | 0.6003 |
| Is the seafood at Halden Bay fresh? | Yes | 0.2679 |
| Where is Corry Vale's closest hospital? | Yes | 0.3020 |
| If I visit Elder Ness, will I see birds? | Yes | 0.3736 |
| How many people reside in Marchwood? | Yes | 0.4150 |
| What is the capital of Mongolia? | No | 0.8463 |
| How do I change the oil in a diesel engine? | No | 0.9032 |
| Who won the 1994 World Cup? | No | 0.9968 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8350 |
| How do I write a for loop in Rust? | No | 0.8365 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I used AI to review my five acceptance criteria by asking how each one could be tested using only the wording of the criterion. This helped me check whether the criteria were specific and measurable enough for someone else to evaluate. I kept the final criteria based on my own corpus.

**2.** I used AI to help me interpret the retrieval distance results from my five in-corpus questions and five out-of-scope questions. It helped me compare the two groups and think through where a relevance cutoff could go. I chose the final cutoff of 0.65 based on the actual distances from my own retrieval results.

**3.** In Unit 2, I used AI to help me review the results of my before evaluation and compare them against the acceptance criteria I had already written. This helped me notice that Criterion 5 was measuring exact wording because I had used full sentences for my `expects` values. I decided to revise the criterion and use shorter key phrases so the evaluation measured whether the correct information was present rather than whether the wording matched exactly.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks preserve complete sentences | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answers contain the expected information | 4 of 5 | 1/5 | 1/5 | 1/5 | MISSED |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

**Criterion 1 — Retrieved chunks contain the answer**

Produced by: `run_eval.py::main`  
Retrieval: `store.py::search`  
Chunks: `chunker.py::split_documents`

Question: `Is the seafood at Halden Bay fresh?`

```text
Best distance: 0.2679
Sources retrieved: guide_eating.md, guide_halden_bay.md

Yes, the seafood in Halden Bay is genuinely fresh because the two harbour restaurants buy directly from the boats that land in the early morning.

This comes from guide_eating.md and guide_halden_bay.md.
```

**Criterion 2 — Every answer names a source**

Produced by: `run_eval.py::main`

Question: `How many people reside in Marchwood?`

```text
According to the provided documents, Marchwood has a population of 180,000 people (guide_marchwood.md).
```

**Criterion 3 — Gate stops out-of-corpus questions**

Produced by: `run_eval.py::check_out_of_scope`

```text
What is the capital of Mongolia? — best distance 0.846 — refused
How do I change the oil in a diesel engine? — best distance 0.903 — refused
Who won the 1994 World Cup? — best distance 0.997 — refused
What is the recommended dosage of ibuprofen for a headache? — best distance 0.835 — refused
How do I write a for loop in Rust? — best distance 0.836 — refused

Gate refused 5 of 5.
```

**Criterion 4 — Chunks preserve complete sentences**

Produced by: `chunker.py::split_documents`

```text
# Corry Vale

## When to go

May to September. Outside those months the pub in the third village closes, the farm shop reduces its hours, and several footpaths become genuinely boggy rather than merely wet. The road is not gritted above the second village and is impassable in snow.
```

**Criterion 5 — Answers contain the expected information**

Produced by: `run_eval.py::main`

Question: `What cities are the most accessible or walkable?`

```text
Based on the provided documents, Thornby Wells is described as the region's most accessible town on foot, being flat, compact, and having level streets and gardens. Marchwood has a modern tram network with level boarding, step-free attractions, and a city museum and covered market that are step-free. Brightwater is also noted as level along the river and through the centre, with a step-free mill museum.

Files used: guide_walking.md and guide_accessibility.md
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | All 5 test questions retrieved the information needed to answer them in each run, which exceeded my target of at least 4 of 5. |
| 2 | Every answer names a source | MET | All 5 answers named at least one source document in all three runs, meeting my target of 5 of 5. |
| 3 | Gate stops out-of-corpus questions | MET | The relevance gate refused all 5 out-of-scope questions, exceeding my target of at least 4 of 5. |
| 4 | Chunks preserve complete sentences | MET | All 5 sampled chunks contained complete sentences without being cut off at the beginning or end, exceeding my target of at least 4 of 5. |
| 5 | Answers contain the expected information | MISSED | Only 1 of 5 answers consistently contained the exact `expects` value. I realized that I had written most of my `expects` values as complete sentences instead of short keywords or phrases, so answers that were factually correct were counted as misses when the model expressed the same information using different wording. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

     **Criterion 5 — Answers contain the expected information**

**Stage:** Evaluation / Generation

**Mechanism:** The system often produced factually correct answers, but most of my original `expects` values were written as complete sentences. Because the criterion checked whether the answer contained that exact wording, correct answers were counted as misses when the model phrased the same fact differently.

For example, the accessibility question expected a full sentence naming Thornby Wells, Marchwood, and Brightwater, while the generated answer correctly discussed those places using different wording. The failure was therefore caused by the way I defined and measured the expected answer rather than by retrieval or generation.

### Additional observation after revising Criterion 5

After correcting the Criterion 5 measurement issue, all five criteria were met. However, I noticed that the accessibility/walkability question had the highest valid retrieval distance at `0.6003`, compared with much lower distances for my other in-corpus questions.

**Stage:** Retrieval / relevance gate

**Mechanism:** The broad accessibility question produced a similarity distance fairly close to my `0.65` relevance cutoff. At the same time, the closest out-of-scope question had a much higher distance of `0.835`. This suggested that the relevance gate could potentially be tightened while still allowing the valid questions in my test set through.

## The Improvement

**What I changed:**  
I changed the `expects` values in `questions.py` from full-sentence answers to short keywords or phrases that represent the key fact each correct answer should contain.

**Why I picked it:**  
My before run showed that Criterion 5 was failing even when the generated answers were factually correct because the expected values were written as complete sentences. Shorter expected phrases make the check measure whether the answer contains the important fact instead of whether the model used exactly the same wording.

### System improvement

**What I changed:**  
I tightened the relevance cutoff from `0.65` to `0.62`.

**Why I picked it:**  
After correcting Criterion 5, all five criteria were met, but the accessibility/walkability question had the highest valid retrieval distance at `0.6003`. The closest out-of-scope question had a much higher distance of `0.835`. I wanted to test whether I could make the relevance gate stricter without rejecting any of my valid test questions.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks preserve complete sentences | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answers contain the expected information | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

The final after run used a relevance cutoff of `0.62`. The accessibility/walkability question still passed the gate with a best distance of `0.6003`, and all five out-of-scope questions were still refused.

**Did it help?**

The evaluation correction helped Criterion 5 measure what I originally intended, increasing its measured result from 1/5 to 5/5.

The actual system improvement did not increase the overall pass rates because all five criteria were already passing after the evaluation correction. However, tightening the relevance cutoff from `0.65` to `0.62` made the relevance gate stricter without reducing performance on my test set. All five valid questions still passed the gate, including the accessibility question at `0.6003`, while all five out-of-scope questions continued to be refused.

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->
After the final system change, all five criteria were met in all three runs, so there are no remaining misses against my current criteria. However, the accessibility/walkability question still has a relatively high best retrieval distance of `0.6003`, which is fairly close to the new `0.62` relevance cutoff.

If I continued improving the system, I would test more broad or differently worded questions before tightening the cutoff any further.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
I would write Criterion 5 differently from the beginning. Instead of checking whether an answer contains a full expected sentence, I would define each `expects` value as a short keyword or key phrase representing the fact that must appear in a correct answer. That would make the criterion test the correctness of the information rather than the model's exact wording.

---

## Capstone

**What This Extends**

This extends my Unit 1/2 system, **The Unofficial Guide**: a retrieval-augmented question answering system over the `city_guides` corpus (chunk by `##` section → embed locally with ChromaDB's `all-MiniLM-L6-v2` → retrieve top 5 → relevance gate at `0.62` → grounded answer from Gemini). Until now it only ever ran as one-off `python app.py ask` commands in my editor's terminal, and nothing it did was recorded anywhere except whatever I happened to copy out of the terminal. What's new is the operational layer: the HTTP service in `serve.py` now writes a structured log record for every request (including refused questions, bad input and errors), with timing per stage and the tokens each request used, and there's a documented single-command run path and a script that measures what one request costs.

**The Shape**

**Shape A — Deploy and instrument.** I'm adding the run path, the instrumentation (a JSON-lines log with named fields for every `/ask` request, written to `logs/requests.jsonl`), and the measurements that come out of it (latency and tokens per request, averaged over real runs). The retrieval, gate and answer logic stay exactly as they were at the end of Unit 2.

Out of scope — things I considered and decided not to do this unit:

- **Hosting it.** I'm taking Path B (local with logs). The system loads ChromaDB and a local embedding model, which is tight on a 512 MB free host, and hosting isn't what I want to spend the unit on.
- **Changing the pipeline.** I'm not touching the chunker, the `0.62` relevance cutoff, `TOP_K`, or the grounding prompt. If a number changes this unit, it should be because of something I measured, not because I retuned retrieval at the same time.
- **Failure hardening.** I'm not adding new timeouts or retry logic around the Gemini call (that's Shape B). I'm only making sure that when something fails, it leaves a log record instead of disappearing.
- **A dashboard or UI.** The log is a file I read back with a script, not a web page.

**Running It**

Path B — local with logs. The service starts with one command, `python serve.py`, which builds the index on a clean checkout if it's missing and then serves `POST /ask` and `GET /health` on `http://localhost:5000`. The exact setup, the environment it needs, and how to talk to it are in [`RUNNING.md`](RUNNING.md). The run record is `logs/requests.jsonl`, committed in this repo.

**Instrumentation**

Every `POST /ask` writes exactly one JSON object per line to `logs/requests.jsonl`. The logger is `runlog.py::write`; the record is assembled in `serve.py::ask`, with per-stage timings from `app.py::ask_pipeline` and token counts read off each Gemini response by `generate.py::_record_tokens`. Failures are logged on the same path as successes — a bad request or an exception writes a record before the error goes back to the caller.

| Field | What it holds |
|---|---|
| `ts` | ISO-8601 UTC timestamp when the request finished |
| `request_id` | 8-character id, also returned to the caller in the JSON response |
| `status` | `answered`, `refused` (gate said no), `bad_request` (no usable question), or `error` (an exception) |
| `http_status` | 200 / 400 / 500 — what the caller got |
| `question` / `answer` | what came in and what went out (answer truncated at 600 chars) |
| `sources`, `best_distance`, `threshold`, `top_k` | what retrieval found and what the gate compared it against |
| `duration_ms` | whole request, end to end, inside the server |
| `retrieval_ms`, `generation_ms` | the two stages that take time (`generation_ms` is null when the gate refused) |
| `model_calls`, `prompt_tokens`, `output_tokens`, `total_tokens`, `cache_hits` | what this one request cost, as reported by the service |
| `error_type`, `error`, `raw_body` | on failures: the exception and message, or the body that was rejected |
| `corpus`, `model` | which corpus and model served it |

Ten entries from my first real session (25 Nov 2026), copied unedited from `logs/requests.jsonl` — eight answered questions, one refusal, one rejected input:

```json
{"ts": "2026-11-25T17:24:11.099+00:00", "request_id": "145e0fd2", "route": "/ask", "corpus": "city_guides", "model": "gemini-3.5-flash-lite", "threshold": 0.62, "top_k": 5, "status": "answered", "http_status": 200, "question": "What cities are the most accessible or walkable?", "answer": "Based on the documents, Thornby Wells is described as the most accessible town on foot in the region (`guide_walking.md` and `guide_accessibility.md`), and the easiest town in the region as it is flat, compact, and everything is within three minutes of everything else (`guide_accessibility.md`). \n\nFiles used: `guide_walking.md` and `guide_accessibility.md`.", "sources": ["guide_accessibility.md", "guide_corry_vale.md", "guide_regional_transport.md", "guide_walking.md"], "best_distance": 0.6003, "retrieval_ms": 532.7, "generation_ms": 5619.1, "duration_ms": 6155.7, "model_calls": 1, "prompt_tokens": 824, "output_tokens": 85, "total_tokens": 909, "cache_hits": 0}
{"ts": "2026-11-25T17:24:28.538+00:00", "request_id": "8792416b", "route": "/ask", "corpus": "city_guides", "model": "gemini-3.5-flash-lite", "threshold": 0.62, "top_k": 5, "status": "answered", "http_status": 200, "question": "Where is Correy Vale's closest hospital?", "answer": "The nearest full hospital to Corry Vale is in Brightwater. \n\n(Source: `guide_corry_vale.md`)", "sources": ["guide_accessibility.md", "guide_corry_vale.md", "guide_thornby_wells.md", "guide_walking.md"], "best_distance": 0.3672, "retrieval_ms": 146.4, "generation_ms": 1020.1, "duration_ms": 1167.0, "model_calls": 1, "prompt_tokens": 552, "output_tokens": 28, "total_tokens": 580, "cache_hits": 0}
{"ts": "2026-11-25T17:25:16.197+00:00", "request_id": "b8a2d6e6", "route": "/ask", "corpus": "city_guides", "model": "gemini-3.5-flash-lite", "threshold": 0.62, "top_k": 5, "status": "answered", "http_status": 200, "question": "If I visit Elder Ness, will I see birds?", "answer": "Yes, you can see birds if you visit Elder Ness, as birds are the reason most visitors come, especially during the spring and autumn migration seasons (April to May and September to October). This information comes from `guide_elder_ness.md`.", "sources": ["guide_elder_ness.md"], "best_distance": 0.3736, "retrieval_ms": 125.1, "generation_ms": 45473.4, "duration_ms": 45598.9, "model_calls": 1, "prompt_tokens": 536, "output_tokens": 51, "total_tokens": 587, "cache_hits": 0}
{"ts": "2026-11-25T17:25:24.596+00:00", "request_id": "af44401e", "route": "/ask", "corpus": "city_guides", "model": "gemini-3.5-flash-lite", "threshold": 0.62, "top_k": 5, "status": "answered", "http_status": 200, "question": "How many people reside in Marchwood?", "answer": "Marchwood has 180,000 people (guide_marchwood.md).", "sources": ["guide_marchwood.md"], "best_distance": 0.415, "retrieval_ms": 108.7, "generation_ms": 6257.1, "duration_ms": 6366.1, "model_calls": 1, "prompt_tokens": 556, "output_tokens": 20, "total_tokens": 576, "cache_hits": 0}
{"ts": "2026-11-25T17:25:46.614+00:00", "request_id": "1d7ccf70", "route": "/ask", "corpus": "city_guides", "model": "gemini-3.5-flash-lite", "threshold": 0.62, "top_k": 5, "status": "answered", "http_status": 200, "question": "Is the seafood at Halden Bay fresh?", "answer": "Yes, Halden Bay's seafood is genuinely fresh because the two harbour restaurants buy directly from boats that land in the early morning. \n\nSources: `guide_eating.md` and `guide_halden_bay.md`.", "sources": ["guide_eating.md", "guide_halden_bay.md"], "best_distance": 0.2679, "retrieval_ms": 114.5, "generation_ms": 634.3, "duration_ms": 749.2, "model_calls": 1, "prompt_tokens": 677, "output_tokens": 49, "total_tokens": 726, "cache_hits": 0}
{"ts": "2026-11-25T17:25:49.999+00:00", "request_id": "d15af05a", "route": "/ask", "corpus": "city_guides", "model": "gemini-3.5-flash-lite", "threshold": 0.62, "top_k": 5, "status": "answered", "http_status": 200, "question": "Where is Correy Vale's closest hospital?", "answer": "The nearest full hospital to Corry Vale is in Brightwater. \n\n(Source: \n- `guide_corry_vale.md`\n- `guide_thornby_wells.md`)", "sources": ["guide_accessibility.md", "guide_corry_vale.md", "guide_thornby_wells.md", "guide_walking.md"], "best_distance": 0.3672, "retrieval_ms": 124.9, "generation_ms": 1209.2, "duration_ms": 1334.7, "model_calls": 1, "prompt_tokens": 552, "output_tokens": 42, "total_tokens": 594, "cache_hits": 0}
{"ts": "2026-11-25T17:25:52.962+00:00", "request_id": "2fb3f900", "route": "/ask", "corpus": "city_guides", "model": "gemini-3.5-flash-lite", "threshold": 0.62, "top_k": 5, "status": "answered", "http_status": 200, "question": "If I visit Elder Ness, will I see birds?", "answer": "Yes, you can see birds, as birds are one of the main reasons visitors come to Elder Ness, with spring (April to May) and autumn (September to October) being the migration seasons for them (guide_elder_ness.md). Additionally, there is a bird observatory that takes day visitors (guide_elder_ness.md).", "sources": ["guide_elder_ness.md"], "best_distance": 0.3736, "retrieval_ms": 131.4, "generation_ms": 777.8, "duration_ms": 909.7, "model_calls": 1, "prompt_tokens": 536, "output_tokens": 70, "total_tokens": 606, "cache_hits": 0}
{"ts": "2026-11-25T17:25:55.828+00:00", "request_id": "39a989af", "route": "/ask", "corpus": "city_guides", "model": "gemini-3.5-flash-lite", "threshold": 0.62, "top_k": 5, "status": "answered", "http_status": 200, "question": "How many people reside in Marchwood?", "answer": "Marchwood has a population of 180,000 people. \n\nSource: guide_marchwood.md", "sources": ["guide_marchwood.md"], "best_distance": 0.415, "retrieval_ms": 108.6, "generation_ms": 712.7, "duration_ms": 821.6, "model_calls": 1, "prompt_tokens": 556, "output_tokens": 26, "total_tokens": 582, "cache_hits": 0}
{"ts": "2026-11-25T17:31:32.209+00:00", "request_id": "f294443f", "route": "/ask", "corpus": "city_guides", "model": "gemini-3.5-flash-lite", "threshold": 0.62, "top_k": 5, "status": "refused", "http_status": 200, "question": "What is the capital of Mongolia?", "answer": "I don't have enough information about that.", "sources": [], "best_distance": 0.8463, "retrieval_ms": 107.3, "generation_ms": null, "duration_ms": 107.6, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cache_hits": 0}
{"ts": "2026-11-25T16:57:35.526+00:00", "request_id": "2d0cd8d6", "route": "/ask", "corpus": "city_guides", "model": "gemini-3.5-flash-lite", "threshold": 0.62, "top_k": 5, "status": "bad_request", "http_status": 400, "question": null, "answer": null, "error": "Send JSON with a question in it, like {\"question\": \"is the housing lottery random?\"}", "raw_body": "{}", "duration_ms": 0.3}
```

Failed runs from the same session. The first is a real configuration failure — my `.env` key was wrong for the first ten requests, and every one of them left a record with the reason. The other two are Gemini returning `503 UNAVAILABLE` (model overloaded) during the cost measurement; `generate.py` only retries on 429s, so these went straight to the caller as 500s:

```json
{"ts": "2026-11-25T16:54:05.989+00:00", "request_id": "f94dad51", "route": "/ask", "corpus": "city_guides", "model": "gemini-3.5-flash-lite", "threshold": 0.62, "top_k": 5, "status": "error", "http_status": 500, "question": "What cities are the most accessible or walkable?", "answer": null, "error_type": "ClientError", "error": "400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}", "duration_ms": 6151.8, "model_calls": 1, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cache_hits": 0}
{"ts": "2026-11-25T17:24:25.304+00:00", "request_id": "b351b1a8", "route": "/ask", "corpus": "city_guides", "model": "gemini-3.5-flash-lite", "threshold": 0.62, "top_k": 5, "status": "error", "http_status": 500, "question": "Is the seafood at Halden Bay fresh?", "answer": null, "error_type": "ServerError", "error": "503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}", "duration_ms": 12146.3, "model_calls": 1, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cache_hits": 0}
{"ts": "2026-11-25T17:25:43.817+00:00", "request_id": "f66fa9a7", "route": "/ask", "corpus": "city_guides", "model": "gemini-3.5-flash-lite", "threshold": 0.62, "top_k": 5, "status": "error", "http_status": 500, "question": "What cities are the most accessible or walkable?", "answer": null, "error_type": "ServerError", "error": "503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}", "duration_ms": 17190.2, "model_calls": 1, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cache_hits": 0}
```

Read the log back with `python tools/read_log.py` (counts by status, latency, where the time goes, tokens). Over that whole session: 52 records — 8 answered, 17 refused, 15 bad requests, 12 errors (10 invalid key, 2 × 503). Every request I sent has a record.

**What It Costs**

**Measured: about 645 tokens per answered question (≈599 in, ≈46 out), one model call, ≈$0.0003 at paid-tier prices. $0 on the free tier I actually use.**

How I measured it: started the service with the cache off (`$env:AI201_CACHE="0"; python serve.py`) and ran `python tools/measure_cost.py`, which sends my five in-corpus questions twice (10 requests) to `POST /ask`, then matches each response's `request_id` to its log record and averages the token counts the Gemini API reported for that request. Two of the ten hit a Gemini 503 and produced no tokens, so the average is over the **8** that answered: 4,789 prompt tokens and 371 output tokens in total → 598.6 in and 46.4 out per request.

Converted at the paid-tier price for `gemini-3.5-flash-lite` ($0.30 per 1M input, $2.50 per 1M output):

```
598.6 / 1,000,000 × $0.30  = $0.000180
 46.4 / 1,000,000 × $2.50  = $0.000116
                   per run ≈ $0.000296
```

A hundred people asking one question a day: 100 × $0.000296 = **$0.030/day**, about **$0.89 a month** (× 30). Refused questions cost nothing in tokens — the gate stops them before the model is called — so this is an upper bound for a mix of in- and out-of-scope questions.

Time is the other cost. Over the same 8 answered requests, the median was 1.25 s, but the mean was 7.9 s because one took 45.6 s; generation was 98% of the time (7.7 s mean) and retrieval about 0.17 s. Refusals took about 0.12 s.
