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
| Scott | CLI spell checker, slides, demo, presentation |

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

# Install dependencies
pip install -r requirements.txt
```

## Branch Strategy

Each team member works on their own branch and merges into `main` via pull requests:

| Branch | Owner | Scope |
|--------|-------|-------|
| `atharv/tabulation-benchmarking` | Atharv | `src/tabulation.py`, `benchmarks/`, `notebooks/atharv_dev.ipynb` |
| `sandeep/naive-memoized` | Sandeep | `src/naive.py`, `src/memoized.py`, `data/`, `notebooks/sandeep_dev.ipynb` |
| `scott/cli-presentation` | Scott | `src/spell_checker.py`, `docs/`, `notebooks/scott_dev.ipynb` |

Shared files (`src/utils.py`, `src/vocab_loader.py`, `tests/`, `README.md`) are edited on `main` or coordinated to avoid conflicts.

## Course

CS 5800: Algorithms — Spring 2026, Northeastern University
Instructor: Dr. Lama Hamandi
