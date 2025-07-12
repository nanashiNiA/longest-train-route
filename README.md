# longest-train-rout(最長片道きっぷの旅)

## 概要
鉄道路線網において、最も長い片道きっぷの経路を求めるプログラムです。
株式会社ドリーム・アーツ 2027年新卒エンジニア採用コーディングテストの解答として作成。

## 問題の詳細
- 駅を点、路線を線としてモデル化された鉄道路線網
- 同じ点を2回通ることはできない（シンプルパス）
- 始点と終点はすべての点の中から自由に選択可能
- 最も長い距離を片道きっぷで旅することができる経路を探索

## アルゴリズム
本実装では以下のアプローチを採用しています：

### 基本アルゴリズム(今回の試験対象)
1. **深さ優先探索（DFS）+ バックトラッキング**
2. **全頂点からの探索**: すべての頂点を始点として最長パスを探索
3. **訪問済み頂点の管理**: 同じ頂点を2回訪問しないよう制御

### 高度な最適化（プラス機能での実装のため試験には関係なし）
1. **並列処理**: multiprocessingを使用した複数始点からの並列探索
2. **グラフ特性判定**: 完全グラフ、疎グラフ、一般グラフの自動判定
3. **貪欲法**: 大規模グラフでの近似解計算
4. **枝刈り最適化**: 残り最大可能距離による早期終了
5. **進捗表示**: 長時間計算に対する進捗監視

計算量: O(V!) (最悪ケース、Vは頂点数)

## 実行方法

### 必要な環境
- Python 3.8以上
- 標準ライブラリのみ使用（外部依存なし）

### インストール・実行

#### 基本版（推奨：採用試験用）
```bash
# リポジトリのクローン
git clone <repository-url>
cd longest-train-route

# シンプル版実行（標準入力から読み込み）
python src/simple_main.py

# ファイルからの入力
python src/simple_main.py < tests/sample_inputs/example1.txt

# 手動入力の場合
python src/simple_main.py
# データを入力後、'end' または Ctrl+Z (Windows) / Ctrl+D (Linux) で終了

# シンプル版のテスト
python -m pytest tests/test_simple_solver.py -v
```

### 詳細な使用方法

#### 1. 手動入力モード
```bash
python src/simple_main.py
```
実行後、以下のように1行ずつデータを入力：
```
1, 2, 8.54
2, 3, 3.11
3, 1, 2.19
3, 4, 4
4, 1, 1.4
end
```

**入力終了方法：**
- `end` と入力してEnter
- Windows: `Ctrl+Z` を押してEnter
- Linux/Mac: `Ctrl+D` を押す

#### 2. ファイルからの入力
```bash
# Windows PowerShell
Get-Content input.txt | python src/simple_main.py

# Linux/Mac
python src/simple_main.py < input.txt

# サンプルファイルを使用
python src/simple_main.py < tests/sample_inputs/example1.txt
```

#### 3. エラーハンドリング
- **不正なフォーマット**: 警告メッセージが表示され、その行は無視されます
- **空行**: 自動的にスキップされます
- **空のグラフ**: "No valid edges found" エラーが表示されます

#### 4. 出力例
```
1
2
3
4
```
最長パスの頂点IDが改行区切りで出力されます。

### トラブルシューティング

#### よくある問題と解決方法

**1. 入力が受け付けられない**
```bash
# 問題: PowerShellでリダイレクトが動作しない
python src/simple_main.py < input.txt  # ❌ 動作しない場合がある

# 解決: Get-Contentを使用
Get-Content input.txt | python src/simple_main.py  # ✅
```

**2. 入力終了ができない**
```bash
# Windowsの場合
end  # Enterを押す
# または
Ctrl+Z  # Enterを押す

# Linux/Macの場合
Ctrl+D
```

**3. 出力が表示されない**
- 入力データが正しいフォーマットか確認
- グラフが連結しているか確認
- 空行や不正な行がないか確認

**4. 期待と異なる結果が出る**
- 同じ距離の最長パスが複数ある場合、辞書順で最小のパスが出力されます
- 入力順序によって結果が変わる場合があります

### 実際の使用例

#### 例1: 基本的な三角形グラフ
```bash
$ python src/simple_main.py
1, 2, 10.0
2, 3, 5.0
3, 1, 3.0
end
```
**出力:**
```
1
2
3
```

#### 例2: ファイルからの実行
```bash
# input.txt の内容:
# 1, 2, 8.54
# 2, 3, 3.11
# 3, 1, 2.19
# 3, 4, 4
# 4, 1, 1.4

$ Get-Content input.txt | python src/simple_main.py
```
**出力:**
```
1
2
3
4
```

#### 高度版（私的追加実装）
```bash
# 基本実行（標準入力から読み込み）
python src/main.py

# ファイルからの入力
python src/main.py < tests/sample_inputs/example1.txt

# ソルバー指定実行
python src/main.py --solver original < tests/sample_inputs/example1.txt
python src/main.py --solver parallel < tests/sample_inputs/difficult_case1.txt
python src/main.py --solver advanced < tests/sample_inputs/performance_killer.txt

# 並列処理のワーカー数指定
python src/main.py --solver parallel --workers 4 < tests/sample_inputs/large_graph.txt

# テストの実行
python -m pytest tests/ -v

# 性能ベンチマーク
python tests/benchmark_solvers.py
```

## ソルバーの種類

### 基本版（推奨：採用試験用）

#### Simple Solver (simple_main.py)
- 基本的な深さ優先探索
- シンプルで確実な実装
- 採用試験の要求を満たす最小限の実装
- 出力フォーマット: `\r\n`改行コード対応

### 高度版（追加実装）

#### 1. Original Solver (original)
- 基本的な深さ優先探索
- 小規模グラフ（頂点数 ≤ 4）に最適
- シンプルで確実な実装

#### 2. Parallel Solver (parallel)
- 並列処理による高速化
- 中〜大規模グラフ（頂点数 > 4）に最適
- 複数の始点から同時に探索
- 進捗表示機能付き

#### 3. Advanced Solver (advanced)
- グラフ特性に基づく戦略選択
- 完全グラフ: 貪欲法による近似
- 疎グラフ: 連結成分ごとの探索
- 一般グラフ: 並列処理との組み合わせ

## 入力フォーマット
```
始点の ID(正の整数値), 終点の ID(正の整数値), 距離(浮動小数点数)\r\n
```

### 入力例
```
1, 2, 8.54
2, 3, 3.11
3, 1, 2.19
3, 4, 4
4, 1, 1.4
```

## 出力フォーマット
最長経路となる点のIDを順番に改行コード(\r\n)で区切って出力

### 出力例
```
2
3
4
1
```

## プロジェクト構造
```
longest-train-route/
├── README.md              # このファイル
├── requirements.txt       # 依存関係（空）
├── difficult_test_cases.txt  # 難しいテストケース定義
├── src/
│   ├── simple_main.py    # 基本版メインエントリーポイント（推奨）
│   ├── simple_solver.py  # 基本版ソルバー
│   ├── main.py           # 高度版メインエントリーポイント
│   ├── graph.py          # グラフデータ構造
│   ├── solver.py         # 基本最長パス探索アルゴリズム
│   └── parallel_solver.py # 並列処理・高度最適化ソルバー
├── tests/
│   ├── test_simple_solver.py # 基本版ユニットテスト
│   ├── test_solver.py    # 高度版ユニットテスト
│   ├── benchmark_solvers.py # 性能ベンチマーク
│   └── sample_inputs/    # テスト用入力ファイル
│       ├── example1.txt
│       ├── simple_line.txt
│       ├── difficult_case1.txt    # 6頂点完全グラフ
│       ├── performance_killer.txt # 8頂点完全グラフ
│       └── large_graph.txt       # 10頂点密グラフ
└── docs/
    └── algorithm_explanation.md  # アルゴリズム詳細説明
```

## 設計の特徴
- **モジュール分割**: グラフ表現、アルゴリズム、入出力処理を分離
- **テスタビリティ**: ユニットテストによる品質保証
- **拡張性**: 異なるアルゴリズムへの切り替えが容易
- **エラーハンドリング**: 不正な入力に対する適切な処理
- **並列処理**: マルチコアCPUの活用
- **適応的戦略**: グラフ特性に基づく最適化

## 性能上の考慮事項

### 小規模グラフ（頂点数 ≤ 4）
- Original Solverが最適
- 全探索による正確な解

### 中規模グラフ（頂点数 5-8）
- Parallel Solverが推奨
- 並列処理による高速化

### 大規模グラフ（頂点数 > 8）
- Advanced Solverが推奨
- グラフ特性に基づく戦略選択
- 完全グラフ: 貪欲法による近似
- 疎グラフ: 連結成分分割

### 性能比較
```
テストケース: difficult_case1.txt (6頂点完全グラフ)
- Original: ~0.5秒
- Parallel: ~0.2秒
- Advanced: ~0.1秒

テストケース: performance_killer.txt (8頂点完全グラフ)
- Original: ~30秒
- Parallel: ~8秒
- Advanced: ~0.5秒
```

## テストケース
- 基本的な線形グラフ
- 環状グラフ
- 完全グラフ（6頂点、8頂点）
- 大規模密グラフ（10頂点）
- スター型グラフ
- 長いチェーングラフ
- 複雑な重みパターン
- エッジケース（空入力、不正フォーマット）

## コマンドラインオプション
```bash
python src/main.py [OPTIONS]

オプション:
  --solver {auto,original,parallel,advanced}
                        使用するソルバー (デフォルト: auto)
  --workers INT         並列処理のワーカー数 (デフォルト: CPU数)
  --timeout INT         タイムアウト時間（秒） (デフォルト: 300)
  -h, --help           ヘルプメッセージを表示
```

## 作成者
由井　拓翔

## ライセンス
MIT License
