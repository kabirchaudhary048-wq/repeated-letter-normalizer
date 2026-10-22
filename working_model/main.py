
import re

from automation import RepeatedLetterDFA
from pattern_classifier import get_repeated_groups, classify_pattern


def analyze_text(text: str) -> None:
    """Detect and classify repeated-letter words in a sentence."""

    dfa = RepeatedLetterDFA()

    words = re.findall(r"[A-Za-z]+", text)

    if not words:
        print("No words found.")
        return

    print("\n=== Automata Text Analyzer ===")

    for word in words:
        detected = dfa.detect(word)

        print(f"\nWord: {word}")
        print(f"Repeated letters detected: {detected}")

        if detected:
            groups = get_repeated_groups(word)
            pattern = classify_pattern(word)

            print(f"Repeated groups: {groups}")
            print(f"Pattern number: {pattern}")
        else:
            print("No normalization candidate detected.")


def main() -> None:
    text = input("Enter a sentence: ")
    analyze_text(text)


if __name__ == "__main__":
    main()
