# cqc_research_lessons 避坑点

审计基线：`ziyu24/cqc_research_lessons@23050e5502789845d8ea5a6e031f0083b5d478bb`

## LESSONS-01 没有真实内容前不要先造复杂卡片体系

- 类型：历史结论已推翻。
- 为何失败：旧仓库先建立六分类、二十余字段、YAML schema 和数百行防御式校验，却没有任何真实条目；贡献者既无法按项目找到内容，也会把维护格式当成主要工作。
- 避坑：按 GitHub 项目名建一级目录，每项目只用一个短 Markdown；索引和校验只覆盖可发现性、必要字段与来源提交。
- 边界：安全边界仍保留：不写秘密、绝对路径、大型产物或完整日志；简化不等于取消证据要求。
- 证据：`ziyu24/cqc_research_lessons@23050e5502789845d8ea5a6e031f0083b5d478bb` 的 `README.md`、`SCHEMA.yaml`、`INDEX.yaml`、`tools/validate.py`。
