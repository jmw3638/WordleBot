import argparse
import os.path

import browser
import guesser
import util

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

    parser.add_argument('-d', '--dictionary',
            help='word dictionary file',
            required=True)

    return parser.parse_args()

def main():
    args = parse_args(argparse.ArgumentParser())

    util.set_v_lvl(args.verbose)

    util.vlog(args, 2)

    if not os.path.isfile(args.dictionary):
        print('Error: no such file {}'.format(args.dictionary))
        exit(1)
    
    dict_file = open(args.dictionary)
    words_list = dict_file.read()

    word_guesser = guesser.WordGuesser(words_list)

    enter_key_coords = util.validate_coords(args.letter_coords)
    if not enter_key_coords:
        print('Error: invalid enter key coords \'{}\''.format(args.letter_coords))
        exit(1)

    board_tl_coords = util.validate_coords(args.board_coords)
    if not board_tl_coords:
        print('Error: invalid board (top left) coords \'{}\''.format(args.board_coords))
        exit(1)

    wordle_game = browser.Browser(enter_key_coords, board_tl_coords)
    wordle_game.init_game()
    
    word = word_guesser.get_random_word()
    if args.start:
        word = args.start

    total_guesses = 6
    for i in range(total_guesses):
        print('Guess #{}: {}'.format(i + 1, word))

        if not wordle_game.enter_word(word):
            print('Error: failed to enter word \'{}\''.format(word))
            exit(1)
        
        results = wordle_game.submit_word()
        if not results:
            print('Error: failed to submit word \'{}\''.format(word))
            exit(1)

        goal = True
        for r in results:
            if not r is util.Results.RIGHT:
                goal = False
                break
        if goal:
            print('Solved Wordle in {} guesses: {}'.format(i + 1, word))
            exit(0)

        if not word_guesser.read_in_results(word, results):
            print('Error: failed read results: {}'.format(results))
            exit(1)

        words = word_guesser.get_possible_words()
        word = word_guesser.get_random_word(words)

    print('Failed to solve Wordle in {} guesses'.format(total_guesses))

if __name__ == "__main__":
    main()
