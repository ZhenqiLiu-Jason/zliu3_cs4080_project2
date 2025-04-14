from typing import Callable, Dict, Any
from mcts_node import MCTSNode

class MCTS:
    def __init__(self, root: MCTSNode, dice_lookup: Dict[str, Any], scoring_func, combination_func):
        self.root = root
        self.dice_lookup = dice_lookup
        self.scoring_func = scoring_func
        self.combination_func = combination_func

    def run_search(self, iterations=1000):
        if not self.root.untried_combinations:
            self.root.untried_combinations = [
                combo for combo, _ in self.combination_func(self.root.state)
            ]

        for _ in range(iterations):
            node = self.tree_policy()
            reward = node.rollout(self.dice_lookup, self.combination_func)
            self.backpropagate(node, reward)

    def tree_policy(self) -> MCTSNode:
        node = self.root
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return node.expand(scoring_func=self.scoring_func)
            node = node.best_child()
        return node

    def backpropagate(self, node: MCTSNode, reward: float):
        while node is not None:
            node.update(reward)
            node = node.parent

    def best_action(self) -> Optional[MCTSNode]:
        # Greedy choice at end of search
        return self.root.best_child(c_param=0)
