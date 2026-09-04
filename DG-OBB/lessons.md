# DG-OBB 避坑点

审计基线：`ziyu24/DG-OBB@fe6edfa2c47aa5a94d8a0cb33ea4cf59016936e1`

## DG-01 类别映射错误会制造虚假的灾难性域差

- 类型：历史结论已推翻。
- 为何失败：旧 DOTA→DIOR 评估丢失类别名，mAP50 约 `0.0036`；修复映射后为 `0.6543`，相差超过 180 倍。原“灾难性 domain gap”是评估错误。
- 避坑：跨数据集前做逐类映射、perfect-GT 和 in-domain sanity；映射修复前的结果不得进入论文。
- 边界：修正不证明不存在真实域差，只撤销错误幅度和归因。
- 证据：`ziyu24/DG-OBB@fe6edfa2c47aa5a94d8a0cb33ea4cf59016936e1` 的 `lab/failed_methods.md`、`doc/legacy/final_discussion_report.md`。

## DG-02 数值有限不等于方法有信号

- 类型：科学证伪。
- 为何失败：FIFG 初版出现 NaN，finite-safe v2 虽消除非有限值但效果近零；修复数值稳定性没有恢复科学收益。
- 避坑：把 finite/gradient sanity 与性能门分开；修 NaN 后仍需重新通过冻结效果门。
- 边界：否定当前 FIFG 实现，不外推所有频域或梯度方法。
- 证据：`ziyu24/DG-OBB@fe6edfa2c47aa5a94d8a0cb33ea4cf59016936e1` 的 `lab/failed_methods.md`、`doc/legacy/p3_triple_prime_v2_finitesafe_max5_go_nogo_report.md`。

## DG-03 复杂模块若输给简单输入变换就没有独立贡献

- 类型：科学证伪。
- 为何失败：GCG 并非必要，resize-only A2 更强更简单，且 GCG crop 在 HRSC 上有害。
- 避坑：为复杂模块设置最小简单控制；若增益被 resize/crop 等输入变换完全解释，停止机制主张。
- 边界：简单 A2 自身仍需公平跨架构验证。
- 证据：`ziyu24/DG-OBB@fe6edfa2c47aa5a94d8a0cb33ea4cf59016936e1` 的 `lab/failed_methods.md`、`doc/legacy/p3_quad_prime_gcg_go_nogo_report.md`。

## DG-04 不同训练日程的正结果不能说明架构通用

- 类型：历史结论已推翻。
- 为何失败：RTMDet 的初始正向比较用了 6 epoch 对 36 epoch 的不公平日程；同日程复核后 A2 的 AP50/AP75 约下降 `1.52` 点且 CI 在零下。
- 避坑：跨架构结论必须同数据、同训练预算和同选模规则；发现日程混杂后撤销旧正结果。
- 边界：A2 在 Oriented R-CNN/two-stage 的结果可单独保留，不能外推 universal architecture。
- 证据：`ziyu24/DG-OBB@fe6edfa2c47aa5a94d8a0cb33ea4cf59016936e1` 的 `lab/failed_methods.md`、`doc/legacy/p5_4_failure_boundary_report.md`。

## DG-05 适用边界必须随反例收窄

- 类型：范围限制。
- 为何失败：两阶段模型上的正结果曾被写成通用架构规律，直到 one-stage 公平反例出现才暴露外推错误。
- 避坑：主张范围只覆盖实际通过的模型家族、数据和协议；跨家族未验证时写未知，不写“通用”。
- 边界：本条要求收窄措辞，不抹除已有效的局部结果。
- 证据：`ziyu24/DG-OBB@fe6edfa2c47aa5a94d8a0cb33ea4cf59016936e1` 的 `lab/result.md`、`doc/legacy/final_key_results_tables.md`。
