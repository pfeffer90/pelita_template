from demo09_polite_random import move
from pelita.utils import setup_test_game

def test_nostep():
    """Check that the bot never steps on its teammate."""

    layout="""
    ########
    #0 #####
    #1. .EE#
    ########
    """
    # run the test for ten random games
    for i in range(10):
        bot = setup_test_game(layout=layout, is_blue=True)
        next_pos, _ = move(bot, None)
        assert next_pos in ((1, 1), (2, 1))
