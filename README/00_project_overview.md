# Automata-Based Repeated-Letter Text Normalizer

## Project overview
This project studies and implements a text-normalization approach inspired by the paper:

**A normalization model for repeated letters in social media hate speech text based on rules and spelling correction**  
Zainab Mansur, Nazlia Omar, Sabrina Tiun, and Eissa M. Alshari  
*PLOS ONE*, published March 21, 2024.  
DOI: https://doi.org/10.1371/journal.pone.0299652

The goal is to identify words with exaggerated consecutive letters and generate more conventional spellings. Examples include `sooooo` and `waaaay`.

## Project boundary
The research paper proposes a rule-based normalization method combined with SymSpell. This project makes the automata component explicit by using a finite-state detector for consecutive repeated characters, followed by a separate rule-based pattern classifier and spelling correction.

The automaton detects a pattern; it does not independently determine the correct English word.

## Main stages
1. Preprocess and tokenize input text.
2. Detect words containing consecutive repeated characters.
3. Classify the repeated-letter positions.
4. Generate candidate spellings using TRL1, TRL2, and TRLM2 transformations.
5. Use spelling suggestions to help choose a replacement.
6. Evaluate the implementation on examples and, if available, a suitable dataset.

## Important evaluation note
The paper reports an 8% reduction in out-of-vocabulary words and an F1 score of 88% for its normalization comparison. These are the paper's reported results, not results of this student implementation. Any project results must be measured separately.
