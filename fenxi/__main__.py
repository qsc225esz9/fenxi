#!/usr/bin/env python3
"""
fenxi - 数据分析命令行工具 / Data Analysis CLI

用法 / Usage:
    python -m fenxi <file> [options]

示例 / Examples:
    python -m fenxi data/sample.csv
    python -m fenxi data/sample.csv --column age
    python -m fenxi data/sample.csv --describe
    python -m fenxi data/sample.csv --correlate age salary
"""

import argparse
import sys
import os

from .loader import DataLoader
from .analyzer import DataAnalyzer
from .visualizer import DataVisualizer


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="fenxi",
        description="数据分析工具 / Data Analysis Tool",
    )
    parser.add_argument("file", help="数据文件路径 / Path to the data file (CSV or JSON)")
    parser.add_argument(
        "--describe",
        action="store_true",
        help="显示描述性统计 / Show descriptive statistics",
    )
    parser.add_argument(
        "--column",
        metavar="COL",
        help="显示某列的直方图 / Show histogram for a column",
    )
    parser.add_argument(
        "--value-counts",
        metavar="COL",
        dest="value_counts",
        help="统计某列的值频次 / Count value frequencies for a column",
    )
    parser.add_argument(
        "--correlate",
        nargs=2,
        metavar=("COL_A", "COL_B"),
        help="计算两列相关系数 / Compute correlation between two columns",
    )
    parser.add_argument(
        "--correlation-matrix",
        action="store_true",
        dest="corr_matrix",
        help="显示相关矩阵 / Show full correlation matrix",
    )
    parser.add_argument(
        "--save-png",
        metavar="FILE",
        dest="save_png",
        help="将直方图保存为 PNG 文件（需要 --column）/ Save histogram as PNG (requires --column)",
    )

    args = parser.parse_args(argv)

    loader = DataLoader()
    try:
        data = loader.load(args.file)
    except (FileNotFoundError, ValueError) as exc:
        print(f"错误 / Error: {exc}", file=sys.stderr)
        return 1

    try:
        analyzer = DataAnalyzer(data)
    except ValueError as exc:
        print(f"错误 / Error: {exc}", file=sys.stderr)
        return 1

    viz = DataVisualizer()

    print(f"\n📊 文件 / File: {args.file}")
    print(f"   行数 / Rows: {analyzer.row_count}")
    print(f"   列数 / Columns: {len(analyzer.columns)}")
    print(f"   列名 / Column names: {', '.join(analyzer.columns)}\n")

    if args.describe or not any([args.column, args.value_counts, args.correlate, args.corr_matrix]):
        print("── 描述性统计 / Descriptive Statistics ──────────────────────────")
        stats = analyzer.describe()
        if not stats:
            print("  (没有数值列 / No numeric columns found)")
        else:
            header = f"{'列名':<20} {'数量':>7} {'均值':>10} {'标准差':>10} {'最小值':>10} {'中位数':>10} {'最大值':>10}"
            print(header)
            print("-" * len(header))
            for col, s in stats.items():
                print(
                    f"{col:<20} {s['count']:>7.0f} {s['mean']:>10.3f} {s['std']:>10.3f} "
                    f"{s['min']:>10.3f} {s['median']:>10.3f} {s['max']:>10.3f}"
                )
        print()

    if args.column:
        col = args.column
        numeric_cols = analyzer.numeric_columns()
        if col not in analyzer.columns:
            print(f"错误 / Error: 列不存在 / Column not found: {col!r}", file=sys.stderr)
            return 1
        if col not in numeric_cols:
            print(f"列 {col!r} 不是数值类型，显示频次统计 / Non-numeric column, showing value counts:")
            counts = analyzer.value_counts(col)
            labels = list(counts.keys())
            values = [float(v) for v in counts.values()]
            print(viz.bar_chart(labels, values, title=f"频次统计 / Value Counts: {col}"))
        else:
            values_list = analyzer.get_numeric_values(col)
            print(viz.histogram(values_list, title=f"直方图 / Histogram: {col}"))
            if args.save_png:
                viz.save_png(values_list, args.save_png, title=col)
                print(f"\n✅ 图片已保存 / Image saved: {args.save_png}")
        print()

    if args.value_counts:
        col = args.value_counts
        if col not in analyzer.columns:
            print(f"错误 / Error: 列不存在 / Column not found: {col!r}", file=sys.stderr)
            return 1
        counts = analyzer.value_counts(col)
        print(f"── 频次统计 / Value Counts: {col} ──")
        for val, cnt in list(counts.items())[:20]:
            print(f"  {val:<30} {cnt}")
        print()

    if args.correlate:
        col_a, col_b = args.correlate
        for col in (col_a, col_b):
            if col not in analyzer.columns:
                print(f"错误 / Error: 列不存在 / Column not found: {col!r}", file=sys.stderr)
                return 1
        r = analyzer.correlation(col_a, col_b)
        if r is None:
            print(f"⚠️  无法计算相关系数 / Cannot compute correlation: {col_a!r} vs {col_b!r}")
        else:
            print(f"── 相关系数 / Correlation: {col_a!r} vs {col_b!r} ──")
            print(f"   r = {r:.4f}")
            if abs(r) >= 0.7:
                strength = "强 / Strong"
            elif abs(r) >= 0.4:
                strength = "中等 / Moderate"
            else:
                strength = "弱 / Weak"
            direction = "正 / Positive" if r >= 0 else "负 / Negative"
            print(f"   强度 / Strength: {strength}  方向 / Direction: {direction}")
        print()

    if args.corr_matrix:
        matrix = analyzer.correlation_matrix()
        cols = list(matrix.keys())
        if not cols:
            print("没有数值列 / No numeric columns for correlation matrix.")
        else:
            print("── 相关矩阵 / Correlation Matrix ──")
            col_width = 10
            header = " " * 20 + "".join(f"{c[:col_width]:>{col_width}}" for c in cols)
            print(header)
            for row_col in cols:
                row_str = f"{row_col:<20}"
                for col in cols:
                    val = matrix[row_col][col]
                    row_str += f"{val:>{col_width}.3f}" if val is not None else f"{'N/A':>{col_width}}"
                print(row_str)
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
