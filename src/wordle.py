import argparse
import os.path

import browser
import guesser
import simulate
import util

def parse_args(parser:argparse.ArgumentParser) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        parser (argparse.ArgumentParser): argument parser

    Returns:
        argparse.Namespace: argument namespace
    """
    subparsers = parser.add_subparsers(dest='operation')

    bot_parser = subparsers.add_parser('bot',
            help='run Wordle browser bot')

    sim_parser = subparsers.add_parser('sim',
            help='run Wordle simulation')

    # General argument parser arguments

    parser.add_argument('dictionary',
            help='word dictionary file')

    parser.add_argument('-w', '--allowed-words',
            help='allowed words dictionary file')

    parser.add_argument('-v', '--verbose',
        help='use verbose logging',
        action='count',
        default=0)

    # Wordle browser bot subparser arguments

    bot_parser.add_argument('-l', '--letter-coords',
            help='screen coords of center of \'enter\' button, format as \'-cx,y\' \'--letter-coords=x,y\'',
            required=True)
    
    bot_parser.add_argument('-b', '--board-coords',
            help='screen coords of top left board space, format as \'-cx,y\' \'--board-coords=x,y\'',
            required=True)

    bot_parser.add_argument('-s', '--start',
            help='choose a word to start the puzzle with',
            type=str,
            default=None)

    # Wordle Simulation subparser arguments

    sim_parser.add_argument('-i', '--iterations',
            help='number of Wordle games to run',
            type=int,
            default=1)
    
    sim_parser.add_argument('-f', '--first',
            help='run simulation with the same first guess each iteration',
            type=str,
            default=None)

    sim_parser.add_argument('-g', '--goal',
            help='run simulation with same goal word each iteration',
            type=str,
            default=None)

    return parser.parse_args()

def browser_bot(args:argparse.Namespace, words_list:str) -> bool:
    """Runs the Wordle browser bot operation.

    Args:
        args (argparse.Namespace): command line arguments
        words_list (str): Wordle game dictionary of words

    Returns:
        bool: operation success or failure
    """
    # Get initial guess, if not specified choose randomly from word dictionary
    start_word = None
    if args.start:
        if len(args.start) != 5:
            print('Error: invalid word length of 5 \'{}\''.format(args.start))
            return False
        elif not util.validate_word(args.start):
            print('Error: invalid word \'{}\''.format(args.start))
            return False
        start_word = args.start
        util.vlog('Using set starting word: {}'.format(start_word))

    # Get coords of enter key on webpage
    enter_key_coords = util.validate_coords(args.letter_coords)
    if not enter_key_coords:
        print('Error: invalid enter key coords \'{}\''.format(args.letter_coords))
        return False

    # Get coords of top left board space on webpage
    board_tl_coords = util.validate_coords(args.board_coords)
    if not board_tl_coords:
        print('Error: invalid board (top left) coords \'{}\''.format(args.board_coords))
        return False

    # Create word guesser object and run bot
    word_guesser = guesser.WordGuesser(words_list, 5)
    browser.run_browser_bot(word_guesser, start_word, enter_key_coords, board_tl_coords)
    return True

def simulation(args:argparse.Namespace, words_list:str, allowed_words:list=None) -> bool:
    """Runs the Wordle simulation operation.

    Args:
        args (argparse.Namespace): command line arguments
        words_list (str): Wordle game dictionary of words
        allowed_words (list, optional): word guesser dictionary of words. Defaults to None.
    
    Returns:
        bool: operation success or failure
    """
    # Get initial guess, randomized if not specified
    start_word = None
    if args.first:
        if len(args.first) != 5:
            print('Error: invalid word length of {} \'{}\''.format(len(args.first), args.first))
            return False
        elif not util.validate_word(args.first):
            print('Error: invalid word \'{}\''.format(args.first))
            return False
        start_word = args.first
        util.vlog('Using persistent starting word: {}'.format(start_word))

    # Get goal word, randomized if not specified
    goal_word = None
    if args.goal:
        if len(args.goal) != 5:
            print('Error: invalid word length of 5 \'{}\''.format(args.goal))
            return False
        elif not util.validate_word(args.goal):
            print('Error: invalid word \'{}\''.format(args.goal))
            return False
        goal_word = args.goal
        util.vlog('Using persistent goal word: {}'.format(goal_word))

    # Create word guesser and simulation objects
    word_guesser = guesser.WordGuesser(words_list, 5)
    sim = simulate.Simulation(word_guesser)

    # Run simulation and print results
    results = sim.run_simulation(args.iterations, start_word, goal_word, allowed_words)
    sim.print_results(results)
    return True

def main():
    """Main function. Runs the selected Wordle operation.
    """
    args = parse_args(argparse.ArgumentParser())

    util.set_v_lvl(args.verbose)
    util.vlog(args, 3)

    # Get word dictionary
    if not os.path.isfile(args.dictionary):
        print('Error: no such file {}'.format(args.dictionary))
        exit(1)
    dict_file = open(args.dictionary)
    words_list = dict_file.read()

    # Optional allowed words dictionary
    allowed_words_list = None
    if args.allowed_words:
        if not os.path.isfile(args.allowed_words):
            print('Error: no such file {}'.format(args.allowed_words))
            exit(1)
        allowed_file = open(args.allowed_words)
        allowed_words_list = allowed_file.read().split()

    # Wordle browser bot operation
    if args.operation == 'bot':
        print('Wordle Browser Bot')
        print('https://www.powerlanguage.co.uk/wordle/')
        browser_bot(args, words_list)
    # Wordle simulation operation
    elif args.operation == 'sim':
        print('Wordle Simulation')
        simulation(args, words_list, allowed_words_list)
    # Invalid operation
    else:
        print('Error: invalid or no operation selected')

if __name__ == "__main__":
    main()
