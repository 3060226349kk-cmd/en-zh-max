#!/usr/bin/env python3
"""兼容入口：中文译文标点规范化。实际逻辑在同目录 check.py（三个翻译技能共用）。

用法：python3 本脚本 "<对照文件>.md"
打印「残留: N」；退出码 0 = 无残留，1 = 有残留。翻译腔信号请用 check.py zh 查看。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = sys.argv[1]
    text = check.fix_text('zh', check.read_text(src))
    Path(src).write_text(text, encoding='utf-8')
    left = check.count_residual('zh', text)
    print('残留:', left)
    return 0 if left == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
