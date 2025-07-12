"""
シンプルな最長パス探索ソルバー
採用試験用の基本実装
"""

from graph import Graph

class SimpleLongestPathSolver:
    """シンプルな最長パス探索ソルバー"""

    def __init__(self, graph: Graph):
        self.graph = graph
        self.vertices = graph.get_all_vertices()

    def find_longest_path(self):
        """最長パスを探索"""
        if not self.vertices:
            return [], 0.0

        max_distance = 0.0
        longest_path = []

        # すべての頂点を始点として探索
        for start_vertex in self.vertices:
            path, distance = self._dfs(start_vertex, set(), 0.0, [start_vertex])
            if distance > max_distance:
                max_distance = distance
                longest_path = path.copy()

        return longest_path, max_distance

    def _dfs(self, current_vertex, visited, current_distance, current_path):
        """深さ優先探索"""
        visited.add(current_vertex)
        max_distance = current_distance
        best_path = current_path.copy()

        # 隣接頂点を探索
        for neighbor, weight in self.graph.get_neighbors(current_vertex):
            if neighbor not in visited:
                new_distance = current_distance + weight
                new_path = current_path + [neighbor]

                path, distance = self._dfs(neighbor, visited, new_distance, new_path)
                if distance > max_distance:
                    max_distance = distance
                    best_path = path

        visited.remove(current_vertex)
        return best_path, max_distance