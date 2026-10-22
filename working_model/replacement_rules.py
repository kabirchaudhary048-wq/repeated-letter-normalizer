
from symspellpy import SymSpell, Verbosity

from candidate_generator import trl1, trl2, trlm2


def lookup_candidate(
    word: str,
    sym_spell: SymSpell,
    max_edit_distance: int = 2,
) -> str | None:
    """Return the closest SymSpell suggestion, or None."""
    suggestions = sym_spell.lookup(
        word.lower(),
        Verbosity.CLOSEST,
        max_edit_distance=max_edit_distance,
    )

    if not suggestions:
        return None

    return suggestions[0].term


def checking_algorithm(
    word: str,
    sym_spell: SymSpell,
    max_edit_distance: int = 2,
) -> str | None:
    """
    CA: try repeated groups truncated to two characters,
    then to one character.
    """
    candidate_two = trl2(word)
    result = lookup_candidate(
        candidate_two,
        sym_spell,
        max_edit_distance,
    )

    if result is not None:
        return result

    candidate_one = trl1(word)
    return lookup_candidate(
        candidate_one,
        sym_spell,
        max_edit_distance,
    )


def double_case_middle_scenario(
    word: str,
    sym_spell: SymSpell,
    max_edit_distance: int = 2,
) -> str:
    """DCMs: truncate repeated groups to one character."""
    candidate = trl1(word)

    result = lookup_candidate(
        candidate,
        sym_spell,
        max_edit_distance,
    )

    return result if result is not None else candidate


def end_scenario(
    word: str,
    sym_spell: SymSpell,
    max_edit_distance: int = 2,
) -> str:
    """Pattern 4: handle repetition at the end."""
    candidate_one = trl1(word)

    if len(candidate_one) < 4:
        return candidate_one

    candidate_two = trl2(word)
    result = lookup_candidate(
        candidate_two,
        sym_spell,
        max_edit_distance,
    )

    return result if result is not None else word


def beginning_middle_end_scenario(
    word: str,
    sym_spell: SymSpell,
    max_edit_distance: int = 2,
) -> str:
    """Shared preliminary procedure for Patterns 5 and 6."""
    result = checking_algorithm(
        word,
        sym_spell,
        max_edit_distance,
    )

    if result is not None:
        return result

    return trlm2(word)


def beginning_middle_end_pattern7(
    word: str,
    sym_spell: SymSpell,
    max_edit_distance: int = 2,
) -> str:
    """Preliminary BMEs procedure for Pattern 7."""
    candidate = trlm2(word)

    result = lookup_candidate(
        candidate,
        sym_spell,
        max_edit_distance,
    )

    return result if result is not None else candidate


def beginning_end_pattern8(
    word: str,
    sym_spell: SymSpell,
    max_edit_distance: int = 2,
) -> str:
    """Preliminary BEs procedure for Pattern 8."""
    result = lookup_candidate(
        word,
        sym_spell,
        max_edit_distance,
    )

    if result is not None:
        return result

    candidate = trlm2(word)
    result = lookup_candidate(
        candidate,
        sym_spell,
        max_edit_distance,
    )

    if result is not None:
        return result

    return trl1(word)


if __name__ == "__main__":
    from symspell_corrector import create_symspell

    sym_spell = create_symspell()

    test_cases = [
        ("CA", "soooo", checking_algorithm),
        ("DCMs", "aaabbcc", double_case_middle_scenario),
        ("End scenario", "helllooo", end_scenario),
        (
            "Patterns 5-6",
            "cccccaaaaannnnn",
            beginning_middle_end_scenario,
        ),
        (
            "Pattern 7",
            "cccccaaaaannnnn",
            beginning_middle_end_pattern7,
        ),
        (
            "Pattern 8",
            "aaabbcc",
            beginning_end_pattern8,
        ),
    ]

    for name, word, function in test_cases:
        result = function(word, sym_spell)
        print(f"{name:15} | {word:20} -> {result}")
