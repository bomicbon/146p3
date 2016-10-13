
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

# calculate the urgent
def UCB1(X,n,nj, C):
    return X + C * sqrt((2 * log(n))/nj)

# deternime if the current bot win or not
def winner(state,identity):
    win_s = 0
    if state.winner == identity:
        win_s = 1
    elif state.winner == 'tie':
        win_s = 0
    else:
        win_s = -1
    return win_s

def best(node):
    win_rate = 0
    for child in node.child_nodes:
        temp_win_rate = child.wins/child.visits
        if temp_win_rate > win_rate:
            win_rate = temp_win_rate
            node = child
        # current_node = choice(current_node.child_nodes)
    return node.parent_action


def traverse_nodes(node, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args
        node:       A tree node from which the search is traversing.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """

    current_node = node
    urgent = 0

    while not current_node.untried_actions: # while there isn't untried action
        for child in current_node.child_nodes:
            temp_urgent = UCB1(child.wins, child.parent.visited, child.visited, explore_faction)
            if temp_urgent > urgent:
                urgent = temp_urgent
                current_node = child
        # current_node = choice(current_node.child_nodes)
        state.apply_move(node.parent_move)
    return current_node
    # pass
    # Hint: return leaf_node


def expand_leaf(node, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """
    rand_action = choice(node.untried_actions)
    new_node = MCTSNode(parent=node, parent_action=rand_action, action_list=state.legal_moves)
    node.child_nodes[rand_action]= new_node
    node.untried_actions.remove(rand_action)
    state.apply_move(rand_action)
    return new_node
    # pass
    # Hint: return new_node


def rollout(state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """
    while not state.is_terminal():
        state.apply_move(choice(state.legal_moves))
    #pass


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
    #pass


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

        node = expand_leaf(traverse_nodes(node, sampled_game, identity_of_bot), state)
        rollout(sampled_game)
        backpropagate(node, winner(sampled_game, identity_of_bot))

    return best(root_node)
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    #return None
