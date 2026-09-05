# DG-OBB 科学问题与失败教训

> 使用边界：教训须结合适用条件与原始证据使用，同条件下的有效反证不能忽略，也不能跨条件自动否决新研究；来源不可访问时须注明“未独立核实”，不得将摘要当作已核实的原始证据。

审计基线：`ziyu24/DG-OBB@fe6edfa2c47aa5a94d8a0cb33ea4cf59016936e1`

快速阅读路径：先读“项目研究什么”→“教训一、二、三”→“方法族停止索引”。

## 项目研究什么

项目研究旋转目标检测的跨域泛化，尤其是多尺度训练能否缓解不同遥感数据集、目标尺度和细长形状带来的域差，并尝试比简单缩放更复杂的域泛化模块。

## 领域位置与当前结论

- **事实**：A2 四尺度 RandomChoiceResize 在 Oriented R-CNN 的 DIOR↔DOTA 两方向 AP75 分别约 `+3.64/+3.55` 点；HRSC 的 `+35.5` 点 AP50 只指长宽比至少 6 的细长切片，不是全 HRSC。RTMDet-M 同预算 6 epoch 复核 AP75 点差为 `-1.198` 点，bootstrap 均值 `-1.521` 点，不能混写。
- **事实**：FIFG 早期 NaN 后，FiniteSafe 修复版完成 12 epoch，AP75 为 `+1.71` 点但未过 `+2` 点门；GCG 未胜过简单 resize。早期评价映射错误曾把 `0.6543` 级结果误写成 `0.0036`。
- **推断**：可保留架构受限的输入尺度策略，不得维持架构通用或复杂模块优越性主张。
- **未知**：停止维护后不再补实验；这些有限结论不能外推到新架构。

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
- 失败原因：Oriented R-CNN 在 DIOR 与 DOTA 双向的 AP75 都提高约 3.6 个点，HRSC 细长目标 AP50 提高约 35.5 个点；RTMDet-M 在同预算 6 epoch、DIOR→DOTA 的点差为 `-1.198` 点，图像 bootstrap 区间约 `[-2.644,-0.352]`。这足以限制无条件通用主张，但检测器与各自日程同时变化，不能单独识别架构为唯一原因。
- 后续做法：把架构作为预设异质性因素，在相同训练预算和输入协议下跨至少两类检测器复现，再决定是否使用“通用”。
- 边界：正结果仍支持 Oriented R-CNN 与当前数据条件下的有效工程策略，不应被反例抹掉。
- 证据：`ziyu24/DG-OBB@fe6edfa2c47aa5a94d8a0cb33ea4cf59016936e1` 的 `lab/result.md`、`doc/legacy/final_key_results_tables.md`、`doc/legacy/p5_4_rtmdet_fair_6ep_report.md`。

## 教训三：复杂域泛化模块必须胜过简单输入缩放

- 失败命题：加入频率或几何条件模块能在简单多尺度训练之外提供独立的跨域机制。
- 失败原因：FIFG 早期数值不稳定，但后续 FiniteSafe 版在 12 epoch 内跳过 4 次更新后完成，AP50/AP75/AP85 分别为 `+0.18/+1.71/+0.73` 点；它是未达项目 `+2` 点门的小幅正结果，不是“无收益”。GCG 低于简单 RandomChoiceResize；现有证据不足以确立复杂模块对强简单基线的独立优势。
- 后续做法：始终保留强而简单的输入变换基线，先验证模块在等预算下的增量，再研究复杂机制。
- 边界：分别保留数值故障、修复后的描述性增益和项目止损决定；未过效应门不证明真实效应为零，也不排除其它域泛化方法。
- 证据：`ziyu24/DG-OBB@fe6edfa2c47aa5a94d8a0cb33ea4cf59016936e1` 的 `lab/failed_methods.md`、`doc/legacy/p3_triple_prime_v2_finitesafe_max5_go_nogo_report.md`、`doc/legacy/p3_quad_prime_gcg_go_nogo_report.md`。

## 方法族停止索引

| 方法族 | 最强负证据或限制 | 停止范围 | 当前 main 证据路径 |
| --- | --- | --- | --- |
| evaluator mapping | 修复后指标由约 `0.0036` 变为 `0.6543` | 停止引用错误映射产生的域差 | `lab/failed_methods.md`；`doc/legacy/final_discussion_report.md` |
| A2 multi-scale resize | ORCNN 双向及 HRSC 细长切片正；RTMDet-M 6ep AP75 点差 `-1.198` 点 | 保留配置条件策略；停止 universal claim | `doc/legacy/p5_4_rtmdet_fair_6ep_report.md`；`doc/legacy/final_key_results_tables.md` |
| FIFG | 早期 NaN；修复后 AP75 `+1.71` 点未达 `+2` 门 | 保留有限正信号；停止当前资源投入，不判零效应 | `doc/legacy/p3_triple_prime_v2_finitesafe_max5_go_nogo_report.md` |
| GCG | 弱于简单 RandomChoiceResize | 停止当前几何条件模块 | `lab/failed_methods.md` |
