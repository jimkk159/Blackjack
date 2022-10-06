import random
suits = ["spade", "heart", "diamond", "club"]
poker_symbol = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
poker_value_dict = {"A": 11, "K": 10, "Q": 10, "J": 10, "10": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5,
                    "4": 4, "3": 3, "2": 2}


class Card:

    def __init__(self, symbol, suit, faced=True):
        # self.id = id_
        self.symbol = symbol
        self.suit = suit
        self.value = poker_value_dict[symbol]
        self.faced = faced


class Deck:

    def __init__(self, deck_num):
        self.deck_num = deck_num
        self.deck = self.create_muti_deck(self.deck_num)

    def create_single_deck(self):
        return [Card(symbol, suit) for symbol in poker_symbol for suit in suits]

    def create_muti_deck(self, deck_num):
        deck = []
        for _ in range(deck_num):
            deck += [Card(symbol, suit) for symbol in poker_symbol for suit in suits]
        return deck

    def print_deck(self):

        count = 0
        for card in self.deck:

            print(card.suit, card.symbol, " ", end="")
            count += 1
            if count == 4:
                print()
                count = 0

    def shuffle(self):
        random.shuffle(self.deck)

    def reset_deck(self):

        self.deck = self.create_muti_deck(self.deck_num)
        self.shuffle()

    def check_deck_num(self):

        if len(self.deck) <= self.deck_num * 52 / 2:
            return True
        return False
