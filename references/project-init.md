# 阶段 -1：项目目录初始化

> 仅在翻译整本书籍/文件时执行。聊天小段翻译跳过。

## 准入 / 准出

- ⚠ **准入：** 用户已提供待翻译内容（文件路径或直接文本）。无输入 = 退回用户索取。
- ✅ **准出：** `source/` 目录存在、原始文件已移入、提取产物已生成、归位验证三项断言全部通过。

## 步骤 1：创建项目目录与子目录

```python
import os, shutil

# 确定源文件所在目录（通常是 Downloads）
src_dir = r'./Downloads'  # 替换为源文件所在目录
book_name = '《项目书籍名称》'           # ← 替换为实际书名
project_dir = os.path.join(src_dir, book_name)
source_dir = os.path.join(project_dir, 'source')
bilingual_dir = os.path.join(project_dir, 'bilingual')

os.makedirs(source_dir, exist_ok=True)
os.makedirs(bilingual_dir, exist_ok=True)
```

## 步骤 2：将原始电子书移入 source/

```python
# 找到原始电子书文件（epub/mobi/azw3/pdf/docx），移入 source/
original_file = os.path.join(src_dir, '原书名.epub')   # ← 替换为实际文件名
target_path = os.path.join(source_dir, os.path.basename(original_file))
shutil.move(original_file, target_path)
print(f'原始文件已移至: {target_path}')
```

> ⚠ **必须用 `shutil.move`（移动），不是 `shutil.copy`（复制）。** 移动后源文件所在目录的根层级不应残留原始电子书。如原始文件在子目录中，同样移入 `source/`。

## 步骤 3：从 source/ 内的文件提取文本

所有提取/转换操作以 `source_dir` 内的文件为输入，提取产物也写入 `source_dir`。**禁止**直接从 Downloads 根目录的文件提取——先移后提。

```python
# 示例：从 EPUB 提取文本为 Markdown（产物写入 source/）
import subprocess

epub_path = os.path.join(source_dir, '原书名.epub')
md_path = os.path.join(source_dir, '原书名.md')
pandoc = r'C:\pandoc-3.9\pandoc.exe'
subprocess.run([pandoc, epub_path, '-t', 'markdown', '--wrap=none', '-o', md_path], check=True)
print(f'Markdown 已转换: {md_path}')
```

其他格式的提取命令：

| 格式 | 工具 | 命令要点 |
|------|------|---------|
| `.epub` | Pandoc | `-t markdown --wrap=none`，保留标题层级 |
| `.docx` / `.html` / `.md` | Pandoc | 同上 |
| `.azw3` | Calibre `ebook-convert` | `D:\Calibre\Calibre Portable\Calibre\ebook-convert.exe` |
| `.mobi` | Python `mobi` 模块 | 输出 Markdown，保留标题层级；详见 `references/mobi-extraction.md` |

## 步骤 4：归位验证 ★ 落盘前必检

```python
# 验证：原始文件已在 source/ 内，根层级无残留
root_files = os.listdir(src_dir)
source_files = os.listdir(source_dir)

# 检查 1：原始电子书在 source/ 内
orig_name = os.path.basename(original_file)
assert orig_name in source_files, \
    f'❌ 原始文件未移入 source/：{orig_name}'

# 检查 2：根层级无同名残留
residual = [f for f in root_files if f == orig_name]
assert len(residual) == 0, f'❌ 原始文件残留在根层级：{residual}'

# 检查 3：提取产物无散落（根层级不应出现与书名相关的 txt/md/html）
extracted = [f for f in root_files
             if f.endswith(('.txt', '.md', '.html'))
             and book_name[1:-1] in f]
assert len(extracted) == 0, f'❌ 提取文件散落在根层级：{extracted}'

print('✅ 文件归位验证通过')
```

## 完成后的目标目录结构

```
源文件所在目录（如 Downloads）/
  └── 《项目书籍名称》/
      ├── source/                          ← 原始电子书 + 提取文本/切割文件
      │   ├── 原书名.epub                  ← 移入的原始文件
      │   ├── 原书名.md                   ← Pandoc 抽出 Markdown
      │   └── ...
      ├── bilingual/                       ← 子代理原始产出（并行翻译时）
      ├── 《书名》 翻译(中英对照).md
      ├── 《书名》 翻译(中英对照).html
      ├── 《书名》 翻译(全中文).md         （可选，脚本派生）
      ├── 《书名》 译文.epub              （全文翻译时）
      └── 《书名》 译文.mobi              （全文翻译时）
```

- 文件夹名用中文书名
- **任何文件不得散落在源文件所在目录的根层级**
- **并行翻译时**：delegate_task 的 `context` 中必须传递正确的 `project_dir` 路径，不要传给子代理 Downloads 根目录路径
