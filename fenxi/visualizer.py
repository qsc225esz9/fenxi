"""数据可视化模块 / Data visualization module"""

import os
import math
from typing import Optional


class DataVisualizer:
    """生成文本图表 / Generates text-based charts."""

    WIDTH = 60  # Chart width in characters

    def histogram(self, values: list[float], title: str = "", bins: int = 10) -> str:
        """
        生成文本直方图 / Generate a text histogram.

        Args:
            values: List of numeric values.
            title: Chart title.
            bins: Number of bins.

        Returns:
            Multi-line string containing the histogram.
        """
        if not values:
            return "(无数据 / No data)"
        min_val = min(values)
        max_val = max(values)
        if min_val == max_val:
            return f"{title}\n所有值相同 / All values equal: {min_val}"

        bin_width = (max_val - min_val) / bins
        counts = [0] * bins
        for v in values:
            idx = min(int((v - min_val) / bin_width), bins - 1)
            counts[idx] += 1

        max_count = max(counts)
        bar_max = self.WIDTH - 20

        lines = []
        if title:
            lines.append(title)
            lines.append("=" * (self.WIDTH))
        for i, count in enumerate(counts):
            lo = min_val + i * bin_width
            hi = lo + bin_width
            bar_len = int(count / max_count * bar_max) if max_count > 0 else 0
            bar = "█" * bar_len
            lines.append(f"[{lo:8.2f}, {hi:8.2f}) | {bar:<{bar_max}} {count}")
        return "\n".join(lines)

    def bar_chart(
        self,
        labels: list[str],
        values: list[float],
        title: str = "",
        max_bars: int = 20,
    ) -> str:
        """
        生成文本条形图 / Generate a text bar chart.

        Args:
            labels: Category labels.
            values: Corresponding values.
            title: Chart title.
            max_bars: Maximum number of bars to show.

        Returns:
            Multi-line string containing the bar chart.
        """
        if not labels:
            return "(无数据 / No data)"

        pairs = sorted(zip(values, labels), reverse=True)[:max_bars]
        sorted_vals, sorted_labels = zip(*pairs)

        max_val = max(sorted_vals) if sorted_vals else 1
        bar_max = self.WIDTH - 25
        max_label_len = max(len(str(l)) for l in sorted_labels)

        lines = []
        if title:
            lines.append(title)
            lines.append("=" * self.WIDTH)
        for label, val in zip(sorted_labels, sorted_vals):
            bar_len = int(val / max_val * bar_max) if max_val > 0 else 0
            bar = "█" * bar_len
            lines.append(f"{str(label):<{max_label_len}} | {bar:<{bar_max}} {val:.1f}")
        return "\n".join(lines)

    def scatter_plot(
        self,
        xs: list[float],
        ys: list[float],
        title: str = "",
        width: int = 60,
        height: int = 20,
    ) -> str:
        """
        生成文本散点图 / Generate a text scatter plot.

        Args:
            xs: X-axis values.
            ys: Y-axis values.
            title: Chart title.
            width: Plot width in characters.
            height: Plot height in characters.

        Returns:
            Multi-line string containing the scatter plot.
        """
        if not xs or not ys:
            return "(无数据 / No data)"
        if len(xs) != len(ys):
            raise ValueError("xs 和 ys 长度必须相同 / xs and ys must have the same length.")

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        range_x = max_x - min_x or 1.0
        range_y = max_y - min_y or 1.0

        grid = [[" "] * width for _ in range(height)]

        for x, y in zip(xs, ys):
            col = min(int((x - min_x) / range_x * (width - 1)), width - 1)
            row = min(int((max_y - y) / range_y * (height - 1)), height - 1)
            grid[row][col] = "●"

        lines = []
        if title:
            lines.append(title)
            lines.append("=" * (width + 10))
        for i, row in enumerate(grid):
            y_label = max_y - i * (range_y / (height - 1))
            lines.append(f"{y_label:8.2f} |{''.join(row)}|")
        lines.append(" " * 9 + "+" + "-" * width + "+")
        x_axis = f"{min_x:.2f}" + " " * (width - 10) + f"{max_x:.2f}"
        lines.append(" " * 10 + x_axis)
        return "\n".join(lines)

    def save_png(
        self,
        values: list[float],
        filepath: str,
        title: str = "",
        kind: str = "histogram",
    ) -> None:
        """
        将图表保存为 PNG 文件（需要 matplotlib）。
        Save chart as a PNG file (requires matplotlib).

        Args:
            values: Numeric values to plot.
            filepath: Output file path.
            title: Chart title.
            kind: Chart type, either 'histogram' or 'bar'.
        """
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError as e:
            raise ImportError(
                "保存图片需要安装 matplotlib / matplotlib is required to save PNG files."
            ) from e

        fig, ax = plt.subplots()
        if kind == "histogram":
            ax.hist(values, bins=10, color="steelblue", edgecolor="white")
        elif kind == "bar":
            ax.bar(range(len(values)), values, color="steelblue")
        else:
            raise ValueError(f"未知图表类型 / Unknown chart kind: {kind!r}")
        if title:
            ax.set_title(title)
        fig.tight_layout()
        fig.savefig(filepath)
        plt.close(fig)
