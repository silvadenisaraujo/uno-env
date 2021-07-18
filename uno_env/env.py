import gym

from typing import List, Tuple
from random import shuffle
from uno_env.exceptions import InvalidStepException
from uno_env.deck import Card, CardType, generate_shuffled_deck
from uno_env.player import Player, PlayerIter

INITIAL_CARDS_FOR_EACH = 7


class UnoEnv(gym.Env):
    """
        The deck is structured as follows:
        Colors = BLUE, GREEN, YELLOW, RED
        4x 0 card
        4x 4+ card
        4x switch color card
        8x 1 - 9 cards
        8x skip card
        8x 2+ card
        8x change direction
        Total of 108 cards.
    """

    def __init__(self, players: List[Player]):
        self.players = players
        self.player_iter = iter(PlayerIter(len(self.players)))
        self.CARD_HANDLER = {
            CardType.PLUS_2: self.handle_plus_two,
            CardType.PLUS_4: self.handle_plus_four,
            CardType.NUMBER: self.handle_number,
            CardType.SWITCH_COLOR: self.handle_switch_color,
            CardType.SWITCH_DIRECTION: self.handle_switch_direction,
            CardType.SKIP_NEXT: self.handle_skip_next,
        }
        self.__init_game()

    def __init_game(self):
        self.done = False
        self.round = 0
        self.direction = 1  # 1 = Clockwise / -1 Counter-clockwise
        self.current_player = 0
        self.deck = []  # Available cards to be picked
        self.pile = []  # Cards played
        self.top_pile = None
        self.current_color = None
        self.amount_to_draw = 0

        self.give_cards()

    def give_cards(self):
        """Give cards to start the game"""
        self.deck = generate_shuffled_deck()
        for player in self.players:
            player.hand.extend(self.draw_cards(INITIAL_CARDS_FOR_EACH))

        top_pile = self.draw_cards(1)[0]
        while top_pile.type != CardType.NUMBER:
            self.pile.append(top_pile)
            top_pile = self.draw_cards(1)[0]

        self.top_pile = top_pile
        self.current_color = self.top_pile.color
        self.pile.append(self.top_pile)

    def draw_cards(self, n: int) -> List[Card]:
        """Draw cards from the shuffled deck
        If the deck does not have all the vailable cards
        then it is mandatory to take the pile of played cards
        re-shuffle and add to the deck again

        Args:
            n (int): amount of cards to draw

        Returns:
            List[Card]: Drawn cards
        """
        if len(self.deck) < n:
            played_cards = self.pile[:-1]
            self.pile = [self.top_pile]
            self.deck.extend(played_cards)
            shuffle(self.deck)
        cards = self.deck[:n]
        del self.deck[:n]
        return cards

    def validate_step(self, card: Card) -> bool:
        """Validate if the step is valid

        Args:
            card (Card): new played card

        Raises:
            InvalidStepException: Invalid step taken

        Returns:
            bool: True if valid
        """
        if card.type in [CardType.SWITCH_COLOR, CardType.PLUS_4]:
            return True
        if card.color == self.top_pile.color:
            return True
        if (
            self.top_pile.type == CardType.NUMBER
            and card.number == self.top_pile.number
        ):
            return True
        return False

    def step(self, action) -> Tuple[object, float, bool, dict]:
        reward = 0.0  # Win it or not!
        player, card, requested_color = action

        """
            If the current player does not have a card that matches
            the top of the pile in color or number
        """
        if card is None:
            self.current_player = next(self.player_iter)
            player.hand.extend(self.draw_cards(1))
            self.round += 1
            return self.pile, reward, self.done, {}

        if not self.validate_step(card):
            raise InvalidStepException(
                f"Invalid card, top of pile is {self.top_pile}"
            )

        """
            If previous play was a plus four or plus two 
            and the current player does not have this card
        """
        if self.amount_to_draw > 0 and card.type not in [
            CardType.PLUS_2,
            CardType.PLUS_4,
        ]:
            player.hand.extend(self.draw_cards(self.amount_to_draw))
            self.current_player = next(self.player_iter)
            self.amount_to_draw = 0
            self.round += 1
            return self.pile, reward, self.done, {}

        """
            Otherwise time to the user to play the card
        """
        self.CARD_HANDLER[card.type](requested_color=requested_color)

        # Update played pile of cards and players hand
        self.pile.extend(card)
        self.top_pile = card
        player.hand.remove(card)

        # Update round
        self.round += 1

        # Validate Reward
        if len(player.hand) == 0:
            reward = 1.0
            self.done = True
            self.reset()

        return self.pile, reward, self.done, {}

    def reset(self):
        """Reset the game!"""
        self.__init_game()

    def render(self):
        """Renders the current state of the environment"""
        print(f"Round #: {self.round}")
        print(f"Pile top: {self.top_pile}")
        print(f"Current Player: {self.current_player}")
        print(
            f"Current Direction: {'CLOCKWISE' if self.player_iter.direction == 1 else 'COUNTER-CLOCKWISE'}"
        )
        print(f"Available cards on deck: {len(self.deck)}")
        print("-" * 60)

    def handle_plus_two(self, *args, **kwargs):
        self.amount_to_draw += 2
        self.current_player = next(self.player_iter)

    def handle_plus_four(self, *args, **kwargs):
        self.amount_to_draw += 4
        self.current_player = next(self.player_iter)

    def handle_number(self, *args, **kwargs):
        self.current_player = next(self.player_iter)

    def handle_switch_color(self, *args, **kwargs):
        self.current_color = kwargs["requested_color"]
        self.current_player = next(self.player_iter)

    def handle_switch_direction(self, *args, **kwargs):
        self.player_iter.change_direction()
        self.current_player = next(self.player_iter)

    def handle_skip_next(self, *args, **kwargs):
        next(self.player_iter)
        self.current_player = next(self.player_iter)
