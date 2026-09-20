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
