from collections import defaultdict

class Graph:
    """無向グラフのデータ構造"""

    def __init__(self):
        self.edges = defaultdict(list)  # 隣接リスト: {vertex: [(neighbor, weight), ...]}
        self.vertices = set()

    def add_edge(self, u, v, weight):
        """エッジの追加（無向グラフとして処理）"""
        self.edges[u].append((v, weight))
        self.edges[v].append((u, weight))
        self.vertices.add(u)
        self.vertices.add(v)

    def get_neighbors(self, vertex):
        """指定した頂点の隣接頂点とその重みを取得"""
        return self.edges[vertex]

    def get_all_vertices(self):
        """全頂点の取得"""
        return list(self.vertices)