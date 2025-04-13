from dice import *
from game import *


dice_set = DiceSet(
    [Dice(weights=[100, 0, 0, 0, 0 ,0]), 
    Dice(weights=[100, 0, 0, 0, 0 ,0]), 
    Dice(weights=[100, 0, 0, 0, 0 ,0]), 
    Dice(weights=[100, 0, 0, 0, 0 ,0]), 
    Dice(), 
    Dice()])

roll = dice_set.roll_all()
combinations = get_scoring_combinations(roll)

print("Here are the faces")
print(f"{[face for face, addr in roll]}\n")

for dice, points in combinations:
    print(f"Combinations: {dice}, Points: {points}")
