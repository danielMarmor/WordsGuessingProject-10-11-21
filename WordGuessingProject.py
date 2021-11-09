
from random import seed
from random import randint
from datetime import datetime
import statistics

_expressions = None
_selected_exp = None
_selected_exp_flat = None
_guesses = None
_guesses_flat = None
_exec_start_time = None
_exec_end_time = None

_points = 0
_BONUS =100
_BONUS_THRESHOLD = 100
_CORRECT_MARK = 5
_INCORRECT_MARK = -1
_NOT_GUESSSED = '_'
_DELIM = ' '


def get_expressions():
    expressions = list([])
    expressions.append('Act as if')
    expressions.append('Act without expectation')
    expressions.append('All is well')
    expressions.append('Allow for delays')
    expressions.append('Always be honest')
    expressions.append('Always be yourself')
    expressions.append('Always deliver quality')
    expressions.append('Ask powerful questions')
    expressions.append('Audit your metrics')
    expressions.append('Audit your mistakes')

    lst_exp = [exp.split(_DELIM) for exp in expressions]
    return lst_exp


def get_user_action():
    action = input('New Game?  (Yes = Press 1,  Quit -Press 0)')
    if action != '1' and action != '0':
        return None
    return action


def get_exp_index():
    index = randint(0, len(_expressions)) - 1
    return index


def init_round():
    global _points, _exec_start_time
    seed(1)
    _points = 0
    _exec_start_time = datetime.now()


def init_guesses():
    global _guesses, _guesses_flat
    exp_flat = get_exp_flat(_selected_exp)
    _guesses_flat = ''.join([_NOT_GUESSSED if x != _DELIM else _DELIM for x in exp_flat])
    _guesses = _guesses_flat.split(_DELIM)


def validate_letter(letter):
    if letter == '' or letter.strip(' ') == '':
        print('Empty Guess!')
        return False
    if len(letter) > 1:
        print('Must Enter Only One Letter!')
        return False
    if not letter.isalpha():
        print('Cannot Enter this letter. Only alpha letters Please!')
        return False
    guess_flat = get_exp_flat(_guesses)
    is_already_guessed = guess_flat.find(letter) != -1
    if is_already_guessed:
        print('Already Guessed!')
        return False
    return True


def get_exp_flat(exp):
    exp = list(exp)
    exp_flat = _DELIM.join(exp)
    return exp_flat


def replace_letter(sentence, letter, index):
    sentence = str(sentence)
    letter = str(letter)
    split_sentence = list(sentence)
    split_sentence[index] = letter
    new_sentence = ''.join(split_sentence)
    return new_sentence


def update_guess(letter):
    global _guesses, _guesses_flat, _selected_exp_flat
    match_indexes_items = [(index, item) for index, item in enumerate(_selected_exp_flat)
                           if str(item).lower() == str(letter).lower()]
    if len(match_indexes_items) == 0:
        return False
    for idx in match_indexes_items:
        index = idx[0]
        update_letter = idx[1]
        _guesses_flat = replace_letter(_guesses_flat, update_letter, index)
        _guesses = _guesses_flat.split(_DELIM)

    return True


def update_points(is_correct):
    global _points
    if is_correct:
        _points += _CORRECT_MARK
    else:
        _points += _INCORRECT_MARK
        _points = max(_points, 0)


def print_guess():
    print(_guesses_flat)


def print_guess_message(is_correct):
    print('Correct Guess!' if is_correct else 'Wrong Guess!')


def is_exp_completed():
    guessed_flat_no_delimiter = _guesses_flat.replace(_DELIM, '')
    is_guess_completed = guessed_flat_no_delimiter.find(_NOT_GUESSSED) == -1
    return is_guess_completed


def calculate_bonus_points():
    global _points
    exec_time_sec = (_exec_end_time - _exec_start_time).total_seconds()
    if exec_time_sec < _BONUS_THRESHOLD:
        _points += _BONUS


def print_final_mark():
    global _points
    print(f'You got total {_points} points!')


def run_game_round():
    global _guesses, _exec_end_time
    init_round()
    init_guesses()
    print('Game Started')
    print_guess()
    while True:
        letter = input('Please Enter Letter: ')
        validation = validate_letter(letter)
        if not validation:
            continue
        is_correct_guess = update_guess(letter)
        update_points(is_correct_guess)
        print_guess_message(is_correct_guess)
        print_guess()
        is_game_completed = is_exp_completed()
        if not is_game_completed:
            continue
        _exec_end_time = datetime.now()
        calculate_bonus_points()
        print_final_mark()
        break


def start_game():
    global _expressions, _selected_exp, _selected_exp_flat
    _expressions = get_expressions()
    while True:
        user_action = get_user_action()
        if user_action is None:
            continue
        if user_action == '0':
            break
        exp_index = get_exp_index()
        _selected_exp = _expressions[exp_index]
        _selected_exp_flat = get_exp_flat(_selected_exp)
        run_game_round()


def main():
    start_game()


main()









