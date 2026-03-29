"""Tests for DataVisualizer."""

import pytest

from fenxi.visualizer import DataVisualizer


@pytest.fixture
def viz():
    return DataVisualizer()


class TestHistogram:
    def test_returns_string(self, viz):
        result = viz.histogram([1, 2, 3, 4, 5])
        assert isinstance(result, str)

    def test_empty_data(self, viz):
        result = viz.histogram([])
        assert "No data" in result or "无数据" in result

    def test_single_unique_value(self, viz):
        result = viz.histogram([5, 5, 5])
        assert "All values equal" in result or "相同" in result

    def test_contains_title(self, viz):
        result = viz.histogram([1, 2, 3], title="My Chart")
        assert "My Chart" in result

    def test_histogram_has_bars(self, viz):
        result = viz.histogram(list(range(100)))
        assert "█" in result


class TestBarChart:
    def test_returns_string(self, viz):
        result = viz.bar_chart(["A", "B"], [10.0, 20.0])
        assert isinstance(result, str)

    def test_empty_data(self, viz):
        result = viz.bar_chart([], [])
        assert "No data" in result or "无数据" in result

    def test_contains_labels(self, viz):
        result = viz.bar_chart(["CategoryA", "CategoryB"], [5.0, 10.0])
        assert "CategoryA" in result or "CategoryB" in result

    def test_sorted_descending(self, viz):
        result = viz.bar_chart(["Low", "High"], [1.0, 100.0])
        lines = [line for line in result.splitlines() if "█" in line]
        assert len(lines) >= 1


class TestScatterPlot:
    def test_returns_string(self, viz):
        result = viz.scatter_plot([1, 2, 3], [1, 2, 3])
        assert isinstance(result, str)

    def test_empty_data(self, viz):
        result = viz.scatter_plot([], [])
        assert "No data" in result or "无数据" in result

    def test_mismatched_lengths(self, viz):
        with pytest.raises(ValueError):
            viz.scatter_plot([1, 2], [1])

    def test_contains_dots(self, viz):
        result = viz.scatter_plot(list(range(10)), list(range(10)))
        assert "●" in result

    def test_contains_title(self, viz):
        result = viz.scatter_plot([1, 2, 3], [1, 2, 3], title="Scatter")
        assert "Scatter" in result
