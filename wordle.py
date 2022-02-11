import argparse
import util

import browser

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

def main():
    args = parse_args(argparse.ArgumentParser())

    util.set_v_lvl(args.verbose)

    util.vlog(args, 2)

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
    
    starting_word = 'hello'
    if args.start:
        starting_word = args.start
        
    if not wordle_game.enter_word(starting_word):
        print('Error: failed to enter word \'{}\''.format(starting_word))
    
    print(wordle_game.submit_word())

if __name__ == "__main__":
    main()
