from dataclasses import dataclass, field
from typing import List
from uno_env.deck import Card


@dataclass
class Player:
    name: str
    hand: List[Card] = field(default_factory=list)


class PlayerIter:
    def __init__(self, n_players: int):
        self.n_players = n_players
        self.direction = 1
        self.current = 0
    
    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self):
        next_index = self.direction + self.current
        if next_index > self.n_players - 1:
            next_index = 0
        elif next_index < 0:
            next_index = self.n_players - 1
        self.current = next_index
        return next_index

    def change_direction(self):
        self.direction *= -1

            
