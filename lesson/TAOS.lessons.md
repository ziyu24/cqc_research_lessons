# TAOS 科学问题与失败教训

审计基线：`ziyu24/TAOS@0c3bded0220758584723f1bf8747ef2eb13a0d5c`

快速阅读路径：先读“项目研究什么”→“教训一、二、四、五”→“方法族停止索引”。

## 项目研究什么

项目研究切片遥感图像中边界截断目标的旋转检测，试图用截断感知辅助监督、分位数/阈值头、动态分配与融合，在不伤害完整目标的前提下提高截断目标定位。

## 领域位置与当前结论

- **事实**：低权重 coupled QC head 在 RTMDet 上对截断 ship AP50 有强正信号，在 LSKNet 上中等，在 Oriented R-CNN 上仅边际；无截断 DIOR-R 两架构均为负，说明效果具有数据与架构条件。
- **事实**：高 IoU 定位仍很弱；量化头 36 epoch 后 true visible ratio 与预测的 Spearman 为 `-0.2419`，AP75_trunc 增量仅 `0.0033`，并使 complete mAP 下降约 1.13 点。
- **事实**：降低损失权重改善 RTMDet/LSKNet，Oriented R-CNN 仍只约 `+0.14` 点；不能声称 candidate recall 与增益严格单调。
- **推断**：当前工程价值更接近“截断监督的架构条件正则”，不是已校准的可见比例/分位数估计器。
- **未知**：更高 IoU 几何恢复与真实完整物体边界重建仍未解决。

## 实际采用过的方法

项目在 RTMDet、LSK 与 Oriented R-CNN 上测试截断辅助损失、quantile/tau 预测、SWA 与动态 K 分配、融合及不同损失权重，并区分 AP50、AP75、截断子集和完整目标。

## 教训一：AP50 大幅提高不能证明截断框定位变紧

- 失败命题：截断目标 AP50 的大增益足以证明方法恢复了准确几何。
- 失败原因：RTMDet 的截断船只 AP50 明显提高，但 AP75 仍接近零；方法可能只把粗略命中推过宽松阈值，没有恢复精确边界与角度。
- 后续做法：同时报告 AP50、AP75、旋转 IoU 分布、角误差和边界端点误差，并把“发现目标”与“紧致定位”分开。
- 边界：对只需粗定位的应用，AP50 改善仍有价值，但不能表述为高质量 OBB 恢复。
- 证据：`ziyu24/TAOS@0c3bded0220758584723f1bf8747ef2eb13a0d5c` 的 `pth_data/phase1_step13_mve_r0_FAILED_20260513_184341/stage2_results.md`、`pth_data/phase1_step13_mve_r0_FAILED_20260513_184341/mve_r0_reaudit_20260513_092852.md`。

## 教训二：分位数头可作正则项，不代表学到了校准几何

- 失败命题：quantile/tau 辅助头改善训练就说明它输出了有统计意义的截断几何分位数。
- 失败原因：项目没有形成校准的分位数覆盖或可解释几何预测，收益更像辅助正则；由定义强制为零的 mismatch 也不能作为学习成功证据。
- 后续做法：用独立标签检验分位数校准、单调性和覆盖，再区分“辅助损失有效”与“概率头语义正确”。
- 边界：即使不具备概率解释，辅助头仍可能作为工程正则项使用，但需降低主张。
- 证据：`ziyu24/TAOS@0c3bded0220758584723f1bf8747ef2eb13a0d5c` 的 `pth_data/phase1_step13_mve_r0_FAILED_20260513_184341/mve_r0_reaudit_20260513_092852.md`、`pth_data/phase1_step13_mve_r0_FAILED_20260513_184341/stage2_results.md`。

## 教训三：截断感知分配不能以伤害完整目标换取局部收益

- 失败命题：SWA 或动态 K 更偏向截断实例，就会改善总体截断检测。
- 失败原因：这些分配方案没有稳定提高截断定位，并明显伤害完整船只；辅助损失权重过大时还压倒基础检测损失。
- 后续做法：把截断与完整目标的性能作为联合约束，检查正样本覆盖和各损失梯度比例，并保留标准分配器对照。
- 边界：在只关心截断目标且允许牺牲完整目标的任务中可重新定义效用，但不能沿用总体改进主张。
- 证据：`ziyu24/TAOS@0c3bded0220758584723f1bf8747ef2eb13a0d5c` 的 `pth_data/phase1_step13_mve_r0_FAILED_20260513_184341/stage2_results.md`、`pth_data/phase1_step13_mve_r0_FAILED_20260513_184341/mve_stage1_results/stage1_diag_summary.md`。

## 教训四：截断辅助监督具有明显架构与数据条件边界

- 失败命题：同一截断感知模块会跨检测器、跨数据集普遍增益。
- 失败原因：RTMDet 的截断船只提高约 12.85 个点，LSK 仅约提高 2.45 个点且总体下降约 1.34，Oriented R-CNN 约提高 0.14；DIOR 无切片条件也为负，效果高度依赖架构和截断生成过程。
- 后续做法：预注册架构、截断率和切片协议的异质性分析，在统一预算下复现后再限定适用范围。
- 边界：RTMDet 特定设置的正信号仍成立，但不能升级为通用旋转检测机制。
- 证据：`ziyu24/TAOS@0c3bded0220758584723f1bf8747ef2eb13a0d5c` 的 `diagnostics/FINAL_MULTI_BASELINE_CROSS_DATASET_EVIDENCE.md`、`diagnostics/EVIDENCE_AUDIT_FOR_WRITING.md`。

## 教训五：训练变久且 AP 恢复，不能掩盖概率语义反向

- 失败命题：36 epoch 后总体 mAP 恢复到参考附近，说明 quantile/visible-ratio head 已经学会目标语义。
- 失败原因：训练量混杂消除后，Spearman 反而从约 `-0.0879` 变成 `-0.2419`；AP75_trunc 增量 `0.0033<0.005`，complete mAP 又下降 `1.13` 点。模型学到的是 anti-calibrated 表示，而非仅“训练不够”。
- 后续做法：概率或分位数头必须单独通过 rank calibration、coverage、单调性和高 IoU 门；总体 AP 只能评价 detector，不替代 head 语义。
- 边界：该 head 仍可能作为无概率解释的辅助正则使用，但必须撤回校准/分位数主张。
- 证据：`ziyu24/TAOS@0c3bded0220758584723f1bf8747ef2eb13a0d5c` 的 `diagnostics/POC_V3_36EP_FINAL_VERDICT.md`、`diagnostics/FINAL_MULTI_BASELINE_CROSS_DATASET_EVIDENCE.md`。

## 方法族停止索引

| 方法族 | 最强负证据或限制 | 停止范围 | 当前 main 证据路径 |
| --- | --- | --- | --- |
| quantile / visible-ratio semantics | 36 epoch Spearman `-0.2419`，高 IoU门失败 | 停止校准语义；可降级为辅助正则 | `diagnostics/POC_V3_36EP_FINAL_VERDICT.md` |
| high-IoU truncation recovery | AP50 可大涨但 AP75_trunc 仍近零 | 停止“精确几何恢复”主张 | `diagnostics/POC_V3_36EP_FINAL_VERDICT.md` |
| SWA / dynamic-K / fusion | 没有稳定截断收益且伤害完整目标 | 停止当前分配与融合路线 | `pth_data/phase2_step21_22_mve_FAILED_20260514_195413/phase2_mve_results/phase2_mve_final_report_20260514_184000.md` |
| coupled QC at `λ_q=0.05` | LSKNet/ORCNN 有明显 trade-off；高权重过正则 | 停止固定默认值的普适主张 | `diagnostics/FINAL_MULTI_BASELINE_CROSS_DATASET_EVIDENCE.md` |
| coupled QC at `λ_q=0.025` | RTMDet 强、LSKNet 中等、ORCNN 仅 `+0.14` 点；DIOR-R 无截断为负 | 保留架构/截断条件结果；停止 universal mechanism | `reports/wp7a_rtmdet_lambdaq0025_eval_20260520_170431.md`；`reports/wp7b_orcnn_lambdaq0025_eval_20260521_011036.md` |
