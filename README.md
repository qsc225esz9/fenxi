# fenxi 📊

**fenxi**（分析）是一个轻量级 Python 数据分析工具，支持从 CSV 和 JSON 文件中加载数据，进行统计分析并生成文本图表。

**fenxi** is a lightweight Python data analysis tool that loads data from CSV and JSON files, performs statistical analysis, and renders text-based charts.

---

## 功能 / Features

- 📂 **数据加载 / Data Loading** — CSV 和 JSON 格式 / CSV and JSON formats
- 📈 **描述性统计 / Descriptive Statistics** — 均值、标准差、四分位数等 / mean, std, quartiles, etc.
- 🔗 **相关分析 / Correlation** — 皮尔逊相关系数及相关矩阵 / Pearson coefficient and full matrix
- 📊 **文本可视化 / Text Charts** — 直方图、条形图、散点图 / histogram, bar chart, scatter plot
- 🖼️ **PNG 导出 / PNG Export** — 需要 matplotlib / requires matplotlib

---

## 快速开始 / Quick Start

```bash
pip install -r requirements.txt
pip install -e .
```

### 基本用法 / Basic Usage

```bash
# 显示描述性统计 / Show descriptive statistics
python -m fenxi data/sample.csv

# 某列直方图 / Histogram for a column
python -m fenxi data/sample.csv --column age

# 两列相关系数 / Correlation between two columns
python -m fenxi data/sample.csv --correlate age salary

# 相关矩阵 / Full correlation matrix
python -m fenxi data/sample.csv --correlation-matrix

# 值频次统计 / Value counts for a categorical column
python -m fenxi data/sample.csv --value-counts department

# 保存直方图为 PNG / Save histogram as PNG
python -m fenxi data/sample.csv --column age --save-png age_hist.png

# 分析 JSON 文件 / Analyze a JSON file
python -m fenxi data/cities.json
```

### Python API

```python
from fenxi import DataLoader, DataAnalyzer, DataVisualizer

data = DataLoader().load("data/sample.csv")
analyzer = DataAnalyzer(data)

print(analyzer.describe())
print(analyzer.correlation("age", "salary"))
print(analyzer.value_counts("department"))

viz = DataVisualizer()
ages = analyzer.get_numeric_values("age")
print(viz.histogram(ages, title="Age Distribution"))
```

---

## 测试 / Tests

```bash
pip install pytest
pytest
```

---

## 项目结构 / Project Structure

```
fenxi/
├── fenxi/              # 主包 / Main package
│   ├── loader.py       # 数据加载 / Data loading
│   ├── analyzer.py     # 统计分析 / Statistical analysis
│   ├── visualizer.py   # 文本可视化 / Text visualization
│   └── __main__.py     # CLI 入口 / CLI entry point
├── tests/              # 单元测试 / Unit tests
├── data/               # 示例数据 / Sample data
│   ├── sample.csv
│   └── cities.json
└── requirements.txt
```