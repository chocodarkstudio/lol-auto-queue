class SpellingCorrector:
    def __init__(self, words) -> None:
        if words is None:
            self.WORDS = ["hola", "ola", "chau"]
        else:
            self.WORDS = self.__format_words(words)

    def __format_words(self, words):
        return set(w.lower().replace("\'", "") for w in words)

    def get(self, word):
        # its a set to avoid repeated matches
        matches = list(set(self.simple_match(word) + self.correction_match(word)))

        # sort by shortest string
        matches.sort(key=lambda x: len(x))

        # add as last option
        #matches.append(word)
        return matches

    def simple_match(self, word):
        if word is None or len(word) == 0:
            return []

        matches = set()

        for spell in word.split(" "):
            for w in self.WORDS:
                if spell in w:
                    matches.add(w)
                    break
        return list(matches)

    def __known(self, words): 
        """The subset of `words` that appear in the dictionary of WORDS."""
        return set(w for w in words if w in self.WORDS)

    def __edits1(self, word):
        """All edits that are one edit away from `word`."""
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    # do a correction
    def correction_match(self, word):
        if word is None or word == "":
            return []

        word = word.lower()

        """All edits that are two edits away from `word`."""
        edit2 = (e2 for e1 in self.__edits1(word) for e2 in self.__edits1(e1))

        """Generate possible spelling corrections for word."""
        # to return the same input on no match, add this -> "or [word]"" at the end
        candidates = (self.__known([word]) or self.__known(self.__edits1(word)) or self.__known(edit2))

        return list(candidates)
