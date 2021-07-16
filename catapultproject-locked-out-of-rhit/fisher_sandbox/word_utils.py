import random

class WordGenerator:
    def __init__(self):
        with open('../words.txt', 'r') as filehandle:
            self.words = filehandle.read().split('\n')

    def _get_random_word(self):
        return self.words[random.randrange(0, len(self.words))]

    def _remove_a_letter(self, word):
        letter_to_remove = word[random.randrange(0, len(word))]
        display_word = word.replace(letter_to_remove, "_")
        return letter_to_remove, display_word

    def generate_words(self, number_of_words):
        letters_removed = []
        display_words = []
        while True:
            if len(letters_removed) == number_of_words:
                return letters_removed, display_words
            word = self._get_random_word()
            letter, display_word = self._remove_a_letter(word)
            if not letter in letters_removed:
                letters_removed.append(letter)
                display_words.append(display_word)

