from app.game.card import Card, Rank, Suit
import random

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in Rank for suit in Suit]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, count):
        drawn_cards = self.cards[:count]
        self.cards = self.cards[count:]
        return drawn_cards

    def reset(self):
        self.__init__()
