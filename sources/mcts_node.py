import math
import random
from typing import List, Tuple, Optional, Dict, Any
from collections import defaultdict, Counter

from dice import Dice, DiceSet

class MCTSNode:
    def __init__(
        self,
        state: List[Tuple[int, str]],  # Each element is (face, die_id)
        remaining_dice: List[str],     # List of die_ids still available
        current_bank: int,
        parent: Optional['MCTSNode'] = None,
        taken_combination: Optional[List[Tuple[int, str]]] = None
    ):
        self.state = state
        self.remaining_dice = remaining_dice
        self.current_bank = current_bank
        self.parent = parent
        self.taken_combination = taken_combination  # The scoring combo that led here

        self.children: List[MCTSNode] = []
        self.visits = 0
        self.total_reward = 0.0

        self.untried_combinations: List[List[Tuple[int, str]]] = []  # To be filled later

    def is_fully_expanded(self) -> bool:
        return len(self.untried_combinations) == 0

    def best_child(self, c_param=math.sqrt(2)) -> 'MCTSNode':
        # Use UCB1 formula to select best child
        choices_weights = [
            (child.total_reward / child.visits) +
            c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def expand(self, scoring_func) -> Optional['MCTSNode']:
        if not self.untried_combinations:
            return None

        combo = self.untried_combinations.pop()
        combo_score = scoring_func(combo)

        # Remove used dice
        used_ids = set(die_id for _, die_id in combo)
        new_remaining = [d for d in self.remaining_dice if d not in used_ids]

        child = MCTSNode(
            state=combo,
            remaining_dice=new_remaining,
            current_bank=self.current_bank + combo_score,
            parent=self,
            taken_combination=combo
        )
        self.children.append(child)
        return child

    def rollout(self, dice_lookup: Dict[str, Any], combination_func) -> int:
        current_score = self.current_bank
        remaining_dice_ids = list(self.remaining_dice)  # Work on a copy

        while remaining_dice_ids:
            dice_set = DiceSet([dice_lookup[die_id] for die_id in remaining_dice_ids])
            faces = dice_set.roll_all()

            combos = combination_func(faces)
            if not combos:
                return 0  # Farkle

            # Greedy approach
            best_combo, points = combos[0]
            current_score += points

            used_ids = {die_id for _, die_id in best_combo}
            remaining_dice_ids = [die_id for die_id in remaining_dice_ids if die_id not in used_ids]

            # Hot dice
            if not remaining_dice_ids:
                remaining_dice_ids = list(dice_lookup.keys())

        return current_score

    def update(self, reward: float):
        self.visits += 1
        self.total_reward += reward

    def is_terminal(self) -> bool:
        return len(self.remaining_dice) == 0

    def fully_qualified_state(self) -> Tuple:
        return (tuple(sorted(self.state)), tuple(sorted(self.remaining_dice)), self.current_bank)

    def __repr__(self):
        return f"<MCTSNode visits={self.visits} reward={self.total_reward:.2f} bank={self.current_bank} remaining={len(self.remaining_dice)}>"]

