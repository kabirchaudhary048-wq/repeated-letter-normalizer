# Algorithms and Processing Pipeline

## Pipeline
1. Receive a sentence.
2. Tokenize it while preserving punctuation where possible.
3. Pass each word through the repeated-character DFA.
4. Leave words without repeated characters unchanged.
5. Classify repeated-letter candidates into one of the paper's pattern scenarios.
6. Generate candidate forms using TRL1, TRL2, and TRLM2.
7. Check candidates with SymSpell.
8. Apply the pattern-specific selection logic.
9. Reassemble the sentence and report the changes.

## Candidate transformations
- **TRL1:** collapse each consecutive run to one character.
- **TRL2:** limit each consecutive run to two characters.
- **TRLM2:** a position-aware transformation that keeps up to two characters in the middle and reduces repetitions at other positions. The exact implementation should follow the paper's algorithm.

## Spelling correction
SymSpell can propose dictionary words based on edit-distance-oriented lookup. A suggested word is a candidate, not a guarantee that the replacement fits the sentence context.

## Safety against overcorrection
- Preserve punctuation and capitalization where practical.
- Avoid replacing a word if no suitable candidate is found.
- Include test cases for valid words that naturally contain repeated letters.
- Log the original word, detected pattern, generated candidates, and selected output for debugging.
