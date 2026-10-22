
class RepeatedLetterDFA:
    """
    Detects consecutive repeated letters using a DFA-style state machine.

    States:
        q_start: No previous character.
        q_last(c): The previous character was c.
        q_found: A consecutive repeated letter was detected.
    """

    def __init__(self):
        self.start_state = "q_start"
        self.accept_state = "q_found"

    def detect(self, word: str) -> bool:
        """Return True if the word contains consecutive repeated letters."""

        state = self.start_state
        previous_char = None

        for char in word.lower():
            if not char.isalpha():
                previous_char = None
                state = self.start_state
                continue

            if state == self.start_state:
                previous_char = char
                state = f"q_last_{char}"

            elif state == f"q_last_{previous_char}":
                if char == previous_char:
                    state = self.accept_state
                else:
                    previous_char = char
                    state = f"q_last_{char}"

            elif state == self.accept_state:
                return True

        return state == self.accept_state
