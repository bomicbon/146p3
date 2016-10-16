
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 100
explore_faction = 2.

# calculate the urgent
def UCB1(X,n,nj, C):
    return X + C * sqrt((2 * log(n))/nj)


# deternime if the current bot win or not
def winner(state,identity):
    if state.winner == identity:
        win_s = 1
    elif state.winner == 'tie':
        win_s = 0
    else:
        win_s = -1
    return win_s


def best_action(node):
    values = {}
    for __, child in node.child_nodes.items():
        values[child] = child.wins/child.visits
    best_win = max(values, key=values.get)
    return best_win.parent_action


def best_child(node,state,identity):
    values = {}
    for __, child in node.child_nodes.items():
        win_rate = child.wins / child.visits  # Win Rate = wins / visited
        if identity != state.player_turn:
            win_rate = 1 - win_rate  # If not player turn -> win_rate is loss Rate
        values[child] = UCB1(win_rate, child.parent.visits, child.visits, explore_faction)
    best_choice = max(values, key=values.get)
    return best_choice


def opponent(role):
    return 'red' if role == 'blue' else 'blue'


def traverse_nodes(node, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """

    current_node = node
    while current_node.untried_actions == [] and state.is_terminal() is False:  # while there isn't untried action
        current_node = best_child(current_node, state, identity)
        state.apply_move(current_node.parent_action)
    return current_node
    # Hint: return leaf_node


def expand_leaf(node, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """
    if state.is_terminal():
        return node
    rand_action = choice(node.untried_actions)
    node.untried_actions.remove(rand_action)
    state.apply_move(rand_action)
    new_node = MCTSNode(parent=node, parent_action=rand_action, action_list=state.legal_moves)
    node.child_nodes[rand_action]= new_node
    return new_node
    # Hint: return new_node


def rollout(state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """
    '''
    while not state.is_terminal():
        best_move = []
        for move in state.legal_moves:
            rollout_state = state.copy()
            me = rollout_state.player_turn
            red_score = rollout_state.score.get('red', 0)
            blue_score = rollout_state.score.get('blue', 0)
            while not rollout_state.is_terminal():
                rollout_state.apply_move(choice(rollout_state.legal_moves))
                if me == 'red':
                    if rollout_state.score.get('red', 0) > red_score:
                        best_move.append(move)
                        break
                    elif rollout_state.score.get('blue', 0) > blue_score:
                        break
                else:
                    if rollout_state.score.get('blue', 0) > blue_score:
                        best_move.append(move)
                        break
                    elif rollout_state.score.get('red', 0) > red_score:
                        break
        if best_move == []:
            best_choice = choice(state.legal_moves)
        else:
            best_choice = choice(best_move)
        state.apply_move(best_choice)
    '''





    ROLLOUTS = 5
    MAX_DEPTH = 10
    while not state.is_terminal():
        values = {}
        for move in state.legal_moves:
            total_score = 0.0

            # Sample a set number of games where the target move is immediately applied.
            for r in range(ROLLOUTS):
                rollout_state = state.copy()
                me = rollout_state.player_turn
                rollout_state.apply_move(move)

                for i in range(MAX_DEPTH):
                    if rollout_state.is_terminal():
                        break
                    rollout_move = choice(rollout_state.legal_moves)
                    rollout_state.apply_move(rollout_move)
                total_score += rollout_state.score.get(me, 0) - rollout_state.score.get(opponent(me), 0)

            expectation = float(total_score) / ROLLOUTS
            # If the current move has a better average score, replace best_move and best_expectation
            values[expectation] = move

        best_move = values[max(values.keys())]
        state.apply_move(best_move)



def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node is not None:
        node.visits += 1
        node.wins += won
        node = node.parent


def think(state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = state.player_turn
    root_node = MCTSNode(parent=None, parent_action=None, action_list=state.legal_moves)

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state.copy()

        # Start at root
        node = root_node

        # Do MCTS - This is all you!

        # selection
        node = traverse_nodes(node, sampled_game, identity_of_bot)
        # expansion
        node = expand_leaf(node, sampled_game)
        # simulation
        rollout(sampled_game)
        # backpropagation
        backpropagate(node, winner(sampled_game, identity_of_bot))
    return best_action(root_node)

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None
