import random

from sqlalchemy import false, true

class Blackjack:

    def __init__(self) -> None:

        # Setting Deck
        self.deck_num = 4
        self.suits = ["spade", "heart", "diamond", "club"]
        self.poker_symbol = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
        self.poker_value_dict = {"A":11,"K":10,"Q":10,"J":10,"10":10,"9":9,"8":8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2}
        self.poker_deck = [ {symbol : {"suit": suit}} for symbol in self.poker_symbol for suit in self.suits ]
        self.deck = self.poker_deck * self.deck_num

        print(self.poker_deck)
        # # Setting Player
        # self.bet = 5
        # self.player_num = 1
        # self.player_cards = []
        # self.players_money = []

        # # Setting Banker
        # self.banker = []

        # self.shuffle(self.deck)
        # self.banker = []
        # self.player_cards = self.reset_player(self.player_num)
        # self.deal_to_all()

    # Game Setting
    # TODO Choice deck number

    def is_insurance():
        pass
    
    def shuffle(self, deck : list):
        random.shuffle(deck)

    # Reset Player Card
    def reset_player(self, player_num):

        return [ [] * player_num ]

    # Game Start
    def deal_to_all(self):
        
        # To each player
        for player_card in self.player_cards:
            self.deal(player_card, true)

        # To banker
        self.deal(self.banker, false)

        # To each player
        for player_card in self.player_cards:
            self.deal(player_card, true)

    def deal(self, cards_in_hand : list, faced):
        card = self.deck.pop()
        cards_in_hand.append({card : [self.poker_dict[card], faced]})

    def check_bust(self, cards_in_hand):
        for card,  in cards_in_hand.items():
            pass

    def ask_insurance():
        pass

    def raise_():
        pass

    def fold():
        pass

    def split():
        pass

    def hit():
        pass

    def stand():
        pass

    def double_down():
        pass

    def bust():
        pass

    # Game End
    def judge():
        pass

    def next():
        pass

    def bet():
        pass

    def stud():
        pass

    def fold():
        pass

    def push():
        pass

    def surrender():
        pass

if __name__ == "__main__":

    game = Blackjack()
