"""textstat 的单元测试。零第三方依赖，直接跑：

    cd python-lab
    python -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

# 让 tests/ 目录下的测试能 import 到上一级的 textstat.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import textstat  # noqa: E402


class TestParseLines(unittest.TestCase):
    def test_empty_input(self):
        stats = textstat.parse_lines([])
        self.assertEqual(stats.total_lines, 0)
        self.assertEqual(stats.chars, 0)
        self.assertEqual(stats.average_line_length, 0.0)

    def test_counts_english_words(self):
        stats = textstat.parse_lines(["hello world", "python 3.12 is fun"])
        self.assertEqual(stats.total_lines, 2)
        # 词的定义是 [A-Za-z0-9_]+：python / 3 / 12 / is / fun，共 5 个；
        # 小数点和空格一样算分隔符，这是我们有意选择的简单规则。
        self.assertEqual(stats.words, 7)          # hello world + python 3 12 is fun
        self.assertEqual(stats.non_empty_lines, 2)

    def test_counts_cjk(self):
        stats = textstat.parse_lines(["你好，世界", "汉化测试"])
        self.assertEqual(stats.cjk_chars, 8)

    def test_blank_lines_are_counted_but_not_non_empty(self):
        stats = textstat.parse_lines(["a", "", "   ", "b"])
        self.assertEqual(stats.total_lines, 4)
        self.assertEqual(stats.non_empty_lines, 2)


class TestFindKeyword(unittest.TestCase):
    def test_case_insensitive_by_default(self):
        self.assertEqual(
            textstat.find_keyword(["Hello", "world"], "hello"),
            [(1, "Hello")],
        )

    def test_respects_case_when_asked(self):
        self.assertEqual(textstat.find_keyword(["Hello"], "hello", ignore_case=False), [])

    def test_line_numbers_start_at_one(self):
        hits = textstat.find_keyword(["x", "x"], "x")
        self.assertEqual([number for number, _ in hits], [1, 2])


class TestFileRoundTrip(unittest.TestCase):
    def test_read_and_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "sample.txt"
            src.write_text("你好 world\n第二行\n", encoding="utf-8")

            lines = textstat.read_text(src)
            self.assertEqual(lines, ["你好 world", "第二行"])

            out = Path(tmp) / "out.json"
            self.assertEqual(textstat.main([str(src), "--json", str(out)]), 0)

            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["total_lines"], 2)
            self.assertEqual(payload["cjk_chars"], 5)   # 你好 + 第二行

    def test_missing_file_exits_with_message(self):
        with self.assertRaises(SystemExit):
            textstat.read_text(Path("definitely-not-here.txt"))


if __name__ == "__main__":
    unittest.main()
