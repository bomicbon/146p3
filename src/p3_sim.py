from p3_game import create_game, State
from timeit import default_timer as time

#import random_bot as red_bot
import rollout_bot as red_bot  # Experiment 1
import rollout_bot as blue_bot

BOTS = {'red': red_bot, 'blue': blue_bot}

# You can set the MCTS tree size like this:
if hasattr(red_bot, 'num_nodes'):
    red_bot.num_nodes = 1000
if hasattr(blue_bot, 'num_nodes'):
    blue_bot.num_nodes = 1000

rounds = 100
wins = {}

# Experiment 1: Tree Size
'''
Blue fixed at 100 nodes/tree.
Test at least 4 sizes for Red tree for at least 100 games.
Plot number of wins of each tree size.
'''
rounds_E1 = 126  # 125 games
E1_times = []
E1_scores_by_size = []
round_counter = 0
for n in range(1, 6):  # Test at least 4 sizes for Red Tree
    start = time()  # To log how much time the simulation takes.
    if hasattr(red_bot, 'num_nodes'):
        red_bot.num_nodes = 100 + (100 * n)  # (200, 300, 400, 500, 600)
    for i in range(1, rounds_E1):
        round_counter += 1
        print("")
        print("Experiment 1, Test %d" % n)
        print("Round %d, fight!" % i)

        game = create_game(4)  # 4x4 grid
        state = State(game)

        while not state.is_terminal():
            move = BOTS[state.player_turn].think(state.copy())
            state.apply_move(move)

        final_score = state.score
        winner = state.winner
        print ("The %s bot wins this round (%s)" % (winner, str(final_score)))
        wins[winner] = wins.get(winner, 0) + 1

    print("")
    print("Final win counts:", dict(wins))
    for color, score in wins.items():
        score_tup = (color, score)
        E1_scores_by_size.append(score_tup)
    print("Test %d end." % n)
    end = time()
    round_timer = end - start
    E1_times.append(round_timer)
    print(end - start, ' total seconds')
    print("")

print("RESULTS")
for i in range(1, 6):
    j = i + 1
    a = i - 1
    a = a * 2
    numnodes = 100 + (100 * a)
    print("Experiment 1: Red Tree at %d nodes." % numnodes)

    print("Wins: ", E1_scores_by_size[a], E1_scores_by_size[a + 1])
# print("Test %d took %d seconds." % (i, E1_times[a]))
    print("")
print("Total number of rounds: %d" % round_counter)

'''
start = time()  # To log how much time the simulation takes.
for i in range(rounds):

    print("")
    print("Round %d, fight!" % i)

    # Specify the size of the grid in vertices. In this case, 4x4
    game = create_game(4)
    state = State(game)     # Create a state from the instance of the game

    while not state.is_terminal():
        move = BOTS[state.player_turn].think(state.copy())
        state.apply_move(move)

    final_score = state.score
    winner = state.winner
    print("The %s bot wins this round! (%s)" % (winner, str(final_score)))
    wins[winner] = wins.get(winner, 0) + 1

print("")
print("Final win counts:", dict(wins))

# Also output the time elapsed.
end = time()
print(end - start, ' seconds')
'''
