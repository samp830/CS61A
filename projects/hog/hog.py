"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled (capped at 11 - NUM_ROLLS).

    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    one_counter = 0
    current_roll = 0
    total= 0
    while current_roll < num_rolls:
        new = dice()
        if new == 1:
            one_counter += 1
        else:
            total += new
        current_roll += 1
    if one_counter > 0:
        return min(11-num_rolls, one_counter)
    else:
        return total
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    return max(opponent_score%10, (opponent_score//10)%10) +1
    # END PROBLEM 2


# Write your prime functions here!
def is_prime(score):
    if score == 0 or score==1:
        return False
    count = 2
    while count <= score ** 0.5:
        if score%count==0:
            return False
        count += 1
    return True

def next_prime(score):
    score+=1
    while is_prime(score) != True:
        score+=1
    return score




def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime rule.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    if num_rolls == 0:
        check_hogtimus= free_bacon(opponent_score)
        if is_prime(check_hogtimus):
            return next_prime(check_hogtimus)
        else:
            return check_hogtimus
    rolled = roll_dice(num_rolls, dice)
    if is_prime(rolled):
        return next_prime(rolled)
    else:
        return rolled

    # END PROBLEM 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog Wild).
    """
    # BEGIN PROBLEM 3
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided
    # END PROBLEM 3

def is_swap(score0, score1):
    """Returns whether one of the scores is double the other.
    """
    # BEGIN PROBLEM 4
    if score1*2 == score0 or score1*.5 == score0:
        return True
    else:
        return False
    # END PROBLEM 4

def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5

    while True:
        if player == 0:
            dice = select_dice(score0,score1)
            score0+=take_turn(strategy0(score0,score1),score1, dice) 
            if is_swap(score0, score1):
                score0, score1 = score1, score0
            if (score0 >= goal) or (score1>=goal):
                break
        if player == 1:
            dice = select_dice(score0,score1)
            score1+=take_turn(strategy1(score1,score0),score0, dice)
            if is_swap(score0, score1):
                score0, score1 = score1, score0
            if (score1 >= goal) or (score0>=goal):
                break
        player = other(player)
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    your_score = -1
    while your_score <= goal:
        opponent_score = -1
        while opponent_score <= goal:
            opponent_score+=1
            assert strategy(your_score, opponent_score) <= 10 and strategy(your_score,opponent_score) >= -1 
        your_score+=1
        assert strategy(your_score,opponent_score) <= 10 and strategy(your_score, opponent_score) >= -1
    
    if callable(strategy):
        return None
    else:
        return check_strategy_roll(strategy)
    # END PROBLEM 6


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    def inner(*args):
        called_amount= 0
        total =0
        while called_amount<num_samples:
            original= fn(*args)
            total += original
            called_amount+=1
        return total/num_samples
    return inner
    # END PROBLEM 7


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8

    num_dice = 1
    avg_val= make_averaged(roll_dice, num_samples)
    dynamic_dice= avg_val(1, dice)
    while num_dice <= 10:
        if avg_val(num_dice, dice) > dynamic_dice:
            dynamic_dice=avg_val(num_dice, dice)
            best_dice=num_dice
        num_dice+=1
    return best_dice



    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    if free_bacon(opponent_score) < margin:
        if is_prime(free_bacon(opponent_score)):
            if next_prime(free_bacon(opponent_score)) >= margin:
                return 0
            else:
                return num_rolls
        return num_rolls
    else:
        return 0
    # Replace this statement
    # END PROBLEM 9
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    if is_swap(free_bacon(opponent_score)+score, opponent_score):
        return 0
    elif bacon_strategy(score, opponent_score, margin, num_rolls) == 0:
        return 0  
    else:
        return num_rolls
    # Replace this statement
    # END PROBLEM 10
check_strategy(swap_strategy)

def final_strategy(score, opponent_score):
    """Returns the number of dice to roll.
    First, it checks how many points rolling 0 dice (free_bacon rule) will result in (= bacon_points).
    Next, it returns 0 if bacon_points plus current score will put the score at 100 or above (which will win),
    and accounts for if that will make you swap to a lower opponent score.
    Next, it returns 10 rolls if using free bacon rule and adding one will result in a win or if adding one can
    result in a beneficial swap.
    Next, it utilizes the swap strategy if opponent score is greater than current score by at least 5.
    Next, it uses the bacon strategy if four sided dice is activated.
    Next, it uses bacon strategy if current score is high (greater than or equal to 78).
    Finally, if none of these other conditions are met, it defaults to bacon strategy.
    """
    # BEGIN PROBLEM 11

    bacon_points = free_bacon(opponent_score)
    if is_prime(bacon_points):
        bacon_points = next_prime(bacon_points)

    if bacon_points + score >= 100 and is_swap(bacon_points + score, opponent_score)==False:
        return 0
    if score+ free_bacon(opponent_score) + 1 >= 100 or (score+1)*2==opponent_score:
        return 10
    if opponent_score-score >= 5:
        return swap_strategy(score,opponent_score,margin=10, num_rolls=6)
    if select_dice(score, opponent_score)== four_sided:
        return bacon_strategy(score, opponent_score, margin=5, num_rolls=4)
    if score >= 78:
        return bacon_strategy(score, opponent_score, margin=5, num_rolls= 5)
    else:
        return bacon_strategy(score,opponent_score,margin=9, num_rolls=5)
      # Replace this statement
    # END PROBLEM 11
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()