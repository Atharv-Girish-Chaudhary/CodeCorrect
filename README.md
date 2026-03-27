# CodeCorrect

**CS 5800 Algorithms — Spring 2026 — Dr. Lama Hamandi**

An algorithmic approach to fixing code typos using edit distance (Levenshtein distance) implemented three ways: naive recursion, top-down memoization, and bottom-up tabulation.

---

## The Problem

Every programmer has been bitten by a typo: `pritn` instead of `print`, `lenght` instead of `length`, `retrun` instead of `return`. Unlike natural language, code typos don't just look wrong — they crash your program. IDEs underline errors, but most lack a suggestion engine that says *"did you mean `print`?"* for arbitrary identifiers.

**Our question:** Given a mistyped programming keyword, function name, or variable, how can we use the edit distance algorithm to instantly suggest the closest valid match from a known codebase vocabulary? And how does the choice of DP strategy affect whether this runs fast enough for real-time use?

---

## Team

| Member | Primary Responsibilities |
|---|---|
| **Atharv Chaudhary** | Bottom-up tabulation + space optimization, benchmarking framework, performance plots, formal complexity proofs |
| **Sandeep Vijayarao** | Naive recursive + memoized implementations, real-world typo dataset collection, accuracy evaluation |
| **Scott Biggs** | CodeCorrect CLI integration (vocab loading, ranking, output formatting), presentation slides, live demo, report writing |

Report writing, presentation prep, and Q&A rehearsal are shared across all three members.

---

## Repository Structure

```
CodeCorrect/
├── src/
│   ├── naive.py          # Naive recursive edit distance (Sandeep)
│   ├── memoized.py       # Top-down memoized edit distance (Sandeep)
│   ├── tabulation.py     # Bottom-up tabulated edit distance (Atharv)
│   ├── spell_checker.py  # CodeCorrect CLI tool (Scott)
│   ├── vocab_loader.py   # Vocabulary file loader (Scott)
│   └── __init__.py
├── data/
│   ├── python_keywords.txt   # ~100 Python keywords + stdlib functions
│   └── typo_dataset.csv      # 50 real-world code typos for accuracy testing
├── tests/
│   ├── test_naive_memoized.py  # 63 tests for naive + memoized (Sandeep)
│   └── test_tabulation.py      # Tests for tabulation (Atharv)
├── docs/
│   └── (project report, complexity proofs)
└── README.md
```

---

## Algorithms

All three implementations solve the same problem: compute the minimum number of single-character edits (insert, delete, replace) needed to transform string `s1` into string `s2`.

### 1. Naive Recursion — `src/naive.py`

Pure recursive solution with no caching. Recomputes overlapping subproblems repeatedly.

```
edit_distance(s1, s2):
  if s1 is empty: return len(s2)
  if s2 is empty: return len(s1)
  if s1[-1] == s2[-1]: return edit_distance(s1[:-1], s2[:-1])
  return 1 + min(
    edit_distance(s1[:-1], s2),       # delete
    edit_distance(s1, s2[:-1]),       # insert
    edit_distance(s1[:-1], s2[:-1])   # replace
  )
```

| Complexity | Bound |
|---|---|
| Time | O(3^(m+n)) |
| Space | O(m+n) — recursion stack |

### 2. Top-Down Memoization — `src/memoized.py`

Same recurrence as naive, but stores results in a `memo` dict so each `(i, j)` subproblem is solved exactly once.

| Complexity | Bound |
|---|---|
| Time | O(m × n) |
| Space | O(m × n) — memo table + O(m+n) stack |

### 3. Bottom-Up Tabulation — `src/tabulation.py`

Iteratively fills an `(m+1) × (n+1)` DP table, eliminating recursion overhead entirely.

| Complexity | Bound |
|---|---|
| Time | O(m × n) |
| Space | O(m × n), optimizable to O(min(m, n)) with two-row trick |

---

## CLRS Connections

| Topic | Connection |
|---|---|
| **Dynamic Programming (Ch. 15)** | Edit distance is the core algorithm; we implement both top-down and bottom-up DP and compare empirically |
| **CLRS Problem 15-5** | The "twiddle" (transposition) operation models `pritn → print` — a dominant typo class in code |
| **Growth of Functions (Ch. 3)** | We prove O(3^(m+n)) for naive vs. O(mn) for DP and validate with empirical timing data |
| **Sorting (Ch. 2, 8)** | After computing distances, we sort candidates to extract the top-k closest matches efficiently |

---

## Setup

```bash
git clone https://github.com/Atharv-Girish-Chaudhary/CodeCorrect.git
cd CodeCorrect
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### Run the CLI spell-checker

```bash
python src/spell_checker.py --word pritn --vocab data/python_keywords.txt --method memoized --top 3
```

**Output:**
```
Top 3 suggestions for 'pritn':
  1. print    (distance: 2)  replace 'r' with 'r' at position 1; insert 't' at position 4
  2. int      (distance: 3)
  3. in       (distance: 4)
```

### Run individual implementations directly

```bash
# Naive
python src/naive.py

# Memoized (includes accuracy evaluation)
python src/memoized.py

# Tabulation
python src/tabulation.py
```

---

## Testing

```bash
# Run Sandeep's tests (naive + memoized)
pytest tests/test_naive_memoized.py -v

# Run Atharv's tests (tabulation)
pytest tests/test_tabulation.py -v

# Run all tests
pytest tests/ -v
```

**Current test results:**
- `test_naive_memoized.py` — 63 passed
- Coverage: known distances, edge cases, operation sequence, symmetry, accuracy evaluation

---

## Benchmarking

Benchmarks run all three strategies on vocabularies of increasing size:

| Vocab Size | Naive | Memoized | Tabulated |
|---|---|---|---|
| 100 | (measured) | (measured) | (measured) |
| 1,000 | (measured) | (measured) | (measured) |
| 10,000 | (measured) | (measured) | (measured) |
| 50,000 | (measured) | (measured) | (measured) |

*(Results to be filled in after benchmarking — Week 4)*

---

## Project Timeline

| Week | Dates | Tasks | Owner | Milestone |
|---|---|---|---|---|
| 1 | 3/9–3/16 | Naive + memoized edit distance; dictionary loading | Sandeep | Core algorithms pass tests ✅ |
| 2 | 3/16–3/23 | Bottom-up tabulation; benchmarking; complexity proofs | Atharv | Progress Report 1 (3/23) |
| 3 | 3/23–3/30 | CLI integration; scale to 50K vocab; real-world typo testing | Scott | End-to-end tool working |
| 4 | 3/30–4/6 | Benchmark plots; project report; CLRS connections | All | Progress Report 2 (4/6) |
| 5 | 4/6–4/13 | Slides, live demo, rehearsal; finalize code and report | All | Final submission (4/13) |

---

## Scope

**We will:**
- Implement edit distance three ways (naive recursion, memoized, tabulated)
- Build a working code-autocorrect CLI tool
- Benchmark and plot performance across vocabulary sizes
- Prove time/space complexity for each approach
- Discuss how CLRS Problem 15-5's six-operation model handles code-specific edits (transpositions)

**We won't:**
- Build an IDE plugin or VS Code extension
- Use machine learning or statistical language models
- Handle multi-token corrections or syntax-level analysis

---

## License

MIT — see [LICENSE](LICENSE)
