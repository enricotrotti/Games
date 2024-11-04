import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100  # max health, increased after defeating monsters
        self.energy = 50
        self.potion_count = 0  # count of healing potions
        self.antidote_count = 0  # count of antidote potions
        self.poisoned_turns = 0  # tracks remaining poison effect

    def attack(self):
        damage = random.randint(10, 20)
        return damage

    def heal(self):
        if self.potion_count > 0:
            self.health = min(self.max_health, self.health + 30)  # health cannot exceed max health
            self.potion_count -= 1
            print(f"{self.name} used a healing potion and gained 30 health points! Healing potions left: {self.potion_count}")
        else:
            print("You don't have any healing potions left!")

    def use_antidote(self):
        if self.antidote_count > 0 and self.poisoned_turns > 0:
            self.poisoned_turns = 0
            self.antidote_count -= 1
            print(f"{self.name} used an antidote potion and cured the poison! Antidotes left: {self.antidote_count}")
        else:
            print("Or you don't have antidotes or are not poisoned.")

    def apply_poison(self):
        if self.poisoned_turns > 0:
            self.health -= 10
            self.poisoned_turns -= 1
            print(f"{self.name} is poisoned! They lose 10 health points. Remaining health: {self.health}")

class Monster:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage

class Dungeon:
    def __init__(self):
        self.monsters = [
            Monster("Pixie", 30, 10),
            Monster("Troll", 50, 15),
            Monster("Gargoyle", 40, 20),
            Monster("Basilisk", 80, 25)
        ]
        self.traps = [
            "Fire Trap", "Snake trap", "Cursed Potion", "Poison Trap"
        ]

    def explore(self, player, floor):
        print(f"\nYou have entered Floor {floor + 1}")
        
        player.apply_poison() # apply poison damage if the player is poisoned

        event = random.choice(["monster", "trap", "item", "nothing"])

        if event == "monster":
            monster = random.choice(self.monsters)
            print(f"A {monster.name} has appeared! It has {monster.health} health points and deals {monster.damage} damage.")
            combat(player, monster)

        elif event == "trap":
            trap = random.choice(self.traps)
            if trap == "Poison Trap":
                player.poisoned_turns = 2  # poison lasts for 2 turns (= floors)
                print(f"You triggered a {trap}! You are poisoned and will lose 10 health each floor for 2 floors.")
            else:
                damage = random.randint(10, 30)
                player.health -= damage
                print(f"You triggered a {trap} and lost {damage} health points!")

        elif event == "item":
            item_found = random.choice(["healing_potion", "antidote_potion"])
            if item_found == "healing_potion":
                print("You found a healing potion!")
                player.potion_count += 1
                print(f"Healing potions in inventory: {player.potion_count}")
            else:
                print("You found an antidote potion!")
                player.antidote_count += 1
                print(f"Antidotes in inventory: {player.antidote_count}")

        else:
            print("There's nothing in this room...")

def combat(player, monster):
    while monster.health > 0 and player.health > 0:
        action = input("What do you want to do? (attack, heal, antidote, run): ").lower()
        
        if action == "attack":
            player_damage = player.attack()
            monster.health -= player_damage
            print(f"You dealt {player_damage} damage to the {monster.name}. Monster's remaining health: {monster.health}")
            
        elif action == "heal":
            player.heal()
        
        elif action == "antidote":
            player.use_antidote()
        
        elif action == "run":
            if random.random() < 0.5:  # 50% chance to fail
                print("You failed to escape, and the monster attacks you!")
                player.health -= monster.damage
                print(f"Damage taken: {monster.damage}. Remaining health: {player.health}")
            else:
                print("You successfully ran away from the monster!")
                return  # end combat if run is successful

        if monster.health > 0:
            player.health -= monster.damage
            print(f"The {monster.name} attacked you! Damage taken: {monster.damage}. Remaining health: {player.health}")

    if player.health <= 0:
        print("You were defeated by the monster...")
    else:
        print(f"You defeated the {monster.name}!")
        player.max_health += 5
        print(f"{player.name}'s maximum health increased by 5! New max health: {player.max_health}")

def game():
    print("Welcome to the Endless Dungeon!")
    name = input("Enter your wizard name: ")
    player = Player(name)
    dungeon = Dungeon()

    # loop through 100 floors
    for floor in range(100):
        print(f"\n>>> You are about to explore Floor {floor + 1} <<<")
        
        # wait for player to press enter to continue
        input("Press Enter to explore the floor...")

        dungeon.explore(player, floor)

        if player.health <= 0:
            print("You have been defeated. Game over.")
            break

        # check if the player has completed all 100 floors
        if floor == 99:
            print(f"Congratulations, {player.name}! You completed all 100 floors!")
            break

game()
