

def trl1(word: str) -> str:
    result = []
    previous_char = None

    for char in word:
        if char != previous_char:
            result.append(char)
        previous_char = char

    return "".join(result)


def trl2(word: str) -> str:
    result = []
    previous_char = None
    count = 0

    for char in word:
        if char == previous_char:
            count += 1
        else:
            previous_char = char
            count = 1

        if count <= 2:
            result.append(char)

    return "".join(result)



def trlm2(word: str) -> str:
    result = []
    i = 0

    while i < len(word):
        j = i + 1

        while j < len(word) and word[j] == word[i]:
            j += 1

        count = j - i

        
        if i == 0:
            keep = 1
        else:
            keep = min(count, 2)

        result.extend([word[i]] * keep)
        i = j

    return "".join(result)



if __name__ == "__main__":
    words = [
        "soooo",
        "waaaaay",
        "loooove",
        "hello",
        "cccccaaaaannnnn",
    ]

    for word in words:
        print(f"Input: {word}")
        print(f"TRL1:  {trl1(word)}")
        print(f"TRL2:  {trl2(word)}")
        print(f"TRLM2: {trlm2(word)}")
        print()
