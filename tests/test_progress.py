import tempfile
from pathlib import Path
import unittest

from tools.progress import HEADINGS, overview, sections


class ProgressTests(unittest.TestCase):
    def fixture(self, root):
        (root/'progress').mkdir()
        (root/'PROJECT_STATUS.md').write_text('| P1（`cqc_P1`） | 原问题 | 正在运行 | 2026-09-30 | 来源 |\n| P2（`cqc_P2`） | 旧问题 | 失败 | 2026-09-30 | 来源 |\n', encoding='utf-8')
        for name,question in [('cqc_P1','原问题'),('cqc_P2','旧问题')]:
            contents = dict.fromkeys(HEADINGS,'说明')
            contents.update({'最初科学问题':question,'执行阶段':'已下发；尚未确认启动。','证据':'[来源](https://github.com/ziyu24/'+name+'/blob/main/lab/result.md)'})
            (root/'progress'/f'{name}.md').write_text('\n\n'.join('## '+k+'\n\n'+v for k,v in contents.items()),encoding='utf-8')

    def test_ended_projects_not_listed_as_live(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);text=overview(root)
            active,historical=text.split('## 已结束及历史项目')
            self.assertIn('[P1](cqc_P1.md)',active)
            self.assertNotIn('[P2]',active)
            self.assertIn('[P2](cqc_P2.md)',historical)
            self.assertIn('尚未确认启动',active)

    def test_missing_page_and_changed_original_question_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);p=root/'progress/cqc_P1.md'
            p.write_text(p.read_text(encoding='utf-8').replace('原问题','新路线'),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'最初问题'):overview(root)
            p.unlink()
            with self.assertRaisesRegex(ValueError,'缺少'):overview(root)

    def test_missing_or_duplicate_evidence_sections_rejected(self):
        with self.assertRaisesRegex(ValueError,'首个小节'):sections('## 核心进展\n\n结果')
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);p=root/'progress/cqc_P1.md';text=p.read_text(encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'重复小节'):sections(text+'\n\n## 证据\n\n覆盖')
            with self.assertRaisesRegex(ValueError,'来源链接'):sections(text.replace('https://github.com/','https://invalid/'))

    def test_generator_preserves_project_pages(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root)
            before={p.name:p.read_bytes() for p in (root/'progress').glob('*.md')}
            self.assertEqual(overview(root),overview(root))
            self.assertEqual(before,{p.name:p.read_bytes() for p in (root/'progress').glob('*.md')})


if __name__=='__main__':unittest.main()
