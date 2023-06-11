from Deck import Deck
from Card import Card
from Player import Player
import sys
import pygame


class Game:
    players = list[Player]
    board = list[dict[str, Card]]
    num_decks = int
    total_rounds = 0
    card_images = {}
    screen = pygame.Surface
    max_width = 1920
    max_height = 1080
    card_spacing = 20
    hidden_round = False
    cards_placed = 0

    def __init__(self, players: list[Player]):
        """
        Creates a new game with the given players
        param players: A list of players
        """
        if len(players) < 2:
            raise ValueError("There must be at least 2 players")
        if len(players) > 4:
            raise ValueError("There can be at most 4 players")
        self.players = players
        self.board = []
        self.num_decks = 1 + (len(players) - 1) // 2
        self.max_cards = self.num_decks * 52
        self.deal_cards()
        self.init_pygame()
        self.start_pygame()

    def deal_cards(self):
        """
        Based on the number of players, deals cards to each player
        for 2 players, one deck is used
        for more players, use following formula to determine number of decks:
        1 + (number_of_players - 1) // 2
        """
        2
        print(f"Dealing {self.num_decks} deck(s)")
        for _ in range(self.num_decks):
            deck = Deck()
            deck.build()
            deck.shuffle()
            # Deal cards to each player
            cards_per_player = 52 // len(self.players)
            for player in self.players:
                for _ in range(cards_per_player):
                    card = deck.draw()
                    if card is None:
                        break
                    player.hand.add(card)

    def get_name(self, uuid: str) -> str:
        """
        Returns the name of the player with the given uuid
        param uuid: The uuid of the player
        """
        for player in self.players:
            if player.uuid == uuid:
                return player.name
        return None

    def show_board(self):
        """
        Prints the current board
        """
        for item in self.board:
            name = self.get_name(item["uuid"])
            card = item["card"]
            if item["is_hidden"]:
                print(f"{name} placed a card")
            else:
                print(f"{name} played {card}")

    def players_with_cards(self) -> list[Player]:
        """
        Returns a list of players who have cards
        """
        players_with_cards = []
        for player in self.players:
            if len(player.hand) + len(player.graveyard) > 0:
                players_with_cards.append(player)
        return players_with_cards

    def place_cards(self, is_hidden: bool = False):
        """
        Each player places a card on the board
        param is_hidden: If true, the card is placed face down
        """
        for player in self.players_with_cards():
            # If player is not AI, wait for user input
            card = player.draw()
            if not player.AI:
                input(f"{player.name}, press enter to place a card")
                print(f"{player.name} drew {card}")
            self.board.append(
                {"uuid": player.uuid, "card": card, "is_hidden": is_hidden}
            )
            if is_hidden:
                print(f"{player.name} placed a card")
            else:
                print(f"{player.name} played {card}")

    def is_draw(self) -> bool:
        """
        Returns true if the game is a draw.
        Game is a draw if the last cards played by each player are the same rank
        """
        if len(self.board) < self.cards_placed:
            return False
        last_card = self.board[-1]["card"]
        for item in self.board[-self.cards_placed:-1]:
            if item["card"] != last_card:
                return False
        return True

    def is_game_over(self) -> bool:
        """
        Returns true if the game is over.
        Game is over if there is only one player with cards left.
        """
        for player in self.players_with_cards():
            if len(player.hand) + len(player.graveyard) == self.max_cards:
                print(f"{player.name} wonnnnnnnnnnnnnn the game!")
                return True
        return False

    def get_game_winner(self) -> str:
        """
        Returns the name of the winner
        Game is won, if a player has all the cards.
        """
        for player in self.players:
            if len(player.hand) + len(player.graveyard) == self.max_cards:
                return player.name
        return None

    def winner_collect_cards(self):
        """
        Player with the highest placed card in the last round collects all the cards
        """
        # Find the highest card
        highest_card = None
        for item in self.board[-self.cards_placed:]:
            if highest_card is None or item["card"] > highest_card:
                highest_card = item["card"]
        highest_card_player = None
        # Find the player who placed the highest card
        for item in self.board[-self.cards_placed:]:
            if item["card"] == highest_card:
                highest_card_player = item["uuid"]
                break
        # Add all the cards to the winner's graveyard
        cards_on_board = []
        for item in self.board:
            cards_on_board.append(item["card"])

        for player in self.players:
            if player.uuid == highest_card_player:
                player.add_to_graveyard(cards_on_board)
                print(f"{player.name} won the round")
                self.draw_round_winner(player.name)
                break

        self.board = []

    def draw_round_winner(self, winner: str):
        """
        Displays the winner of the round
        """
        self.draw_text(f"{winner} won the round", 50, (255, 255, 255))

    def play_round(self, hidden_round: bool = False):
        """
        Single round of the game:
        1. Each player places a card on the board
        2. If the placed cards are the same rank, burn the cities
        3. If not a draw, the player with the highest rank wins the round
        4. Check if the game is over
        """
        self.cards_placed = len(self.players_with_cards())

        if self.cards_placed < 2:
            return

        self.place_cards(hidden_round)

        if hidden_round:
            print("Placing cards face up")
            return False
        else:
            if self.is_draw():
                print("Its a draw, time to burn the cities!")
                print("Placing cards face down")
                return True

        return False

    def play_game(self):
        """
        Play the game until there is a winner
        """
        while True:
            self.play_round()
            if self.is_game_over():
                print("Game over")
                for player in self.players_with_cards():
                    print(f"{player.name} has {len(player.hand)} cards left in hand")
                    print(
                        f"{player.name} has {len(player.graveyard)} cards left in hand"
                    )
                break

    def init_load_cards(self):
        for suit in Deck.suits:
            for rank in Deck.ranks:
                card = Card(suit, rank)
                card_image = pygame.image.load(
                    f"images/cards/{card.value.lower()}_of_{card.suit.lower()}.png"
                )
                card_image = pygame.transform.scale_by(card_image, 0.25)
                self.card_images[(card.value.lower(), card.suit.lower())] = card_image
        # Load hidden card
        card_image = pygame.image.load("images/cards/card_hidden.png")
        card_image = pygame.transform.scale_by(card_image, 0.25)
        self.card_image_height = card_image.get_height()
        self.card_image_width = card_image.get_width()
        self.card_images[("hidden", "hidden")] = card_image

    def init_pygame(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.max_width, self.max_height))
        pygame.display.set_caption("Burn the Cities")
        self.init_load_cards()

    def draw_static_elements(self) -> list[dict]:
        self.screen.blit(
            pygame.image.load("images/assets/card-game-background.png"), (0, 0)
        )
        # Add hiddens cards in the middle
        center_x = self.max_width // 2
        center_y = self.max_height // 2
        player_count = len(self.players_with_cards())
        total_width = (
            player_count * self.card_image_width + player_count * self.card_spacing
        )
        total_height = self.card_image_height

        start_x = center_x - total_width // 2
        start_y = center_y - total_height // 2

        for i in range(player_count):
            x = start_x + (i % player_count) * (self.card_image_width + self.card_spacing)
            y = start_y
            self.screen.blit(self.card_images[("hidden", "hidden")], (x, y))
        # Draw buttons
        font = pygame.font.Font("freesansbold.ttf", 32)
        button_listeners = []
        ## Draw "Draw Card" button
        button_width = 200
        button_height = 50

        draw_card_button = pygame.Rect(
            center_x - (2 * button_width + self.card_spacing) // 2,
            self.max_height - (button_height * 2),
            200,
            50,
        )
        pygame.draw.rect(self.screen, (0, 0, 0), draw_card_button)
        draw_card_text = font.render("Draw Card", True, (255, 255, 255))
        draw_card_text_rect = draw_card_text.get_rect(center=draw_card_button.center)
        self.screen.blit(draw_card_text, draw_card_text_rect)
        button_listeners.append({"button_name": "Draw Card", "button": draw_card_button})
        ## Draw "Quit" button
        quit_game_button = pygame.Rect(
            center_x - (2 * button_width + self.card_spacing) // 2 + button_width + self.card_spacing, 
            self.max_height - (button_height * 2),
            200, 
            50
        )
        pygame.draw.rect(self.screen, (0, 0, 0), quit_game_button)
        quit_game_text = font.render("Quit Game", True, (255, 255, 255))
        quit_game_text_rect = quit_game_text.get_rect(center=quit_game_button.center)
        self.screen.blit(quit_game_text, quit_game_text_rect)
        button_listeners.append({"button_name": "Quit Game", "button": quit_game_button})

        # Draw names above the cards
        for i, player in enumerate(self.players_with_cards()):
            player_name = font.render(player.name, True, (0, 0, 0))
            player_name_rect = player_name.get_rect(center=(start_x + i * (self.card_image_width + self.card_spacing) + self.card_image_width // 2, start_y - 30))
            self.screen.blit(player_name, player_name_rect)
        return button_listeners

    def handle_button_click(self, listener: dict):
        if listener["button_name"] == "Draw Card":
            self.hidden_round = self.play_round(self.hidden_round)
            self.winner_collect_cards()
        elif listener["button_name"] == "Quit Game":
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_button_listeners(self, button_listeners: list[dict], button_clicked: bool) -> bool:
        for listener in button_listeners:
                if pygame.mouse.get_pressed()[0] and not button_clicked:
                    if listener["button"].collidepoint(pygame.mouse.get_pos()):
                        self.handle_button_click(listener)
                        button_clicked = True
        if not pygame.mouse.get_pressed()[0]:
            button_clicked = False
        return button_clicked
    
    def render_cards(self):
        # Render cards from board
        center_x = self.max_width // 2
        center_y = self.max_height // 2
        player_count = len(self.players_with_cards())
        total_width = ( player_count * self.card_image_width + player_count * self.card_spacing )
        total_height = self.card_image_height

        start_x = center_x - total_width // 2
        start_y = center_y - total_height // 2
        if len(self.board) < player_count:
            return

        if player_count == 0:
            return

        for i in range(len(self.board)):
            x = start_x + (i % player_count) * (self.card_image_width + self.card_spacing)
            y = start_y
            item = self.board[i]
            if item["is_hidden"]:
                self.screen.blit(self.card_images[("hidden", "hidden")], (x, y))
            else:
                card: Card = item["card"]
                value, suit = card.get_value_and_suit()
                self.screen.blit(self.card_images[(value.lower(), suit.lower())], (x, y))




    def start_pygame(self):
        running = True
        button_clicked = False
        while running:
            button_listeners = self.draw_static_elements()
            button_clicked = self.handle_button_listeners(button_listeners, button_clicked)
            self.render_cards()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
            
            pygame.display.update()


new_game = Game([Player("Rasmus"), Player("Liza")])


# # Game loop
# card_spacing = 10
# Card_Game = Game([Player("Rasmus"), Player("Liza")])
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     x = 0
#     y = 0
#     for item in Card_Game.board:
#         card = item["card"]
#         value, suit = card.value.lower(), card.suit.lower()
#         card_image = card_images[(value, suit)]
#         screen.blit(card_image, (x, y))
#         x += card_image_width + card_spacing
#         if x + card_image_width > screen.get_width():
#             x = 0
#             y += card_image_height + card_spacing
#     pygame.display.update()
