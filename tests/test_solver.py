import unittest
import sys
import os

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from graph import Graph
from solver import LongestPathSolver

class TestLongestPathSolver(unittest.TestCase):

    def setUp(self):
        """テスト用のセットアップ"""
        self.graph = Graph()

    def test_simple_linear_graph(self):
        """線形グラフのテスト"""
        # 1 -- 2 -- 3 -- 4
        self.graph.add_edge(1, 2, 1.0)
        self.graph.add_edge(2, 3, 2.0)
        self.graph.add_edge(3, 4, 3.0)

        solver = LongestPathSolver(self.graph)
        path, distance = solver.find_longest_path()

        # 最長パスは 1-2-3-4 または 4-3-2-1
        self.assertEqual(len(path), 4)
        self.assertAlmostEqual(distance, 6.0)

    def test_cycle_graph(self):
        """環状グラフのテスト"""
        # 1 -- 2
        # |    |
        # 4 -- 3
        self.graph.add_edge(1, 2, 1.0)
        self.graph.add_edge(2, 3, 2.0)
        self.graph.add_edge(3, 4, 3.0)
        self.graph.add_edge(4, 1, 4.0)

        solver = LongestPathSolver(self.graph)
        path, distance = solver.find_longest_path()

        # サイクルなので3つのエッジを通るパスが最長
        self.assertEqual(len(path), 4)
        self.assertAlmostEqual(distance, 9.0)  # 4.0 + 3.0 + 2.0

    def test_example_from_problem(self):
        """問題例のテスト"""
        self.graph.add_edge(1, 2, 8.54)
        self.graph.add_edge(2, 3, 3.11)
        self.graph.add_edge(3, 1, 2.19)
        self.graph.add_edge(3, 4, 4.0)
        self.graph.add_edge(4, 1, 1.4)

        solver = LongestPathSolver(self.graph)
        path, distance = solver.find_longest_path()

        # パスの長さとおおよその距離を確認
        self.assertTrue(len(path) >= 3)
        self.assertTrue(distance > 10.0)

    def test_single_vertex(self):
        """単一頂点のテスト"""
        # エッジがない場合
        solver = LongestPathSolver(self.graph)
        path, distance = solver.find_longest_path()

        self.assertEqual(len(path), 0)
        self.assertEqual(distance, 0.0)

    def test_disconnected_graph(self):
        """非連結グラフのテスト"""
        # 1 -- 2    3 -- 4
        self.graph.add_edge(1, 2, 1.0)
        self.graph.add_edge(3, 4, 2.0)

        solver = LongestPathSolver(self.graph)
        path, distance = solver.find_longest_path()

        # 各連結成分で最長パスを探索
        self.assertTrue(len(path) >= 2)
        self.assertTrue(distance > 0.0)

if __name__ == '__main__':
    unittest.main()