from dice import Dice, DiceSet
from game import get_scoring_combinations


dice_set = DiceSet(
    [Dice(),
    Dice(),
    Dice(),
    Dice(),
    Dice(),
    Dice()])

roll = dice_set.roll_all()
combinations = get_scoring_combinations(roll)

print("Here are the faces")
print(f"{[face for face, addr in roll]}\n")

for dice, points in combinations:
    print(f"Combinations: {dice}, Points: {points}")

