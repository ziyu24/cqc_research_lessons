# pcp-obb-score-study 避坑点

审计基线：`ziyu24/pcp-obb-score-study@0df97a23936c0893704f8cf03c652625522060f9`

## PCPSCORE-01 新构造得到更松界不能写成性能改进

- 类型：科学证伪。
- 为何失败：S1 方案 (c) 的结果明确为 `LOOSER`，没有得到更紧的 score/coverage 界。
- 避坑：预先确定“更紧/更松”的方向与单位；负结果原样进入正文或失败记录，不用新颖构造替代效果。
- 边界：只否定方案 (c)，不抹除项目其他 score 比较与统计结果。
- 证据：`ziyu24/pcp-obb-score-study@0df97a23936c0893704f8cf03c652625522060f9` 的 `lab/failed_methods.md`、`lab/result.md`。
