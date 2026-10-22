# Project Results: Repeated-Letter Text Normalizer

## 1. Project overview

This project implements a prototype for normalizing words that contain
repeated consecutive letters. It is based on the ideas in the research
paper:

Mansur, Z., Omar, N., Tiun, S., & Alshari, E. M. (2024). *A
normalization model for repeated letters in social media hate speech
text based on rules and spelling correction*. PLOS ONE, 19(3), e0299652.
https://doi.org/10.1371/journal.pone.0299652

The prototype combines repeated-letter detection, three letter-reduction
transformations, SymSpell spelling suggestions, a preliminary pattern
classifier, and replacement procedures.

**Important scope note:** This is a college-project prototype inspired
by the paper. The current implementation has not been verified as a
complete reproduction of every rule in the paper, and the paper's
reported evaluation metrics have not been reproduced.

## 2. Main components

### Repeated-letter detector

The detector scans a word one character at a time and compares each
character with the previous character. It reports repetition when two
adjacent alphabetic characters are the same.

Examples: - `soooo` contains repeated `o` characters. - `hello` contains
the adjacent pair `ll`. - `world` contains no adjacent repeated letters.

The detector is a finite-state-style component: it tracks the previous
character and whether a repetition has been detected. It identifies a
pattern; it does not perform the spelling correction itself.

### Repeated-letter transformations

The project implements three transformations:

  -----------------------------------------------------------------------
  Transformation          Purpose                 Example
  ----------------------- ----------------------- -----------------------
  TRL1                    Keep one character from `soooo` → `so`
                          each consecutive group  

  TRL2                    Keep up to two          `soooo` → `soo`
                          characters from each    
                          consecutive group       

  TRLM2                   Special reduction that  `cccccaaaaannnnn` →
                          keeps two characters in `caann`
                          middle groups and one   
                          at other positions for  
                          the paper's illustrated 
                          case                    
  -----------------------------------------------------------------------

The TRLM2 example is a documented intermediate result from the paper. It
does not mean that every word's final normalized form should be `caann`
or that this example alone verifies every TRLM2 edge case.

### SymSpell spelling suggestions

The project uses `symspellpy` and its bundled English frequency
dictionary to obtain spelling suggestions. SymSpell can rank suggestions
using edit distance and word frequency.

A dictionary suggestion is not automatically guaranteed to be the
intended correction. The surrounding pattern rules are meant to guide
candidate selection.

### Pattern classifier and replacement procedures

A preliminary classifier assigns repeated-letter words to pattern
scenarios. The replacement module includes preliminary implementations
of the Checking Algorithm (CA), the double-case-middle procedure (DCMs),
the end scenario, the shared BMs-MEs procedure, BMEs for Pattern 7, and
BEs for Pattern 8.

These procedures form a working starting point, but their conditions and
fallback behavior have not all been validated against the paper's full
tables and flowcharts. The integrated pipeline therefore should be
described as a preliminary implementation rather than a fully faithful
reproduction of the research method.

## 3. Tests performed

The project's basic automated test suite contains five tests covering:

1.  Repeated-letter detection.
2.  TRL1 behavior.
3.  TRL2 behavior.
4.  The documented TRLM2 example.
5.  Behavior for a word without repeated letters.

The test suite was run during development. After correcting the detector
test so that `hello` correctly counts as containing repeated adjacent
letters, the user reported that the tests passed.

These tests verify only the specific behaviors listed above. They do not
measure normalization accuracy across a dataset or prove that all eight
pattern rules match the research paper.

To run the tests from the `working_model` directory:

``` bash
python -m unittest test_normalizer.py
```

To run the demonstration pipeline:

``` bash
python normalizer.py
```

## 4. Observed demonstration behavior

During development, the pipeline produced outputs including:

  -----------------------------------------------------------------------
  Input                   Observed output         Interpretation
  ----------------------- ----------------------- -----------------------
  `waaaay`                `way`                   A plausible
                                                  normalization of
                                                  repeated letters

  `abc`                   `abc`                   An ordinary word with
                                                  no repeated-letter
                                                  pattern remains
                                                  unchanged

  `cccccaaaaannnnn`       `can` in one integrated The spelling lookup
                          run                     selected a shorter
                                                  dictionary candidate
                                                  rather than preserving
                                                  the paper's
                                                  intermediate candidate
                                                  `caann`
  -----------------------------------------------------------------------

The `cccccaaaaannnnn` result demonstrates an important limitation: a
spelling-correction system may choose a valid dictionary word that is
not the intended normalization. The paper's `caann` example is the
output of TRLM2 at an intermediate stage; additional paper-specific
checks are needed after that stage. The project should not claim that
the final output is correct solely because SymSpell returned a
dictionary suggestion.

Outputs can vary with the exact code version and dictionary lookup
settings. The examples above are development observations, not a formal
evaluation dataset.

## 5. Connection to Automata Theory

The clearest automata-theory component is the repeated-letter detector.
It can be described using two conceptual states:

-   **q0:** no adjacent repeated pair has been detected.
-   **q1:** an adjacent repeated pair has been detected; this is the
    accepting state.

While scanning the input, the detector remembers the previous character.
If the current character equals the previous character, it transitions
to q1. Once q1 is reached, detection has succeeded.

This illustrates state-based processing of a string. The spelling
correction, transformations, and rule-based replacement stages are
additional algorithms in the overall text-normalization pipeline; they
should not all be described as finite automata.

## 6. Results and conclusion

The project demonstrates a working prototype that brings together:

-   adjacent repeated-letter detection;
-   TRL1, TRL2, and TRLM2 transformations;
-   SymSpell dictionary-based candidate suggestions;
-   a preliminary eight-pattern classifier;
-   initial replacement procedures;
-   basic automated tests.

The tests and demonstrations show that the main components can execute
together, but the current work does **not** establish a measured
accuracy score. The research paper's reported results, including its 88%
F1 score and 8% reduction in out-of-vocabulary words, belong to the
authors' experiments and must not be presented as results achieved by
this project.

## 7. Limitations and future improvements

The following work would be needed for a stronger reproduction:

1.  Verify the classifier's pattern conditions against the paper's
    original Table 2 and flowcharts.
2.  Validate the exact behavior of TRLM2 on more examples.
3.  Complete and test each replacement procedure, including its fallback
    conditions.
4.  Prevent unverified dictionary suggestions from being treated
    automatically as correct replacements.
5.  Build a labeled test set and report measurable metrics such as
    precision, recall, F1 score, and out-of-vocabulary reduction.
6.  Compare the project's results with a baseline using the same data
    and evaluation method.

## Reference

Mansur, Z., Omar, N., Tiun, S., & Alshari, E. M. (2024). A normalization
model for repeated letters in social media hate speech text based on
rules and spelling correction. *PLOS ONE, 19*(3), e0299652.
https://doi.org/10.1371/journal.pone.0299652
