class Card:
    """
    Represents a playing card
    """
    def __init__(self, suit:str, rank:int):
        """
        Initializes a card with a suit and rank
        param suit: The suit of the card, must be Hearts, Diamonds, Spades, or Clubs
        param rank: The rank of the card, must be 2-14
        """
        if suit not in ["Hearts", "Diamonds", "Spades", "Clubs"]:
            raise ValueError("Invalid Suit")
        if rank not in range(2, 15):
            raise ValueError("Invalid Rank")
        
        self.suit = suit
        self.rank = rank
        self.value = self.__set_value()


    def __set_value(self) -> str:
        # 2, 3, 4, 5, 6, 7, 8, 9, 10
        if self.rank == 11:
            return "Jack"
        elif self.rank == 12:
            return "Queen"
        elif self.rank == 13:
            return "King"
        elif self.rank == 14:
            return "Ace"
        else:
            return str(self.rank)
    
    def get_suit_and_rank(self):
        return self.suit, str(self.rank)

    def get_value_and_suit(self):
        return self.value, self.suit

    def __str__(self):
        return f"{self.value} of {self.suit}"
    
    def __repr__(self):
        return f'Card("{self.value}", "{self.suit}", {self.rank})'

    def __eq__(self, other: 'Card') -> bool:
        return self.rank == other.rank

    def __lt__(self, other: 'Card') -> bool:
        return self.rank < other.rank
    
    def __gt__(self, other: 'Card') -> bool:
        return self.rank > other.rank
    
    def __le__(self, other: 'Card') -> bool:
        return self.rank <= other.rank
    
    def __ge__(self, other: 'Card') -> bool:
        return self.rank >= other.rank
    
    def __ne__(self, other: 'Card') -> bool:
        return self.rank != other.rank
