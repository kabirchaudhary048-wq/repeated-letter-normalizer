# Research Paper Summary

## Problem
Social media users often repeat letters to add emphasis, for example `sooooo` or `waaaay`. Such forms can be out-of-vocabulary (OOV) words and may make downstream text processing less effective.

## Proposed approach
The paper proposes RBPsWRL-Sym, which combines:
- rule-based patterns based on the positions of repeated letters;
- candidate generation by reducing repeated letters in different ways;
- SymSpell spelling correction to suggest valid in-vocabulary words.

## Four main phases
1. **Text preprocessing:** tokenize text and prepare words for processing.
2. **Candidate detection:** identify OOV words containing repeated letters.
3. **Candidate generation:** generate possible replacements with SymSpell, TRL1, TRL2, and TRLM2.
4. **Replacement:** apply pattern-specific rules and choose an appropriate candidate.

## Candidate-generation methods
- **TRL1:** reduce repeated letters so each run has one instance.
- **TRL2:** reduce repeated letters so each run has at most two instances.
- **TRLM2:** apply a special rule that reduces repeated letters at the beginning/end while allowing two instances for repetitions in the middle.

## Pattern handling
The paper describes eight scenarios based on whether repeated-letter groups occur at the beginning, middle, or end of a word, and whether there are multiple repeated groups.

## Reported findings
The paper reports an 8% reduction in OOV words and an F1 score of 88% in its comparison with two earlier normalization methods. It also reports improved downstream hate-speech classification metrics after normalization.

## Limitations noted by the paper
Some slang, abbreviations, and unconventional expressions may remain unresolved because a standard spelling dictionary may not contain them.

## Source
Mansur, Z., Omar, N., Tiun, S., & Alshari, E. M. (2024). *A normalization model for repeated letters in social media hate speech text based on rules and spelling correction*. PLOS ONE, 19(3), e0299652. https://doi.org/10.1371/journal.pone.0299652
