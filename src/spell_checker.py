#!/usr/bin/env python3
"""
CodeCorrect CLI Spell Checker

Usage: python spell_checker.py --word <mistyped> --vocab <file> --method <naive|memoized|tabulation>
"""

import sys
sys.path.insert(0, 'src')

import argparse
import sys
from vocab_loader import load_vocabulary
from naive import edit_distance_naive
from memoized import edit_distance_memoized
from tabulation import edit_distance_tabulation

def get_edit_distance_func(method):
    if method == 'naive':
        return edit_distance_naive
    elif method == 'memoized':
        return edit_distance_memoized
    elif method == 'tabulation':
        return edit_distance_tabulation
    else:
        raise ValueError(f"Unknown method: {method}")

def main():
    parser = argparse.ArgumentParser(description="CodeCorrect Spell Checker")
    parser.add_argument('--word', required=True, help='Mistyped word')
    parser.add_argument('--vocab', required=True, help='Path to vocabulary file')
    parser.add_argument('--method', choices=['naive', 'memoized', 'tabulation'], default='tabulation', help='DP method')
    parser.add_argument('--top', type=int, default=5, help='Number of suggestions')
    
    args = parser.parse_args()
    
    vocab = load_vocabulary(args.vocab)
    func = get_edit_distance_func(args.method)
    
    # Compute distances
    suggestions = []
    for v in vocab:
        dist = func(args.word, v)
        suggestions.append((dist, v))
    
    # Sort by distance
    suggestions.sort()
    
    # Print top suggestions
    print(f"Suggestions for '{args.word}':")
    for dist, word in suggestions[:args.top]:
        print(f"  {word} (distance: {dist})")

if __name__ == '__main__':
    main()