from Card import Card
from random import shuffle

class Deck:
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
    ranks = list(range(2, 15))
    cards = [Card]
    def __init__(self):
        "Initializes a deck of cards"
        self.cards = []

    def build(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        "Shuffles the deck of cards"
        shuffle(self.cards)

    def show(self):
        for card in self.cards:
            print(card)

    def add(self, card: Card):
        self.cards.append(card)

    def draw(self) -> Card:
        return self.cards.pop()

    def __len__(self) -> int:
        return len(self.cards)
