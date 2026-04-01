"""
CodeCorrect — Streamlit Demo App

Launch with:  streamlit run app.py
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from vocab_loader import load_vocabulary
from naive import edit_distance_naive
from memoized import edit_distance_memoized
from tabulation import edit_distance_tabulation, edit_distance_optimized

METHODS = {
    "Naive Recursion": edit_distance_naive,
    "Memoized (Top-Down)": edit_distance_memoized,
    "Tabulation (Bottom-Up)": edit_distance_tabulation,
    "Space-Optimized": edit_distance_optimized,
}

VOCAB_PATH = os.path.join(os.path.dirname(__file__), "data", "python_keywords.txt")

st.set_page_config(page_title="CodeCorrect", page_icon="⌨️", layout="centered")

st.title("⌨️ CodeCorrect")
st.caption("Edit distance spell checker for programmer typos — CS 5800 Final Project")

# --- Sidebar controls ---
st.sidebar.header("Settings")
word = st.sidebar.text_input("Mistyped word", value="pritn", max_chars=30)
method_name = st.sidebar.selectbox("DP Method", list(METHODS.keys()), index=3)
top_n = st.sidebar.slider("Top-N suggestions", min_value=1, max_value=20, value=5)
compare_all = st.sidebar.checkbox("Compare all methods", value=False)

# Warn about naive on long inputs
if method_name == "Naive Recursion" and len(word) > 10:
    st.sidebar.warning("⚠️ Naive recursion is exponential — may be slow for words longer than ~10 characters.")

# --- Load vocabulary ---
if not os.path.exists(VOCAB_PATH):
    st.error(f"Vocabulary file not found: {VOCAB_PATH}")
    st.stop()

vocab = load_vocabulary(VOCAB_PATH)

if not word.strip():
    st.info("Enter a mistyped word in the sidebar to get started.")
    st.stop()

# --- Compute suggestions ---
func = METHODS[method_name]

start = time.perf_counter()
suggestions = [(func(word, v), v) for v in vocab]
elapsed = time.perf_counter() - start
suggestions.sort()

st.subheader(f"Suggestions for `{word}`")
st.markdown(f"**Method:** {method_name} · **Time:** {elapsed*1000:.2f} ms · **Vocabulary:** {len(vocab)} words")

# Results table
col1, col2 = st.columns([1, 3])
col1.markdown("**Rank**")
col2.markdown("**Word (edit distance)**")
for i, (dist, w) in enumerate(suggestions[:top_n], 1):
    col1, col2 = st.columns([1, 3])
    col1.write(f"{i}.")
    col2.write(f"`{w}` — distance **{dist}**")

# --- Compare all methods ---
if compare_all:
    st.divider()
    st.subheader("Method Comparison")

    timings = {}
    for name, fn in METHODS.items():
        if name == "Naive Recursion" and len(word) > 12:
            timings[name] = None  # skip to avoid hanging
            continue
        t0 = time.perf_counter()
        _ = [(fn(word, v), v) for v in vocab]
        timings[name] = (time.perf_counter() - t0) * 1000

    for name, ms in timings.items():
        if ms is None:
            st.write(f"**{name}:** ⏭️ skipped (word too long for exponential algorithm)")
        else:
            st.write(f"**{name}:** {ms:.2f} ms")

    # Bar chart
    chart_data = {k: v for k, v in timings.items() if v is not None}
    if chart_data:
        st.bar_chart(chart_data, horizontal=True)
