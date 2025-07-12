import sys

class LongestPathSolver:
    """最長パス問題のソルバー"""

    def __init__(self, graph):
        self.graph = graph
        self.best_path = []
        self.best_distance = 0.0

    def find_longest_path(self):
        """全頂点から開始して最長パスを探索"""
        self.best_path = []
        self.best_distance = 0.0

        vertices = self.graph.get_all_vertices()

        # 各頂点を始点として探索
        for start_vertex in vertices:
            visited = set()
            path = []
            self._dfs(start_vertex, visited, path, 0.0)

        return self.best_path, self.best_distance

    def _dfs(self, current, visited, path, total_distance):
        """深さ優先探索による最長パス探索"""
        # 現在の頂点を訪問
        visited.add(current)
        path.append(current)

        # 現在のパスが最長か確認
        if total_distance > self.best_distance:
            self.best_distance = total_distance
            self.best_path = path[:]  # 深いコピー

        # 隣接頂点を探索
        for neighbor, weight in self.graph.get_neighbors(current):
            if neighbor not in visited:
                self._dfs(neighbor, visited, path, total_distance + weight)

        # バックトラッキング
        visited.remove(current)
        path.pop()