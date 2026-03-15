"""数据加载模块 / Data loading module"""

import json
import csv
import os
from typing import Optional


class DataLoader:
    """支持从 CSV 和 JSON 文件加载数据 / Loads data from CSV and JSON files."""

    SUPPORTED_FORMATS = (".csv", ".json")

    def load(self, filepath: str) -> list[dict]:
        """
        从文件加载数据 / Load data from a file.

        Args:
            filepath: Path to the data file (CSV or JSON).

        Returns:
            A list of dicts representing rows of data.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is not supported.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件未找到 / File not found: {filepath}")

        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".csv":
            return self._load_csv(filepath)
        elif ext == ".json":
            return self._load_json(filepath)
        else:
            raise ValueError(
                f"不支持的文件格式 / Unsupported format: {ext}. "
                f"支持的格式 / Supported: {self.SUPPORTED_FORMATS}"
            )

    def _load_csv(self, filepath: str) -> list[dict]:
        rows = []
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
        return rows

    def _load_json(self, filepath: str) -> list[dict]:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            # Support {"data": [...]} wrapper format
            for key in ("data", "records", "rows"):
                if key in data and isinstance(data[key], list):
                    return data[key]
            return [data]
        raise ValueError("JSON 文件格式无效 / Invalid JSON format: expected list or dict.")
