# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that contains the answer.

**Why this target:**

I chose 4 out of 5 because some information in the City Guides may appear in only one section or document, probably making it harder.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**

Since every answer should come from the documents in the corpus (and where I got the questions from) I expect the system to consistently identify where its information came from.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" — in at least 4 of 5 tries.


**Why this target:**

I chose 4 of 5 because the City Guides cover travel topics such as towns, transport, food, and accessibility, so an unrelated question may still share general words with a guide. I still want the gate to reject nearly all clearly unrelated questions instead of letting the model guess.

---

## 4. Chunks preserve + keep sentences complete

At least 4 of 5 sampled chunks begin and end with complete sentences rather than cutting a sentence in half.


**Why this target:**
The City Guides use headings followed by descriptive paragraphs, and an answer may depend on several sentences in one section. I want chunks to preserve those sentences so important information is not split awkwardly. I chose 4 out of 5 because a chunk boundary can occasionally fall near the middle of a paragraph.


---

## 5. Your choice


For at least 4 out of my 5 test questions, the final answer contains a word or phrase defined (set as expected) for that question in questions.py file.

**Why this target:**
The expects field represents a key fact that should appear in a correct answer. I chose 4 out of 5 because one answer may express the correct information using slightly different wording than what i wrote myself in the questions.py file.

> **Revised in Unit 2:** For at least 4 of my 5 test questions, the final answer contains the key fact represented by the `expects` value, even if the wording is different.
>
> **Why revised:** I originally wrote most of my `expects` values as complete sentences instead of short keywords or phrases. Because of that, factually correct answers were counted as misses when the model expressed the same information using different wording. The revised criterion measures whether the correct information is present instead of requiring an exact phrase match.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->

---

## Capstone criteria

## 1. Every trial request is observable

In each of 3 trials, at least 18 of 18 requests leave a matching structured log
record in `logs/trials_before.jsonl`, with the request ID returned to the caller
matching the record in the log.

**Why this target:** Observability is the central extension. Every request
category is included in the battery, so 18/18 catches missing success, refusal,
bad-input, and injected-failure records instead of only checking the happy path.

## 2. Real in-corpus requests complete successfully

In each of 3 trials, at least 4 of 5 real in-corpus questions return HTTP 200
with a generated answer rather than an HTTP 500 or a relevance refusal.

**Why this target:** The model can return transient 503s, so 5/5 would be
unreasonably strict for a hosted model. Four of five still requires repeated
successful end-to-end answers while leaving room for one real provider failure.

## 3. Out-of-scope requests are refused without model calls

In each of 3 trials, at least 5 of 5 out-of-scope questions return the exact
refusal `"I don't have enough information about that."`, with zero recorded
total tokens.

**Why this target:** The gate behavior is deterministic and should not spend
model tokens. Five out of five is strict because this is a fixed, already-measured
bad path rather than a model-generated fact.

## 4. Malformed input consistently becomes a 400

In each of 3 trials, at least 5 of 5 malformed requests return HTTP 400, leave
a `bad_request` log record, and produce no HTTP 500.

**Why this target:** A request with no usable question should be separated from
provider or server failures. The target is 5/5 because malformed input is
entirely under the application's control.

## 5. Injected provider failures are logged as errors

In each of 3 trials, all 3 injected failures—the invalid key, 503 overload, and
timeout—return a JSON error response and leave a matching log record with
`status: "error"` and an error message.

**Why this target:** The criterion tests the failure side of the operational
layer. It is strict at 3/3 because the run harness deliberately injects these
three cases, so a missing or unlogged error would show a real observability
gap rather than an external-model fluctuation.
