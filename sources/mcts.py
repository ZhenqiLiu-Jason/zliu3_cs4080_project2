import time
from typing import Callable, Dict, Any
from mcts_node import MCTSNode

class MCTS:
    def __init__(
        self,
        root: MCTSNode,
        dice_lookup: Dict[str, Any],
        combination_func: Callable,  # get_scoring_combinations
        scoring_func: Callable,      # score_combination
        time_limit: float = 1.0
    ):
        self.root = root
        self.dice_lookup = dice_lookup
        self.combination_func = combination_func
        self.scoring_func = scoring_func
        self.time_limit = time_limit

    def run(self):
        start_time = time.time()
        while time.time() - start_time < self.time_limit:
            node = self.select(self.root)
            reward = node.rollout(self.dice_lookup, self.combination_func)
            self.backpropagate(node, reward)

    def select(self, node: MCTSNode) -> MCTSNode:
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return node.expand(scoring_func=self.scoring_func)
            else:
                node = node.best_child()
        return node

    def backpropagate(self, node: MCTSNode, reward: float):
        while node is not None:
            node.update(reward)
            node = node.parent

    def best_action(self) -> MCTSNode:
        return max(self.root.children, key=lambda n: n.visits, default=None)

