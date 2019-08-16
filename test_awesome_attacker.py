from pelita.utils import setup_test_game

from awesome_attacker import move


def test_eat_food():
    # do we eat food when it's available?
    layout = """
    ########
    #    0.#
    #.1  EE#
    ########
    """
    bot = setup_test_game(layout=layout, is_blue=True)
    next_move, _ = move(bot, None)
    assert next_move == (6, 1)


def test_change_position_if_possible_with_enemy_nearby():
    # move if an enemy is close. The basic attacker could get stuck in place and become prey.
    layout = """
    ########
    #   .E0#
    #1E    #
    ########
    """
    bot_positions = [(6, 1), (1, 2)]
    enemy_positions = [(5, 1), (2, 2)]
    food_positions = [(4, 1)]
    Numberoftest = 100
    for i in range(Numberoftest):
        bot = setup_test_game(layout=layout, is_blue=True, bots=bot_positions, enemy=enemy_positions,
                              food=food_positions)
        next_move, _ = move(bot, None)
        assert next_move != (6, 1)


def test_no_kamikaze():
    # do we avoid enemies when they can kill us?
    layout = """
    ########
    #    E.#
    #.1  0E#
    ########
    """
    bot = setup_test_game(layout=layout, is_blue=True)
    next_move, _ = move(bot, None)
    assert next_move == (4, 2) or next_move == (5, 2)


def test_do_not_step_on_enemy():
    # check that we don't step back on an enemy when we are fleeing
    layout = """
    ########
    #    E.#
    #.1 #0E#
    ########
    """
    bot = setup_test_game(layout=layout, is_blue=True)
    next_move, _ = move(bot, None)
    assert next_move == (5, 2)
