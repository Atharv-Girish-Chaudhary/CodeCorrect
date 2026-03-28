# CodeCorrect

> **CS 5800: Algorithms — Spring 2026 — Northeastern University**  
> Instructor: Dr. Lama Hamandi

A Python-based spell-checker for programmer typos — built on edit distance (Levenshtein distance) and dynamic programming.

---

## The Problem

Every programmer has been bitten by a typo: `pritn` instead of `print`, `lenght` instead of `length`, `retrun` instead of `return`. Unlike natural language, code typos don't just look wrong — they crash your program. Most IDEs underline errors but don't suggest corrections for arbitrary identifiers.

**Our question:** Given a mistyped token, how can we use edit distance to instantly suggest the closest valid match from a known vocabulary — and how does the choice of DP strategy affect real-time performance?

Motivated by **CLRS 3rd Edition, Chapter 15 (Dynamic Programming)** and **Problem 15-5** (edit distance with twiddle/transposition operations).

---

## Team

| Member | Primary Responsibilities |
|---|---|
| **Atharv Chaudhary** | Bottom-up tabulation, space-optimized variant, benchmarking framework, performance plots, complexity proofs |
| **Sandeep Vijayarao** | Naive recursive + memoized implementations, real-world typo dataset collection, accuracy evaluation |
| **Scott Biggs** | CodeCorrect CLI integration (vocab loading, ranking, output formatting), presentation slides, live demo |

Report writing, presentation prep, and Q&A rehearsal are shared across all three members.

---

## Repository Structure

```
CodeCorrect/
├── src/
│   ├── naive.py               # Naive recursive edit distance (Sandeep)
│   ├── memoized.py            # Top-down memoized edit distance (Sandeep)
│   ├── tabulation.py          # Bottom-up tabulated edit distance (Atharv)
│   ├── spell_checker.py       # CodeCorrect CLI tool (Scott)
│   ├── vocab_loader.py        # Vocabulary file loader (Scott)
│   └── __init__.py
├── tests/
│   ├── test_naive_memoized.py # 63 tests — naive + memoized (Sandeep)
│   └── test_tabulation.py     # 27 tests — tabulation (Atharv)
├── data/
│   ├── python_keywords.txt    # ~100 Python keywords + stdlib functions
│   └── typo_dataset.csv       # 50 real-world code typos for accuracy testing
├── benchmarks/
│   ├── benchmark.py           # Timing script across all three approaches
│   ├── results/               # Raw timing data (CSVs)
│   └── plots/                 # Generated performance charts
├── notebooks/
│   ├── atharv_dev.ipynb       # Tabulation experiments + DP table visualization
│   ├── sandeep_dev.ipynb      # Naive/memoized experiments
│   └── scott_dev.ipynb        # CLI development + demo
├── docs/
│   ├── progress_report_1.docx
│   └── final_report.docx
├── README.md
└── requirements.txt
```

---

## Algorithms

All three implementations solve the same problem: compute the minimum number of single-character edits (insert, delete, replace) to transform string `s1` into string `s2`.

### 1. Naive Recursion — `src/naive.py`

Pure recursive solution. Recomputes overlapping subproblems repeatedly — exponential blowup.

```
edit_distance(s1, s2):
  if s1 is empty: return len(s2)
  if s2 is empty: return len(s1)
  if s1[-1] == s2[-1]: return edit_distance(s1[:-1], s2[:-1])
  return 1 + min(
    edit_distance(s1[:-1], s2),      # delete
    edit_distance(s1, s2[:-1]),      # insert
    edit_distance(s1[:-1], s2[:-1]) # replace
  )
```

| | Complexity |
|---|---|
| Time | O(3^(m+n)) |
| Space | O(m+n) — recursion stack |

### 2. Top-Down Memoization — `src/memoized.py`

Same recurrence as naive, but caches results in a `memo` dict so each `(i, j)` subproblem is solved exactly once.

| | Complexity |
|---|---|
| Time | O(m × n) |
| Space | O(m × n) memo table + O(m+n) stack |

### 3. Bottom-Up Tabulation — `src/tabulation.py`

Iteratively fills an `(m+1) × (n+1)` DP table. No recursion overhead. Includes a space-optimized rolling two-row variant.

| | Complexity |
|---|---|
| Time | O(m × n) |
| Space | O(m × n) full table, O(min(m,n)) space-optimized |

---

## CLRS Connections

| Topic | Connection |
|---|---|
| **Dynamic Programming (Ch. 15)** | Edit distance exhibits optimal substructure and overlapping subproblems — the two hallmarks of DP |
| **CLRS Problem 15-5** | The "twiddle" (transposition) operation models `pritn → print`, the dominant typo class in code |
| **Growth of Functions (Ch. 3)** | We prove O(3^(m+n)) for naive vs. O(mn) for DP and validate empirically with timing benchmarks |
| **Sorting (Ch. 2, 8)** | Candidates are sorted by edit distance to extract top-k suggestions efficiently |

---

## Setup

```bash
git clone https://github.com/Atharv-Girish-Chaudhary/CodeCorrect.git
cd CodeCorrect
python3 -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

### CLI spell-checker

```bash
python src/spell_checker.py --word <mistyped> --vocab <vocab_file> --method <method> --top <N>
```

**Arguments:**

- `--word`: Mistyped word to correct (required)
- `--vocab`: Path to vocabulary file, one word per line (required)
- `--method`: DP method: `naive`, `memoized`, or `tabulation` (default: `tabulation`)
- `--top`: Number of suggestions to return (default: 5)

**Example:**

```bash
python src/spell_checker.py --word pritn --vocab data/python_keywords.txt --method tabulation --top 3
```

**Output:**

```
Top 3 suggestions for 'pritn':
  1. print    (distance: 2)
  2. int      (distance: 3)
  3. in       (distance: 4)
```

### Run implementations directly

```bash
python src/naive.py
python src/memoized.py
python src/tabulation.py
```

---

## Vocabulary Files & Scaling

Small vocab files are tracked in git. Large vocabularies (50K+) are **not tracked** to keep the repo lightweight — download or generate them locally.

### Option 1: Real-World English Dictionary (Recommended)

```bash
cd data/
curl -O https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
cd ..
```

~370K real English words, public domain.

### Option 2: Generate Synthetic Vocabulary

```bash
python3 -c "with open('data/large_vocab.txt', 'w') as f: [f.write(f'word{i}\n') for i in range(50000)]"
```

### File Reference

| File | Tracked? | Purpose |
|---|---|---|
| `python_keywords.txt` | ✅ Yes | Python keywords reference |
| `typo_dataset.csv` | ✅ Yes | Test dataset |
| `words_alpha.txt` | ❌ No | Real dictionary (download on-demand) |
| `large_vocab.txt` | ❌ No | Synthetic 50K words (generated locally) |

---

## Testing

```bash
# All tests
pytest tests/ -v

# Individual
pytest tests/test_tabulation.py -v
pytest tests/test_naive_memoized.py -v
```

**Current results:**

- `test_tabulation.py` — 27 passed
- `test_naive_memoized.py` — 63 passed

---

## Benchmarking

```bash
python benchmarks/benchmark.py
```

Benchmarks all three strategies across vocabularies of increasing size (100 → 50K words):

| Vocab Size | Naive | Memoized | Tabulated |
|---|---|---|---|
| 100 | — | — | — |
| 1,000 | — | — | — |
| 10,000 | — | — | — |
| 50,000 | — | — | — |

*(Results to be filled in — Week 4)*

---

## Branch Strategy

| Branch | Owner | Scope |
|---|---|---|
| `atharv/tabulation-benchmarking` | Atharv | `src/tabulation.py`, `benchmarks/`, `notebooks/atharv_dev.ipynb` |
| `sandeep/naive-memoized` | Sandeep | `src/naive.py`, `src/memoized.py`, `data/`, `notebooks/sandeep_dev.ipynb` |
| `scott/cli-scaling-integration` | Scott | `src/spell_checker.py`, `docs/`, `notebooks/scott_dev.ipynb` |

---

## Project Timeline

| Week | Dates | Tasks | Owner | Status |
|---|---|---|---|---|
| 1 | 3/9–3/16 | Naive + memoized implementations; vocab loader | Sandeep | ✅ Done |
| 2 | 3/16–3/23 | Bottom-up tabulation; benchmarking; complexity proofs | Atharv | ✅ Done |
| 3 | 3/23–3/30 | CLI integration; scale to 50K vocab; typo testing | Scott | 🔄 In Progress |
| 4 | 3/30–4/6 | Benchmark plots; project report; CLRS connections | All | ⏳ Upcoming |
| 5 | 4/6–4/13 | Slides, demo, rehearsal; finalize submission | All | ⏳ Upcoming |

---

## Scope

**In scope:**

- Edit distance implemented three ways (naive, memoized, tabulated)
- Working CLI autocorrect tool with top-k ranking
- Benchmarks and performance plots across vocabulary sizes
- Formal time/space complexity proofs for each approach
- CLRS Problem 15-5 twiddle operation discussion

**Out of scope:**

- IDE plugins or VS Code extensions
- Machine learning or statistical language models
- Multi-token corrections or syntax-level analysis

---

## License

MIT — see [LICENSE](LICENSE)
