# CodeCorrect

CS 5800 Final Project — Spell checker for code typos using edit distance (Dynamic Programming)

# CodeCorrect

CS 5800 Final Project — Spell checker for code typos using edit distance (Dynamic Programming)

## Overview

CodeCorrect is a Python-based tool that takes a mistyped programming token (keyword, function name, or variable) and returns ranked suggestions using edit distance. The project implements three DP strategies — naive recursion, memoization, and bottom-up tabulation — and benchmarks their performance on vocabularies of increasing size.

Motivated by CLRS 3rd Edition, Problem 15-5 (Edit Distance with twiddle operations).

## Team

| Member | Role |
|--------|------|
| Atharv Chaudhary | Bottom-up tabulation, space-optimized version, benchmarking |
| Sandeep | Naive recursive, memoized implementations, dataset testing |
| Scott | CLI spell checker (integrate, scale to 50K vocab, test with real datasets), slides, demo, presentation |

## Project Structure

```
CodeCorrect/
├── src/                        # Core implementations
│   ├── naive.py                # Naive recursive edit distance
│   ├── memoized.py             # Top-down memoized edit distance
│   ├── tabulation.py           # Bottom-up tabulated edit distance
│   ├── spell_checker.py        # CLI tool for code autocorrect
│   ├── vocab_loader.py         # Loads keyword/vocabulary files
│   └── utils.py                # Shared utilities (DP table printer, etc.)
├── tests/                      # Unit tests
│   ├── test_naive.py
│   ├── test_memoized.py
│   ├── test_tabulation.py
│   └── test_spell_checker.py
├── data/                       # Vocabulary and test data
│   ├── python_keywords.txt     # Python built-in keywords
│   ├── python_stdlib.txt       # Standard library function names
│   └── typo_dataset.csv        # Known typo → correct pairs
├── benchmarks/                 # Performance measurement
│   ├── benchmark.py            # Timing script for all three approaches
│   ├── results/                # Raw timing data (CSVs)
│   └── plots/                  # Generated charts and graphs
├── notebooks/                  # Jupyter notebooks for dev/debug/demo
│   ├── atharv_dev.ipynb        # Atharv — tabulation experiments & benchmarking
│   ├── sandeep_dev.ipynb       # Sandeep — naive/memoized experiments
│   └── scott_dev.ipynb         # Scott — CLI development & demo
├── docs/                       # Reports and documentation
│   ├── progress_report_1.docx
│   └── final_report.docx
├── README.md
└── requirements.txt
```

## Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/CodeCorrect.git
cd CodeCorrect

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## CLI Usage

The spell checker can be run from the command line:

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
python src/spell_checker.py --word prin --vocab data/python_keywords.txt --method tabulation
# Output: Suggestions for 'prin':
#   print (distance: 1)
#   in (distance: 2)
#   True (distance: 3)
```

## Vocabulary Files & Scaling

For scaling tests and real-world spell-checking, you need a large vocabulary (~50K+ words). Large vocabulary files are **not tracked in git** to keep the repository lightweight—download or generate them locally.

### Option 1: Real-World English Dictionary (Recommended)

Download from [dwyl/english-words](https://github.com/dwyl/english-words) (~370K actual English words):

```bash
cd data/
curl -O https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
cd ..
```

**Benefits:**
- ~370,000 real English words
- Clean (alphabetic only, no symbols/numbers)
- Perfect for testing spell-checker accuracy
- Public domain / Unlicense

### Option 2: Generate Synthetic Vocabulary

For quick testing without download:

```bash
python3 -c "with open('data/large_vocab.txt', 'w') as f: [f.write(f'word{i}\n') for i in range(50000)]"
```

Creates 50K synthetic words instantly (~400 KB file).

### Using with CLI & Notebook

**CLI:**
```bash
# Real dictionary
python src/spell_checker.py --word prin --vocab data/words_alpha.txt --method tabulation

# Synthetic
python src/spell_checker.py --word word12345 --vocab data/large_vocab.txt --method tabulation
```

**Notebook:**
The notebook (`notebooks/scott_dev.ipynb`) automatically downloads `words_alpha.txt` if missing, then runs scaling and accuracy tests.

### File Reference

| File | Size | Tracked? | Purpose |
|------|------|----------|---------|
| `python_keywords.txt` | ~1 KB | ✅ Yes | Python keywords reference |
| `typo_dataset.csv` | ~1 KB | ✅ Yes | Test dataset (expandable by team) |
| `words_alpha.txt` | ~5.8 MB | ❌ No | Real dictionary (download on-demand) |
| `large_vocab.txt` | ~400 KB | ❌ No | Synthetic 50K words (generated for testing) |

## Implementation: CLI Tool & Scaling (Scott's Tasks)

This branch (`scott/cli-scaling-integration`) completes three key objectives:

### 1. CLI Tool Integration
- **`src/spell_checker.py`**: Main CLI tool
- **`src/vocab_loader.py`**: Vocabulary loading utility
- **`src/naive.py`, `src/memoized.py`**: DP implementations (complement to `tabulation.py`)
- **Features**: Accepts any vocabulary file, supports 3 DP methods, ranks suggestions by edit distance

### 2. Scaling to 50K+ Vocabulary
- Tested with 50K synthetic and 370K real-world word dictionaries
- Tabulation method handles large vocabularies efficiently (milliseconds per word)
- Auto-download real vocabulary in notebook if missing

### 3. Real-World Testing
- **`data/typo_dataset.csv`**: Expandable test dataset of common code typos
- **Accuracy metrics**: Notebook calculates success rate on typo dataset
- **Performance measurement**: Load time, computation time, suggestion quality

### Development Notebook
**`notebooks/scott_dev.ipynb`** provides an interactive demo with:
- Vocabulary setup (auto-downloads real dictionary)
- CLI integration examples
- Scaling performance tests
- Accuracy validation on typo dataset

## Branch Strategy

Each team member works on their own branch and merges into `main` via pull requests:

| Branch | Owner | Scope |
|--------|-------|-------|
| `atharv/tabulation-benchmarking` | Atharv | `src/tabulation.py`, `benchmarks/`, `notebooks/atharv_dev.ipynb` |
| `sandeep/naive-memoized` | Sandeep | `src/naive.py`, `src/memoized.py`, `data/`, `notebooks/sandeep_dev.ipynb` |
| `scott/cli-scaling-integration` | Scott | `src/spell_checker.py`, `docs/`, `notebooks/scott_dev.ipynb` |

Shared files (`src/utils.py`, `src/vocab_loader.py`, `tests/`, `README.md`) are edited on `main` or coordinated to avoid conflicts.

## Course

CS 5800: Algorithms — Spring 2026, Northeastern University
Instructor: Dr. Lama Hamandi
