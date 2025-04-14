import argparse
import random
from mcts.searcher.mcts import MCTS

from dice import Dice, DiceSet
from mcts_farkle import FarkleState


def parse_single_weight(w_str):
    try:
        weights = list(map(float, w_str.split(",")))
        if len(weights) != 6:
            raise ValueError
        return weights
    except Exception:
        raise argparse.ArgumentTypeError("Each weight entry must be 6 comma-separated numbers (e.g., 1,1,1,1,1,5)")


def generate_dice_set(weights_list=None):
    dice_set = []
    weights_list = weights_list or []

    for i in range(6):
        if i < len(weights_list):
            die = Dice(weights=weights_list[i])
        else:
            die = Dice()  # Fair by default
        dice_set.append(die)

    return dice_set


def main():
    # CLI parsing
    parser = argparse.ArgumentParser(description="Run Farkle MCTS simulation with optional dice weights.")
    parser.add_argument("--time_limit", type=int, default=1000, help="MCTS time limit in ms")
    parser.add_argument("--weights", type=parse_single_weight, action='append',
                        help="Comma-separated weights for a die, can be repeated up to 6 times")

    args = parser.parse_args()

    # Automatically generate searcher name
    searcher_name = f"mcts-{args.time_limit}ms"
    searcher = MCTS(time_limit=args.time_limit)

    # Initialize game
    dice = generate_dice_set(args.weights)
    print(f"Using searcher: {searcher_name}")
    print("Dice Probabilities:")
    for i, die in enumerate(dice):
        print(f"Die {die.die_id}:")
        die.describe()

    initial_roll = [(die.roll(), die.die_id) for die in dice]
    state = FarkleState(dice_list=dice, combination=initial_roll)

    print(f"Initial roll: {[face for face, _ in initial_roll]}")
    turn = 0

    while not state.is_terminal():
        turn += 1
        possible_actions = state.get_possible_actions()
        print(f"\nTurn {turn}, {len(possible_actions)} possible actions")

        action = searcher.search(initial_state=state)
        print(f"Chosen action: {action}")

        state = state.take_action(action)

        if not state.is_terminal():
            print(f"New roll: {[face for face, _ in state.combination]}")
        else:
            print("Turn ended. Banked score:", state.get_reward())

    print("-" * 60)
    print(f"Final banked score after {turn} turns: {state.get_reward()}")


# Main execution
if __name__ == "__main__":
    main()
