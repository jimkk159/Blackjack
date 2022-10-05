import random


class Card:

    def __init__(self):
        pass


class Player:

    def __init__(self, id_, money=100, bet=5):
        self.id = id_
        self.stake = bet
        self.money = money
        self.cards = []
        self.insurance = False
        self.result = ""


class Blackjack:

    def __init__(self):

        self.game_end = True

        # Setting Deck
        self.deck_num = 1
        self.suits = ["spade", "heart", "diamond", "club"]
        self.poker_symbol = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        self.poker_value_dict = {"A": 11, "K": 10, "Q": 10, "J": 10, "10": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5,
                                 "4": 4, "3": 3, "2": 2}
        self.poker_deck = [{"symbol": symbol, "suit": suit, "value": self.poker_value_dict[symbol], "faced": True} for
                           symbol in self.poker_symbol for suit in self.suits]
        self.deck = self.poker_deck * self.deck_num

        # Setting Player
        self.player_num = 2
        self.players_in = []
        self.players_out = []
        self.create_player(self.player_num)

        # Setting Banker
        self.banker = []

        self.shuffle(self.deck)

        while self.game_end:
            self.game_restart()

            # self.players_in[0].cards = [{'symbol': 'Q', 'suit': 'spade', 'value': 10, 'faced': True},
            #                             {'symbol': 'A', 'suit': 'heart', 'value': 11, 'faced': True}]

            print(self.banker)
            print(self.players_in[0].cards)
            print(self.players_in[1].cards)
            self.is_insurance()
            self.check_blackjack()
            self.choice()
            if self.banker_time() == "banker lose":
                # Return money to players
                pass

            self.compare_cards()
            self.give_money()
            self.game_end = False

    def create_player(self, player_num):

        for id_ in range(player_num):
            player = Player(id_=id_)
            self.players_in.append(player)

    # Game Setting
    # TODO Choice deck number
    def game_restart(self):

        # Setting Player
        self.player_num = 2
        # self.player_num = int(input("How many players want to participate?"))

        # Set Player bet
        # Check Player bet
        self.set_bet()

        self.reset_result()
        self.reset_insurance()
        self.reset_cards()
        self.deal_to_all()

    def shuffle(self, deck: list):
        random.shuffle(deck)

    # Reset Cards in hand
    def set_bet(self):

        for player in self.players_in:
            # player["bet"] = int(input("How much money do you want to bet?"))
            player.stake = 5

    # Reset Result
    def reset_result(self):

        for player in self.players_in:
            player.result = ""

    # Reset Insurance
    def reset_insurance(self):

        for player in self.players_in:
            player.insurance = False

    # Reset Cards in hand
    def reset_cards(self):

        # Reset Banker
        self.banker = []

        # Reset Player
        for player in self.players_in:
            player.cards = []

    # Game Start
    def deal_to_all(self):

        # To each player
        for player in self.players_in:
            self.deal(player.cards)

        # To banker
        self.deal(self.banker, faced=False)

        # To each player
        for player in self.players_in:
            self.deal(player.cards)

        # To banker
        self.deal(self.banker)

    def deal(self, cards_in_hand: list, faced=True):
        card = self.deck.pop()
        card["faced"] = faced
        cards_in_hand.append(card)

    def check_bust(self, cards_in_hand):

        if self.check_sum_switch_ace(cards_in_hand) > 21:
            return True
        return False

    def check_sum(self, cards_in_hand):

        total = 0
        for card in cards_in_hand:
            total += card["value"]
        return total

    def check_sum_switch_ace(self, cards_in_hand):

        if self.check_sum(cards_in_hand) > 21:
            self.switch_ace_value(cards_in_hand)

        return self.check_sum(cards_in_hand)

    def check_cards_blackjack(self, cards_in_hand):

        if len(cards_in_hand) == 2 and self.check_sum(cards_in_hand) == 21:
            return True
        return False

    def switch_ace_value(self, cards_in_hand):

        for card in cards_in_hand:
            if card["symbol"] == "A" and card["value"] == 11:
                card["value"] = 1
                return True
        return False

    def is_insurance(self):

        if self.banker[1]["symbol"] == "A":
            for player in self.players_in:
                choice = input("Want to buy a insurande?")
                if choice == "y":
                    player.insurance = True

    def check_blackjack(self):

        for player in self.players_in:

            if self.check_cards_blackjack(self.banker):

                if self.check_cards_blackjack(player.cards):
                    player.result = "push"
                else:
                    player.result = "lose"

            if self.check_cards_blackjack(player.cards):
                player.result = "win"

    def choice(self):

        for player in self.players_in:
            choice = input("Your choice?")
            self.player_choice(choice, player)
            print(player.cards)
            print(player.result)

    def player_choice(self, choice, player):

        if choice == "double":
            self.double_down(player)

        if choice == "fold":
            self.fold(player)

        if choice == "hit":
            while True:
                self.deal(player.cards)
                if self.check_bust(player.cards):
                    player.result = "lose"
                    break
                if input("Another Card?") != "y":
                    break
        # self.split(player)

    def double_down(self, player):

        player.stake *= 2
        self.deal(player.cards)

    def fold(self, player):

        player.money -= player.stake / 2
        player.result = "fold"

    def banker_time(self):

        while self.check_sum_switch_ace(self.banker) < 17:
            self.deal(self.banker)
            if self.check_bust(self.banker):
                return "banker lose"

    def compare_cards(self):

        banker_point = self.check_sum_switch_ace(self.banker)
        for player in self.players_in:

            player_point = self.check_sum_switch_ace(player.cards)
            if player_point > banker_point:
                player.result = "win"
            elif player_point < banker_point:
                player.result = "win"
            else:
                player.result = "push"

    def give_money(self):

        for player in self.players_in:

            if player.result == "win":
                player.money += player.stake

            if player.result == "blackjack":
                player.money += 1.5 * player.stake

            if player.result == "5 card charlie":
                player.money += 2 * player.stake

            if player.result == "lose":

                player.money -= player.stake



            if self.check_sum_switch_ace(self.banker) == 21 and player.insurance:
                player.money += player.stake

if __name__ == "__main__":
    game = Blackjack()
