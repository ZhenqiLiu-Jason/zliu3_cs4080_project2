from mcts.searcher.mcts import MCTS

from dice import Dice, DiceSet
from mcts_farkle import FarkleState

dice_list = [Dice() for _ in range(6)]
dice_set = DiceSet(dice_list)

initial_roll = dice_set.roll_all()

# Create initial state
initial_state = FarkleState(
    dice_list=dice_list,
    combination=initial_roll,
    bank=0,
    terminal=False
)

# Run MCTS to pick best action
mcts = MCTS(iteration_limit=10000)
best_action = mcts.search(initial_state)

# Show result
print("Initial roll:", [face for face, _ in initial_roll])
print("Best action chosen:", best_action)
