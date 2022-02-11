import random
import re

import util

class WordGuesser:
    def __init__(self, words_list:str):
        self.words_list = words_list
        self.right_set = ['', '', '', '', '']
        self.partial_set = ['', '', '', '', '']
        self.wrong_set = ''

    def validate_letter(self, letter:str):
        # Check string size, must be 1
        if len(letter) != 1:
            util.vlog('Not a single letter: {}'.format(letter))
            return False

        # Check if character is valid letter
        if letter not in util.get_alphabet():
            util.vlog('Not a valid letter: {}'.format(letter))
            return False

        return True

    def add_right(self, letter:str, position:int):
        if not self.validate_letter(letter):
            return False

        # Validate letter position
        if position < 0 or position >= len(self.partial_set):
            util.vlog('Invalid position: {}'.format(position))
            return False

        # Check if letter is already at position
        if self.right_set[position] == letter:
            return True
    
        # Check for existing correct letter at position
        if self.right_set[position] != '':
            util.vlog('Failed to add \'{}\' to right set, position {} contains \'{}\''.format(letter, position, self.right_set[position]))
            return False

        util.vlog('Adding \'{}\' to right set (position: {})'.format(letter, position), 3)
        self.right_set[position] = letter
        return True

    def add_partial(self, letter:str, position:int):
        if not self.validate_letter(letter):
            return False
        
        # Validate letter position
        if position < 0 or position >= len(self.partial_set):
            util.vlog('Invalid position: {}'.format(position))
            return False
        
        # Check if letter already in partial subset
        if letter not in self.partial_set[position]:
            util.vlog('Adding \'{}\' to partial set (position: {})'.format(letter, position), 3)
            self.partial_set[position] += letter
        return True
    
    def add_wrong(self, letter:str):
        if not self.validate_letter(letter):
            return False

        # Check if letter already in wrong set
        if letter not in self.wrong_set:
            util.vlog('Adding \'{}\' to wrong set'.format(letter), 3)
            self.wrong_set += letter
        return True

    def get_random_word(self, word_list:list=[]):
        # Check if word list passed in, otherwise use full words list
        if len(word_list) < 1:
            word_list = self.words_list.split()

        return random.choice(word_list)
    
    def read_in_results(self, word:str, results:list):
        util.vlog('Reading in results for guess: {}'.format(word))

        # Validate word, result pair
        if len(word) != len(results):
            util.vlog('Word length {} does not match results length {}'.format(len(word), len(results)))
            return False
        
        # Validate word letters
        for l in word:
            if not self.validate_letter(l):
                util.vlog('Invalid letter in guess: {}'.format(l))
                return False

        # Loop through each letter, result pair
        i = 0 
        for r in results:
            letter = word[i]
            util.vlog('{}: {}'.format(letter, r))

            # Add letter to appropriate set
            if r is util.Results.WRONG:
                if letter not in self.partial_set:
                    self.add_wrong(letter) 
            elif r is util.Results.RIGHT:
                self.add_right(letter, i)
            elif r is util.Results.PARTIAL:
                self.add_partial(letter, i)
            else:
                util.vlog('Invalid result: {}'.format(r))
                return False
            i += 1

        return True

    
    def get_possible_words(self):
        util.vlog('Getting possible words from current result state')
        util.vlog('Right set: {}'.format(self.right_set), 2)
        util.vlog('Partial set: {}'.format(self.partial_set), 2)
        util.vlog('Wrong set: {}'.format(self.wrong_set), 2)

        # Build regular expression from result sets
        final_reg_exp = '^'
        for i in range(len(self.right_set)):
            right_l = self.right_set[i]
            partial_l = self.partial_set[i]

            # Set correctly guessed letter for current position
            if right_l != '':
                util.vlog('Letter \'{}\' in right set at {}'.format(right_l, i), 3)
                reg_exp = right_l
            # Remove letters in partial set for current position
            elif partial_l != '':
                util.vlog('Letters \'{}\' in partial set at {}'.format(partial_l, i), 3)
                reg_exp = '[^'
                reg_exp += self.partial_set[i]
                reg_exp += self.wrong_set
                reg_exp += ']'
            # Remove letters not in word for current position
            else:
                util.vlog('No info for position {}'.format(i), 3)
                reg_exp = '[^'
                reg_exp += self.wrong_set
                reg_exp += ']'

            util.vlog('Regex: \'{}\''.format(reg_exp), 3)
            final_reg_exp += reg_exp

        final_reg_exp += '$'
        util.vlog('Final Regex: \'{}\''.format(final_reg_exp), 2)
        
        # Search for matches in word dictionary
        match = re.findall(final_reg_exp, self.words_list, re.MULTILINE)
        if match:
            util.vlog('Matches ({}): {}'.format(len(match), match), 4)

            # Get all partial letters (in word, wrong position)
            partials = ''
            for p in self.partial_set:
                partials += p
            util.vlog('Partial letters: {}'.format(partials), 3)

            # Refine search by factoring in partial letters
            possible_words = []
            for word in match:
                valid = True
                for l in partials:
                   if l not in word: 
                       valid = False
                if valid:
                    possible_words.append(word)
            util.vlog('Refined Matches ({}): {}'.format(len(possible_words), possible_words), 4)

            return possible_words
        else:
            util.vlog('No matches found from current result state')

        return False