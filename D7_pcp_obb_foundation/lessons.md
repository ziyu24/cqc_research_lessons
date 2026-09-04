# D7_pcp_obb_foundation 避坑点

审计基线：`ziyu24/D7_pcp_obb_foundation@84da96973a464562cd965fbb0c9759a25bae5a58`

## D7-01 数值支持未收敛不是科学负结果

- 类型：协议/实现无效。
- 为何失败：r009/r010 的 Sobol 或方向数收敛差仍超过 `1%`，边界命中且稀疏 hull 不合法；这说明数值支撑未闭合，不能判定科学方法好坏。
- 避坑：先满足冻结数值误差和边界门，再比较方法；不得靠提高方向数、删除难例或只报 aggregate 规避。
- 边界：方法效果保持未知，数值实现本身需新任务重构。
- 证据：`ziyu24/D7_pcp_obb_foundation@84da96973a464562cd965fbb0c9759a25bae5a58` 的 `lab/failed_methods.md`、`lab/result.md`。

## D7-02 不存在的适配器不能冒充强基线

- 类型：协议/实现无效。
- 为何失败：r008 要求的 no-pose EAV adapter 实际不存在；用普通方法改名不能形成与主路线匹配的强对照。
- 避坑：基线在预注册前必须有可执行代码、方法身份和输入输出闭环；找不到就报告资产缺口。
- 边界：不否定 EAV 概念，只否定该轮基线声明。
- 证据：`ziyu24/D7_pcp_obb_foundation@84da96973a464562cd965fbb0c9759a25bae5a58` 的 `lab/failed_methods.md`。

## D7-03 固定网格与样本预算冲突时先判协议不可行

- 类型：协议/实现无效。
- 为何失败：r007 在冻结网格和预算下理论支持至多为 4，却要求更高支持，DOTA H1-Q2 无法满足。
- 避坑：在运行前用组合计数或上界证明门可达；不可达不靠改规则或数据后沿用同一任务。
- 边界：这不是 DOTA 上方法性能失败。
- 证据：`ziyu24/D7_pcp_obb_foundation@84da96973a464562cd965fbb0c9759a25bae5a58` 的 `lab/failed_methods.md`。

## D7-04 已被后续修复的资产缺口不得继续列为失败

- 类型：历史结论已推翻。
- 为何失败：r004 的旧资产缺口已被 r006 纠正；继续引用旧阻塞会让后续任务重复停在已不存在的问题。
- 避坑：每个条目标注 superseding 证据；修复后保留“为何旧结论无效”，但不再作为当前门。
- 边界：只撤销资产阻塞，不自动证明科学路线成立。
- 证据：`ziyu24/D7_pcp_obb_foundation@84da96973a464562cd965fbb0c9759a25bae5a58` 的 `lab/failed_methods.md`、`lab/result.md`。

## D7-05 只在少数 detector 稳定的决策反转不能宣称家族规律

- 类型：科学证伪。
- 为何失败：LTT/DOTA 决策反转仅在 3 个 detector 中 1 个成立，没有稳定 family 证据；追加数据集、网格或 gate 不能把选择性结果变成机制。
- 避坑：家族主张要求预先冻结的多 detector 同向复现；否则收窄为单模型观察或停止。
- 边界：单个 detector 的现象可以报告，但不支持通用方法。
- 证据：`ziyu24/D7_pcp_obb_foundation@84da96973a464562cd965fbb0c9759a25bae5a58` 的 `lab/failed_methods.md`、`doc/reports/FINAL_PROJECT_REPORT.md`。

## D7-06 通用 tiling/fusion 组件不能靠组合获得新颖性

- 类型：科学证伪。
- 为何失败：tiling、union、NMS、WBF、boundary 与 TTA fusion 都已有直接先验；Möbius/Atlas CP 也与先前工作正面碰撞。
- 避坑：组合前做不可归约检查；若核心只剩现有算子串联，作为基线或工程实现，不作为主贡献。
- 边界：组件仍可用于系统实现。
- 证据：`ziyu24/D7_pcp_obb_foundation@84da96973a464562cd965fbb0c9759a25bae5a58` 的 `lab/failed_methods.md`、`doc/reports/D1_TERMINAL_DECISION.md`。

## D7-07 discordant 支持不足时不得降低阈值挽救切换策略

- 类型：科学证伪。
- 为何失败：capture-history switching 只有 30 个 discordant 单位，低于预注册 100；数据不支持可靠判断策略切换。
- 避坑：按独立决策单位做功效/支持审计；不足时停止，不改阈值、不换 score proxy、不用 fusion 制造样本。
- 边界：只否定该载体和支持规模，不否定所有历史切换决策。
- 证据：`ziyu24/D7_pcp_obb_foundation@84da96973a464562cd965fbb0c9759a25bae5a58` 的 `lab/failed_methods.md`、`doc/reports/D1_FINAL_APPEAL_TERMINAL_DECISION.md`。
