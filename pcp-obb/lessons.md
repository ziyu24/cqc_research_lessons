# pcp-obb 避坑点

审计基线：`ziyu24/pcp-obb@f9a241f0b4c77f47b92b5559e10aef705e397175`

## PCP-01 线性角度 conformal score 会在周期边界折返

- 类型：科学证伪。
- 为何失败：把角度当普通实数做残差与区间，在 `0/π` 等价边界会把相近方向当成远离或生成错误覆盖集合，不能替代轴向商空间处理。
- 避坑：角度 score、距离和 canonicalization 都在 π-quotient 上定义，并用跨边界构造例测试。
- 边界：普通线性 conformal 对非周期变量仍可使用。
- 证据：`ziyu24/pcp-obb@f9a241f0b4c77f47b92b5559e10aef705e397175` 的 `lab/failed_methods.md`、`lab/result.md`。

## PCP-02 分桶最差覆盖失败要先检查有效样本数

- 类型：历史结论已推翻。
- 为何失败：HRSC WSC 曾被归因于高长宽比尾部，实际高 AR bins 样本充足且覆盖 `0.86/0.96`；瓶颈是 `[2,3)` 仅 31 个样本、coverage `0.2903` 的稀疏中等 AR bin。
- 避坑：报告每 bin 的样本数、排除规则和区间；不能仅凭 bin 标签或极端性解释最差覆盖。
- 边界：这不使 WSC 自动通过，只修正失败机制归因。
- 证据：`ziyu24/pcp-obb@f9a241f0b4c77f47b92b5559e10aef705e397175` 的 `doc/notes/wsc_failure_hrsc_per_bin.md`。
