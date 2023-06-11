from Deck import Deck
from Card import Card
from uuid import uuid4, UUID
class Player:
    uuid = UUID
    name = str
    hand = Deck
    graveyard = Deck
    AI = bool

    def __init__(self, name: str, AI: bool = True):
        """
        Initializes a player. When a player is an AI, the computer will play for them.
        If the player is not an AI, the player will play for themselves.
        param name: Name of the player
        param AI: If true, the player is an AI
        """
        self.uuid = uuid4()
        self.name = name
        self.hand = Deck()
        self.graveyard = Deck()
        self.AI = AI
    
    def draw(self) -> Card:
        if len(self.hand) == 0 and len(self.graveyard) == 0:
            return None
        if len(self.hand) == 0:
            self.hand = self.graveyard
            self.graveyard = Deck()
            print(f"{self.name} reshuffled their graveyard")
        
        return self.hand.draw()
    
    def add_to_graveyard(self, cards: list[Card]):
        for card in cards:
            self.graveyard.add(card)
    
