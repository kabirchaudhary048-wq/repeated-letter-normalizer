# Eight Repeated-Letter Pattern Scenarios

The paper groups repeated-letter cases according to the locations of repeated groups in a word. The exact rule implementation should be checked against the paper's figures and tables during development.

| Pattern | General scenario |
|---|---|
| 1 | Repetition at the beginning |
| 2 | One repeated group in the middle |
| 3 | Multiple repeated groups in the middle |
| 4 | Repetition at the end |
| 5 | Repetition at the beginning and middle |
| 6 | Repetition in the middle and at the end |
| 7 | Repetition at the beginning, middle, and end |
| 8 | Repetition at the beginning and end |

## Design approach
Use the automaton to detect consecutive repetition. Then use a run-based classifier to record repeated groups and their positions. Keeping detection and classification separate makes the implementation easier to test and explain.

## Important caution
These are high-level descriptions of the scenarios. Do not invent missing decision rules: implement the detailed branch logic from the paper's method section and figures when coding the normalizer.
