import argparse
from tracemalloc import start
import pyautogui
import time

close_init_prompt = (-740, 328)
letter_dict = {
    'a': (-1160, 926),
    'b': (-912, 990),
    'c': (-1010, 990),
    'd': (-1060, 926),
    'e': (-1083, 862),
    'f': (-1010, 926),
    'g': (-960, 926),
    'h': (-912, 926),
    'i': (-838, 862),
    'j': (-860, 926),
    'k': (-813, 926),
    'l': (-762, 926),
    'm': (-813, 990),
    'n': (-860, 990),
    'o': (-789, 862),
    'p': (-740, 862),
    'q': (-1182, 862),
    'r': (-1034, 862),
    's': (-1109, 926),
    't': (-985, 862),
    'u': (-887, 862),
    'v': (-960, 990),
    'w': (-1132, 862),
    'x': (-1060, 990),
    'y': (-937, 862),
    'z': (-1109, 990)
}

def parse_args(parser):
    parser.add_argument('-v', '--verbose',
            help='use verbose logging',
            action='count',
            default=0)

    parser.add_argument('-s', '--start',
            help='choose a word to start the puzzle with')

    return parser.parse_args()

def vlog(message, level=1):
    if log_level >= level:
        print(message)

def click(pos):
    pyautogui.click(pos)
    vlog('Left mouse button pressed at {}'.format(pos))

def enter_word(word):
    if not len(word) == 5:
        return False

    for letter in word:
        letter = letter.lower()
        if letter not in letter_dict:
            return False

    for letter in word:
        vlog('Submitting letter: {}'.format(letter_dict[letter]))
        click(letter_dict[letter])
    return True

def main():
    args = parse_args(argparse.ArgumentParser())

    global log_level
    log_level = args.verbose

    vlog(args)
    
    # Sleep to allow user to open Worldle game
    # https://www.powerlanguage.co.uk/wordle/
    time.sleep(3)
    vlog('Sleep complete, continuing program')

    click(close_init_prompt)
    time.sleep(0.5)
    
    starting_word = 'hello'
    if args.start:
        starting_word = args.start
        
    if not enter_word(starting_word):
        print('Error: failed to enter word \'{}\''.format(starting_word))

if __name__ == "__main__":
    main()
