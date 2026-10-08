# Python 练习项目约定

- 每个练习尽量独立、可单独运行：`python <脚本>.py <参数>`。
- 不引入重型框架；能用标准库就用标准库。需要第三方库时写进 `requirements.txt` 并说明用途。
- 路径统一 `pathlib.Path`；读写文本显式 `encoding="utf-8"`。
- 新功能配一个 `tests/test_*.py`（标准库 `unittest`，零额外依赖），运行方式：
  ```powershell
  cd python-lab
  python -m unittest discover -s tests -v
  ```
- 中文输出乱码时先看控制台代码页，而不是改代码里的编码。
- 相关技能：`python-lab`、`code-review-student`。
