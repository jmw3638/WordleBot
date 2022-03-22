import browser
import guesser
import simulate
import wordle
import util

def main():
    print('Testing Wordle Program...')
    util.set_v_lvl(10)

    print('Multiple Word Set:')
    mult_set = guesser.WordSet(5, True)
    print(mult_set)
    mult_set.add_letter('a', 1)
    print('Add \'a\' at pos 1')
    print(mult_set)
    mult_set.add_letter('b', 1)
    print('Add \'b\' at pos 1')
    print(mult_set)
    mult_set.add_letter('a', 1)
    print('Add \'a\' at pos 1')
    print(mult_set)
    print('Letter \'a\' at pos 1')
    print(mult_set.letter_in_set('a'))
    print('Letter \'b\' at pos 1')
    print(mult_set.letter_in_set('b'))
    print('Letter \'c\' at pos 1')
    print(mult_set.letter_in_set('c'))
    print('*' * 50)

    print('Non-Multiple Word Set:')
    non_mult_set = guesser.WordSet(5, False)
    print(non_mult_set)    
    non_mult_set.add_letter('a', 1)
    print('Add \'a\' at pos 1')
    print(non_mult_set)
    non_mult_set.add_letter('b', 1)
    print(non_mult_set)
    non_mult_set.add_letter('a', 1)
    print('Add \'a\' at pos 1')
    print(non_mult_set)
    print('Letter \'a\' at pos 1')
    print(non_mult_set.letter_in_set('a'))
    print('Letter \'b\' at pos 1')
    print(non_mult_set.letter_in_set('b'))
    print('Letter \'c\' at pos 1')
    print(non_mult_set.letter_in_set('c'))

    

if __name__ == '__main__':
    main()