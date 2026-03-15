"""数据分析模块 / Data analysis module"""

import math
from typing import Any, Optional


class DataAnalyzer:
    """对数据集执行统计分析 / Performs statistical analysis on a dataset."""

    def __init__(self, data: list[dict]):
        """
        Args:
            data: List of dicts (rows) to analyze.
        """
        if not data:
            raise ValueError("数据不能为空 / Data cannot be empty.")
        self._data = data
        self._columns = list(data[0].keys())

    @property
    def columns(self) -> list[str]:
        """返回列名列表 / Return the list of column names."""
        return list(self._columns)

    @property
    def row_count(self) -> int:
        """返回数据行数 / Return the number of rows."""
        return len(self._data)

    def numeric_columns(self) -> list[str]:
        """返回数值类型列名 / Return names of numeric columns."""
        numeric = []
        for col in self._columns:
            values = self._get_numeric_values(col)
            if values:
                numeric.append(col)
        return numeric

    def describe(self) -> dict[str, dict[str, float]]:
        """
        计算每个数值列的描述性统计 / Compute descriptive statistics for each numeric column.

        Returns:
            Dict mapping column name to stats dict with keys:
            count, mean, std, min, max, median, q1, q3.
        """
        result = {}
        for col in self.numeric_columns():
            values = self._get_numeric_values(col)
            result[col] = self._stats(values)
        return result

    def correlation(self, col_a: str, col_b: str) -> Optional[float]:
        """
        计算两列之间的皮尔逊相关系数 / Compute Pearson correlation between two columns.

        Args:
            col_a: First column name.
            col_b: Second column name.

        Returns:
            Correlation coefficient, or None if computation is not possible.
        """
        a = self._get_numeric_values(col_a)
        b = self._get_numeric_values(col_b)
        paired = self._paired(col_a, col_b)
        if len(paired) < 2:
            return None
        xs, ys = zip(*paired)
        return self._pearson(list(xs), list(ys))

    def correlation_matrix(self) -> dict[str, dict[str, Optional[float]]]:
        """
        计算所有数值列之间的相关矩阵 / Compute correlation matrix for all numeric columns.

        Returns:
            Nested dict[col_a][col_b] = correlation coefficient.
        """
        cols = self.numeric_columns()
        matrix: dict[str, dict[str, Optional[float]]] = {}
        for a in cols:
            matrix[a] = {}
            for b in cols:
                if a == b:
                    matrix[a][b] = 1.0
                else:
                    matrix[a][b] = self.correlation(a, b)
        return matrix

    def get_numeric_values(self, column: str) -> list[float]:
        """
        返回某列所有有效数值 / Return all valid numeric values in a column.

        Args:
            column: Column name.

        Returns:
            List of float values, skipping non-numeric entries.
        """
        if column not in self._columns:
            raise KeyError(f"列不存在 / Column not found: {column!r}")
        return self._get_numeric_values(column)

    def value_counts(self, column: str) -> dict[str, int]:
        """
        统计某列中每个值出现的次数 / Count occurrences of each value in a column.

        Args:
            column: Column name.

        Returns:
            Dict mapping value to count, sorted by count descending.
        """
        if column not in self._columns:
            raise KeyError(f"列不存在 / Column not found: {column!r}")
        counts: dict[str, int] = {}
        for row in self._data:
            val = str(row.get(column, ""))
            counts[val] = counts.get(val, 0) + 1
        return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_numeric_values(self, column: str) -> list[float]:
        values = []
        for row in self._data:
            raw = row.get(column)
            try:
                values.append(float(raw))
            except (TypeError, ValueError):
                pass
        return values

    def _paired(self, col_a: str, col_b: str) -> list[tuple[float, float]]:
        pairs = []
        for row in self._data:
            try:
                a = float(row.get(col_a))
                b = float(row.get(col_b))
                pairs.append((a, b))
            except (TypeError, ValueError):
                pass
        return pairs

    @staticmethod
    def _stats(values: list[float]) -> dict[str, float]:
        n = len(values)
        if n == 0:
            return {}
        sorted_vals = sorted(values)
        mean = sum(values) / n
        variance = sum((x - mean) ** 2 for x in values) / (n - 1) if n > 1 else 0.0
        std = math.sqrt(variance)

        def quantile(p: float) -> float:
            pos = p * (n - 1)
            lo, hi = int(pos), min(int(pos) + 1, n - 1)
            return sorted_vals[lo] + (pos - lo) * (sorted_vals[hi] - sorted_vals[lo])

        return {
            "count": float(n),
            "mean": mean,
            "std": std,
            "min": sorted_vals[0],
            "q1": quantile(0.25),
            "median": quantile(0.50),
            "q3": quantile(0.75),
            "max": sorted_vals[-1],
        }

    @staticmethod
    def _pearson(xs: list[float], ys: list[float]) -> Optional[float]:
        n = len(xs)
        if n < 2:
            return None
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        std_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
        std_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
        if std_x == 0 or std_y == 0:
            return None
        return cov / (std_x * std_y)
