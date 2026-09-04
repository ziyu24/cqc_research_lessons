# DG-OBB 科学问题与失败教训

审计基线：`ziyu24/DG-OBB@fe6edfa2c47aa5a94d8a0cb33ea4cf59016936e1`

## 项目研究什么

项目研究旋转目标检测的跨域泛化，尤其是多尺度训练能否缓解不同遥感数据集、目标尺度和细长形状带来的域差，并尝试比简单缩放更复杂的域泛化模块。

## 实际采用过的方法

项目在 DOTA、DIOR 和 HRSC 间做双向迁移，比较四尺度 RandomChoiceResize、FIFG、GCG 等模块，并在 Oriented R-CNN 与 RTMDet 上复核架构依赖；同时审计 DOTAMetric 的类别映射。

## 教训一：类别映射错误可以制造巨大的虚假域差

- 失败命题：接近零的跨域 AP 证明模型完全不能迁移。
- 失败原因：评价器的类别索引映射错误使真值与预测错位，修复后指标从约 0.0036 变为 0.6543，超过一百八十倍差异主要是测量错误。
- 后续做法：跨数据集评价前用少量人工样本验证类别名、索引、忽略类和预测行映射，并对恒等预测做 sanity check。
- 边界：修复评价器后仍存在的性能差才可用于域泛化结论；本教训不说明真实域差大小。
- 证据：`ziyu24/DG-OBB@fe6edfa2c47aa5a94d8a0cb33ea4cf59016936e1` 的 `lab/failed_methods.md`、`doc/legacy/final_discussion_report.md`。

## 教训二：跨域增益可能强烈依赖检测器架构

- 失败命题：多尺度训练揭示了对所有旋转检测器都成立的通用域泛化机制。
- 失败原因：Oriented R-CNN 在 DIOR 与 DOTA 双向的 AP75 都提高约 3.6 个点，HRSC 细长目标 AP50 提高约 35.5 个点；但 RTMDet-M 的公平短日程复核反而约下降 1.52 个点。
- 后续做法：把架构作为预设异质性因素，在相同训练预算和输入协议下跨至少两类检测器复现，再决定是否使用“通用”。
- 边界：正结果仍支持 Oriented R-CNN 与当前数据条件下的有效工程策略，不应被反例抹掉。
- 证据：`ziyu24/DG-OBB@fe6edfa2c47aa5a94d8a0cb33ea4cf59016936e1` 的 `lab/result.md`、`doc/legacy/final_key_results_tables.md`、`doc/legacy/p5_4_failure_boundary_report.md`。

## 教训三：复杂域泛化模块必须胜过简单输入缩放

- 失败命题：加入频率或几何条件模块能在简单多尺度训练之外提供独立的跨域机制。
- 失败原因：FIFG 出现数值不稳定且没有收益，GCG 也低于简单 RandomChoiceResize；复杂度没有形成增量贡献。
- 后续做法：始终保留强而简单的输入变换基线，先验证模块在等预算下的增量，再研究复杂机制。
- 边界：失败针对现有实现和数据，不排除具有新观测或更强约束的域泛化方法。
- 证据：`ziyu24/DG-OBB@fe6edfa2c47aa5a94d8a0cb33ea4cf59016936e1` 的 `lab/failed_methods.md`、`doc/legacy/p3_triple_prime_v2_finitesafe_max5_go_nogo_report.md`、`doc/legacy/p3_quad_prime_gcg_go_nogo_report.md`。
