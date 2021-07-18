from dataclasses import dataclass
from enum import Enum
from itertools import product
from random import shuffle
from typing import List, Union


class Color(Enum):
    """Available colors in a UNO game"""

    BLUE = 1
    RED = 2
    YELLOW = 3
    GREEN = 4


class CardType(Enum):
    """Available cards in a UNO game"""

    NUMBER = 1
    PLUS_2 = 2
    SWITCH_COLOR = 3
    PLUS_4 = 4
    SWITCH_DIRECTION = 5
    SKIP_NEXT = 6


@dataclass
class Card:
    """An UNO card"""

    color: Color
    number: Union[int, None]
    type: CardType


def generate_shuffled_deck() -> List[Card]:
    """Generates a shuffled deck to start a new game

    Returns:
        List[Card]: Shuffled list of cards
    """
    deck: List[Card] = []

    # 4 cards number zero
    zeros = [Card(color, 0, CardType.NUMBER) for color in Color]
    deck.extend(zeros)

    # 2 cards for each number from 0 to 9 for each color
    number_colors = product(range(1, 10), Color)
    numbers = [
        Card(
            number=number_color[0], color=number_color[1], type=CardType.NUMBER
        )
        for number_color in number_colors
    ]

    deck.extend(numbers)
    deck.extend(numbers)

    # 4 cards of plus four
    plus_four = [Card(color, None, CardType.PLUS_4) for color in Color]
    deck.extend(plus_four)

    # 8 cards of skip next player, 2 per color
    skip_next = [Card(color, None, CardType.SKIP_NEXT) for color in Color]
    deck.extend(skip_next)
    deck.extend(skip_next)

    # 8 cards of switch direction, 2 per color
    plus_two = [Card(color, None, CardType.PLUS_2) for color in Color]
    deck.extend(plus_two)
    deck.extend(plus_two)

    # 4 cards of switch color
    switch_color = [
        Card(color, None, CardType.SWITCH_COLOR) for color in Color
    ]
    deck.extend(switch_color)

    # 8 cards of switch direction, 2 per color
    switch_direction = [
        Card(color, None, CardType.SWITCH_DIRECTION) for color in Color
    ]
    deck.extend(switch_direction)
    deck.extend(switch_direction)

    shuffle(deck)
    return deck
