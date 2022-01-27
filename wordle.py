import argparse
import pyautogui
import time

def parse_args(parser):
    parser.add_argument('-v', '--verbose',
            help='use verbose logging',
            action='count',
            default=0)

    parser.add_argument('-s', '--start',
            help='choose a word to start the puzzle with')

    parser.add_argument('-c', '--coords',
            help='screen coords of center of \'enter\' button, format as \'-cx,y\' \'--coords=x,y\'',
            required=True)

    return parser.parse_args()

def vlog(message, level=1):
    if log_level >= level:
        print(message)

def build_letter_dict(coords):
    vlog('Enter button coords: {}'.format(coords))
    letter_dict = {}

    rel_coords = (coords[0] + 60, coords[1])
    for l in 'zxcvbnm':
        letter_dict[l] = rel_coords
        vlog('Added \'{}\' to dict with coords {}'.format(l, rel_coords), 3)
        rel_coords = (rel_coords[0] + 50, rel_coords[1])

    rel_coords = (rel_coords[0], rel_coords[1] - 65)
    for l in 'lkjhgfdsa':
        letter_dict[l] = rel_coords
        vlog('Added \'{}\' to dict with coords {}'.format(l, rel_coords), 3)
        rel_coords = (rel_coords[0] - 50, rel_coords[1])

    rel_coords = (rel_coords[0] + 30, rel_coords[1] - 65)
    for l in 'qwertyuiop':
        letter_dict[l] = rel_coords
        vlog('Added \'{}\' to dict with coords {}'.format(l, rel_coords), 3)
        rel_coords = (rel_coords[0] + 50, rel_coords[1])

    vlog(letter_dict, 4)
    return letter_dict

def click(pos):
    pyautogui.click(pos)
    vlog('Left mouse button pressed at {}'.format(pos), 2)

def enter_word(word, letter_dict):
    if not len(word) == 5:
        return False

    for letter in word:
        letter = letter.lower()
        if letter not in letter_dict:
            return False

    for letter in word:
        vlog('Submitting letter: {}'.format(letter))
        click(letter_dict[letter])
    return True

def main():
    args = parse_args(argparse.ArgumentParser())

    global log_level
    log_level = args.verbose

    vlog(args, 2)

    str_coords = args.coords
    split_coords = str_coords.split(',')
    coords = (int(split_coords[0]), int(split_coords[1]))
    letter_dict = build_letter_dict(coords)

    # Sleep to allow user to open Worldle game
    # https://www.powerlanguage.co.uk/wordle/
    time.sleep(3)
    vlog('Sleep complete, continuing program')

    click(coords)
    time.sleep(0.5)
    
    starting_word = 'hello'
    if args.start:
        starting_word = args.start
        
    if not enter_word(starting_word, letter_dict):
        print('Error: failed to enter word \'{}\''.format(starting_word))

if __name__ == "__main__":
    main()
