from math import ceil
from player import Players
from card import Deck
from card import Card
class Blackjack:

    def __init__(self):

        self.game_end = True

        # Setting Deck
        self.deck_num = 4
        self.deck = Deck(self.deck_num)
        self.deck.shuffle()

        # Setting Player
        self.player_num = 1
        self.players = Players(self.player_num)

        # Setting Banker
        self.banker = []
        self.min_bet = 5

        # Leave game player
        self.leave_man = 0

    def start(self):

        while self.game_end:
            self.game_restart()
            # self.banker = [{'symbol': 'Q', 'suit': 'spade', 'value': 10, 'faced': True},
            #                {'symbol': 'A', 'suit': 'heart', 'value': 11, 'faced': True}]
            self.players.in_[0].hands[0] = Card(symbol='5', suit='spade')
            self.players.in_[0].hands[1] = Card(symbol='6', suit='heart')

            # print(len(self.deck))
            print("Banker")
            print(self.banker[0].symbol, self.banker[0].suit, " ", end="")
            print(self.banker[1].symbol, self.banker[1].suit, " ", end="")
            print()
            self.players.print_all_status()

            self.is_insurance()
            self.check_blackjack()
            self.players.leave_game()
            self.leave_and_money()

            self.choice()
            self.players.leave_game()
            self.leave_and_money()

            self.banker_time()
            if not self.check_bust(self.banker):
                self.compare_cards()
                self.players.leave_game()
                self.leave_and_money()

            self.players.print_all_result()
            if input("Continue?") == "n":
                self.game_end = False

    # Game Setting
    def game_restart(self):

        if self.deck.check_deck_num():
            self.deck.reset_deck()

        # Reset Player
        # self.player_num = int(input("How many players want to participate?"))
        self.players.reset_all(self.min_bet)

        # Reset Banker Cards
        self.banker = []
        self.deal_to_all()

        # Nobody leave
        self.leave_man = 0

    # Deal Card
    def deal(self, cards_in_hand: list, faced=True):
        card = self.deck.deck.pop()
        card.faced = faced
        cards_in_hand.append(card)

    def deal_to_all(self):

        # To each player
        for player in self.players.in_:
            self.deal(player.hands, faced=False)

        # To banker
        self.deal(self.banker, faced=False)

        # To each player
        for player in self.players.in_:
            self.deal(player.hands)

        # To banker
        self.deal(self.banker)

    # Game Start
    def is_insurance(self):

        if self.banker[1].symbol == "A":
            for player in self.players.in_:
                choice = input("Want to buy an insurance?")
                if choice == "y":
                    player.insurance = True
                pass

    # Check Sum
    def check_sum(self, cards_in_hand):

        total = 0
        for card in cards_in_hand:
            total += card.value
        return total

    def switch_ace_value(self, cards_in_hand):

        for card in cards_in_hand:
            if card.symbol == "A" and card.value == 11:
                card.value = 1
                return True
        return False

    def check_sum_switch_ace(self, cards_in_hand):

        if self.check_sum(cards_in_hand) > 21:
            self.switch_ace_value(cards_in_hand)

        return self.check_sum(cards_in_hand)

    # Check Bust
    def check_bust(self, cards_in_hand):

        if self.check_sum_switch_ace(cards_in_hand) > 21:
            return True
        return False

    # Check blackjack
    def check_cards_blackjack(self, cards_in_hand):

        if len(cards_in_hand) == 2 and self.check_sum(cards_in_hand) == 21:
            return True
        return False

    def check_blackjack(self):

        for player in self.players.in_:

            if self.check_cards_blackjack(self.banker):

                if self.check_cards_blackjack(player.hands):
                    player.result = "push"
                else:
                    player.result = "lose"

            if self.check_cards_blackjack(player.hands):
                player.result = "blackjack"

    # Player time
    def choice(self):

        for player in self.players.in_:
            choice = input("Fold?")
            if choice == 'y':
                self.fold(player)

        for player in self.players.in_:
            self.player_choice(player)
        self.players.leave_game()
        self.leave_and_money()

    def player_choice(self, player):

        first_ask = True
        while not player.fold:
            choice = input(f"Player {player.id} choice?")
            if choice == "double" and self.check_sum_switch_ace(player.hands) == 11 and len(player.hands) == 2 and first_ask:
                self.double_down(player)
                if self.check_bust(player.hands):
                    player.result = "lose"
                self.players.print_all_status()

            elif choice == "split":
                pass

            if choice == "stand":
                break

            if not player.double:
                if choice == "hit":
                    self.hit(player)

            first_ask = False

    def double_down(self, player):

        player.double = True
        self.deal(player.hands)

    def fold(self, player):

        player.fold = True
        player.result = "fold"

    def hit(self, player):

        while True:
            self.deal(player.hands)
            if self.check_bust(player.hands):
                player.result = "lose"
                break

            if len(player.hands) >= 5:
                player._5_card_charlie = True

            self.players.print_all_status()
            if input("Another Card?") != "y":
                break

    # It's banker time
    def banker_time(self):

        while self.check_sum_switch_ace(self.banker) < 17:
            self.deal(self.banker)
            self.banker_bust()

    def banker_bust(self):

        if self.check_bust(self.banker):
            for player in self.players.in_:
                player.result = "win"
            self.players.leave_game()
            self.leave_and_money()
            return True
        return False

    # Compare the card score in hand
    def compare_cards(self):

        banker_point = self.check_sum_switch_ace(self.banker)
        for player in self.players.in_:

            player_point = self.check_sum_switch_ace(player.hands)
            if player_point > banker_point:
                player.result = "win"
            elif player_point < banker_point:
                player.result = "win"
            else:
                player.result = "push"

    # Exchange the money
    def give_money(self, player):

        if player.result == "win":

            if player._5_card_charlie:
                player.money += 3 * player.stake
            elif player.double:
                player.money += 2 * player.stake
            else:
                player.money += player.stake

        if player.result == "blackjack":

            if player.double:
                if player._5_card_charlie:
                    player.money += 6 * player.stake
                else:
                    player.money += 3 * player.stake
            else:
                if player._5_card_charlie:
                    player.money += 3 * player.stake
                else:
                    player.money += 1.5 * player.stake

        if player.result == "lose":

            if player.double:
                player.money -= 2 * player.stake
            else:
                player.money -= player.stake

        if player.result == "fold":

            player.money -= ceil(player.stake / 2)

        if self.check_sum_switch_ace(self.banker) == 21 and player.insurance:
            player.money += player.stake

    def leave_and_money(self):

        leaving_player = len(self.players.out)
        while self.leave_man != leaving_player:

            self.give_money(self.players.out[self.leave_man])
            self.leave_man += 1
