import argparse
import enum
import pyautogui
import time
from PIL import ImageGrab

import util

class Results(enum.Enum):
    INVALID = 0
    EMPTY = 1
    RIGHT = 2
    PARTIAL = 3
    WRONG = 4

def parse_args(parser):
    parser.add_argument('-v', '--verbose',
            help='use verbose logging',
            action='count',
            default=0)

    parser.add_argument('-s', '--start',
            help='choose a word to start the puzzle with')

    parser.add_argument('-l', '--letter-coords',
            help='screen coords of center of \'enter\' button, format as \'-cx,y\' \'--letter-coords=x,y\'',
            required=True)
    
    parser.add_argument('-b', '--board-coords',
            help='screen coords of top left board space, format as \'-cx,y\' \'--board-coords=x,y\'',
            required=True)

    return parser.parse_args()

def click(pos):
    pyautogui.click(pos)
    util.vlog('Left mouse button pressed at {}'.format(pos), 2)

def enter_word(word, letter_dict):
    if not len(word) == 5:
        return False

    for letter in word:
        letter = letter.lower()
        if letter not in letter_dict:
            return False

    for letter in word:
        util.vlog('Submitting letter: {}'.format(letter))
        click(letter_dict[letter])
    return True

def get_result(color):
    color_dict = {
        (-1, -1, -1): Results.INVALID,
        (255, 255, 255): Results.EMPTY,
        (106, 170, 100): Results.RIGHT,
        (201, 180, 88): Results.PARTIAL,
        (120, 124, 126): Results.WRONG
    }

    if color in color_dict:
        return color_dict[color]
    util.vlog('{} not in color dict'.format(color))
    return False

def get_row_results(row, board_dict):
    results = []
    index = row * 5
    util.vlog('Row {} results (index {}):'.format(row, index), 2)

    for i in range(index, index + 5):
        coords = board_dict[i]
        mult = 3
        box = (coords[0] - mult, coords[1] - mult, coords[0] + mult, coords[1] + mult)
        image = ImageGrab.grab(box)
        color_avg = image.getcolors(mult * mult)

        r = get_result(color_avg[0][1])
        if r:
            results.append(r)
            util.vlog('{} ({}): {}'.format(i, index + i, r), 2)
        else:
            util.vlog('Row {} results failed'.format(row))
            return False

    return results

def main():
    args = parse_args(argparse.ArgumentParser())

    util.set_v_lvl(args.verbose)

    util.vlog(args, 2)

    l_split_coords = args.letter_coords.split(',')
    l_coords = (int(l_split_coords[0]), int(l_split_coords[1]))
    letter_dict = util.build_letter_dict(l_coords)

    b_split_coords = args.board_coords.split(',')
    b_coords = (int(b_split_coords[0]), int(b_split_coords[1]))
    board_dict = util.build_board_dict(b_coords)

    # Sleep to allow user to open Worldle game
    # https://www.powerlanguage.co.uk/wordle/
    time.sleep(3)
    util.vlog('Sleep complete, continuing program')

    click(l_split_coords)
    time.sleep(0.5)
    
    starting_word = 'hello'
    if args.start:
        starting_word = args.start
        
    if not enter_word(starting_word, letter_dict):
        print('Error: failed to enter word \'{}\''.format(starting_word))

    for i in range(6):
        results = get_row_results(i, board_dict)
        if not results:
            print('Error: failed to get row {} results'.format(i))

if __name__ == "__main__":
    main()
