"""Build a readable progress overview from project pages; no polling or remote writes."""
from __future__ import annotations

import argparse
from pathlib import Path
import re

HEADINGS = ('最初科学问题', '核心进展', '服务器当前内容', '核验说明', '执行阶段', '下一步与维护', '证据')


def projects(root: Path) -> dict[str, tuple[str, str, str]]:
    rows = {}
    for line in (root / 'PROJECT_STATUS.md').read_text(encoding='utf-8').splitlines():
        if not line.startswith('| '):
            continue
        cells = [v.strip() for v in line.strip('|').split('|')]
        match = re.search(r'`([^`]+)`', cells[0])
        if match and len(cells) == 5:
            name = match.group(1)
            if name in rows:
                raise ValueError(f'项目重复：{name}')
            rows[name] = (cells[0].split('（')[0].strip('`'), cells[1], cells[2])
    if not rows:
        raise ValueError('项目总表为空')
    return rows


def sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r'^## (.+)$', text, re.M))
    data = {}
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        key = match.group(1)
        if key in data:
            raise ValueError(f'重复小节：{key}')
        data[key] = text[match.end():end].strip()
    if not matches or matches[0].group(1) != HEADINGS[0]:
        raise ValueError('首个小节必须是最初科学问题')
    for key in HEADINGS:
        if not data.get(key):
            raise ValueError(f'缺少内容：{key}')
    if not re.search(r'https://github\.com/ziyu24/[^\s)]+', data['证据']):
        raise ValueError('缺少可回读的来源链接')
    return data


def first(text: str) -> str:
    return text.split('\n\n')[0].replace('\n', ' ').replace('|', '／')


def overview(root: Path) -> str:
    rows = projects(root)
    pages = {p.stem for p in (root / 'progress').glob('*.md')} - {'README', 'INDEX'}
    if pages != set(rows):
        raise ValueError(f'进展页与总表不一致：缺少{sorted(set(rows)-pages)}，额外{sorted(pages-set(rows))}')
    text = ['# 当前项目核心进展', '', '本页由各项目进展页生成；只展示最后已观察的事实，不是实时监控，也不改变[项目级状态](../PROJECT_STATUS.md)。任务下发不等于已启动，执行结束不等于已充分核验。维护方式见[主动更新约定](README.md)。', '', '## 存活项目', '', '| 项目 | 当前最核心进展 | 执行阶段（带观察时间） |', '| --- | --- | --- |']
    historical = []
    for name, (label, question, status) in rows.items():
        data = sections((root / 'progress' / f'{name}.md').read_text(encoding='utf-8'))
        if first(data['最初科学问题']) != question:
            raise ValueError(f'{name}：最初问题与项目总表不一致，须凭原始证据同步修订')
        link = f'[{label}]({name}.md)'
        if status in {'失败', '成功', '已结束'}:
            historical.append(f'- {link}：{status}。')
        else:
            text.append(f'| {link} | {first(data["核心进展"])} | {first(data["执行阶段"])} |')
    text.extend(['', '## 已结束及历史项目', '', '以下仅保留本库已有登记与来源摘要；建立页面不恢复维护，也不进入停止维护仓库。', '', *historical, ''])
    return '\n'.join(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path('.'))
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        content = overview(args.root)
        path = args.root / 'progress/INDEX.md'
        if args.check:
            if not path.is_file() or path.read_text(encoding='utf-8') != content:
                raise ValueError('总览未同步：运行 python tools/progress.py .')
        else:
            path.write_text(content, encoding='utf-8', newline='\n')
    except (ValueError, OSError) as error:
        print(error)
        return 1
    print('PROGRESS VALID')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
