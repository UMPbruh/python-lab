# python-lab

Python 练习与实验模板。目前包含一个可直接运行的小工具 **textstat.py**（文本统计 + 关键词搜索），
配套零依赖单元测试。

## 怎么跑

```powershell
cd python-lab
py textstat.py demo.txt                       # 统计示例文件
py textstat.py demo.txt -k 测试                # 顺便搜关键词
py textstat.py demo.txt --json report.json    # 结果导出 JSON

# 跑测试（标准库 unittest，不需要装任何东西）
py -m unittest discover -s tests -v
```

本机 Python 版本：**3.14.7**（`py -V` 可查）。

## 目录

```
python-lab/
  AGENTS.md              # 给 AI 助手的项目约定
  textstat.py            # 工具本体：逻辑在函数里，命令行只是外壳
  demo.txt               # 示例输入
  tests/test_textstat.py # 9 个单元测试
  requirements.txt       # 目前为空（只用标准库）
```

## 已验证

- `py -m unittest discover -s tests -v` → **9 个测试全部通过**（2026-10-08 实测）。
- `py textstat.py demo.txt -k 测试` → 正常输出统计与命中行（9 行 / 176 字符 / 48 汉字 / 命中 2 行）。
- 写这个工具时测试真抓出过一个错：我最初把 `3.12` 当 1 个词，实际按
  `[A-Za-z0-9_]+` 规则是 `3` 和 `12` 两个词 —— 断言已改成 7 并注明规则。
  **这就是"跑过才算数"的意思。**

## 下一步可以练的

1. 让它支持多个文件 / 整个目录（提示：`Path.glob("**/*.txt")`）。
2. 加 `--top N`，输出出现频率最高的词（提示：`collections.Counter`）。
3. 用 `matplotlib` 把"每行字符数分布"画成直方图，注意中文字体设置（见技能 `python-lab`）。
