# 最長パス探索アルゴリズムの詳細説明

## 概要

このプロジェクトは、無向グラフにおける最長パス問題を解決するためのアルゴリズムを実装しています。最長パス問題は、グラフ内の任意の2つの頂点間の最長の単純パス（同じ頂点を2回以上通らないパス）を見つける問題です。

## アルゴリズムの詳細

### 1. グラフデータ構造

```python
class Graph:
    def __init__(self):
        self.edges = defaultdict(list)  # 隣接リスト
        self.vertices = set()           # 頂点の集合
```

- **隣接リスト**: 各頂点に対して、隣接する頂点とその重みを格納
- **無向グラフ**: エッジ(u,v)を追加する際、両方向のエッジを自動的に追加

### 2. 最長パス探索アルゴリズム

#### 基本アプローチ
1. **全頂点からの開始**: 各頂点を始点として探索を実行
2. **深さ優先探索(DFS)**: 各始点から到達可能な全てのパスを探索
3. **バックトラッキング**: 訪問済み頂点を記録し、同じ頂点を2回訪問しない

#### アルゴリズムの擬似コード
```
function find_longest_path():
    best_path = []
    best_distance = 0

    for each vertex v in graph:
        visited = empty set
        path = empty list
        dfs(v, visited, path, 0)

    return best_path, best_distance

function dfs(current, visited, path, total_distance):
    visited.add(current)
    path.append(current)

    if total_distance > best_distance:
        best_distance = total_distance
        best_path = copy(path)

    for each neighbor, weight of current:
        if neighbor not in visited:
            dfs(neighbor, visited, path, total_distance + weight)

    visited.remove(current)
    path.pop()
```

### 3. 時間・空間計算量

#### 時間計算量
- **最悪ケース**: O(V!) - 完全グラフの場合
- **平均ケース**: O(V * E) - スパースグラフの場合

#### 空間計算量
- **再帰スタック**: O(V) - 最長パスの長さ
- **訪問配列**: O(V) - 頂点数分のメモリ
- **総合**: O(V)

### 4. 最適化の可能性

#### メモ化による改善
```python
def dfs_with_memo(self, current, visited_mask):
    if (current, visited_mask) in self.memo:
        return self.memo[(current, visited_mask)]

    # DFS処理...

    self.memo[(current, visited_mask)] = result
    return result
```

#### 枝刈りによる改善
- 現在の最長距離を超える可能性がない場合の早期終了
- 対称性を利用した重複探索の削減

## 入力・出力フォーマット

### 入力フォーマット
```
u, v, weight
```
- `u, v`: 頂点番号（整数）
- `weight`: エッジの重み（浮動小数点数）
- 各行は1つのエッジを表す

### 出力フォーマット
```
vertex1
vertex2
vertex3
...
```
- 最長パスを構成する頂点を順番に出力
- 各行に1つの頂点番号

## 使用例

### 入力例
```
1, 2, 8.54
2, 3, 3.11
3, 1, 2.19
3, 4, 4
4, 1, 1.4
```

### 期待される出力
```
1
2
3
4
```

## 制限事項と注意点

1. **NP困難問題**: 最長パス問題はNP困難な問題のため、大規模グラフでは実行時間が指数的に増加
2. **メモリ使用量**: 深い再帰呼び出しによりスタックオーバーフローの可能性
3. **精度**: 浮動小数点数の計算誤差の蓄積

## 今後の改善案

1. **並列処理**: 複数の始点からの探索を並列実行
2. **ヒューリスティック**: 貪欲法や局所探索法との組み合わせ
3. **近似アルゴリズム**: 大規模グラフに対する近似解法の実装