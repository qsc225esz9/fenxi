"""Tests for DataAnalyzer."""

import math
import pytest

from fenxi.analyzer import DataAnalyzer


@pytest.fixture
def sample_data():
    return [
        {"name": "Alice", "age": "30", "salary": "70000", "dept": "Eng"},
        {"name": "Bob", "age": "25", "salary": "55000", "dept": "Sales"},
        {"name": "Carol", "age": "35", "salary": "85000", "dept": "Eng"},
        {"name": "Dave", "age": "28", "salary": "60000", "dept": "Sales"},
        {"name": "Eve", "age": "40", "salary": "95000", "dept": "Mgmt"},
    ]


@pytest.fixture
def analyzer(sample_data):
    return DataAnalyzer(sample_data)


class TestDataAnalyzerInit:
    def test_empty_data_raises(self):
        with pytest.raises(ValueError, match="empty"):
            DataAnalyzer([])

    def test_columns(self, analyzer):
        assert "age" in analyzer.columns
        assert "salary" in analyzer.columns

    def test_row_count(self, analyzer):
        assert analyzer.row_count == 5


class TestNumericColumns:
    def test_identifies_numeric_columns(self, analyzer):
        numeric = analyzer.numeric_columns()
        assert "age" in numeric
        assert "salary" in numeric

    def test_excludes_text_columns(self, analyzer):
        numeric = analyzer.numeric_columns()
        assert "name" not in numeric
        assert "dept" not in numeric


class TestDescribe:
    def test_describe_returns_stats(self, analyzer):
        stats = analyzer.describe()
        assert "age" in stats
        assert "salary" in stats

    def test_describe_count(self, analyzer):
        stats = analyzer.describe()
        assert stats["age"]["count"] == 5

    def test_describe_mean_age(self, analyzer):
        stats = analyzer.describe()
        expected_mean = (30 + 25 + 35 + 28 + 40) / 5
        assert abs(stats["age"]["mean"] - expected_mean) < 1e-9

    def test_describe_min_max(self, analyzer):
        stats = analyzer.describe()
        assert stats["age"]["min"] == 25.0
        assert stats["age"]["max"] == 40.0

    def test_describe_median(self, analyzer):
        stats = analyzer.describe()
        # Sorted ages: 25, 28, 30, 35, 40 → median = 30
        assert stats["age"]["median"] == 30.0

    def test_describe_std(self, analyzer):
        stats = analyzer.describe()
        ages = [30, 25, 35, 28, 40]
        mean = sum(ages) / len(ages)
        expected_std = math.sqrt(sum((x - mean) ** 2 for x in ages) / (len(ages) - 1))
        assert abs(stats["age"]["std"] - expected_std) < 1e-9

    def test_describe_no_numeric_columns(self):
        data = [{"name": "Alice"}, {"name": "Bob"}]
        analyzer = DataAnalyzer(data)
        assert analyzer.describe() == {}


class TestCorrelation:
    def test_perfect_positive_correlation(self):
        data = [{"x": str(i), "y": str(i)} for i in range(1, 6)]
        analyzer = DataAnalyzer(data)
        r = analyzer.correlation("x", "y")
        assert abs(r - 1.0) < 1e-9

    def test_perfect_negative_correlation(self):
        data = [{"x": str(i), "y": str(-i)} for i in range(1, 6)]
        analyzer = DataAnalyzer(data)
        r = analyzer.correlation("x", "y")
        assert abs(r + 1.0) < 1e-9

    def test_zero_variance_returns_none(self):
        data = [{"x": "5", "y": str(i)} for i in range(1, 6)]
        analyzer = DataAnalyzer(data)
        assert analyzer.correlation("x", "y") is None

    def test_correlation_symmetric(self, analyzer):
        r_ab = analyzer.correlation("age", "salary")
        r_ba = analyzer.correlation("salary", "age")
        assert abs(r_ab - r_ba) < 1e-9

    def test_correlation_range(self, analyzer):
        r = analyzer.correlation("age", "salary")
        assert r is not None
        assert -1.0 <= r <= 1.0


class TestCorrelationMatrix:
    def test_matrix_shape(self, analyzer):
        matrix = analyzer.correlation_matrix()
        numeric_cols = analyzer.numeric_columns()
        assert set(matrix.keys()) == set(numeric_cols)
        for col in numeric_cols:
            assert set(matrix[col].keys()) == set(numeric_cols)

    def test_diagonal_is_one(self, analyzer):
        matrix = analyzer.correlation_matrix()
        for col in analyzer.numeric_columns():
            assert matrix[col][col] == 1.0


class TestGetNumericValues:
    def test_returns_list_of_floats(self, analyzer):
        values = analyzer.get_numeric_values("age")
        assert isinstance(values, list)
        assert all(isinstance(v, float) for v in values)
        assert len(values) == 5

    def test_skips_non_numeric(self):
        data = [{"x": "1"}, {"x": "abc"}, {"x": "3"}]
        analyzer = DataAnalyzer(data)
        assert analyzer.get_numeric_values("x") == [1.0, 3.0]

    def test_invalid_column_raises(self, analyzer):
        with pytest.raises(KeyError):
            analyzer.get_numeric_values("nonexistent")


class TestValueCounts:
    def test_value_counts_returns_counts(self, analyzer):
        counts = analyzer.value_counts("dept")
        assert counts["Eng"] == 2
        assert counts["Sales"] == 2
        assert counts["Mgmt"] == 1

    def test_value_counts_sorted_descending(self, analyzer):
        counts = analyzer.value_counts("dept")
        values = list(counts.values())
        assert values == sorted(values, reverse=True)

    def test_value_counts_invalid_column(self, analyzer):
        with pytest.raises(KeyError):
            analyzer.value_counts("nonexistent")
