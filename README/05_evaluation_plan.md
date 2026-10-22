# Evaluation Plan

## Functional tests
Test at least:
- ordinary words with no repeated consecutive letters;
- exaggerated repetitions at the beginning, middle, and end;
- repeated groups at multiple positions;
- words that should remain unchanged;
- punctuation and capitalization;
- cases where spelling correction has no suitable suggestion.

## Metrics
If a labeled set of expected normalized words is available, calculate:
- **Precision:** proportion of replacements made by the system that are correct.
- **Recall:** proportion of words that should be normalized that the system normalizes correctly.
- **F1 score:** harmonic mean of precision and recall.

For OOV reduction, count OOV tokens before and after normalization using the same vocabulary checker and dataset.

## Baseline comparison
A useful baseline is a simple rule that limits each repeated run to one or two characters. Compare it with the pattern-based implementation on the same examples.

## Reporting
Clearly separate:
1. values reported in the research paper;
2. measurements produced by this implementation;
3. qualitative examples.

Do not claim to reproduce the paper's reported scores unless the experiments were actually reproduced.
