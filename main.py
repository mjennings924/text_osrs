import random
import json # for saving data
import os

def xp_for_level(level):
    return level * level * 100

def save_game():
    data = {
        "skills": skills,
        "health": health,
        "inventory": inventory,
        "bank": bank
    }
    with open(f"{username}.json", "w") as f:
        json.dump(data, f)
    print("Game saved.")

def load_game():
    global skills, health, inventory, bank
    with open(f"{username}.json", "r") as f:
        data = json.load(f)
        skills = data["skills"]
        health = data["health"]
        inventory = data["inventory"]
        bank = data["bank"]
    print("Game loaded")

username = input("Enter your username: ")

if os.path.exists(f"{username}.json"):
    choice = input("Load existing character? (y/n): ").lower()
else:
    choice = "n"

skills = {
    "Attack": {"level": 1, "xp": 0},
    "Mining": {"level": 1, "xp": 0},
    "Fishing": {"level": 1, "xp": 0},
    "Woodcutting": {"level": 1, "xp": 0},
}

health = 100
inventory = {}
bank = {}

if choice == "y":
    load_game()
else:
    print(f"Welcome to Gielinor, {username}")

def show_stats():
    print("\n=== STATS ===")
    print(f"Health: {health}")
    for s, d in skills.items():
        print(f"{s}: Level {d['level']} ({d['xp']} XP)")
    print("=============\n")

def show_inventory():
    print("\n=== INVENTORY ===")
    if not inventory:
        print("Empty")
    for item, qty in inventory.items():
        print(f"{item} x{qty}")
    print("=================\n")

def show_bank():
    print("\n=== BANK ===")
    if not bank:
        print("Empty")
    for item, qty in bank.items():
        print(f"{item} x{qty}")
    print("=============\n")

def add_item(container, item, amount=1):
    container[item] = container.get(item, 0) + amount

def add_xp(skill, amount):
    data = skills[skill]
    data["xp"] += amount
    print(f"+{amount} XP in {skill}")

    while data["level"] < 99 and data["xp"] >= xp_for_level(data["level"] + 1):
        data["level"] += 1
        print(f"{skill} level up! ({data['level']})")

def mine():
    print("You mine some ore...")
    add_item(inventory, "Copper ore")
    add_xp("Mining", 25)

def fish():
    print("You catch a fish.")
    add_item(inventory, "Raw shrimp")
    add_xp("Fishing", 25)

def chop():
    print("You chop some logs...")
    add_item(inventory, "Logs")
    add_xp("Woodcutting", 25)

def attack():
    global health
    print("You fight a goblin.")
    if random.random < 0.6:
        print("You default the goblin")
        add_item(inventory, "Bones")
        add_xp("Attack", 40)
    else:
        dmg = random.randint(1, 5)
        health -= dmg
        print(f"You take {dmg} damage.")
        if health <= 0:
            print("You died. Game over.")
            save_game()
            exit()

def deposit(item, qty):
    if inventory.get(item, 0) >= qty:
        inventory[item] -= qty
        add_item(bank, item, qty)
        if inventory[item] == 0:
            del inventory[item]
        print(f"Deposited {qty} {item}")
    else:
        print("Not enough items")

def withdraw(item, qty):
    if bank.get(item, 0) >= qty:
        bank[item] -= qty
        add_item(inventory, item, qty)
        if bank[item] == 0:
            del bank[item]
        print(f"Withdraw {qty} {item}")
    else:
        print("Not enough items in bank")

print("Type 'help' for commands.")

while True:
    cmd = input("> ").lower().split()

    if not cmd:
        continue

    if cmd[0] == "help":
        print("""
Commands:
stats
inv
bank
mine | fish | chop | attack
deposit <item> <qty>
withdraw <item> <qty>
save
quit
""")
        
    elif cmd[0] == "stats":
        show_stats()

    elif cmd[0] == "inv":
        show_inventory()
    
    elif cmd[0] == "bank":
        show_bank()
    
    elif cmd[0] == "mine":
        mine()
    
    elif cmd[0] == "fish":
        fish()

    elif cmd[0] == "attack":
        attack()

    elif cmd[0] == "deposit" and len(cmd) == 3:
        deposit(cmd[1], int(cmd[2]))

    elif cmd[0] == "save":
        save_game()

    elif cmd[0] == "quit":
        save_game()
        print("Goodbye")
        break

    else:
        print("Unknown command.")