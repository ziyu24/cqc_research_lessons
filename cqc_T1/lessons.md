# cqc_T1 避坑点

审计基线：`ziyu24/cqc_T1@ffda4284e0183849d5287f931950aa5dad97ba66`

## T1-01 patch 指标与母图指标不能混用

- 类型：范围限制。
- 为何失败：同一模型的预切 patch AP 与 original-image 经映射、全局 NMS 后的 AP 属于不同评价空间；历史上把 `71.609` patch mAP 与 `61.430` mother AP07 直接比较会把口径差异误作 evaluator bug 或方法变化。
- 避坑：指标名必须携带 population、merge 和 evaluator；跨空间只作并列表，不算差值。
- 边界：各口径内部仍可公平比较冻结对照。
- 证据：`ziyu24/cqc_T1@ffda4284e0183849d5287f931950aa5dad97ba66` 的 `reports/partition_instability_top_journal_route.md`、`reports/dota10_evaluation_closure.md`。

## T1-02 低状态翻转可能是表示坍塌而非鲁棒

- 类型：科学证伪。
- 为何失败：SPEAR v3 把 incompatible flip 降到 0%，但 proposal R@0.3 只有全体 `3.679%`、敏感目标 `0.737%`，大量 tile 没有 proposal；稳定来自不再检测，而不是恢复目标。
- 避坑：鲁棒门必须与正常 recall、budget utilization 和强等算力对照合取；只看方差或翻转率会奖励坍塌。
- 边界：只否定冻结 SPEAR representation，不否定所有 phase-robust 表示。
- 证据：`ziyu24/cqc_T1@ffda4284e0183849d5287f931950aa5dad97ba66` 的 `reports/partition_instability_top_journal_route.md`、`reports/dota10_spear_stage_a.md`。

## T1-03 Oracle 或整图正参考不是可部署方法

- 类型：范围限制。
- 为何失败：多相位 oracle 和 whole-mother reference 证明信息或准确率上限，但 oracle 使用 GT 选择，whole-mother 需要约 10--12 GiB 且部分模型明显更慢；它们不能直接声称解决部署问题。
- 避坑：把上界、reference 和 deployable method 三层分开；方法还需无 GT、单次推理、内存和延迟门。
- 边界：正参考仍可证明问题存在并给候选设计上限。
- 证据：`ziyu24/cqc_T1@ffda4284e0183849d5287f931950aa5dad97ba66` 的 `reports/partition_instability_top_journal_route.md`、`reports/dota10_partition_free_reference.md`。

## T1-04 局部因果充分性不保证可学习的全局鲁棒性

- 类型：科学证伪。
- 为何失败：CPET 冻结特征干预在 111 个失败目标中恢复 48 个，显著胜控制；但 matched 训练后 selected 相对 P-ERM/hash 的 phase reduction 接近零且 bootstrap 下界为负。
- 避坑：局部替换实验通过后仍必须做匹配训练和完整 shift gate；不得把“某特征能救样本”直接写成“网络能学会鲁棒”。
- 边界：因果干预事实保留，只否定其当前训练转化路径。
- 证据：`ziyu24/cqc_T1@ffda4284e0183849d5287f931950aa5dad97ba66` 的 `reports/dota10_cpet_gate1.md`、`reports/dota10_cpet_formal_result.md`、`reports/dota10_cpet_phase_gate.md`。

## T1-05 精确输出和省显存必须与实际代价合取

- 类型：科学证伪。
- 为何失败：PNEE/流式和 liveness 路线有的能保持局部 exact，有的降低约 33% allocated memory，但在大图上仍超 6 GiB、reserved 不降或速度比基线慢数倍；cuDNN workspace cap 又没有额外收益。
- 避坑：部署候选同时冻结最终输出等价、峰值 allocated/reserved、端到端延迟和规模复杂度；一项通过不能覆盖其他项失败。
- 边界：约 33% 生命周期内存空间是真实工程线索，但不足以称部署闭合。
- 证据：`ziyu24/cqc_T1@ffda4284e0183849d5287f931950aa5dad97ba66` 的 `reports/partition_instability_top_journal_route.md`、`reports/dota10_pnee_p0b2_closure.md`。

## T1-06 实例效应不能扩大成 aggregate 或边界机制

- 类型：范围限制。
- 为何失败：SODA-A 的 physical-instance PIR 为 `4.2624%` 且 oracle recall 有余量，但 aggregate AP range 仅 `0.066394`；near-boundary 不比 central 差，crossing 样本又不足。
- 避坑：分别报告实例、总体性能和机制分层；某层成立不自动传播到另两层。
- 边界：跨数据集实例级 partition effect 可保留，boundary mechanism 在 SODA 上是不可评而非失败。
- 证据：`ziyu24/cqc_T1@ffda4284e0183849d5287f931950aa5dad97ba66` 的 `reports/partition_instability_top_journal_route.md`、`reports/second_large_dataset_audit.md`。
