import random

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.balance = 1500  # starting balance
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0

    def move(self, steps, board):
        if not self.in_jail:
            self.position = (self.position + steps) % len(board) # if new position > board's length-> back to the beginning
            slot = board[self.position]
            print(f"{self.name} moves to {slot.name}.")
            slot.action(self)
        else:
            self.handle_jail()

    def pay(self, amount):
        self.balance -= amount

    def receive(self, amount):
        self.balance += amount
    
    def add_get_out_of_jail_card(self):
        print(f"{self.name} received a Get Out of Jail Free card!")

    def receive_rent_discount(self, discount):
        print(f"{self.name} received a {discount}/100 discount on the next rent!")

    def go_to_jail(self):
        self.in_jail = True
        self.jail_turns = 0

    def handle_jail(self):
        print(f"{self.name} is in jail (Turn {self.jail_turns + 1} of 3)")
        choice = input(f"{self.name}, do you want to Pay 50 Euro to get out of jail or try with Dice? (p/d): ")
        if choice.lower() == 'p' and self.balance >= 50:
            self.balance -= 50
            self.in_jail = False
            self.jail_turns = 0
            print(f"{self.name} paid 50 Euro and now is free.")
        else:
            dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
            print(f"{self.name} rolls the dice and gets {dice1} and {dice2}.")
            if dice1 == dice2:
                self.in_jail = False
                self.jail_turns = 0
                print(f"{self.name} rolled a double and is now free!")
                self.move(dice1 + dice2, game.board) 
            else:
                self.jail_turns += 1
                if self.jail_turns >= 3:
                    self.balance -= 50
                    self.in_jail = False
                    self.jail_turns = 0
                    print(f"{self.name} waited all turns and pays 50 Euro to get out.")

class Slot:
    def __init__(self, name):
        self.name = name

    def action(self, player):
        print(f"{player.name} is on {self.name}. No specific action.")

class Property(Slot):
    def __init__(self, name, cost, rent):
        super().__init__(name)
        self.cost = cost
        self.rent = rent
        self.owner = None

    def action(self, player):
        if self.owner is None:
            if player.balance >= self.cost:
                choice = input(f"{player.name}, do you want to spend {self.cost} Euro to buy {self.name}? (y/n): ")
                if choice.lower() == 'y':
                    player.balance -= self.cost
                    self.owner = player
                    player.properties.append(self)
                    print(f"{player.name} bought {self.name} for {self.cost} Euro.")
                else:
                    print(f"{player.name} decided not to buy {self.name}.")
            else:
                print(f"{player.name} does not have enough money to buy {self.name}.")
        elif self.owner != player:
            player.balance -= self.rent
            self.owner.balance += self.rent
            print(f"{player.name} pays {self.rent} Euro rent to {self.owner.name} for being on {self.name}.")
        else:
            print(f"{player.name} is on their own property {self.name}.")

class FreeParking(Slot):
    def action(self, player):
        if game.jackpot > 0:
            print(f"{player.name} found {game.jackpot} Euro in Free Parking!")
            player.balance += game.jackpot
            game.jackpot = 0
        else:
            print(f"{player.name} is resting in Free Parking. No extra funds available.")

class SpecialSlot(Slot):
    def __init__(self, name, type):
        super().__init__(name)
        self.type = type

    def action(self, player):
        if self.type == "Jail":
            player.in_jail = True
            print(f"{player.name} goes to jail!")
        elif self.type == "Start":
            player.balance += 200
            print(f"{player.name} passes Go and collects 200 Euro!")
        else:
            print(f"{player.name} is on {self.name}.")
class TaxSlot(SpecialSlot):
    def __init__(self, name, tax_amount):
        super().__init__(name, "Tax")
        self.tax_amount = tax_amount

    def action(self, player):
        player.pay(self.tax_amount)
        print(f"{player.name} paid {self.tax_amount} Euro in taxes at {self.name}.")

class Card:
    def __init__(self, description, effect):
        self.description = description
        self.effect = effect

    def apply(self, player):
        print(f"Card: {self.description}")
        self.effect(player)

def create_chance_cards():
    return [
        Card("Pay 100 Euro in taxes", lambda player: player.pay(100)),
        Card("Go to jail without passing from the Start", lambda player: player.go_to_jail()),
        Card("Receive 200 Euro from an inheritance", lambda player: player.receive(200)),
    ]

def create_community_chest_cards():
    return [
        Card("Get Out of Jail Free (to keep)", lambda player: player.add_get_out_of_jail_card()),
        Card("Get a 50/100 of discount on next rent", lambda player: player.receive_rent_discount(50)),
        Card("Move forward 3 slots", lambda player: player.move(3, game.board)),
        Card("Double the Free Parking jackpot!", lambda player: game.double_jackpot()),
        Card("All players pay 25 Euro to Free Parking", lambda player: game.community_fund_tax(25))
    ]

class CardSlot(Slot):
    def __init__(self, name, type, card_deck):
        super().__init__(name)
        self.type = type
        self.card_deck = card_deck

    def action(self, player):
        card = random.choice(self.card_deck)
        card.apply(player)

class MonopolyGame:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.chance_cards = create_chance_cards()
        self.community_chest_cards = create_community_chest_cards()
        self.board = [
            SpecialSlot("Inizio", "Start"),
            Property("Vicolo Corto", 60, 2),
            CardSlot("Probabilità", "Chance", self.chance_cards),
            Property("Vicolo Stretto", 60, 4),
            TaxSlot("Tassa patrimoniale", 200),
            Property("Bastioni Gran Sasso", 100, 6),
            CardSlot("Imprevisti", "Community Chest", self.community_chest_cards),
            Property("Viale Monterosa", 100, 6),
            Property("Viale Vesuvio", 120, 8),
            SpecialSlot("Prigione", "Jail"),
            Property("Via Accademia", 140, 10),
            Property("Corso Ateneo", 140, 10),
            Property("Piazza Università", 160, 12),
            Property("Via Verdi", 180, 14),
            CardSlot("Probabilità", "Chance", self.chance_cards),
            Property("Corso Raffaello", 180, 14),
            Property("Piazza Dante", 200, 16),
            FreeParking("Parcheggio Gratuito"),
            Property("Via Marco Polo", 220, 18),
            CardSlot("Imprevisti", "Community Chest", self.community_chest_cards),
            Property("Corso Magellano", 220, 18),
            Property("Largo Colombo", 240, 20),
            Property("Viale Costantino", 260, 22),
            Property("Viale Traiano", 260, 22),
            Property("Piazza Giulio Cesare", 280, 24),
            Property("Via Roma", 300, 26),
            Property("Corso Impero", 300, 26),
            CardSlot("Probabilità", "Chance", self.chance_cards),
            Property("Largo Augusto", 320, 28),
            CardSlot("Imprevisti", "Community Chest", self.community_chest_cards),
            Property("Viale dei Giardini", 350, 35),
            TaxSlot("Tassa di lusso", 100),
            Property("Parco della Vittoria", 400, 50),
        ]
        self.turn = 0
        self.jackpot = 0

    def increase_jackpot(self, amount):
        self.jackpot += amount
        print(f"The Free Parking jackpot has increased by {amount} Euro.")

    def double_jackpot(self):
        self.jackpot *= 2
        print("The Free Parking jackpot has been doubled!")

    def community_fund_tax(self, amount):
        for player in self.players:
            if player.balance >= amount:
                player.balance -= amount
                self.jackpot += amount
        print(f"All players have contributed ${amount} to the Free Parking jackpot!")

    def play_turn(self):
        player = self.players[self.turn]
        print(f"\nIt's {player.name}'s turn. Balance: ${player.balance}")
        input("Press Enter to roll the dice...")
        steps = random.randint(1, 6) + random.randint(1, 6)
        print(f"{player.name} rolled the dice and got {steps}.")
        player.move(steps, self.board)

        # next player's turn
        self.turn = (self.turn + 1) % len(self.players)

    def game_over(self):
        # end game if only one player has money left
        active_players = [p for p in self.players if p.balance > 0]
        return len(active_players) == 1

    def start_game(self):
        print("Welcome to Monopoly!")
        while not self.game_over():
            self.play_turn()

        winner = [p for p in self.players if p.balance > 0][0]
        print(f"The game is over! The winner is {winner.name} with a balance of ${winner.balance}!")

player_names = ["Alice", "Bob", "Charlie"]
game = MonopolyGame(player_names)
game.start_game()
