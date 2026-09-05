# bgc_obb 科学问题与失败教训

审计基线：`ziyu24/bgc_obb@ebfa89e77c7d831bf521cad48d652fa1de123bf5`

快速阅读路径：先读“项目研究什么”→“教训一、二、三”→“方法族停止索引”。

## 项目研究什么

项目研究弱监督旋转检测中，中心与形状参数块之间的几何梯度冲突能否预测定位错误，并据此对实例重加权。

## 领域位置与当前结论

- **事实**：vanilla mAP 约 `0.4515`，Frobenius、Log-Euclidean、Bures 分别约 `0.4206/0.4449/0.4302`，均未形成收益。
- **事实**：被动 Log-Euclidean 信号与目标误差的 Spearman 仅约 `0.023`；选择最强约 9% 子集后也只有约 `0.107<0.15`。
- **推断**：被动诊断未支持预设的单调风险排序，不能把全部问题归于重加权；但近零 Spearman 不是“无任何预测信息”的证明，也未排除训练早期信号或优化器伤害。
- **未知**：PCGrad 路线受 DDP/非确定性异常污染，不能用其结果裁决梯度投影方法本身。

## 实际采用过的方法

项目用 Frobenius、Log-Euclidean、Bures 和 AIRM 等 SPD 几何度量构造块梯度冲突分数，在玩具数据、被动全量诊断和实际重加权训练中比较其与旋转 IoU 误差及 AP 的关系。

## 教训一：玩具相关性不能替代真实任务中的预测效度

- 失败命题：小型合成样本上的微弱正相关足以支持梯度冲突是定位风险代理。
- 失败原因：玩具相关约 0.073，只跨过宽松阈值；全量数据中不同检测器、度量、观测和子集上的相关接近零或反号，信号没有外部延伸。
- 后续做法：玩具实验只验证构造是否可能工作，核心代理必须在冻结的真实样本上报告相关、排序、校准和置信区间。
- 边界：玩具反例可以否定数学实现，玩具正例不能确认现实预测能力。
- 证据：`ziyu24/bgc_obb@ebfa89e77c7d831bf521cad48d652fa1de123bf5` 的 `decisions/A1_BGC_final_failure_summary_2026-05-12.md`、`results/d7_toy_redo/summary.json`。

## 教训二：被动信号无效与重加权伤害是两个不同问题

- 失败命题：训练 AP 下降只能说明重加权优化不稳定，风险代理本身仍可能正确。
- 失败原因：被动 Log-Euclidean 在末期 checkpoint 的 Spearman 仅约 0.023，未达到项目设定的 0.15 单调排序效应；但高低分组仍有约 0.036 的误差差，不能断言统计独立。主动/被动训练不是同一条完整轨迹，且缺少中期 checkpoint，不能进一步裁决时序变化或重加权的独立因果效应。
- 后续做法：先用被动、无干预数据验证代理，再测试干预；将“测不准”和“用坏了”分别归因。
- 边界：支持停止当前末期单调代理和已测重加权设置；不排除非单调信息、早期效应或未训练的 AIRM。原始报告中“重加权不是失败原因”的排他归因证据不足，本文不继承。
- 证据：`ziyu24/bgc_obb@ebfa89e77c7d831bf521cad48d652fa1de123bf5` 的 `decisions/A1_BGC_final_failure_summary_2026-05-12.md`、`results/E2_passive_bgc.md`。

## 教训三：数值几何正确不保证统计代理有效

- 失败命题：SPD 度量实现数值稳定并尊重几何结构，就应能预测定位误差。
- 失败原因：FP32 下多种度量可正确计算，但真实相关性仍近零；FP16 还出现 NaN，AIRM 代价高。数学合法性、数值稳定性和预测有效性是三项独立要求。
- 后续做法：依次验证定义、数值和外部预测效度，不用前两项替代第三项；高成本度量需证明增量价值。
- 边界：本结论否定这些冲突分数作为当前风险代理，不否定 SPD 几何在其他估计目标中的用途。
- 证据：`ziyu24/bgc_obb@ebfa89e77c7d831bf521cad48d652fa1de123bf5` 的 `decisions/A1_BGC_final_failure_summary_2026-05-12.md`、`decisions/D-2A-failure-2026-05-12.md`。

## 方法族停止索引

| 方法族 | 最强负证据或限制 | 停止范围 | 当前 main 证据路径 |
| --- | --- | --- | --- |
| BGC observable | 被动相关仅约 `0.023`，精选子集约 `0.107<0.15` | 停止将块梯度冲突作为当前定位风险代理 | `results/E2_passive_bgc.md`；`decisions/A1_BGC_final_failure_summary_2026-05-12.md` |
| SPD metric variants | Frob/LE/Bures 均低于 vanilla，且共享弱相关 | 停止仅换几何度量的挽救 | `decisions/A1_BGC_final_failure_summary_2026-05-12.md` |
| instance reweighting | 被动信号先失败，训练也下降 | 停止当前权重机制；区分 signal 与 intervention | `decisions/A1_BGC_final_failure_summary_2026-05-12.md` |
| PCGrad | DDP/非确定性异常破坏比较 | 只判运行无效，不裁决 PCGrad 一般效果 | `decisions/D-2A-failure-2026-05-12.md` |
