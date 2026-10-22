
from pattern_classifier import classify_pattern
from replacement_rules import (
    checking_algorithm,
    double_case_middle_scenario,
    end_scenario,
    beginning_middle_end_scenario,
    beginning_middle_end_pattern7,
    beginning_end_pattern8,
)
from symspell_corrector import create_symspell


def normalize_word(word: str, sym_spell) -> str:
    """Select a preliminary replacement procedure by pattern."""
    pattern = classify_pattern(word)

    if pattern is None:
        return word

    if pattern == 1:
        # Pattern 1: repetition at the beginning.
        from candidate_generator import trl1
        return trl1(word)

    if pattern == 2:
        result = checking_algorithm(word, sym_spell)
        return result if result is not None else word

    if pattern == 3:
        return double_case_middle_scenario(word, sym_spell)

    if pattern == 4:
        return end_scenario(word, sym_spell)

    if pattern in (5, 6):
        return beginning_middle_end_scenario(word, sym_spell)

    if pattern == 7:
        from candidate_generator import trlm2
        return trlm2(word)

    if pattern == 8:
        return beginning_end_pattern8(word, sym_spell)

    return word


if __name__ == "__main__":
    sym_spell = create_symspell()

    test_words = [
        "aaaa",
        "soooo",
        "waaaay",
        "aaabbcc",
        "helloooo",
        "cccccaaaaannnnn",
        "abc",
    ]

    for word in test_words:
        print(f"{word:20} -> {normalize_word(word, sym_spell)}")
