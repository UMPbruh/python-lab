"""文本统计小工具：统计行数、字符数、词数、中文字数，并支持关键词搜索。

作为 Python 实验模板使用：
- 逻辑放在可导入的函数里（方便单元测试），命令行只是外壳；
- 只依赖标准库。

用法：
    python textstat.py demo.txt
    python textstat.py demo.txt --keyword 汉化
    python textstat.py demo.txt --json out.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

# 连续的中日韩统一表意文字算 1 个"汉字"
CJK_PATTERN = re.compile(r"[\u4e00-\u9fff]")
# 英文/数字词：把连续字母数字下划线算一个词
WORD_PATTERN = re.compile(r"[A-Za-z0-9_]+")


@dataclass
class TextStats:
    """统计结果。dataclass 自带 __init__/__eq__/__repr__，测试里比较很方便。"""

    path: str
    total_lines: int
    non_empty_lines: int
    chars: int
    chars_no_space: int
    words: int
    cjk_chars: int

    @property
    def average_line_length(self) -> float:
        if self.total_lines == 0:
            return 0.0
        return round(self.chars / self.total_lines, 2)


def parse_lines(lines: list[str], path: str = "<memory>") -> TextStats:
    """对已经读进来的文本行做统计（纯函数，不碰文件系统）。"""
    text = "\n".join(lines)
    return TextStats(
        path=path,
        total_lines=len(lines),
        non_empty_lines=sum(1 for line in lines if line.strip()),
        chars=len(text),
        chars_no_space=len(re.sub(r"\s", "", text)),
        words=len(WORD_PATTERN.findall(text)),
        cjk_chars=len(CJK_PATTERN.findall(text)),
    )


def read_text(path: Path) -> list[str]:
    """读文本并按行拆开。编码失败时给出人话提示，而不是抛一堆栈。"""
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"找不到文件：{path}") from None
    except UnicodeDecodeError as exc:
        raise SystemExit(
            f"按 UTF-8 解码失败（{exc}）。文件可能是 GBK/GB18030 编码，"
            f"可改用 encoding='gb18030' 再试。"
        ) from None
    return content.splitlines()


def find_keyword(lines: list[str], keyword: str, *, ignore_case: bool = True) -> list[tuple[int, str]]:
    """返回 [(行号从1开始, 该行内容)]，方便打印上下文。"""
    needle = keyword.lower() if ignore_case else keyword
    hits: list[tuple[int, str]] = []
    for number, line in enumerate(lines, start=1):
        haystack = line.lower() if ignore_case else line
        if needle in haystack:
            hits.append((number, line))
    return hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="统计文本文件的行/字/词数")
    parser.add_argument("path", type=Path, help="要统计的文本文件（UTF-8）")
    parser.add_argument("--keyword", "-k", help="在文件中搜索这个关键词并打印所在行")
    parser.add_argument("--json", type=Path, help="把统计结果另存为 JSON")
    args = parser.parse_args(argv)

    lines = read_text(args.path)
    stats = parse_lines(lines, path=str(args.path))

    print(f"文件：{stats.path}")
    print(f"总行数：{stats.total_lines}（非空 {stats.non_empty_lines}）")
    print(f"字符数：{stats.chars}（不含空白 {stats.chars_no_space}）")
    print(f"英文/数字词数：{stats.words}")
    print(f"汉字数：{stats.cjk_chars}")
    print(f"平均行长：{stats.average_line_length}")

    if args.keyword:
        hits = find_keyword(lines, args.keyword)
        print(f"\n关键词「{args.keyword}」命中 {len(hits)} 行：")
        for number, line in hits[:20]:
            print(f"  {number:>5}| {line.strip()}")
        if len(hits) > 20:
            print(f"  ...（还有 {len(hits) - 20} 行未显示）")

    if args.json:
        payload = asdict(stats) | {"average_line_length": stats.average_line_length}
        args.json.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"\n已写入 {args.json}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
