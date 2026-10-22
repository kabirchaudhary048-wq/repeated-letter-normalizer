
from pathlib import Path
from importlib.resources import files

from symspellpy import SymSpell, Verbosity


def create_symspell(max_dictionary_edit_distance: int = 2) -> SymSpell:
    sym_spell = SymSpell(
        max_dictionary_edit_distance=max_dictionary_edit_distance,
        prefix_length=7,
    )

    dictionary_path = files("symspellpy").joinpath(
        "frequency_dictionary_en_82_765.txt"
    )

    dictionary_loaded = sym_spell.load_dictionary(
        str(dictionary_path),
        term_index=0,
        count_index=1,
    )

    if not dictionary_loaded:
        raise RuntimeError("Failed to load the English frequency dictionary.")

    return sym_spell


def get_spelling_candidates(
    word: str,
    sym_spell: SymSpell,
    max_edit_distance: int = 2,
) -> list[dict]:
    suggestions = sym_spell.lookup(
        word.lower(),
        Verbosity.ALL,
        max_edit_distance=max_edit_distance,
    )

    return [
        {
            "word": item.term,
            "distance": item.distance,
            "frequency": item.count,
        }
        for item in suggestions
    ]


if __name__ == "__main__":
    sym_spell = create_symspell()

    for word in ["helllo", "soooo", "freind"]:
        print(f"\nInput: {word}")
        for candidate in get_spelling_candidates(word, sym_spell):
            print(candidate)
