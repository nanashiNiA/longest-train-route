"""
シンプルな最長パス問題ソルバー
採用試験用の基本実装
"""

import sys
import re
from graph import Graph
from simple_solver import SimpleLongestPathSolver

def parse_input():
    """標準入力からグラフデータを解析"""
    graph = Graph()

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            # 正規表現でパース（ホワイトスペースを考慮）
            pattern = r'^\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*$'
            match = re.match(pattern, line)

            if match:
                u = int(match.group(1))
                v = int(match.group(2))
                weight = float(match.group(3))
                graph.add_edge(u, v, weight)
            else:
                print(f"Warning: Invalid input format: {line}", file=sys.stderr)

    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    return graph

def format_output(path):
    """結果を指定フォーマットで出力"""
    for vertex in path:
        print(vertex, end='\r\n')

def main():
    """メイン処理"""
    # 入力解析
    graph = parse_input()

    # グラフが空の場合の処理
    if not graph.get_all_vertices():
        print("No valid edges found", file=sys.stderr)
        return

    # ソルバー実行
    solver = SimpleLongestPathSolver(graph)
    longest_path, max_distance = solver.find_longest_path()

    # 結果出力
    if longest_path:
        format_output(longest_path)
    else:
        print("No path found", file=sys.stderr)

if __name__ == "__main__":
    main()