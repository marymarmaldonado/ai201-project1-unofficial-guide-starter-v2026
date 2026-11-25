# Capstone trials — after

Run 2026-11-25_1512, 3 trials, cache off, model `gemini-3.5-flash-lite`, threshold `0.62`.
Produced by `tools/run_trials.py::main`; log records in `logs/trials_after.jsonl`.

## Measurements per trial

| Measure | Trial 1 | Trial 2 | Trial 3 |
|---|---|---|---|
| `log_records_written` | 18/18 | 18/18 | 18/18 |
| `in_corpus_200` | 5/5 | 5/5 | 5/5 |
| `in_corpus_expects_found` | 5/5 | 5/5 | 5/5 |
| `in_corpus_has_sources` | 5/5 | 5/5 | 5/5 |
| `in_corpus_ms_median` | 1022 | 1644 | 951 |
| `in_corpus_ms_max` | 2366 | 3124 | 1368 |
| `in_corpus_under_2s` | 4/5 | 3/5 | 5/5 |
| `in_corpus_under_3s` | 5/5 | 4/5 | 5/5 |
| `in_corpus_under_5s` | 5/5 | 5/5 | 5/5 |
| `in_corpus_under_10s` | 5/5 | 5/5 | 5/5 |
| `in_corpus_tokens_mean` | 678.6 | 680.4 | 677.4 |
| `in_corpus_tokens_max` | 923 | 936 | 910 |
| `out_of_scope_refused` | 5/5 | 5/5 | 5/5 |
| `out_of_scope_ms_max` | 46 | 67 | 55 |
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
| 1 | in_corpus | What cities are the most accessible or walkable? | 200 | answered | 2366.5 | 923 | Based on the provided documents, **Thornby Wells** is described as the region's most accessible town on foot, being flat |
| 1 | in_corpus | Is the seafood at Halden Bay fresh? | 200 | answered | 907.8 | 726 | Yes, Halden Bay's seafood is genuinely fresh because the two harbour restaurants buy directly from boats that land in th |
| 1 | in_corpus | Where is Correy Vale's closest hospital? | 200 | answered | 1386.4 | 579 | The nearest full hospital to Corry Vale is in Brightwater.   (Source: guide_corry_vale.md) |
| 1 | in_corpus | If I visit Elder Ness, will I see birds? | 200 | answered | 757.7 | 587 | Yes, you can see birds if you visit Elder Ness, as birds are what most visitors come for, especially during the spring a |
| 1 | in_corpus | How many people reside in Marchwood? | 200 | answered | 1021.8 | 578 | According to guide_marchwood.md, Marchwood has 180,000 people. |
| 1 | out_of_scope | What is the capital of Mongolia? | 200 | refused | 43.9 | 0 | I don't have enough information about that. |
| 1 | out_of_scope | How do I change the oil in a diesel engine? | 200 | refused | 42.6 | 0 | I don't have enough information about that. |
| 1 | out_of_scope | Who won the 1994 World Cup? | 200 | refused | 46.4 | 0 | I don't have enough information about that. |
| 1 | out_of_scope | What is the recommended dosage of ibuprofen for a heada | 200 | refused | 45.9 | 0 | I don't have enough information about that. |
| 1 | out_of_scope | How do I write a for loop in Rust? | 200 | refused | 46.1 | 0 | I don't have enough information about that. |
| 1 | bad_input | empty object | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 1 | bad_input | empty question | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 1 | bad_input | whitespace question | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 1 | bad_input | question is a number | 400 | bad_request | 0.0 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 1 | bad_input | body is not JSON | 400 | bad_request | 0.0 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 1 | injected | invalid API key — What cities are the most accessible o | 500 | error | 45.8 | 0 | RuntimeError: 400 INVALID_ARGUMENT. API key not valid. (injected by run_trials) |
| 1 | injected | 503 model overloaded — Is the seafood at Halden Bay fre | 500 | error | 7048.9 | 0 | RuntimeError: Still failing after 4 attempts (rate limited or model overloaded). Wait a minute and try again — your key  |
| 1 | injected | timeout — Where is Correy Vale's closest hospital? | 500 | error | 51.7 | 0 | TimeoutError: The read operation timed out (injected by run_trials) |
| 2 | in_corpus | What cities are the most accessible or walkable? | 200 | answered | 1644.3 | 936 | Based on the provided documents, **Thornby Wells** is noted as the easiest town in the region, being flat, compact, and  |
| 2 | in_corpus | Is the seafood at Halden Bay fresh? | 200 | answered | 2053.6 | 726 | Yes, Halden Bay's seafood is genuinely fresh because the two harbour restaurants buy directly from boats that land in th |
| 2 | in_corpus | Where is Correy Vale's closest hospital? | 200 | answered | 1320.2 | 577 | Based on `guide_corry_vale.md`, the nearest full hospital to Corry Vale is in Brightwater. |
| 2 | in_corpus | If I visit Elder Ness, will I see birds? | 200 | answered | 3124.2 | 584 | Yes, bird watching is one of the main reasons visitors come to Elder Ness, particularly during the spring (April to May) |
| 2 | in_corpus | How many people reside in Marchwood? | 200 | answered | 769.4 | 579 | Marchwood has a population of 180,000 people (guide_marchwood.md). |
| 2 | out_of_scope | What is the capital of Mongolia? | 200 | refused | 40.9 | 0 | I don't have enough information about that. |
| 2 | out_of_scope | How do I change the oil in a diesel engine? | 200 | refused | 46.2 | 0 | I don't have enough information about that. |
| 2 | out_of_scope | Who won the 1994 World Cup? | 200 | refused | 67.1 | 0 | I don't have enough information about that. |
| 2 | out_of_scope | What is the recommended dosage of ibuprofen for a heada | 200 | refused | 46.4 | 0 | I don't have enough information about that. |
| 2 | out_of_scope | How do I write a for loop in Rust? | 200 | refused | 47.2 | 0 | I don't have enough information about that. |
| 2 | bad_input | empty object | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 2 | bad_input | empty question | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 2 | bad_input | whitespace question | 400 | bad_request | 0.0 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 2 | bad_input | question is a number | 400 | bad_request | 0.0 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 2 | bad_input | body is not JSON | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 2 | injected | invalid API key — What cities are the most accessible o | 500 | error | 45.9 | 0 | RuntimeError: 400 INVALID_ARGUMENT. API key not valid. (injected by run_trials) |
| 2 | injected | 503 model overloaded — Is the seafood at Halden Bay fre | 500 | error | 7047.4 | 0 | RuntimeError: Still failing after 4 attempts (rate limited or model overloaded). Wait a minute and try again — your key  |
| 2 | injected | timeout — Where is Correy Vale's closest hospital? | 500 | error | 43.1 | 0 | TimeoutError: The read operation timed out (injected by run_trials) |
| 3 | in_corpus | What cities are the most accessible or walkable? | 200 | answered | 970.2 | 910 | Based on the provided documents, Thornby Wells is described as the region's most accessible town on foot and the easiest |
| 3 | in_corpus | Is the seafood at Halden Bay fresh? | 200 | answered | 1367.8 | 727 | Yes, Halden Bay's seafood is genuinely fresh because the boats land in the early morning and the two harbour restaurants |
| 3 | in_corpus | Where is Correy Vale's closest hospital? | 200 | answered | 721.0 | 579 | The nearest full hospital to Corry Vale is in Brightwater.   (Source: guide_corry_vale.md) |
| 3 | in_corpus | If I visit Elder Ness, will I see birds? | 200 | answered | 898.4 | 590 | Yes, you can see birds if you visit Elder Ness, as birds are the main reason most visitors come, especially during the s |
| 3 | in_corpus | How many people reside in Marchwood? | 200 | answered | 951.4 | 581 | According to guide_marchwood.md, Marchwood has a population of 180,000 people. |
| 3 | out_of_scope | What is the capital of Mongolia? | 200 | refused | 39.7 | 0 | I don't have enough information about that. |
| 3 | out_of_scope | How do I change the oil in a diesel engine? | 200 | refused | 46.4 | 0 | I don't have enough information about that. |
| 3 | out_of_scope | Who won the 1994 World Cup? | 200 | refused | 54.7 | 0 | I don't have enough information about that. |
| 3 | out_of_scope | What is the recommended dosage of ibuprofen for a heada | 200 | refused | 47.8 | 0 | I don't have enough information about that. |
| 3 | out_of_scope | How do I write a for loop in Rust? | 200 | refused | 46.4 | 0 | I don't have enough information about that. |
| 3 | bad_input | empty object | 400 | bad_request | 0.1 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 3 | bad_input | empty question | 400 | bad_request | 0.0 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 3 | bad_input | whitespace question | 400 | bad_request | 0.0 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 3 | bad_input | question is a number | 400 | bad_request | 0.0 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 3 | bad_input | body is not JSON | 400 | bad_request | 0.0 | 0 | Send JSON with a question in it, like {"question": "is the housing lottery random?"} |
| 3 | injected | invalid API key — What cities are the most accessible o | 500 | error | 47.8 | 0 | RuntimeError: 400 INVALID_ARGUMENT. API key not valid. (injected by run_trials) |
| 3 | injected | 503 model overloaded — Is the seafood at Halden Bay fre | 500 | error | 20257.7 | 0 | RuntimeError: Still failing after 4 attempts (rate limited or model overloaded). Wait a minute and try again — your key  |
| 3 | injected | timeout — Where is Correy Vale's closest hospital? | 500 | error | 44.8 | 0 | TimeoutError: The read operation timed out (injected by run_trials) |
