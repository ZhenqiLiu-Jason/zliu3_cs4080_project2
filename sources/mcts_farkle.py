from mcts.base.base import BaseState
from typing import List, Tuple, Dict, Optional, Any

from dice import Dice, DiceSet
from game import score_combination, get_scoring_combinations

class FarkleState(BaseState):
    def __init__(
        self,
        dice_list: List[Dice],
        combination: List[Tuple[int, str]],
        bank: int = 0,
        terminal: bool = False,
    ):
        self.dice_lookup = {die.die_id: die for die in dice_list}
        self.combination = combination  # this is the roll for this state
        self.bank = bank
        self.terminal = terminal

    def get_current_player(self) -> int:
        return 1  # Always maximizer for single-player Farkle

    def get_possible_actions(self):
        if self.terminal:
            return []

        scoring_combos = get_scoring_combinations(self.combination)
        return scoring_combos + [(None, scoring_combos[0][1])]

    def take_action(self, action):
        combo, points = action

        # Bank now (stop the turn and keep the bank)
        if combo is None:
            return FarkleState(
                dice_list=list(self.dice_lookup.values()),
                combination=[],  # No more dice to roll
                bank=self.bank + points,
                terminal=True
            )

        # Remove used dice
        used_ids = {die_id for _, die_id in combo}
        remaining_ids = [die_id for (_, die_id) in self.combination if die_id not in used_ids]

        # Hot dice: if all dice were used, reroll all
        if not remaining_ids:
            remaining_ids = list(self.dice_lookup.keys())

        # Reroll the remaining dice
        dice_set = DiceSet([self.dice_lookup[die_id] for die_id in remaining_ids])
        new_combination = dice_set.roll_all()

        # Check if Farkle (no scoring options)
        if not get_scoring_combinations(new_combination):
            return FarkleState(
                dice_list=list(self.dice_lookup.values()),
                combination=new_combination,
                bank=0,  # lose all banked points
                terminal=True
            )

        # Not terminal: continue playing
        return FarkleState(
            dice_list=list(self.dice_lookup.values()),
            combination=new_combination,
            bank=self.bank + points,
            terminal=False
        )

    def is_terminal(self) -> bool:
        return self.terminal

    def get_reward(self) -> float:
        return self.bank
