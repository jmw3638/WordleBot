
from enum import Enum

class Results(Enum):
    INVALID = 0
    EMPTY = 1
    RIGHT = 2
    PARTIAL = 3
    WRONG = 4

def vlog(message:str=None, level:int=1):
    try:
        if message is None:
            return log_level
        elif log_level >= level:
            print(message, flush=True)
    except:
        return None

def set_v_lvl(level:int):
    global log_level
    log_level = level

def get_wordle_results(guess_word:str, goal_word:str):
    if len(guess_word) != len(goal_word):
        vlog('Word size mismatch: {}, {}'.format(guess_word, goal_word))
        return False

    guess_word = guess_word.lower()
    goal_word = goal_word.lower()

    vlog('{} <-> {}'.format(guess_word, goal_word), 5)

    results = []
    index = 0
    for l in guess_word.lower():
        result = Results.INVALID

        if l == goal_word[index]:
            result = Results.RIGHT
        elif l in goal_word:
            result = Results.PARTIAL
        else:
            result = Results.WRONG

        vlog('{} | {} | {}'.format(l, goal_word[index], result), 5)
        results.append(result)
        index += 1

    return results

def get_alphabet():
    return 'abcdefghijklmnopqrstuvwxyz'

def validate_word(word:str):
    for l in word:
        if not validate_letter(l):
            vlog('Invalid letter in word: {}'.format(word))
            return False
    return True

def validate_letter(letter:str):
    # Check string size, must be 1
    if len(letter) != 1:
        vlog('Not a single letter: {}'.format(letter))
        return False

    # Check if character is valid letter
    if letter not in get_alphabet():
        vlog('Not a valid letter: {}'.format(letter))
        return False

    return True

def validate_coords(coords_str:str):
    coords_split = coords_str.split(',')
    if len(coords_split) != 2:
        vlog('Invalid coords: {}'.format(coords_str))
        return False

    x = coords_split[0]
    y = coords_split[1]

    if not x.isnumeric():
        vlog('Invalid x coord: {}'.format(x))
        return False
    if not y.isnumeric():
        vlog('Invalid y coord: {}'.format(y))
        return False

    coords = (int(x), int(y))
    return coords

def build_letter_dict(coords:tuple):
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
        vlog('Added \'{}\' to letter dict with coords {}'.format(l, rel_coords), 3)
        rel_coords = (rel_coords[0] + 50, rel_coords[1])

    vlog(letter_dict, 4)
    return letter_dict

def build_board_dict(coords:tuple):
    vlog('Top left space coords: {}'.format(coords))
    board_dict = {}

    count = 0
    rel_coords = (coords[0], coords[1])
    for r in range(6):
        for c in range(5):
            board_dict[count] = rel_coords
            vlog('Added \'{}\' to board dict with coords {}'.format(count, rel_coords), 3)
            rel_coords = (rel_coords[0] + 67, rel_coords[1])
            count += 1
        rel_coords = (coords[0], rel_coords[1] + 67)

    vlog(board_dict, 4)
    return board_dict