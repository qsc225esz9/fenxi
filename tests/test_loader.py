"""Tests for DataLoader."""

import json
import os
import tempfile
import pytest

from fenxi.loader import DataLoader


@pytest.fixture
def loader():
    return DataLoader()


@pytest.fixture
def csv_file(tmp_path):
    f = tmp_path / "test.csv"
    f.write_text("name,age,score\nAlice,30,95\nBob,25,80\nCarol,35,88\n", encoding="utf-8")
    return str(f)


@pytest.fixture
def json_file(tmp_path):
    f = tmp_path / "test.json"
    data = [
        {"name": "Alice", "age": 30, "score": 95},
        {"name": "Bob", "age": 25, "score": 80},
    ]
    f.write_text(json.dumps(data), encoding="utf-8")
    return str(f)


@pytest.fixture
def json_wrapped_file(tmp_path):
    f = tmp_path / "wrapped.json"
    data = {"data": [{"x": 1}, {"x": 2}]}
    f.write_text(json.dumps(data), encoding="utf-8")
    return str(f)


class TestDataLoaderCSV:
    def test_load_csv_returns_list_of_dicts(self, loader, csv_file):
        data = loader.load(csv_file)
        assert isinstance(data, list)
        assert len(data) == 3

    def test_load_csv_correct_keys(self, loader, csv_file):
        data = loader.load(csv_file)
        assert set(data[0].keys()) == {"name", "age", "score"}

    def test_load_csv_correct_values(self, loader, csv_file):
        data = loader.load(csv_file)
        assert data[0]["name"] == "Alice"
        assert data[0]["age"] == "30"  # CSV values are strings

    def test_load_csv_all_rows(self, loader, csv_file):
        data = loader.load(csv_file)
        names = [row["name"] for row in data]
        assert names == ["Alice", "Bob", "Carol"]


class TestDataLoaderJSON:
    def test_load_json_list(self, loader, json_file):
        data = loader.load(json_file)
        assert isinstance(data, list)
        assert len(data) == 2

    def test_load_json_values(self, loader, json_file):
        data = loader.load(json_file)
        assert data[0]["name"] == "Alice"
        assert data[0]["age"] == 30

    def test_load_json_wrapped(self, loader, json_wrapped_file):
        data = loader.load(json_wrapped_file)
        assert isinstance(data, list)
        assert data[0]["x"] == 1


class TestDataLoaderErrors:
    def test_file_not_found(self, loader):
        with pytest.raises(FileNotFoundError):
            loader.load("/nonexistent/path/file.csv")

    def test_unsupported_format(self, loader, tmp_path):
        f = tmp_path / "data.xlsx"
        f.write_text("dummy")
        with pytest.raises(ValueError, match="Unsupported format"):
            loader.load(str(f))

    def test_invalid_json(self, loader, tmp_path):
        f = tmp_path / "bad.json"
        f.write_text("not json", encoding="utf-8")
        with pytest.raises(Exception):
            loader.load(str(f))


class TestDataLoaderSampleFiles:
    """Test with the bundled sample data files."""

    def _sample_path(self, filename):
        here = os.path.dirname(__file__)
        return os.path.join(here, "..", "data", filename)

    def test_load_sample_csv(self, loader):
        path = self._sample_path("sample.csv")
        data = loader.load(path)
        assert len(data) == 30
        assert "age" in data[0]

    def test_load_cities_json(self, loader):
        path = self._sample_path("cities.json")
        data = loader.load(path)
        assert len(data) == 10
        assert "city" in data[0]
