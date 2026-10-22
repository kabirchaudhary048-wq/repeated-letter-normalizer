
def get_repeated_groups(word: str) -> list[dict]:
    """Return consecutive repeated-letter groups and their positions."""
    word = word.lower()
    groups = []
    i = 0

    while i < len(word):
        j = i + 1

        while j < len(word) and word[j] == word[i]:
            j += 1

        if word[i].isalpha() and j - i > 1:
            if i == 0:
                position = "beginning"
            elif j == len(word):
                position = "end"
            else:
                position = "middle"

            groups.append({
                "character": word[i],
                "count": j - i,
                "start": i,
                "end": j - 1,
                "position": position,
            })

        i = j

    return groups


def analyze_word(word: str) -> dict:
    """Collect repetition information for pattern matching."""
    groups = get_repeated_groups(word)

    return {
        "word": word,
        "has_repetition": bool(groups),
        "groups": groups,
        "repeated_group_count": len(groups),
        "positions": {group["position"] for group in groups},
        "first_group_length": groups[0]["count"] if groups else 1,
        "last_group_length": groups[-1]["count"] if groups else 1,
    }


def classify_pattern(word: str) -> int | None:
    """Preliminary mapping to the paper's eight pattern scenarios."""
    data = analyze_word(word)

    if not data["has_repetition"]:
        return None

    positions = data["positions"]
    rlc = data["repeated_group_count"]
    first_len = data["first_group_length"]
    last_len = data["last_group_length"]

    if positions == {"beginning"} and rlc == 1:
        return 1

    if positions == {"middle"} and rlc == 1:
        return 2

    if positions == {"middle"} and rlc >= 2:
        return 3

    if positions == {"end"} and rlc == 1:
        return 4

    if positions == {"beginning", "middle"}:
        if first_len > 1 and last_len == 1 and rlc > 1:
            return 5

    if positions == {"middle", "end"}:
        if first_len == 1 and last_len > 1 and rlc > 2:
            return 6

    if positions == {"beginning", "middle", "end"}:
        if first_len > 1 and last_len > 1 and rlc > 2:
            return 7

    if positions == {"beginning", "end"}:
        if first_len > 1 and last_len > 1 and rlc == 2:
            return 8

    return None


if __name__ == "__main__":
    test_words = [
        "aaaa",
        "soooo",
        "waaaay",
        "aaabbcc",
        "helloooo",
        "abc",
        "cccccaaaaannnnn",
    ]

    for word in test_words:
        result = analyze_word(word)
        print(f"\nWord: {word}")
        print(f"Groups: {result['groups']}")
        print(f"Pattern: {classify_pattern(word)}")
