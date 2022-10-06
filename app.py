import random


class Card:

    def __init__(self, symbol, suit, faced=True):
        # self.id = id_
        self.symbol = symbol
        self.suit = suit
        # self.value = value
        self.faced = faced


class Player:

    def __init__(self, id_, money=100, bet=5):
        self.id = id_
        self.stake = bet
        self.money = money
        self.cards = []
        self.insurance = False
        self._5_card_charlie = False
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
        self.deck = []

        # Setting Player
        self.player_num = 3
        self.players_in = []
        self.players_out = []
        self.create_player(self.player_num)

        # Setting Banker
        self.banker = []
        self.min_bet = 5

        while self.game_end:
            self.game_restart()

            self.banker = [{'symbol': 'Q', 'suit': 'spade', 'value': 10, 'faced': True},
                           {'symbol': 'A', 'suit': 'heart', 'value': 11, 'faced': True}]
            # self.players_in[0].cards = [{'symbol': 'Q', 'suit': 'spade', 'value': 10, 'faced': True},
            #                             {'symbol': 'A', 'suit': 'heart', 'value': 11, 'faced': True}]
            print(len(self.deck))
            print(self.banker)
            print(self.players_in[0].cards)
            print(self.players_in[1].cards)
            print(self.players_in[2].cards)
            self.is_insurance()
            self.check_blackjack()
            self.out_game_player()
            print()
            print(len(self.players_in))
            print(len(self.players_out))

            self.choice()
            self.out_game_player()
            self.banker_time()
            if not self.check_bust(self.banker):
                self.compare_cards()
                self.out_game_player()
            if input("Continue?") == "n":
                self.game_end = False

    def create_player(self, player_num):

        for id_ in range(player_num):
            player = Player(id_=id_)
            self.players_in.append(player)

    # Game Setting
    def game_restart(self):

        # Setting Player
        self.player_num = 2
        # self.player_num = int(input("How many players want to participate?"))
        self.check_deck()
        self.reset_player()
        self.deal_to_all()

    def check_deck(self):

        if len(self.deck) <= self.deck_num * 52 / 2:
            self.reset_deck()

    def reset_deck(self):

        self.deck = self.poker_deck * self.deck_num
        self.shuffle(self.deck)

    def shuffle(self, deck: list):
        random.shuffle(deck)

    # Reset Player
    def reset_player(self):

        self.player_enter()
        self.set_bet()
        self.reset_result()
        self.reset_insurance()
        self.reset_cards()

    # Player enter table
    def player_enter(self):

        while self.players_out:
            self.players_in.append(self.players_out.pop())
        self.players_in.sort(key=lambda x: x.id)

    # Reset Cards in hand
    def set_bet(self):

        for player in self.players_in:

            while True:
                # player.stake = int(input("How much money do you want to bet?"))

                # Check Player bet
                if player.stake >= player.money:
                    player.stake = player.money
                    print("All in")

                if player.stake < self.min_bet:
                    print(f"At least {self.min_bet} dollar")
                    continue
                break

    # Reset Result
    def reset_result(self):

        for player in self.players_in:
            player.result = ""

    # Reset Insurance
    def reset_insurance(self):

        for player in self.players_in:
            player.insurance = False

    # Reset 5 Card Charlie
    def reset_charlie(self):

        for player in self.players_in:
            player._5_card_charlie = False

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
                # choice = input("Want to buy a insurande?")
                # if choice == "y":
                #     player.insurance = True
                pass

    def check_blackjack(self):

        for player in self.players_in:

            if self.check_cards_blackjack(self.banker):

                if self.check_cards_blackjack(player.cards):
                    player.result = "push"
                else:
                    player.result = "lose"

            if self.check_cards_blackjack(player.cards):
                player.result = "blackjack"

    def out_game_player(self):

        out_game = []
        for player in self.players_in:

            if player.result != "":
                out_game.append(player.id)

        while out_game:
            out_player_id = out_game.pop()
            pick_id = 0
            for num in range(len(self.players_in)):
                if self.players_in[num].id == out_player_id:
                    pick_id = num
                    break
            out_game_player = self.players_in.pop(pick_id)
            self.players_out.append(out_game_player)
            self.give_money(out_game_player)

    def choice(self):

        for player in self.players_in:
            choice = input("Your choice?")
            self.player_choice(choice, player)
            print(player.cards)
            print(player.result)
        self.out_game_player()

    def player_choice(self, choice, player):

        if choice == "double" and self.check_sum_switch_ace(player.cards) == 11:
            self.double_down(player)
            if self.check_bust(player.cards):
                player.result = "lose"

        elif choice == "fold":
            self.fold(player)

        elif choice == "hit":
            self.hit(player)

        elif choice == "split":
            pass

        # self.split(player)

    def double_down(self, player):

        player.stake *= 2
        self.deal(player.cards)

    def fold(self, player):

        player.result = "fold"

    def hit(self, player):

        while True:
            self.deal(player.cards)
            if self.check_bust(player.cards):
                player.result = "lose"
                break

            if len(player.cards) >= 5:
                player._5_card_charlie = True

            if input("Another Card?") != "y":
                break

    def banker_time(self):

        while self.check_sum_switch_ace(self.banker) < 17:
            self.deal(self.banker)
            self.banker_bust()

    def banker_bust(self):

        if self.check_bust(self.banker):
            for player in self.players_in:
                player.result = "win"
            self.out_game_player()
            return True
        return False

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

    def give_money(self, player):

        if player.result == "win":
            if player._5_card_charlie:
                player.money += 2 * player.stake
            else:
                player.money += player.stake

        if player.result == "blackjack":
            if player._5_card_charlie:
                player.money += 3 * player.stake
            else:
                player.money += 1.5 * player.stake

        if player.result == "lose":
            player.money -= player.stake

        if player.result == "fold":
            player.money -= int(player.stake / 2)

        if self.check_sum_switch_ace(self.banker) == 21 and player.insurance:
            player.money += player.stake


if __name__ == "__main__":
    game = Blackjack()
