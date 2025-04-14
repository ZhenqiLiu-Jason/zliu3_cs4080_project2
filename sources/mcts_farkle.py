from mcts.base.base import BaseState, BaseAction
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

        # Farkled
        if not scoring_combos:
            return []

        # HOT DICE: all dice were used
        used_ids = {die_id for _, die_id in scoring_combos[0][0]}
        is_hot_dice = len(used_ids) == len(self.combination)

        # Generate a list of actions and append a banking option
        actions = [FarkleAction(combo, points) for combo, points in scoring_combos]
        
        # You always roll after a hot dice
        if not is_hot_dice:
            actions.append(FarkleAction(None, scoring_combos[0][1]))

        return actions

    def take_action(self, action):
        combo = action.combo 
        points = action.points

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


class FarkleAction(BaseAction):
    def __init__(self, combo: Optional[List[Tuple[int, str]]], points: int):
        """
        combo: list of (face, die_id), or None to represent 'bank now'
        points: points earned from this action
        """
        self.combo = tuple(combo) if combo is not None else None
        self.points = points

    def __str__(self):
        if self.combo is None:
            return f"Bank({self.points})"
        else:
            lines = "\n".join(f"  {face} : {die_id}" for face, die_id in self.combo)
            return f"Combo(\n{lines}\nPoints: {self.points})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return isinstance(other, FarkleAction) and self.combo == other.combo and self.points == other.points

    def __hash__(self):
        return hash((self.combo, self.points))
