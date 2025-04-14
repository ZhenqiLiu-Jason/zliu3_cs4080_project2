import argparse
import random
from mcts.searcher.mcts import MCTS

from dice import Dice, DiceSet
from mcts_farkle import FarkleState


def generate_dice_set():
    return [Dice() for _ in range(6)]

def main():
    # CLI parsing
    parser = argparse.ArgumentParser(description="Run Farkle MCTS simulation.")
    parser.add_argument("--time_limit", type=int, default=1000, help="Time limit for MCTS searcher in ms")
    args = parser.parse_args()

    # Automatically generate searcher name
    searcher_name = f"mcts-{args.time_limit}ms"
    searcher = MCTS(time_limit=args.time_limit)

    # Initialize game
    dice = generate_dice_set()
    initial_roll = [(die.roll(), die.die_id) for die in dice]
    state = FarkleState(dice_list=dice, combination=initial_roll)

    print(f"Initial roll: {[face for face, _ in initial_roll]}")
    print(f"Using searcher: {searcher_name}")
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
