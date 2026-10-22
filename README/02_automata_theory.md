# Automata Theory Background

## Why use an automaton?
A finite automaton reads a string one symbol at a time and changes state according to a transition function. Here, it can detect whether two identical characters occur consecutively in a word.

## DFA definition
A deterministic finite automaton is a 5-tuple:

**M = (Q, Σ, δ, q₀, F)**

- **Q:** finite set of states.
- **Σ:** input alphabet.
- **δ:** transition function.
- **q₀:** start state.
- **F:** set of accepting states.

## Proposed detector
For lowercase English letters, use:
- `q_start`: no character has been read yet.
- `q_last_a` through `q_last_z`: the previous character was the corresponding letter.
- `q_found`: a consecutive repeated character has been found.

This gives 28 states: one start state, 26 previous-character states, and one accepting state.

## Transition idea
- From `q_start`, reading `a` moves to `q_last_a`.
- From `q_last_a`, reading `a` moves to `q_found`.
- From `q_last_a`, reading `b` moves to `q_last_b`.
- From `q_found`, every subsequent character stays in `q_found`.

The same logic applies to all letters. In implementation, a dictionary or indexed state representation can avoid writing out every transition manually.

## What this automaton does not do
The detector recognizes consecutive repetition. It does not decide whether `bookkeeper` is correct, whether `soooo` should become `so`, or whether a candidate is the best dictionary word. Those decisions belong to later normalization and spelling-correction stages.

## Complexity
A single pass over a word of length *n* takes **O(n)** time. The detector uses a constant amount of state, so its auxiliary space is **O(1)** for the scanning process.
