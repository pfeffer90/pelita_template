# This bot selects a food pellet at random, then goes and tries to get it by
# following the shortest path to it.
# It tries on the way to avoid being killed by the enemy: if the next move
# to get to the food would put it on a ghost, then it chooses a random safe
# position

# Improvements
# No random escape?
# Split into defender and attacker
# no random food target

TEAM_NAME = 'Basic Attacker Bots'


import networkx

from utils import walls_to_graph


def move(bot, state):
    enemy = bot.enemy
    # we need to create a dictionary to keep information (state) along rounds
    # the state object will be passed untouched at every new round
    if state is None:
        # initialize the state dictionary
        state = {}
        # each bot needs its own state dictionary to keep track of the
        # food targets
        state[0] = (None, None) #Target, Path
        state[1] = (None, None)
        # initialize a graph representation of the maze
        # this can be shared among our bots
        state['graph'] = walls_to_graph(bot.walls)

    currently_active_bot = bot.turn
    target, path = state[currently_active_bot]

    # choose a target food pellet if we still don't have one or
    # if the old target has been already eaten
    location_food = enemy[0].food
    if (target is None) or (target not in location_food):
        # position of the target food pellet
        target = bot.random.choice(location_food)
        # use networkx to get the shortest path from here to the target
        # we do not use the first position, which is always equal to bot_position
        maze = state['graph']
        current_position = bot.position
        path = get_shortest_path(maze, current_position, target)
        state[currently_active_bot] = (target, path)

    # get the next position along the shortest path to reach our target
    next_pos = path.pop(0)
    # if we are not in our homezone we should check if it is safe to proceed
    if next_pos not in bot.homezone:
        # get a list of safe positions
        safe_positions = []
        for pos in bot.legal_positions:
            if pos not in (enemy[0].position, enemy[1].position):
                safe_positions.append(pos)

        # we are about to step on top of an enemy
        if next_pos not in safe_positions:
            # 1. Let's forget about this target and this path
            #    We will choose a new target in the next round
            state[currently_active_bot] = (None, None)
            # Choose one safe position at random (this always includes the
            # current position
            next_pos = bot.random.choice(safe_positions)

    return next_pos, state


def get_shortest_path(maze, current_position, target):
    return networkx.shortest_path(maze, current_position, target)[1:]

