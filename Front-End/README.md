# Automata-Based Text Normalizer Frontend

This is a small Streamlit interface for the existing Python college project. It:
- accepts a sentence and normalizes each word using `normalize_word`;
- preserves spaces and punctuation;
- displays a conceptual DFA-style state diagram;
- shows a character-by-character detector trace for a selected word.

## Setup

Copy `app.py` into your existing `working_model` folder. Your folder should contain:
- `automation.py`
- `normalizer.py`
- `symspell_corrector.py`
- `candidate_generator.py`
- `pattern_classifier.py`
- `replacement_rules.py`

From the `working_model` folder, install the frontend dependencies:

```powershell
pip install streamlit pandas
```

Then launch the interface:

```powershell
python -m streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`, and open it in your browser.

## Example

Input:

`hiiiiiii how are youuuuuuuu`

The interface processes each word with the current project normalizer. The expected simple intention is a result like `hi how are you`, but the exact output depends on the current classifier and replacement logic in `normalizer.py`.

## Important limitation

The frontend illustrates the repeated-letter detector and calls the project's current normalization pipeline. It does not make the research implementation more accurate by itself. The pattern classifier and replacement procedures are still a preliminary implementation; review outputs before claiming they faithfully reproduce all eight paper rules.
