
from pattern_classifier import get_repeated_groups, classify_pattern

test_words = [
    "aaaa",
    "waaaay",
    "soooo",
    "helloooo",
    "aaabbcc",
    "abc",
]

for word in test_words:
    print(f"\nWord: {word}")
    print("Groups:", get_repeated_groups(word))
    print("Pattern:", classify_pattern(word))
