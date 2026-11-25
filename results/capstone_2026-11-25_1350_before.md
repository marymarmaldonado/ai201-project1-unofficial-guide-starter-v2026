# Capstone trials — before

Run 2026-11-25_1350, 3 trials, cache off, model `gemini-3.5-flash-lite`, threshold `0.62`.
Produced by `tools/run_trials.py::main`; log records in `logs/trials_before.jsonl`.

## Measurements per trial

| Measure | Trial 1 | Trial 2 | Trial 3 |
|---|---|---|---|
| `log_records_written` | 18/18 | 18/18 | 18/18 |
| `in_corpus_200` | 5/5 | 3/5 | 5/5 |
| `in_corpus_expects_found` | 5/5 | 2/5 | 5/5 |
| `in_corpus_has_sources` | 5/5 | 3/5 | 5/5 |
| `in_corpus_ms_median` | 811 | 2729 | 1632 |
| `in_corpus_ms_max` | 6222 | 2861 | 15336 |
| `in_corpus_under_2s` | 4/5 | 1/5 | 3/5 |
| `in_corpus_under_3s` | 4/5 | 3/5 | 3/5 |
| `in_corpus_under_5s` | 4/5 | 3/5 | 3/5 |
| `in_corpus_under_10s` | 5/5 | 3/5 | 3/5 |
| `in_corpus_tokens_mean` | 680 | 745 | 674.8 |
| `in_corpus_tokens_max` | 934 | 935 | 904 |
| `out_of_scope_refused` | 5/5 | 5/5 | 5/5 |
| `out_of_scope_ms_max` | 99 | 108 | 103 |
| `out_of_scope_zero_tokens` | 5/5 | 5/5 | 5/5 |
| `bad_input_400` | 5/5 | 5/5 | 5/5 |
| `bad_input_500` | 0/5 | 0/5 | 0/5 |
| `bad_input_logged` | 5/5 | 5/5 | 5/5 |
| `injected_logged_as_error` | 3/3 | 3/3 | 3/3 |
| `injected_status_codes` | 500,500,500 | 500,500,500 | 500,500,500 |
| `injected_has_error_message` | 3/3 | 3/3 | 3/3 |

## Every request

| Trial | Group | Request | HTTP | Logged as | ms | Tokens | Detail |
|---|---|---|---|---|---|---|---|
| 1 | in_corpus | What cities are the most accessible or walkable? | 200 | answered | 6222.2 | 934 | According to **guide_accessibility.md**, **Thornby Wells** is the easiest town in the region because it is flat, compact |
| 1 | in_corpus | Is the seafood at Halden Bay fresh? | 200 | answered | 919.5 | 726 | Yes, Halden Bay's seafood is genuinely fresh because the two harbour restaurants buy directly from boats that land in th |
| 1 | in_corpus | Where is Correy Vale's closest hospital? | 200 | answered | 810.8 | 576 | According to guide_corry_vale.md, the nearest full hospital to Corry Vale is in Brightwater. |
| 1 | in_corpus | If I visit Elder Ness, will I see birds? | 200 | answered | 734.1 | 579 | Yes, you can see birds if you visit Elder Ness, as birds are what most visitors come for and spring and autumn migration |
| 1 | in_corpus | How many people reside in Marchwood? | 200 | answered | 795.8 | 585 | Based on the provided document, Marchwood has a population of 180,000 people (guide_marchwood.md). |
| 1 | out_of_scope | What is the capital of Mongolia? | 200 | refused | 93.0 | 0 | I don't have enough information about that. |
| 1 | out_of_scope | How do I change the oil in a diesel engine? | 200 | refused | 93.5 | 0 | I don't have enough information about that. |
| 1 | out_of_scope | Who won the 1994 World Cup? | 200 | refused | 92.6 | 0 | I don't have enough information about that. |
| 1 | out_of_scope | What is the recommended dosage of ibuprofen for a heada | 200 | refused | 98.8 | 0 | I don't have enough information about that. |
| 1 | out_of_scope | How do I write a for loop in Rust? | 200 | refused | 96.4 | 0 | I don't have enough information about that. |
| 1 | bad_input | empty object | 400 | bad_request | 0.2 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 1 | bad_input | empty question | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 1 | bad_input | whitespace question | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 1 | bad_input | question is a number | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 1 | bad_input | body is not JSON | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 1 | injected | invalid API key — What cities are the most accessible o | 500 | error | 89.1 | 0 | RuntimeError: 400 INVALID_ARGUMENT. API key not valid. (injected by run_trials) |
| 1 | injected | 503 model overloaded — Is the seafood at Halden Bay fre | 500 | error | 89.9 | 0 | RuntimeError: 503 UNAVAILABLE. This model is currently experiencing high demand. (injected by run_trials) |
| 1 | injected | timeout — Where is Correy Vale's closest hospital? | 500 | error | 89.7 | 0 | TimeoutError: The read operation timed out (injected by run_trials) |
| 2 | in_corpus | What cities are the most accessible or walkable? | 200 | answered | 2728.6 | 935 | According to `guide_accessibility.md`, **Thornby Wells** is described as the easiest town in the region because it is fl |
| 2 | in_corpus | Is the seafood at Halden Bay fresh? | 200 | answered | 921.5 | 726 | Yes, Halden Bay's seafood is genuinely fresh because the two harbour restaurants buy directly from boats that land in th |
| 2 | in_corpus | Where is Correy Vale's closest hospital? | 200 | answered | 2860.9 | 574 | The nearest full hospital to Corry Vale is in Brightwater (guide_corry_vale.md). |
| 2 | in_corpus | If I visit Elder Ness, will I see birds? | 500 | error | 1429.9 | 0 | ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spik |
| 2 | in_corpus | How many people reside in Marchwood? | 500 | error | 1942.6 | 0 | ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spik |
| 2 | out_of_scope | What is the capital of Mongolia? | 200 | refused | 107.9 | 0 | I don't have enough information about that. |
| 2 | out_of_scope | How do I change the oil in a diesel engine? | 200 | refused | 101.3 | 0 | I don't have enough information about that. |
| 2 | out_of_scope | Who won the 1994 World Cup? | 200 | refused | 96.9 | 0 | I don't have enough information about that. |
| 2 | out_of_scope | What is the recommended dosage of ibuprofen for a heada | 200 | refused | 101.3 | 0 | I don't have enough information about that. |
| 2 | out_of_scope | How do I write a for loop in Rust? | 200 | refused | 98.3 | 0 | I don't have enough information about that. |
| 2 | bad_input | empty object | 400 | bad_request | 0.2 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 2 | bad_input | empty question | 400 | bad_request | 0.2 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 2 | bad_input | whitespace question | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 2 | bad_input | question is a number | 400 | bad_request | 0.3 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 2 | bad_input | body is not JSON | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 2 | injected | invalid API key — What cities are the most accessible o | 500 | error | 96.2 | 0 | RuntimeError: 400 INVALID_ARGUMENT. API key not valid. (injected by run_trials) |
| 2 | injected | 503 model overloaded — Is the seafood at Halden Bay fre | 500 | error | 96.7 | 0 | RuntimeError: 503 UNAVAILABLE. This model is currently experiencing high demand. (injected by run_trials) |
| 2 | injected | timeout — Where is Correy Vale's closest hospital? | 500 | error | 97.9 | 0 | TimeoutError: The read operation timed out (injected by run_trials) |
| 3 | in_corpus | What cities are the most accessible or walkable? | 200 | answered | 15335.9 | 904 | According to `guide_accessibility.md`, **Thornby Wells** is the easiest town in the region because it is flat, compact,  |
| 3 | in_corpus | Is the seafood at Halden Bay fresh? | 200 | answered | 12521.6 | 727 | Yes, Halden Bay's seafood is genuinely fresh because the boats land in the early morning and the two harbour restaurants |
| 3 | in_corpus | Where is Correy Vale's closest hospital? | 200 | answered | 920.3 | 576 | Based on guide_corry_vale.md, the nearest full hospital to Corry Vale is in Brightwater. |
| 3 | in_corpus | If I visit Elder Ness, will I see birds? | 200 | answered | 1632.4 | 588 | Yes, you can see birds if you visit Elder Ness, as birds are the main reason most visitors come, especially during the s |
| 3 | in_corpus | How many people reside in Marchwood? | 200 | answered | 814.1 | 579 | Marchwood has a population of 180,000 people (guide_marchwood.md). |
| 3 | out_of_scope | What is the capital of Mongolia? | 200 | refused | 103.2 | 0 | I don't have enough information about that. |
| 3 | out_of_scope | How do I change the oil in a diesel engine? | 200 | refused | 93.4 | 0 | I don't have enough information about that. |
| 3 | out_of_scope | Who won the 1994 World Cup? | 200 | refused | 94.6 | 0 | I don't have enough information about that. |
| 3 | out_of_scope | What is the recommended dosage of ibuprofen for a heada | 200 | refused | 90.3 | 0 | I don't have enough information about that. |
| 3 | out_of_scope | How do I write a for loop in Rust? | 200 | refused | 90.9 | 0 | I don't have enough information about that. |
| 3 | bad_input | empty object | 400 | bad_request | 0.2 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 3 | bad_input | empty question | 400 | bad_request | 0.2 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 3 | bad_input | whitespace question | 400 | bad_request | 0.2 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 3 | bad_input | question is a number | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 3 | bad_input | body is not JSON | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 3 | injected | invalid API key — What cities are the most accessible o | 500 | error | 95.7 | 0 | RuntimeError: 400 INVALID_ARGUMENT. API key not valid. (injected by run_trials) |
| 3 | injected | 503 model overloaded — Is the seafood at Halden Bay fre | 500 | error | 89.3 | 0 | RuntimeError: 503 UNAVAILABLE. This model is currently experiencing high demand. (injected by run_trials) |
| 3 | injected | timeout — Where is Correy Vale's closest hospital? | 500 | error | 95.5 | 0 | TimeoutError: The read operation timed out (injected by run_trials) |
