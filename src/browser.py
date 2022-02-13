import pyautogui
import time
from PIL import ImageGrab

import guesser
import util

def run_browser_bot(word_guesser:guesser.WordGuesser, start_word:str, enter_key_coords:tuple, board_tl_coords:tuple):
    wordle_game = Browser(enter_key_coords, board_tl_coords)
    wordle_game.init_game()
    
    guess = word_guesser.get_random_word()
    if start_word:
        guess = start_word

    total_guesses = 6
    for i in range(total_guesses):
        print('Guess #{}: {}'.format(i + 1, guess))

        if not wordle_game.enter_word(guess):
            print('Error: failed to enter word \'{}\''.format(guess))
            exit(1)
        
        results = wordle_game.submit_word()
        if not results:
            print('Error: failed to submit word \'{}\''.format(guess))
            exit(1)

        solved = True
        for r in results:
            if not r is util.Results.RIGHT:
                solved = False
                break
        if solved:
            print('Solved Wordle in {} guesses'.format(i + 1))
            exit(0)

        if not word_guesser.read_in_results(guess, results):
            print('Error: failed read results: {}'.format(results))
            exit(1)

        words = word_guesser.get_possible_words()
        guess = word_guesser.get_random_word(words)

    print('Failed to solve Wordle in {} guesses'.format(total_guesses))

class Browser:
    def __init__(self, enter_key_coords:tuple, board_tl_coords:tuple):
        self.enter_key_coords = enter_key_coords
        self.board_topleft_coords = board_tl_coords

        self.letter_coords_dict = util.build_letter_dict(enter_key_coords)
        self.board_coords_dict = util.build_board_dict(board_tl_coords)

        self.current_row = 0

    def init_game(self):
        util.vlog('Initializing Wordle game...')
        # Sleep to allow user to open Worldle game
        # https://www.powerlanguage.co.uk/wordle/
        time.sleep(3)
        util.vlog('Sleep complete, continuing program', 2)

        self.click(self.board_topleft_coords)
        time.sleep(0.5)

    def click(self, pos:tuple):
        pyautogui.click(pos)
        util.vlog('Left mouse button pressed at {}'.format(pos), 2)

    def enter_word(self, word:str):
        if not len(word) == 5:
            util.vlog('Invalid length for word: {}'.format(word), 2)
            return False

        util.vlog('Entering word: {}'.format(word))

        for letter in word:
            letter = letter.lower()
            if letter not in self.letter_coords_dict:
                return False

        for letter in word:
            util.vlog('Submitting letter: {}'.format(letter), 2)
            self.click(self.letter_coords_dict[letter])
        return True

    def submit_word(self):
        if self.current_row == -1:
            util.vlog('No row to submit')
            return False
            
        util.vlog('Submitted word')
        self.click(self.enter_key_coords)

        # Sleep for 3 seconds to allow Wordle to submit word
        time.sleep(3)
        util.vlog('Sleep complete, continuing program', 2)

        results = self.get_row_results(self.current_row)

        if self.current_row == len(self.board_coords_dict) - 1:
            util.vlog('Last row complete')
            self.current_row = -1
        else:
            self.current_row += 1
            util.vlog('Submitted word, next row: {}'.format(self.current_row))
        return results

    def get_result(self, color:tuple):
        color_dict = {
            (-1, -1, -1): util.Results.INVALID,
            (255, 255, 255): util.Results.EMPTY,
            (106, 170, 100): util.Results.RIGHT,
            (201, 180, 88): util.Results.PARTIAL,
            (120, 124, 126): util.Results.WRONG
        }

        if color in color_dict:
            return color_dict[color]
        util.vlog('{} not in color dict'.format(color))
        return False

    def get_row_results(self, row:int):
        if self.current_row > len(self.board_coords_dict) - 1 or self.current_row < 0:
            util.vlog('Invalid row {}'.format(row))
            return False

        results = []
        index = row * 5
        util.vlog('Row {} results (index {}):'.format(row, index), 2)

        for i in range(index, index + 5):
            coords = self.board_coords_dict[i]
            mult = 3
            box = (coords[0] - mult, coords[1] - mult, coords[0] + mult, coords[1] + mult)
            image = ImageGrab.grab(box)
            color_avg = image.getcolors(mult * mult)

            r = self.get_result(color_avg[0][1])
            if r:
                results.append(r)
                util.vlog('{} ({}): {}'.format(i, index + i, r), 2)
            else:
                util.vlog('Row {} results failed'.format(row))
                return False

        return results

    def get_current_results(self):
        return self.get_row_results(self.current_row)

    def get_board_results(self):
        results = []
        for i in range(6):
            r = self.get_row_results(i)
            if r:
                results.append(r)
            else:
                util.vlog('Failed to get row {} results'.format(i))
                results.append([])
        return results