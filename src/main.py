import sys
import re
import time
import argparse
from graph import Graph
from solver import LongestPathSolver
from parallel_solver import ParallelLongestPathSolver, AdvancedLongestPathSolver

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
        print(vertex)

def progress_callback(message):
    """進捗表示用コールバック"""
    print(f"[進捗] {message}", file=sys.stderr)

def analyze_graph(graph):
    """グラフの特性を分析"""
    vertices = graph.get_all_vertices()
    if not vertices:
        return "empty"

    n = len(vertices)
    total_edges = sum(len(graph.get_neighbors(v)) for v in vertices) // 2

    print(f"グラフ分析:", file=sys.stderr)
    print(f"  頂点数: {n}", file=sys.stderr)
    print(f"  エッジ数: {total_edges}", file=sys.stderr)
    print(f"  密度: {total_edges / (n * (n-1) / 2):.3f}" if n > 1 else "  密度: N/A", file=sys.stderr)

    # グラフタイプの判定
    if total_edges == n * (n - 1) // 2:
        return "complete"
    elif total_edges < n * 2:
        return "sparse"
    else:
        return "general"

def select_solver(graph, solver_type="auto", max_workers=None):
    """グラフの特性に基づいてソルバーを選択"""
    if solver_type == "auto":
        graph_type = analyze_graph(graph)
        vertices = graph.get_all_vertices()

        if len(vertices) <= 4:
            solver_type = "original"
        elif graph_type == "complete" and len(vertices) > 6:
            solver_type = "advanced"
        elif len(vertices) > 8:
            solver_type = "parallel"
        else:
            solver_type = "original"

    print(f"選択されたソルバー: {solver_type}", file=sys.stderr)

    if solver_type == "parallel":
        solver = ParallelLongestPathSolver(graph, max_workers)
        solver.set_progress_callback(progress_callback)
        return solver
    elif solver_type == "advanced":
        return AdvancedLongestPathSolver(graph)
    else:
        return LongestPathSolver(graph)

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description="最長パス問題ソルバー")
    parser.add_argument("--solver", choices=["auto", "original", "parallel", "advanced"],
                       default="auto", help="使用するソルバー")
    parser.add_argument("--workers", type=int, default=None,
                       help="並列処理のワーカー数")
    parser.add_argument("--timeout", type=int, default=300,
                       help="タイムアウト時間（秒）")

    args = parser.parse_args()

    # 入力解析
    print("グラフデータを読み込み中...", file=sys.stderr)
    graph = parse_input()

    # グラフが空の場合の処理
    if not graph.get_all_vertices():
        print("No valid edges found", file=sys.stderr)
        return

    # ソルバー選択
    solver = select_solver(graph, args.solver, args.workers)

    # 最長パス探索（タイムアウト付き）
    print("最長パス探索開始...", file=sys.stderr)
    start_time = time.time()

    try:
        longest_path, max_distance = solver.find_longest_path()

        elapsed_time = time.time() - start_time
        print(f"探索完了: {elapsed_time:.2f}秒", file=sys.stderr)
        print(f"最長距離: {max_distance:.3f}", file=sys.stderr)
        print(f"パス長: {len(longest_path)}", file=sys.stderr)

        # 結果出力
        if longest_path:
            format_output(longest_path)
        else:
            print("No path found", file=sys.stderr)

    except KeyboardInterrupt:
        print("\n計算が中断されました", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"エラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()