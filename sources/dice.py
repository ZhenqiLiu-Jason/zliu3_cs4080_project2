import random

class Dice:
    """
    This Dice class represents a dice, which can take up any faces and weights.
    """

    def __init__(self, faces=(1,2,3,4,5,6), weights=None):
        """
        Create a dice with custom faces and weights.
        Default is a fair 6-faced dice.
        """
        self.faces = faces
        self.weights = weights or [1] * len(faces)

    def roll(self):
        return random.choices(self.faces, weights=self.weights, k=1)[0]

    def probability_map(self):
        """
        Returns a dictionary mapping each face to its probability.
        """
        total = sum(self.weights)
        return {face: w / total for face, w in zip(self.faces, self.weights)}

    def describe(self):
        """
        Prints a human-readable summary of the die's faces and bias.
        """
        for face, prob in self.probability_map().items():
            print(f"  Face {face}: {prob:.2%} probability")


class DiceSet:
    """
    Represents DiceSet object that can holds a list of 
    Dice objects and rolls all of them.
    """
    def __init__(self, dice_list):
        self.dice = dice_list

    def roll_all(self):
        return [(die.roll(), die) for die in self.dice]

