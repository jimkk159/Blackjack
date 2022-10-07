from math import floor
from player import Hand, Players
from card import Card, Deck


class Blackjack:

    def __init__(self):

        self.game_end = True

        # Setting Deck
        self.deck_num = 4
        self.deck = Deck(self.deck_num)
        self.deck.shuffle()

        # Setting Player
        self.player_num = 2
        self.players = Players(self.player_num)

        # Setting Banker
        self.banker = []
        self.min_bet = 5

        # Leave game player
        self.leave_man = 0

    def start(self):

        while self.game_end:
            self.game_restart()
            # self.banker = [Card(symbol='K', suit='spade'),
            #                Card(symbol='A', suit='heart')]
            self.players.in_[0].hands[0].cards = [Card(symbol='A', suit='spade'),
                                                  Card(symbol='A', suit='heart')]

            print("*" * 20)
            print("New Round Begin")
            print("*" * 20)
            self.print_banker()
            self.players.print_all_status()
            print()

            self.is_insurance()
            self.check_blackjack()
            self.players.leave_game()
            self.leave_and_money()
            self.players.print_all_result()

            self.choice()
            self.players.leave_game()
            self.leave_and_money()

            self.banker_time()
            if not self.check_bust(self.banker):
                self.compare_cards()
                self.players.leave_game()
                self.leave_and_money()

            self.print_banker()
            self.players.print_all_status(choice="out")
            print()
            self.players.print_all_result()
            print(self.check_sum_switch_ace(self.players.out[0].hands[0].cards))
            print("*" * 20)
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
            self.deal(player.hands[0].cards)

        # To banker
        self.deal(self.banker, faced=False)

        # To each player
        for player in self.players.in_:
            self.deal(player.hands[0].cards)

        # To banker
        self.deal(self.banker)

    # Game Start
    def is_insurance(self):

        if self.banker[1].symbol == "A":
            for player in self.players.in_:
                if player.money >= floor(player.stake / 2):
                    choice = input("Want to buy an insurance?")
                    if choice == "y":
                        player.money -= floor(player.stake / 2)
                        player.insurance = True

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

                if self.check_cards_blackjack(player.hands[0].cards):
                    player.hands[0].result = "push"
                else:
                    player.hands[0].result = "lose"

            elif self.check_cards_blackjack(player.hands[0].cards):
                player.hands[0].result = "blackjack"

    # It's Player Round
    def choice(self):

        for player in self.players.in_:
            choice = input("Fold?")
            if choice == 'y':
                self.fold(player)

        for player in self.players.in_:
            self.player_choice(player)
        self.players.leave_game()
        self.leave_and_money()

    def fold(self, player):

        player.fold = True
        player.hands[0].result = "fold"

    def player_choice(self, player):

        if not player.fold:

            print()
            choice = input(f"Player {player.id} choice?")
            if choice == "double" and len(player.hands[0].cards) == 2 and player.money >= player.stake:

                self.double_down(player)
                if self.check_bust(player.hands[0].cards):
                    print("bust")
                    player.hands[0].result = "lose"
            else:

                hand_count = 0
                while True:

                    # print("-----------------------------")
                    # print("hand_count", hand_count, len(player.hands))

                    if hand_count >= len(player.hands):
                        print("break")
                        break

                    while True:

                        if choice == "split" \
                                and len(player.hands[hand_count].cards) == 2 \
                                and player.hands[hand_count].cards[0].symbol == player.hands[hand_count].cards[1].symbol \
                                and player.money >= player.stake:

                            player.money -= player.stake
                            split_hand = Hand()
                            split_hand.cards.append(player.hands[hand_count].cards.pop())

                            player.hands[hand_count].is_ace_split = True
                            split_hand.is_ace_split = True

                            player.hands.append(split_hand)

                        if choice == "stand":
                            choice = ""
                            break

                        if choice == "hit":
                            self.hit(player.hands[hand_count])
                            if player.hands[hand_count].is_ace_split:
                                choice = ""
                                break

                        print()
                        self.players.print_all_status()
                        print("Bust?", hand_count, self.check_bust(player.hands[hand_count].cards))
                        if self.check_bust(player.hands[hand_count].cards):
                            print("This hand is bust")
                            choice = ""
                            player.hands[hand_count].result = "lose"
                            break
                        choice = input(f"Player {player.id} Hand {hand_count} choice?")

                    hand_count += 1
        # print("-----------------------------")
        # print("This is outside")
        # print("-----------------------------")

    def double_down(self, player):

        player.double = True
        player.money -= player.stake
        self.deal(player.hands[0].cards)

    def hit(self, hand):

        self.deal(hand.cards)
        if len(hand.cards) >= 5:
            hand._5_card_charlie = True

    # It's banker time
    def banker_time(self):

        while self.check_sum_switch_ace(self.banker) < 17:
            self.deal(self.banker)
            self.banker_bust()

    def banker_bust(self):

        if self.check_bust(self.banker):
            for player in self.players.in_:
                for hand in player.hands:
                    if hand.result == "":
                        hand.result = "win"

            self.players.leave_game()
            self.leave_and_money()
            return True
        return False

    # Compare the card score in hand
    def compare_cards(self):

        banker_point = self.check_sum_switch_ace(self.banker)
        for player in self.players.in_:
            for hand in player.hands:
                if hand.result == "":

                    if hand._5_card_charlie:
                        hand.result = "win"
                    else:
                        player_point = self.check_sum_switch_ace(hand.cards)
                        if player_point > banker_point:
                            hand.result = "win"
                        elif player_point < banker_point:
                            hand.result = "lose"
                        else:
                            hand.result = "push"

    # Exchange the money
    def give_money(self, player):

        for hand in player.hands:
            self.give_hand_money(hand, player)

        if player.fold:
            player.money += floor(player.stake / 2)

        if self.check_sum_switch_ace(self.banker) == 21 and player.insurance:
            player.money += 2 * floor(player.stake / 2)

    def give_hand_money(self, hand, player):

        if hand.result == "win":

            if hand._5_card_charlie or player.double:

                player.money += 4 * player.stake

            else:
                player.money += 2 * player.stake

        if hand.result == "blackjack":

            if player.double:
                player.money += 5 * player.stake

            elif hand._5_card_charlie:
                player.money += floor(5.5 * player.stake)

            else:
                player.money += floor(2.5 * player.stake)

        if hand.result == "push":
            if player.double:
                player.money += 2 * player.stake
            else:
                player.money += player.stake

    def leave_and_money(self):

        leaving_player = len(self.players.out)
        while self.leave_man != leaving_player:
            self.give_money(self.players.out[self.leave_man])
            self.leave_man += 1

    def print_banker(self):

        print("Banker has: ")
        print("cards: ", end="")
        for card in self.banker:
            print(f"{card.symbol} {card.suit} ", end="")
        print(f"{self.check_sum_switch_ace(self.banker)} ")
        print()
