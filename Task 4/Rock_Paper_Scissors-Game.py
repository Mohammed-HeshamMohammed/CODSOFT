import random

# Initializing scores
us_score = 0
pc_score = 0

print("\nWelcome!\n Let's Play Rock-Paper-Scissors! :D")

def game(us_ch):
    global us_score, pc_score  # Declareing global variables

    choices = ["rock", "paper", "scissors"]
    pc_ch = random.choice(choices)  # Get pc's choice

    # Displaying choices
    print(f"\nYou chose: {us_ch}\nComputer chose: {pc_ch}")

    # Determining result
    if us_ch == pc_ch:
        print("\nIt's a Draw!")
    elif (us_ch == "rock" and pc_ch == "scissors") or \
            (us_ch == "scissors" and pc_ch == "paper") or \
            (us_ch == "paper" and pc_ch == "rock"):
        print("\nNice!\nYou win!")
        us_score += 1  # Update user score
    else:
        pc_score += 1  # Update pc score
        print("\nOH!, you lose!\nBetter Luck Next Time :D")

    return pc_ch  # Return pc's choice for display

def normalizeinginputs(us_ch):
    """
    Normalize user inputs to match expected typos
    """
    us_ch = us_ch.lower().strip()
    choices = {
        "rock": ["rock", "roc", "r", "rok", "rocks", '1'],
        "paper": ["paper", "pap", "p", "pa", "papers", '2'],
        "scissors": ["scissors", "sciss", "s", "cissors", "siscors", '3'],
    }
    # Finding correct normalized input
    for choice, variations in choices.items():
        if us_ch in variations:
            return choice
    return None  # Return None if no valid input is found

def display_choice(choice, mirror=False):
    """
    Return ASCII art for the given choice.
    for fun :D
    If mirror=True, return the mirrored version for the computer.
    """
    if choice == "rock":
        if mirror:
            return """\
      _______
     (____   '---
    (_____)
    (_____)
     (____)
      (___'__.---
"""
        else:
            return """\
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""
    elif choice == "paper":
        if mirror:
            return """\
      _______
 ____(___    '---
(______
(_______
 (_______
    (__________.---
"""
        else:
            return """\
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
"""
    elif choice == "scissors":
        if mirror:
            return """\
      _______
 ____(___    '---
(______
 (__________
    (____)
      (___'__.---
"""
        else:
            return """\
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""
    return ""

#Game's Main loop
while True:
    print("\nPick one: Rock, Paper, or Scissors")
    us_ch = input("Your choice: ")

    # Normalized user's input
    normalized_ch = normalizeinginputs(us_ch)

    # Handle invalid choices
    if normalized_ch is None:
        print("Invalid choice.")
        continue

    # Getting pc's choice
    pc_ch = game(normalized_ch)

    # Getting ASCII art for both choices
    us_art = display_choice(normalized_ch)
    pc_art = display_choice(pc_ch, mirror=True)

    # Printing choices side by side
    print("\nYour choice vs Computer's choice:\n")
    print(us_art + "\n    vs    \n" + pc_art)

    # Displaying current score
    print(f"\nScore: You -> {us_score}, Computer -> {pc_score}")

    # Ask if user wants to play again
    play_again = input("\nDo you want to play again? (yes/no): ").lower()
    if play_again not in ('yes', 'y', 'ye', 'ys', 'es', 'yeah', 'yep', 'yess'):
        break  # Exit the game loop if user does not want to play again

print("Thank you for playing! :D")
