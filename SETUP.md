# Setup & Usage Guide

> For project overview, algorithms, and benchmark results, see [README.md](README.md).

---

## Quick Start

```bash
git clone https://github.com/Atharv-Girish-Chaudhary/CodeCorrect.git
cd CodeCorrect
pip install -r requirements.txt
python src/spell_checker.py --word pritn --vocab data/python_keywords.txt --top 3
```

---

## Installation

```bash
git clone https://github.com/Atharv-Girish-Chaudhary/CodeCorrect.git
cd CodeCorrect
python3 -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Requirements

- Python 3.10+
- Dependencies: `pandas`, `jupyter`, `pytest`, `matplotlib`, `streamlit`

---

## Usage

### CLI Spell Checker

```bash
python src/spell_checker.py --word <mistyped> --vocab <vocab_file> --method <method> --top <N>
```

**Arguments:**

| Flag | Required | Default | Description |
|---|---|---|---|
| `--word` | Yes | — | Mistyped word to correct |
| `--vocab` | Yes | — | Path to vocabulary file (one word per line) |
| `--method` | No | `tabulation` | DP method: `naive`, `memoized`, `tabulation`, `optimized` |
| `--top` | No | `5` | Number of suggestions to return |

**Example:**

```bash
python src/spell_checker.py --word pritn --vocab data/python_keywords.txt --method tabulation --top 3
```

**Output:**

```
Suggestions for 'pritn':
  print (distance: 2)
  write (distance: 2)
  in (distance: 3)
```

### Streamlit Demo

```bash
streamlit run app.py
```

Opens a browser-based UI where you can type a word, pick a DP method, adjust top-N, and compare all methods side-by-side with timing.

### Run Implementations Directly

```bash
python src/naive.py
python src/memoized.py
python src/tabulation.py
```

---

## Testing

```bash
# All tests
pytest tests/ -v

# By file
pytest tests/test_tabulation.py -v
pytest tests/test_naive.py -v
pytest tests/test_memoized.py -v
pytest tests/test_naive_memoized.py -v
pytest tests/test_spell_checker.py -v
pytest tests/test_vocab_loader.py -v
```

**Current results: 175 passed**

| Test File | Tests | Coverage |
|---|---|---|
| `test_tabulation.py` | 28 | Tabulation + space-optimized |
| `test_naive.py` | 30 | Naive recursive |
| `test_memoized.py` | 40 | Memoized top-down |
| `test_naive_memoized.py` | 63 | Cross-implementation consistency |
| `test_spell_checker.py` | 8 | CLI integration + error handling |
| `test_vocab_loader.py` | 6 | Vocabulary file loading |

---

## Vocabulary Files & Scaling

Small vocab files are tracked in git. Large vocabularies (50K+) are **not tracked** to keep the repo lightweight.

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
| `python_keywords.txt` | ✅ Yes | 109 Python keywords + stdlib functions |
| `typo_dataset.csv` | ✅ Yes | 59 real-world code typos for testing |
| `words_alpha.txt` | ❌ No | Real dictionary (download on-demand) |
| `large_vocab.txt` | ❌ No | Synthetic 50K words (generated locally) |

---

## Repository Structure

```
CodeCorrect/
├── src/
│   ├── __init__.py
│   ├── naive.py               # Naive recursive edit distance (Sandeep)
│   ├── memoized.py            # Top-down memoized edit distance (Sandeep)
│   ├── tabulation.py          # Bottom-up + space-optimized edit distance (Atharv)
│   ├── spell_checker.py       # CodeCorrect CLI tool (Scott)
│   └── vocab_loader.py        # Vocabulary file loader (Scott)
├── tests/
│   ├── conftest.py            # Shared test configuration
│   ├── test_tabulation.py     # 28 tests (Atharv)
│   ├── test_naive.py          # 30 tests
│   ├── test_memoized.py       # 40 tests
│   ├── test_naive_memoized.py # 63 tests (Sandeep)
│   ├── test_spell_checker.py  # 8 tests — CLI integration
│   └── test_vocab_loader.py   # 6 tests — vocab loading
├── data/
│   ├── python_keywords.txt    # 109 Python keywords + stdlib functions
│   └── typo_dataset.csv       # 59 real-world code typos for accuracy testing
├── benchmarks/
│   └── benchmark_results.png  # Performance comparison plots
├── notebooks/
│   ├── atharv_benchmarking.ipynb         # Benchmarking script + plot generation
│   ├── edit_distance_tabulation.ipynb    # Tabulation development + DP table visualization
│   ├── edit_distance_optimized.ipynb     # Space-optimized variant experiments
│   └── scott_dev.ipynb                   # CLI development + demo
├── app.py                     # Streamlit demo frontend
├── LICENSE
├── README.md
├── SETUP.md
└── requirements.txt
```
