
from automation import RepeatedLetterDFA

dfa = RepeatedLetterDFA()

test_words = [
    "hello",
    "soooo",
    "waaaay",
    "bookkeeper",
    "automata",
    "HELLO",
    "abc123",
]

for word in test_words:
    result = dfa.detect(word)
    print(f"{word:12} -> {result}")
