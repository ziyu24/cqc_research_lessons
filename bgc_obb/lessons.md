# bgc_obb 避坑点

审计基线：`ziyu24/bgc_obb@ebfa89e77c7d831bf521cad48d652fa1de123bf5`

## BGC-01 小型 toy 相关不能替代全量信号验证

- 类型：科学证伪。
- 为何失败：toy 子集曾出现 Spearman `+0.073` 的弱正号，但全量、多层和分组结果大多接近零，未达到预注册 `0.15`；正号来自低样本噪声，不能说明冲突分数具有排序能力。
- 避坑：先冻结最低相关阈值并在全量独立单位上验证；toy 只用于实现冒烟，不用于决定是否扩展方法。
- 边界：只否定当前 BGC 冲突观测量，不否定所有梯度冲突或难例度量。
- 证据：`ziyu24/bgc_obb@ebfa89e77c7d831bf521cad48d652fa1de123bf5` 的 `decisions/A1_BGC_final_failure_summary_2026-05-12.md`、`results/d7_toy_redo/summary.json`。

## BGC-02 先隔离“信号无效”与“重加权损伤”

- 类型：范围限制。
- 为何失败：被动 BGC 在权重恒为 1 时保持 vanilla 性能，却仍只有约 `0.023` 的相关；这说明主失败在 `G_conflict` 信号，而不是重加权器把好信号用坏。
- 避坑：候选分数失败时先跑不改变训练的被动读出和恒等权重对照，再决定是否调优化器或权重函数。
- 边界：该诊断不证明所有主动重加权都无效，只禁止用调权重掩盖当前信号失效。
- 证据：`ziyu24/bgc_obb@ebfa89e77c7d831bf521cad48d652fa1de123bf5` 的 `decisions/A1_BGC_final_failure_summary_2026-05-12.md`、`results/E2_passive_bgc.md`。

## BGC-03 候选全负后不得继续阈值购物

- 类型：科学证伪。
- 为何失败：所有 BGC 变体均低于 vanilla，最优 LE 仍约低 `0.66` AP 点；即使换成更含角度信息的检测器，最佳子集相关也只有 `0.107`，仍未过门。
- 避坑：当冻结候选矩阵方向一致为负且强诊断仍不过门时停止，不再调 `tau`、gate、warmup 或选择有利子集。
- 边界：结论限于该项目冻结的数据、检测器、分数和训练协议。
- 证据：`ziyu24/bgc_obb@ebfa89e77c7d831bf521cad48d652fa1de123bf5` 的 `decisions/A1_BGC_final_failure_summary_2026-05-12.md`、`decisions/D-2A-failure-2026-05-12.md`。
