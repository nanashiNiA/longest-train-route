#!/usr/bin/env python3
"""
ソルバーの性能比較ベンチマーク
"""

import sys
import os
import time
import subprocess
from pathlib import Path

# プロジェクトルートを追加
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from graph import Graph
from solver import LongestPathSolver
from parallel_solver import ParallelLongestPathSolver, AdvancedLongestPathSolver

def load_graph_from_file(file_path):
    """ファイルからグラフを読み込み"""
    graph = Graph()

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # カンマ区切りの形式を解析
            parts = [p.strip() for p in line.split(',')]
            if len(parts) == 3:
                u = int(parts[0])
                v = int(parts[1])
                weight = float(parts[2])
                graph.add_edge(u, v, weight)

    return graph

def benchmark_solver(solver, graph, name):
    """ソルバーの性能を測定"""
    print(f"\n=== {name} ===")

    start_time = time.time()
    try:
        path, distance = solver.find_longest_path()
        elapsed_time = time.time() - start_time

        print(f"実行時間: {elapsed_time:.3f}秒")
        print(f"最長距離: {distance:.3f}")
        print(f"パス長: {len(path)}")
        print(f"パス: {path}")

        return elapsed_time, distance, len(path)

    except Exception as e:
        print(f"エラー: {e}")
        return None, None, None

def run_benchmarks():
    """全テストケースでベンチマーク実行"""
    test_files = [
        "tests/sample_inputs/example1.txt",
        "tests/sample_inputs/simple_line.txt",
        "tests/sample_inputs/difficult_case1.txt",
        "tests/sample_inputs/performance_killer.txt",
        "tests/sample_inputs/large_graph.txt"
    ]

    results = {}

    for test_file in test_files:
        if not os.path.exists(test_file):
            print(f"警告: {test_file} が見つかりません")
            continue

        print(f"\n{'='*50}")
        print(f"テストケース: {test_file}")
        print(f"{'='*50}")

        # グラフ読み込み
        graph = load_graph_from_file(test_file)
        vertices = graph.get_all_vertices()

        if not vertices:
            print("グラフが空です")
            continue

        print(f"頂点数: {len(vertices)}")
        print(f"エッジ数: {sum(len(graph.get_neighbors(v)) for v in vertices) // 2}")

        # 各ソルバーでテスト
        solvers = [
            (LongestPathSolver(graph), "Original Solver"),
            (ParallelLongestPathSolver(graph, max_workers=4), "Parallel Solver"),
            (AdvancedLongestPathSolver(graph), "Advanced Solver")
        ]

        test_results = {}

        for solver, name in solvers:
            time_taken, distance, path_length = benchmark_solver(solver, graph, name)
            if time_taken is not None:
                test_results[name] = {
                    'time': time_taken,
                    'distance': distance,
                    'path_length': path_length
                }

        results[test_file] = test_results

    # 結果サマリー
    print(f"\n{'='*60}")
    print("性能比較サマリー")
    print(f"{'='*60}")

    for test_file, test_results in results.items():
        print(f"\n{test_file}:")
        for solver_name, result in test_results.items():
            print(f"  {solver_name}: {result['time']:.3f}秒, "
                  f"距離={result['distance']:.3f}, パス長={result['path_length']}")

def test_command_line():
    """コマンドライン実行のテスト"""
    test_files = [
        "tests/sample_inputs/difficult_case1.txt",
        "tests/sample_inputs/performance_killer.txt"
    ]

    print(f"\n{'='*60}")
    print("コマンドライン実行テスト")
    print(f"{'='*60}")

    for test_file in test_files:
        if not os.path.exists(test_file):
            continue

        print(f"\nテストファイル: {test_file}")

        # 各ソルバーでコマンドライン実行
        solvers = ["original", "parallel", "advanced"]

        for solver in solvers:
            print(f"\n--- {solver} solver ---")

            try:
                start_time = time.time()

                # コマンドライン実行
                cmd = [
                    sys.executable, "src/main.py",
                    "--solver", solver
                ]

                with open(test_file, 'r') as input_file:
                    result = subprocess.run(
                        cmd,
                        stdin=input_file,
                        capture_output=True,
                        text=True,
                        timeout=60  # 60秒タイムアウト
                    )

                elapsed_time = time.time() - start_time

                if result.returncode == 0:
                    print(f"実行時間: {elapsed_time:.3f}秒")
                    print(f"出力: {result.stdout.strip()}")
                else:
                    print(f"エラー: {result.stderr.strip()}")

            except subprocess.TimeoutExpired:
                print("タイムアウト（60秒）")
            except Exception as e:
                print(f"エラー: {e}")

if __name__ == "__main__":
    print("最長パス問題ソルバー性能ベンチマーク")
    print("=" * 60)

    # ライブラリベンチマーク
    run_benchmarks()

    # コマンドライン実行テスト
    test_command_line()