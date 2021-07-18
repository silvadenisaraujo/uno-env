import random
from uno_env.deck import Card, CardType, Color
from uno_env.player import Player
from uno_env.env import UnoEnv

LEN_TEST_PLAYERS = 4
TEST_PLAYERS = [Player(name=f"player_{x}") for x in range(LEN_TEST_PLAYERS)]


def test_init_game():
    UnoEnv(players=TEST_PLAYERS)


def test_draw_cards():
    env = UnoEnv(players=TEST_PLAYERS)
    cards = env.draw_cards(50)
    assert len(cards) == 50


def test_validate_step_same_number():
    env = UnoEnv(players=TEST_PLAYERS)
    card = Card(
        color=random.choice(list(Color)),
        number=env.top_pile.number,
        type=CardType.NUMBER,
    )
    assert env.validate_step(card) == True


def test_validate_step_same_color():
    env = UnoEnv(players=TEST_PLAYERS)
    card = Card(
        color=env.top_pile.color,
        number=random.randint(0, 9),
        type=CardType.NUMBER,
    )
    assert env.validate_step(card) == True


def test_validate_step_switch_color():
    env = UnoEnv(players=TEST_PLAYERS)
    card = Card(color=None, number=None, type=CardType.SWITCH_COLOR)
    assert env.validate_step(card) == True


def test_validate_step_plus_two():
    env = UnoEnv(players=TEST_PLAYERS)
    card = Card(color=env.top_pile.color, number=None, type=CardType.PLUS_2)
    assert env.validate_step(card) == True


def test_validate_step_plus_four():
    env = UnoEnv(players=TEST_PLAYERS)
    card = Card(color=env.top_pile.color, number=None, type=CardType.PLUS_4)
    assert env.validate_step(card) == True


def test_validate_step_change_direction():
    env = UnoEnv(players=TEST_PLAYERS)
    card = Card(
        color=env.top_pile.color, number=None, type=CardType.SWITCH_DIRECTION
    )
    assert env.validate_step(card) == True


def test_invalidate_step_different_color_and_number():
    env = UnoEnv(players=TEST_PLAYERS)
    possible_numbers = [x for x in range(9)]
    possible_numbers.remove(env.top_pile.number)
    possible_colors = list(Color)
    possible_colors.remove(env.top_pile.color)
    card = Card(
        color=random.choice(possible_colors),
        number=random.choice(possible_numbers),
        type=CardType.NUMBER,
    )
    assert env.validate_step(card) == False


def test_render_game():
    env = UnoEnv(players=TEST_PLAYERS)
    env.render()


def test_handle_plus_two():
    env = UnoEnv(players=TEST_PLAYERS)
    env.handle_plus_two()
    assert env.current_player == 1
    assert env.amount_to_draw == 2


def test_handle_plus_four():
    env = UnoEnv(players=TEST_PLAYERS)
    env.handle_plus_four()
    assert env.current_player == 1
    assert env.amount_to_draw == 4


def test_handle_number():
    env = UnoEnv(players=TEST_PLAYERS)
    env.handle_number()
    assert env.current_player == 1
    assert env.amount_to_draw == 0


def test_handle_switch_color():
    env = UnoEnv(players=TEST_PLAYERS)
    env.handle_switch_color(requested_color=Color.RED)
    assert env.current_color == Color.RED
    assert env.amount_to_draw == 0
    assert env.current_player == 1


def test_handle_switch_direction():
    env = UnoEnv(players=TEST_PLAYERS)
    env.handle_switch_direction()
    assert env.current_player == LEN_TEST_PLAYERS - 1

def test_handle_skip_next():
    env = UnoEnv(players=TEST_PLAYERS)
    env.handle_skip_next()
    assert env.current_player == 2