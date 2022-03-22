import random
import re

import util

class WordGuesser:
    def __init__(self, words_list:str, word_length:int):
        self.words_list = words_list
        self.word_length = word_length
        self.right_set = WordSet(word_length, False)
        self.partial_set = WordSet(word_length, True)
        self.wrong_set = WordSet(word_length, True)

    def reset_game_state(self):
        self.right_set.clear_set()
        self.partial_set.clear_set()
        self.wrong_set.clear_set()
        util.vlog('Reset word guesser game state', 3)

    def get_random_word(self, word_list:list=[]):
        # Check if word list passed in, otherwise use full words list
        if len(word_list) < 1:
            word_list = self.words_list.split()

        word = random.choice(word_list)
        util.vlog('Chose random word: {}'.format(word), 3)
        return word
    
    def read_in_results(self, word:str, results:list):
        util.vlog('Reading in results for guess: {}'.format(word), 3)

        # Validate word, result pair
        if len(word) != len(results):
            util.vlog('Word length {} does not match results length {}'.format(len(word), len(results)))
            return False
        
        # Validate word letters
        if not util.validate_word(word):
            util.vlog('Invalid letter in guess: {}'.format(word))
            return False

        # Loop through each letter, result pair
        observed = []
        i = 0 
        for r in results:
            letter = word[i]
            observed.append(letter)
            util.vlog('{}: {}'.format(letter, r), 4)

            # Add letter to appropriate set
            if r is util.Results.WRONG:
                if not self.partial_set.letter_in_set(letter):
                    self.wrong_set.add_letter(letter, i)
            elif r is util.Results.RIGHT:
                self.right_set.add_letter(letter, i)
            elif r is util.Results.PARTIAL:
                self.partial_set.add_letter(letter, i)
            else:
                util.vlog('Invalid result: {}'.format(r))
                return False
            i += 1

        return True
    
    def get_possible_words(self):
        util.vlog('Getting possible words from current result state', 3)
        util.vlog('Right set: {}'.format(self.right_set), 5)
        util.vlog('Partial set: {}'.format(self.partial_set), 5)
        util.vlog('Wrong set: {}'.format(self.wrong_set), 5)

        # Build regular expression from result sets
        final_reg_exp = '^'
        for i in range(self.word_length):
            right_l = self.right_set.get_pos_letters(i)
            partial_l = self.partial_set.get_pos_letters(i)
            wrong_l = self.wrong_set.get_all_letters()

            # Set correctly guessed letter for current position
            if right_l != '':
                util.vlog('Letter \'{}\' in right set at {}'.format(right_l, i), 6)
                reg_exp = right_l
            # Remove letters in partial set for current position
            elif partial_l != '':
                util.vlog('Letters \'{}\' in partial set at {}'.format(partial_l, i), 6)
                reg_exp = '[^'
                reg_exp += partial_l
                reg_exp += wrong_l
                reg_exp += ']'
            # Remove letters not in word for current position
            else:
                util.vlog('No info for position {}'.format(i), 6)
                reg_exp = '[^'
                reg_exp += wrong_l
                reg_exp += ']'

            util.vlog('Regex: \'{}\''.format(reg_exp), 5)
            final_reg_exp += reg_exp

        final_reg_exp += '$'
        util.vlog('Final Regex: \'{}\''.format(final_reg_exp), 5)
        
        # Search for matches in word dictionary
        match = re.findall(final_reg_exp, self.words_list, re.MULTILINE)
        if match:
            util.vlog('Matches ({}): {}'.format(len(match), match), 6)

            # Get all partial letters (in word, wrong position)
            partials = self.partial_set.get_all_letters()
            util.vlog('Partial letters: {}'.format(partials), 6)

            # Refine search by factoring in partial letters
            possible_words = []
            for word in match:
                valid = True
                for l in partials:
                   if l not in word: 
                       valid = False
                if valid:
                    possible_words.append(word)
            util.vlog('Possible Words: {}'.format(len(possible_words)), 3)
            util.vlog(possible_words, 4)

            return possible_words
        else:
            util.vlog('No matches found from current result state')

        return []

class WordSet:
    def __init__(self, word_length:int, multiple:bool):
        self.word_length = word_length
        self.letters = [''] * word_length
        self.multiple = multiple

    def add_letter(self, letter:str, position:int):
        if not util.validate_letter(letter):
            return False

        # Validate letter position
        if position < 0 or position >= self.word_length:
            util.vlog('Invalid position: {}'.format(position))
            return False

        # Check if letter is already at position
        if self.multiple and letter in self.letters[position]:
            util.vlog('Letter \'{}\' already in word set at position {}'.format(letter, position), 5)
            return True
    
        # Check for existing correct letter at position
        if not self.multiple and self.letters[position] != '':
            util.vlog('Failed to add \'{}\' to word set, position {} contains \'{}\''.format(letter, position, self.letters[position]), 5)
            return False

        util.vlog('Adding \'{}\' to word set (position: {})'.format(letter, position), 5)
        self.letters[position] += letter
        return True

    def get_all_letters(self):
        letters = ''
        for i in range(len(self.letters)):
            letters += self.get_pos_letters(i)
        return letters

    def get_pos_letters(self, position:int):
        if position < 0 or position > len(self.letters):
            util.vlog('Invalid position {} for word set of length {}'.format(position, len(self.letters)))
            return False
        return self.letters[position]

    def letter_in_set(self, letter:str):
        contains = False
        for i in range(len(self.letters)):
            if self.letter_at_position(letter, i):
                util.vlog('Letter \'{}\' in word set at position {}'.format(letter, i))
                contains = True
        return contains

    def letter_at_position(self, letter:str, position:int):
        if position < 0 or position > len(self.letters):
            util.vlog('Invalid position {} for word set of length {}'.format(position, len(self.letters)))
            return False
        return letter in self.letters[position]

    def clear_set(self):
        self.letters = [''] * self.word_length

    def __str__(self):
        return str(self.letters)