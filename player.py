class Player:

    def __init__(self, id_, money=100, init_stake=5):
        self.id = id_
        self.stake = init_stake
        self.money = money
        self.hands = []
        self.fold = False
        self.double = False
        self.insurance = False
        self._5_card_charlie = False
        self.result = ""

    def print_cards(self):
        print(f"Player {self.id}:")
        for card in self.hands:
            print(f"{card.symbol} {card.suit} ", end="")
        print()

    def print_money(self):
        print(f"Player {self.id} has {self.money}")

    def print_result(self):
        print(f"Player {self.id} result is {self.result}")

    def print_status(self):
        print(f"Player {self.id} has:")
        print(f"money: {self.money} ", end="")
        print(f"stake: {self.stake} ", end="")
        print(f"cards: ", end="")
        for card in self.hands:
            print(f"{card.symbol} {card.suit} ", end="")
        print()

class Players:

    def __init__(self, player_num):
        self.player_num = player_num
        self.in_ = self.create(self.player_num)
        self.out = []

    # Create Player
    def create(self, player_num):
        in_game = []
        for id_ in range(player_num):
            player = Player(id_=id_)
            in_game.append(player)
        return in_game

    # Reset Player
    def reset_all(self, min_bet):

        self.enter()
        self.set_stake(min_bet)
        self.reset_result()
        self.reset_double()
        self.reset_fold()
        self.reset_insurance()
        self.reset_cards()

    # Enter table
    def enter(self):

        while self.out:
            self.in_.append(self.out.pop())
        self.in_.sort(key=lambda x: x.id)

    # Set stake
    def set_stake(self, min_bet):

        for player in self.in_:

            while True:
                # player.stake = int(input("How much money do you want to bet?"))

                # Check Player stake
                if player.stake >= player.money:
                    player.stake = player.money
                    print("All in")

                if player.stake < min_bet:
                    print(f"At least {min_bet} dollar")
                    continue
                break

    # Reset Result
    def reset_result(self):

        for player in self.in_:
            player.result = ""

    # Reset Double
    def reset_double(self):

        for player in self.in_:
            player.double = False

    # Reset Fold
    def reset_fold(self):

        for player in self.in_:
            player.fold = False

    # Reset Insurance
    def reset_insurance(self):

        for player in self.in_:
            player.insurance = False

    # Reset 5 Card Charlie
    def reset_charlie(self):

        for player in self.in_:
            player._5_card_charlie = False

    # Reset Cards in hand
    def reset_cards(self):

        # Reset Player
        for player in self.in_:
            player.hands = []

    # People who win or lose
    def leave_game(self):

        out_game = []
        # out_game = filter(lambda x: x.result != "")
        for player in self.in_:

            if player.result != "":
                out_game.append(player.id)

        while out_game:
            out_player_id = out_game.pop()
            pick_id = 0
            for num in range(len(self.in_)):
                if self.in_[num].id == out_player_id:
                    pick_id = num
                    break
            out_game_player = self.in_.pop(pick_id)
            self.out.append(out_game_player)

    # Print Players Cards
    def print_all_cards(self):

        for player in self.in_:
            player.print_cards()

    # Print Players Moneys
    def print_all_money(self):

        for player in self.in_:
            player.print_money()

    # Print Players Status
    def print_all_status(self):

        for player in self.in_:
            player.print_status()

    # Print Players Result
    def print_all_result(self):

        for player in self.in_:
            player.print_result()
