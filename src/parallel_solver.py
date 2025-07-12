import sys
import time
import threading
from itertools import combinations
from collections import deque

class ParallelLongestPathSolver:
    """並列処理対応の最長パス問題ソルバー"""

    def __init__(self, graph, max_workers=None):
        self.graph = graph
        self.best_path = []
        self.best_distance = 0.0
        self.max_workers = max_workers or min(4, 8)  # CPU数ではなく固定値
        self.progress_callback = None
        self.lock = threading.Lock()

    def set_progress_callback(self, callback):
        """進捗表示用コールバックを設定"""
        self.progress_callback = callback

    def find_longest_path(self):
        """並列処理による最長パス探索"""
        vertices = self.graph.get_all_vertices()

        if not vertices:
            return [], 0.0

        # 頂点数が少ない場合は逐次処理
        if len(vertices) <= 4:
            return self._sequential_search(vertices)

        # 並列処理の準備
        start_vertices = self._select_start_vertices(vertices)

        if self.progress_callback:
            self.progress_callback(f"探索開始: {len(start_vertices)}個の始点で並列処理")

        # スレッドベースの並列処理
        threads = []
        results = []

        # 結果を格納するリスト
        thread_results = [None] * len(start_vertices)

        def search_worker(vertex, index):
            """個別のスレッドで実行する探索"""
            visited = set()
            path = []
            best_local_path = []
            best_local_distance = [0.0]

            self._dfs_optimized(vertex, visited, path, 0.0,
                               best_local_path, best_local_distance)

            thread_results[index] = (best_local_path, best_local_distance[0])

        # スレッド作成と開始
        for i, vertex in enumerate(start_vertices):
            thread = threading.Thread(target=search_worker, args=(vertex, i))
            threads.append(thread)
            thread.start()

        # 全スレッドの完了を待機
        for thread in threads:
            thread.join()

        # 結果の統合
        for result in thread_results:
            if result:
                path, distance = result
                if distance > self.best_distance:
                    self.best_distance = distance
                    self.best_path = path

        # 並列処理で最適解が見つからない場合は、全探索を実行
        if len(self.best_path) < len(vertices) and len(vertices) <= 6:
            exhaustive_path, exhaustive_distance = self._exhaustive_search(vertices)
            if exhaustive_distance > self.best_distance:
                self.best_distance = exhaustive_distance
                self.best_path = exhaustive_path

        return self.best_path, self.best_distance

    def _select_start_vertices(self, vertices):
        """効率的な始点選択"""
        n = len(vertices)

        # 頂点数が多い場合は、次数の高い頂点を優先
        if n > 10:
            degree_vertices = [(v, len(self.graph.get_neighbors(v))) for v in vertices]
            degree_vertices.sort(key=lambda x: x[1], reverse=True)
            # 上位50%の頂点を始点として使用
            top_count = max(1, min(self.max_workers * 2, n // 2))
            return [v for v, _ in degree_vertices[:top_count]]
        else:
            return vertices

    def _dfs_optimized(self, current, visited, path, total_distance,
                      best_path, best_distance):
        """最適化された深さ優先探索"""
        visited.add(current)
        path.append(current)

        # 現在のパスが最長か確認
        if total_distance > best_distance[0]:
            best_distance[0] = total_distance
            best_path[:] = path.copy()

        # 隣接頂点を効率的に探索
        neighbors = self.graph.get_neighbors(current)

        # 重みでソートして有望な経路を優先探索
        neighbors.sort(key=lambda x: x[1], reverse=True)

        for neighbor, weight in neighbors:
            if neighbor not in visited:
                # 枝刈り: 残りの最大可能距離を計算
                remaining_max = self._estimate_remaining_distance(neighbor, visited)
                if total_distance + weight + remaining_max > best_distance[0]:
                    self._dfs_optimized(neighbor, visited, path,
                                      total_distance + weight, best_path, best_distance)

        visited.remove(current)
        path.pop()

    def _estimate_remaining_distance(self, vertex, visited):
        """残りの最大可能距離を推定"""
        neighbors = self.graph.get_neighbors(vertex)
        unvisited_neighbors = [n for n, _ in neighbors if n not in visited]

        if not unvisited_neighbors:
            return 0.0

        # 最大重みのエッジを残り頂点数分推定
        max_weights = sorted([w for _, w in neighbors], reverse=True)
        return sum(max_weights[:len(unvisited_neighbors)])

    def _sequential_search(self, vertices):
        """逐次処理による探索（小規模グラフ用）"""
        self.best_path = []
        self.best_distance = 0.0

        for i, start_vertex in enumerate(vertices):
            if self.progress_callback and i % max(1, len(vertices) // 10) == 0:
                self.progress_callback(f"逐次処理進捗: {i+1}/{len(vertices)}")

            visited = set()
            path = []
            self._dfs_optimized(start_vertex, visited, path, 0.0,
                               self.best_path, [self.best_distance])

        return self.best_path, self.best_distance

class AdvancedLongestPathSolver:
    """高度な最適化を適用したソルバー"""

    def __init__(self, graph):
        self.graph = graph
        self.best_path = []
        self.best_distance = 0.0
        self.memo = {}  # メモ化用

    def find_longest_path(self):
        """高度な最適化による最長パス探索"""
        vertices = self.graph.get_all_vertices()

        if not vertices:
            return [], 0.0

        # 小規模グラフの場合は全探索
        if len(vertices) <= 6:
            return self._exhaustive_search(vertices)

        # グラフの特性に基づいて戦略を選択
        if self._is_complete_graph(vertices):
            return self._complete_graph_strategy(vertices)
        elif self._is_sparse_graph(vertices):
            return self._sparse_graph_strategy(vertices)
        else:
            return self._general_strategy(vertices)

    def _is_complete_graph(self, vertices):
        """完全グラフかどうかを判定"""
        n = len(vertices)
        expected_edges = n * (n - 1) // 2
        actual_edges = sum(len(self.graph.get_neighbors(v)) for v in vertices) // 2
        return actual_edges == expected_edges

    def _is_sparse_graph(self, vertices):
        """疎グラフかどうかを判定"""
        n = len(vertices)
        actual_edges = sum(len(self.graph.get_neighbors(v)) for v in vertices) // 2
        return actual_edges < n * 2

    def _complete_graph_strategy(self, vertices):
        """完全グラフ用の戦略"""
        # 完全グラフでは、最長パスは全頂点を含む可能性が高い
        # 貪欲法で近似解を求める
        return self._greedy_longest_path(vertices)

    def _sparse_graph_strategy(self, vertices):
        """疎グラフ用の戦略"""
        # 疎グラフでは、連結成分ごとに探索
        components = self._find_connected_components(vertices)
        best_path = []
        best_distance = 0.0

        for component in components:
            path, distance = self._search_component(component)
            if distance > best_distance:
                best_distance = distance
                best_path = path

        return best_path, best_distance

    def _general_strategy(self, vertices):
        """一般的なグラフ用の戦略"""
        # 並列処理と逐次処理を組み合わせ
        parallel_solver = ParallelLongestPathSolver(self.graph)
        return parallel_solver.find_longest_path()

    def _greedy_longest_path(self, vertices):
        """貪欲法による最長パス近似"""
        if not vertices:
            return [], 0.0

        best_path = []
        best_distance = 0.0

        # 各頂点を始点として貪欲探索
        for start in vertices:
            path, distance = self._greedy_search_from(start, vertices)
            if distance > best_distance:
                best_distance = distance
                best_path = path

        # 貪欲法の結果が不十分な場合は、全探索を実行
        if len(best_path) < len(vertices):
            # 小規模グラフの場合は全探索
            if len(vertices) <= 6:
                exhaustive_path, exhaustive_distance = self._exhaustive_search(vertices)
                if exhaustive_distance > best_distance:
                    return exhaustive_path, exhaustive_distance

        return best_path, best_distance

    def _greedy_search_from(self, start, all_vertices):
        """指定頂点からの貪欲探索"""
        path = [start]
        visited = {start}
        total_distance = 0.0

        current = start
        while len(visited) < len(all_vertices):
            neighbors = self.graph.get_neighbors(current)
            best_neighbor = None
            best_weight = 0.0

            for neighbor, weight in neighbors:
                if neighbor not in visited and weight > best_weight:
                    best_neighbor = neighbor
                    best_weight = weight

            if best_neighbor is None:
                break

            path.append(best_neighbor)
            visited.add(best_neighbor)
            total_distance += best_weight
            current = best_neighbor

        return path, total_distance

    def _find_connected_components(self, vertices):
        """連結成分を発見"""
        visited = set()
        components = []

        for vertex in vertices:
            if vertex not in visited:
                component = []
                self._dfs_component(vertex, visited, component)
                components.append(component)

        return components

    def _dfs_component(self, vertex, visited, component):
        """連結成分を発見するためのDFS"""
        visited.add(vertex)
        component.append(vertex)

        for neighbor, _ in self.graph.get_neighbors(vertex):
            if neighbor not in visited:
                self._dfs_component(neighbor, visited, component)

    def _search_component(self, component):
        """連結成分内での最長パス探索"""
        if len(component) <= 4:
            # 小規模成分は全探索
            return self._exhaustive_search(component)
        else:
            # 大規模成分は貪欲法
            return self._greedy_longest_path(component)

    def _exhaustive_search(self, vertices):
        """全探索（小規模グラフ用）"""
        best_path = []
        best_distance = 0.0

        for start in vertices:
            visited = set()
            path = []
            self._dfs_exhaustive(start, visited, path, 0.0, best_path, [best_distance])

        return best_path, best_distance

    def _dfs_exhaustive(self, current, visited, path, total_distance,
                       best_path, best_distance):
        """全探索用DFS"""
        visited.add(current)
        path.append(current)

        if total_distance > best_distance[0]:
            best_distance[0] = total_distance
            best_path[:] = path.copy()

        for neighbor, weight in self.graph.get_neighbors(current):
            if neighbor not in visited:
                self._dfs_exhaustive(neighbor, visited, path,
                                   total_distance + weight, best_path, best_distance)

        visited.remove(current)
        path.pop()