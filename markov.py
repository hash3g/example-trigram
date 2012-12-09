import random
import re
import string
import textwrap


class Markov(object):
    """
    Markov-chain text generator. Translated
    from the original PHP into Python (haykranen.nl)
    Currently working on a generator of poetry.
    """

    def __init__(self, textfile, length=600, letters=''):
        forbid = string.punctuation

        text = " ".join(textwrap.wrap(textfile)).strip()
        self.text = re.sub('[%s]+' % re.escape(forbid), ' ', text).lower()

        self.text_list = self.generate_markov_list(self.text)
        self.markov_table = self.generate_markov_table(self.text_list)
        self.length = length
        self.letters = letters

    def _run(self, letters=''):
        return self.generate_poetry(self.length, self.markov_table)

    def generate_markov_list(self, text):
        return text.split()

    def generate_markov_table(self, text_list):
        self.table = {}

        # walk through text, make index table
        for i in range(len(self.text_list) - 1):
            char = Token(text_list[i])
            if char.token_value not in self.table:
                self.table[char.token_value] = {}

        # walk array again, count numbers
        for i in range(len(text_list) - 1):

            char_index = Token(text_list[i])
            char_count = Token(text_list[i + 1])

            table = self.table[char_index.token_value]
            if char_count.token_value not in table.keys():
                self.table[char_index.token_value][char_count.token_value] = 1
            else:
                self.table[char_index.token_value][char_count.token_value] += 1

        return self.table

    def generate_poetry(self, length, table):
        o = list()
        for i in range(4):
            o.append(self.generate_markov_text(length, table))
        return '. '.join(o)

    def lookup_proper_word(self, table, callback=lambda x: x):
        # loop cycle 5 times before we do not find the word with letters
        word = None

        for k in range(5):
            word = callback()
            if re.match('[%s]+' % re.escape(self.letters), word):
                break

        return word

    def lookup_proper_words_from_table(self, tablewords):
        words = []
        for word in tablewords:
            if re.match('[%s]+' % re.escape(self.letters), word, re.I | re.U):
                words.append(word)
        return words

    def generate_markov_text(self, length, table):

        words = self.lookup_proper_words_from_table(table.keys())
        if not words:
            return ''

        result = ''
        for j in range(10):
            o = list()

            word = random.choice(words)

            if not word:
                continue

            o.append(word)
            for i in range(length):

                newword = self.lookup_proper_word(table,
                    lambda x=None: self.return_weighted_char(table[word]))

                if newword:
                    word = newword
                    o.append(newword)
                else:
                    word = random.choice(words)

            if len(' '.join(o)) > len(result):
                result = ' '.join(o)

        return result

    def return_weighted_char(self, array):
        if not array:
            return False
        else:
            total = sum(array.values())
            rand = random.randint(1, total)
            for key, value in array.iteritems():
                if rand <= value:
                    return key
                rand -= value


class Token(object):

    def __init__(self, token):
        self.token_ending = token[:-2]
        self.token_value = token
