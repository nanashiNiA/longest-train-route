import unittest
import sys
import os

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from graph import Graph
from simple_solver import SimpleLongestPathSolver

class TestSimpleLongestPathSolver(unittest.TestCase):

    def setUp(self):
        """テスト用のセットアップ"""
        self.graph = Graph()

    def test_simple_linear_graph(self):
        """線形グラフのテスト"""
        # 1 -- 2 -- 3 -- 4
        self.graph.add_edge(1, 2, 1.0)
        self.graph.add_edge(2, 3, 2.0)
        self.graph.add_edge(3, 4, 3.0)

        solver = SimpleLongestPathSolver(self.graph)
        path, distance = solver.find_longest_path()

        # 最長パスは 1-2-3-4 または 4-3-2-1
        self.assertEqual(len(path), 4)
        self.assertAlmostEqual(distance, 6.0)

    def test_example_from_problem(self):
        """問題例のテスト"""
        self.graph.add_edge(1, 2, 8.54)
        self.graph.add_edge(2, 3, 3.11)
        self.graph.add_edge(3, 1, 2.19)
        self.graph.add_edge(3, 4, 4.0)
        self.graph.add_edge(4, 1, 1.4)

        solver = SimpleLongestPathSolver(self.graph)
        path, distance = solver.find_longest_path()

        # 期待される最長パス: 1 → 2 → 3 → 4
        # 期待される距離: 8.54 + 3.11 + 4.0 = 15.65
        self.assertEqual(len(path), 4)
        self.assertAlmostEqual(distance, 15.65, places=2)

        # パスの順序を確認（始点は1、終点は4）
        self.assertEqual(path[0], 1)
        self.assertEqual(path[-1], 4)

    def test_single_vertex(self):
        """単一頂点のテスト"""
        # エッジがない場合
        solver = SimpleLongestPathSolver(self.graph)
        path, distance = solver.find_longest_path()

        self.assertEqual(len(path), 0)
        self.assertEqual(distance, 0.0)

    def test_cycle_graph(self):
        """環状グラフのテスト"""
        # 1 -- 2
        # |    |
        # 4 -- 3
        self.graph.add_edge(1, 2, 1.0)
        self.graph.add_edge(2, 3, 2.0)
        self.graph.add_edge(3, 4, 3.0)
        self.graph.add_edge(4, 1, 4.0)

        solver = SimpleLongestPathSolver(self.graph)
        path, distance = solver.find_longest_path()

        # サイクルなので3つのエッジを通るパスが最長
        self.assertEqual(len(path), 4)
        self.assertAlmostEqual(distance, 9.0)  # 4.0 + 3.0 + 2.0

if __name__ == '__main__':
    unittest.main()