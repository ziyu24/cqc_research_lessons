# TAOS 避坑点

审计基线：`ziyu24/TAOS@0c3bded0220758584723f1bf8747ef2eb13a0d5c`

## TAOS-01 由定义强制为零的 mismatch 不是学习成功

- 类型：协议/实现无效。
- 为何失败：B 臂直接令 `tau_pred=tau_geo`，C 臂 residual 近零且强缩放后也等于 `tau_geo`，因此 mismatch 恒为 0；该数字由构造决定，不代表 TauHead 学会截断真值。
- 避坑：诊断指标必须能被候选独立改变，并同时报告对真实 `tau_GT` 的 recall/precision。
- 边界：零 mismatch 可作为实现恒等检查，不能作性能结论。
- 证据：`ziyu24/TAOS@0c3bded0220758584723f1bf8747ef2eb13a0d5c` 的 `pth_data/phase1_step13_mve_r0_FAILED_20260513_184341/mve_r0_reaudit_20260513_092852.md`。

## TAOS-02 辅助损失压倒基础损失时需先排除优化失衡

- 类型：协议/实现无效。
- 为何失败：多个 epoch 的辅助损失约为 base detection loss 的 6--14 倍；coupled 相对 independent 没有达到 mismatch 和 AP75 门，结果可能受尺度支配。
- 避坑：训练前记录各损失量级、梯度比例和无辅助基线；候选失败时不得只看总 loss 正常就声称机制被公平测试。
- 边界：当前证据不能单独证明损失尺度是唯一原因，也不把科学失败改判为成功。
- 证据：`ziyu24/TAOS@0c3bded0220758584723f1bf8747ef2eb13a0d5c` 的 `pth_data/phase1_step13_mve_r0_FAILED_20260513_184341/mve_r0_reaudit_20260513_092852.md`、`stage2_results.md`。

## TAOS-03 早期 sanity PASS 不代表最终决策树通过

- 类型：范围限制。
- 为何失败：Stage 1 三 epoch 只证明训练有限且早期行为符合预期；Stage 2 仍在 mismatch 降幅和 AP75 节点失败，整体为 FAIL。
- 避坑：冒烟、数值稳定和正式效果分开编号；只在最终冻结终点报告科学通过。
- 边界：Stage 1 的工程健康证据仍有效。
- 证据：`ziyu24/TAOS@0c3bded0220758584723f1bf8747ef2eb13a0d5c` 的 `pth_data/phase1_step13_mve_r0_FAILED_20260513_184341/mve_stage1_results/stage1_diag_summary.md`、`stage2_results.md`。
