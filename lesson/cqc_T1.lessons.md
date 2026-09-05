# cqc_T1 科学问题与失败教训

> 使用边界：教训须结合适用条件与原始证据使用，同条件下的有效反证不能忽略，也不能跨条件自动否决新研究；来源不可访问时须注明“未独立核实”，不得将摘要当作已核实的原始证据。

审计基线：当前主线 `ziyu24/cqc_T1@a395f8fb2ae20751df9659a22e5f614f107c1ae4`；主线精简前的历史实验以 `ziyu24/cqc_T1@a622277bc62d12cf010a3eb9ab1c8e1bab12a23e` 为只读证据锚点。2026-09-05 补查服务器 Home/tmpfs、实际执行代码并直接复算保存预测；覆盖与补救判断见当前主线 `doc/RESEARCH_AUDIT_20260905.md`。本文不把内部任务编号、运行过程或项目自造术语当作科学结论。

快速阅读路径：先读“项目研究什么”→“教训二、四、七、九”→“方法族停止索引”。

## 项目研究什么

T1 实际研究了三个相互关联、但不能混为一谈的问题：

1. **测量问题**：同一幅超大遥感图像仅改变切片网格原点时，同一物理目标的旋转检测结果会怎样变化；总体 AP 是否掩盖了实例级检出、类别和几何状态翻转。
2. **干预问题**：这些变化主要来自边界截断、上下文变化还是下采样相位；随机切片、跨布局融合、相位对齐、等变模块、教师信息或局部重裁能否在保持检测能力和计算预算时减少变化。
3. **执行问题**：能否不以普通重叠切片近似整图推理，而把整图检测器改写成输出完全一致、显存更低且延迟可接受的执行过程。

## 领域位置与当前结论

平移敏感和下采样混叠不是 T1 首次发现：一般目标检测器的小平移敏感已有系统研究，抗混叠、APS、LPS、TIPS 也已有同行评审论文。T1 可能有区分度的对象，是以**母图中的物理实例身份**为单位，跨多个实际切片布局做配对测量，并同时核算不稳定性、可恢复上界和代价；这只是基于仓库证据的潜在贡献边界，不是已被小范围共同体认可或已达到发表标准的判断。

- **事实**：DOTA-v1.0 的四类检测器都出现跨布局实例状态变化；SODA-A 也有实例级变化，但总体 AP 波动很小。固定上下文的小位移实验在最大步长倍数附近形成低翻转“凹口”，支持下采样相位参与机制，但逐层归因只在一个检测器上完成。
- **事实**：项目测试的修复路线没有在预设效果、检测能力和成本下闭合。固定候选审计与 GT 贪心定向重裁的收益未达项目门，因而停止当前路线；后者不是所有同预算重裁的最优上界，也不否定分区不稳定现象。
- **事实**：RTMDet-M 在相同母图的两套标注及各自训练的 checkpoint 下均做到逐输出相等，本进程物理显存采样峰值降到 5976 MiB；这不是瞬时硬预算证明。RTMDet-S 只相对已经 atomized 的参考降低 1.73%，相对默认执行反而增加显存且输出不相等。它是模型与参考函数受限的工程结果，不是通用整图检测器或论文级证明。
- **推断**：母图实例配对比只报总体 AP 更适合回答“切片布局是否改变同一目标”这一问题；但项目自定义指标尚不能视为领域标准。
- **未知**：没有仓库证据证明该测量协议已被独立团队复现或被同行共同体接受；也没有第二种检测器完成精确低显存执行，因此方法的跨架构普适性仍未知。

**补救判断**：当前没有“有限修补即可闭合”的顶刊路线。M 与母图测量资产值得保留，但通用执行器、新诊断 benchmark 或新修复机制都需要实质新研究；这是投入判断，不是任何期刊都不能发表或方向永久无效的证明。

相关先验工作：[Manfredi 与 Wang 的目标检测平移等变研究](https://arxiv.org/abs/2008.05787)、[Zhang 的抗混叠下采样](https://proceedings.mlr.press/v97/zhang19a.html)、[Chaman 与 Dokmanić 的 APS](https://openaccess.thecvf.com/content/CVPR2021/html/Chaman_Truly_Shift-Invariant_Convolutional_Neural_Networks_CVPR_2021_paper.html)、[Rojas-Gomez 等人的 LPS](https://proceedings.neurips.cc/paper_files/paper/2022/hash/e87b1e06be8c3594c810e8991e77ea40-Abstract-Conference.html)、[Saha 与 Gokhale 的 TIPS](https://openaccess.thecvf.com/content/WACV2025/html/Saha_Improving_Shift_Invariance_in_Convolutional_Neural_Networks_with_Translation_Invariant_WACV_2025_paper.html)。

## 实际采用过的方法

- **跨布局测量**：在固定切片尺寸和重叠下改变网格原点，用母图 GT 身份配对候选与最终检测，统计总体 AP、实例状态翻转、召回上界及跨布局互补。
- **输入和输出侧修复**：随机偏移训练、相位扰动、七布局推理与 NMS、同布局候选恢复、GT 定向重裁、固定边界重裁和增加重叠。
- **相位和表示侧修复**：局部相位对齐、状态化 LatticeDet、已发表的 APS-D、TIPS、学习式相位选择、步长自由提案支路，以及使用整图或幸运相位特征的教师/替换实验。
- **整图执行改写**：整图原生参考、FP64 流式/分块算子、局部残差与逐元素重算、直接固定核执行，以及只改写 RTMDet 固定算子族的 ExactRTM 宏执行器。

## 教训一：不要把已有的“平移敏感”包装成新的科学问题

- 失败命题：发现检测结果随切片原点变化，就足以构成新的现象或机制贡献。
- 失败原因：卷积网络的移位敏感、下采样混叠以及检测器的小平移性能变化已有公开研究；APS、LPS、TIPS 也已分别处理相位选择或移位不变性。若只重复“换个原点结果会变”，贡献与现有文献直接碰撞。
- 后续做法：新工作应把命题限定为母图物理实例的跨切片重复测量、原坐标配对、布局间状态转移及其可恢复性/成本；在立项时先证明这些估计对象不是已有移位实验的改名。
- 边界：仓库的碰撞分析只能界定潜在差异，不能证明新颖性，更不能代替正式文献检索、同行评审或独立复现。
- 证据：`ziyu24/cqc_T1@a622277bc62d12cf010a3eb9ab1c8e1bab12a23e` 的 `reports/partition_instability_collision_review.md`、`reports/partition_instability_top_journal_route.json`。

## 教训二：测到实例不稳定，不等于存在足够大的可修复收益

- 失败命题：实例状态会跨布局翻转，因此选择或融合更好的布局必然能显著提高单次推理结果。
- 失败原因：DOTA-v1.0 的 RTMDet 在七布局间有 1895/28853（6.57%）实例状态变化，但固定候选池的召回审计只增加 0.485 个百分点；限定 15% 额外像素、用 GT 位置贪心选择的定向重裁仅增加 0.182 AP，跨边界召回增加 0.711 个百分点，未达预设实用效应。测量效应和干预收益是两个不同估计对象。
- 后续做法：先明确 oracle 获得了哪些额外信息、覆盖哪些候选或动作。只有证明穷尽或有有效松弛界时才称严格上界；GT 辅助的贪心策略仍只是有特权信息的诊断对照，不能以其失败排除所有同预算策略。
- 边界：项目据这些小收益停止当前修补路线是止损决策；15% 贪心重裁不是同预算最优重裁的上界，也没有否定全部分区干预。七布局联合结果同样不能充当单布局可部署收益。
- 证据：`ziyu24/cqc_T1@18df509d3f5e46dedf0f8733c44b6fe5b6716b21` 的 `doc/physical_instance_oracle_p0a_result.md`、`doc/physical_instance_oracle_p0b_result.md`、`lab/discussion.md`。

## 教训三：不能先验地把切片失败归因于边界截断或上下文不足

- 失败命题：目标靠近切片边界、可见比例下降或上下文变少，是分区不稳定的主因，因此增加重叠就能解决。
- 失败原因：DOTA 配对样本中 94.55% 的命中/漏检转换保持相同最佳可见比例，中央与近边界候选召回接近；在上下文固定的小位移实验中，四类检测器仍出现与下采样步长相关的翻转凹口。SODA-A 复现了实例不稳定，但近边界实例并未更差，且真正跨边界样本过少，无法支持边界机制。
- 后续做法：把截断、上下文、采样相位分成可独立干预的变量；先做固定上下文位移和成对可见性审计，再决定重叠、补上下文或相位方法。
- 边界：现有结果表明边界不是该数据与设置下的充分主解释，不代表任何遥感数据、目标尺度或切片器中边界都不重要；SODA-A 对跨边界机制本身证据不足。
- 证据：`ziyu24/cqc_T1@a622277bc62d12cf010a3eb9ab1c8e1bab12a23e` 的 `reports/partition_instability_top_journal_route.json`、`reports/second_large_dataset_audit.json`。

## 教训四：组件级移位等变不能直接推出真实切片检测等变

- 失败命题：把 APS-D、TIPS 或相位选择器装入检测器，就会消除真实切片布局引起的输出变化。
- 失败原因：真实裁剪改变上下文与 padding，不同于完整或循环域上的纯平移。APS-D 检测器移植在一幅母图的 34 个共同 GT × 9 个不兼容位移、共 306 个目标—位移配对上，总翻转为 `3→3`；这不是 306 个独立图像对，也不是逐目标事件完全相同（原敏感子集为 `3→2`）。81 个稠密分支/位移检查中 75 个不能整数余类对齐，构成当前全链路严格等变的反例。另一 TIPS 训练对照的翻转下降 10.86%，召回下降 1.64 个百分点，MAC 增加 42.08%。
- 后续做法：引入等变组件前，先写清其数学作用域与实际裁剪算子的差异，并分别验证特征对齐、完整检测输出、任务能力和计算成本；一个组件通过不能替代全检测器验证。
- 边界：反例可否定当前实现的严格等变；一幅母图上的三次翻转不足以估计总体改善率。APS-D 算子身份核验不是完整检测器训练配方复现，不否定 APS、TIPS 原始结论或所有等变网络。
- 证据：`ziyu24/cqc_T1@18df509d3f5e46dedf0f8733c44b6fe5b6716b21` 的 `doc/coset_equiv_p0_result.md`；`ziyu24/cqc_T1@a622277bc62d12cf010a3eb9ab1c8e1bab12a23e` 的 `reports/dota10_tips_training_gate.json`。

## 教训五：稳定性指标必须以检测能力未坍塌为前提

- 失败命题：实例翻转变少，说明表示或提案对切片相位更鲁棒。
- 失败原因：步长自由提案支路实现了零翻转，但总体提案召回仅 3.68%，敏感实例召回仅 0.74%，448 个切片中有 278 个没有提案；它是稳定地漏检，而不是稳定地检测。
- 后续做法：将稳定性、召回/AP、候选覆盖和计算量设为合取门槛，并与能力匹配的基线比较；任何稳定性改善都必须报告分母中仍可被检测的实例数。
- 边界：当任务能力和覆盖确实匹配时，较低翻转仍是有效证据；本教训针对的是用退化模型“优化”稳定性指标。
- 证据：`ziyu24/cqc_T1@a622277bc62d12cf010a3eb9ab1c8e1bab12a23e` 的 `reports/dota10_spear_stage_a.json`、`reports/dota10_partition_free_reference.json`。

## 教训六：oracle 的因果充分性、信息覆盖和可学习性必须分开证明

- 失败命题：整图教师或幸运相位特征能事后恢复部分漏检，就说明学生模型能够学会同样的修复。
- 失败原因：整图教师只覆盖 1895 个布局依赖实例中的 1061 个，真正可恢复的失败为 317/798（39.72%），对全部漏检的覆盖也只有 18.44%；冻结的幸运相位特征替换确实比对照恢复更多样本，但匹配训练后的相位模型没有降低不兼容变化，置信区间下界也不支持改善。事后使用理想信息证明的是局部因果充分性，不是输入中含有足够信息，更不是优化过程能学到它。
- 后续做法：依次检验教师覆盖率与增量信息、可由部署输入预测的程度、能力匹配下的端到端学习效果；某环节失败时停止对应外推，条件实质改变则重新评估，不把 oracle 诊断写成方法结果。
- 边界：冻结替换仍可用于定位瓶颈，整图教师也可作为诊断参照；失败的是从诊断直接外推可学习修复。
- 证据：`ziyu24/cqc_T1@a622277bc62d12cf010a3eb9ab1c8e1bab12a23e` 的 `reports/dota10_mips_headroom.json`、`reports/dota10_cpet_gate1.json`、`reports/dota10_cpet_phase_gate.json`。

## 教训七：逐输出“精确”等价必须冻结参考数值函数和对照身份

- 失败命题：权重、输入和数学算子相同，默认 CUDA 执行、固定算子计划与重写执行就应逐位相同；若不同就是重写错误。
- 失败原因：源码中的 fixed 和 ExactRTM 都已经将同两个卷积 atomize；二者相对 default 还同时关闭 TF32、改变确定性标志。因此 fixed→ExactRTM 的相等只验证已改写参考上的生命周期变化，不证明默认模型等价恢复。直接复算发现 default→ExactRTM 在 458 图上全部有张量变化，其中 321 图检测数量变化；阈值临界候选可解释数值漂移如何传至检测，但没有单独分离 TF32、内核选择和归约次序的作用。
- 后续做法：同时保留默认实现、同数值标志但未 atomize 的整张卷积参考、改写执行，分开估计数值策略、算子改写与生命周期收益。记录精度、shape、阈值及后处理；kernel/reduction plan 仅在后端可观测且可固定时验证，否则保持相同输入 shape 或明确改为预注册容差契约，不能仅以 FP32/deterministic 标签冒充计划已冻结。
- 边界：原“撤销反证”只可指削弱生命周期 bug 归因，不能撤销默认输出不等的事实。fixed→ExactRTM 相等仍成立；原生框架不因此错误，近似任务效用也不因严格相等失败而必然失败。
- 证据：`ziyu24/cqc_T1@a395f8fb2ae20751df9659a22e5f614f107c1ae4` 的 `doc/RESEARCH_AUDIT_20260905.md`、`doc/exactrtm_project_protocol.md`、`src/scripts/run_exactrtm_s_full_shard.py`、`src/scripts/audit_saved_predictions.py`。

## 教训八：单模型的显存成功与单算子的失败都不能外推为通用结论

- 失败命题：一个 RTMDet 规格把峰值显存压到预算内，就证明得到通用低显存整图检测方法；反过来，一个直接流式算子太慢，就证明固定显存下的精确整图检测不可能。
- 失败原因：M 的两组标注/checkpoint 共享 458 母图，两个卷积特化后采样峰值为 5976 MiB、记录 E2E 增加约 5%–6%；DOTA10 的 native/compiled 还使用不同版本 runner 和准入顺序，不能当作已闭合的强基线性能比较。S 的 1.73% 仅是已 atomized 参考上的生命周期收益，相对 default 反而多用 25.08% 显存；缺少同数值标志的未改写对照，不能从中推断整个分块技术只有该收益。直接固定核或 FP64 实现的失败同样不能形成不可能性定理。
- 后续做法：联合核对参考身份、同输入顺序、输出等价和完整重复计时，区分 allocator、采样物理峰值与硬预算保证；按主张范围补强切片/offload 基线及跨架构证据，而不是凑够模型数便称通用方法。失败只约束被测实现与成本边界。
- 边界：RTMDet-M 的结果是可复核的工程成功，不应被 RTMDet-S 的失败抹掉；但在跨架构证据缺失前，也不能提升为通用科学方法或发表完成。
- 证据：`ziyu24/cqc_T1@a395f8fb2ae20751df9659a22e5f614f107c1ae4` 的 `doc/RESEARCH_AUDIT_20260905.md`、`doc/exact_dense_obb_final_report.md`、`doc/exactrtm_project_protocol.md`；`ziyu24/cqc_T1@a622277bc62d12cf010a3eb9ab1c8e1bab12a23e` 的 `reports/dota10_pnee_p0b2_closure.json`。

## 教训九：状态能贯穿检测器，不等于全链路状态等变且成本可接受

- 失败命题：在所有 stride-2 位点保留 lattice state，并把它传过 FPN、point prior 和 OBB decode，就足以得到可训练的分区等变检测器。
- 失败原因：LatticeDet 的权重加载和全链路 state propagation smoke 均通过，只证明状态可以传递；在共同物理 dense chart 上，确定性 selector 的 `dx=32` 最大绝对误差仍为 `81.434`，移除 channel attention 后分类误差仍为 `35.898`、距离回归误差为 `5996.686`，所需交换关系并不成立。与此同时，全层 APS/LPS/SPD/GES/phase-bank 强基线的固定算术下界至少为 `112.402G` Conv MAC，即原图的 `1.580×`，已超过 `1.25×` 成本上限，训练无法补救机制门与成本门的同时失败。
- 后续做法：若主张对任意权重严格等变，训练前先在统一物理坐标中验证“输入平移—状态变换—FPN 重索引—检测读出”的交换关系；按冻结的全相位物化计算图计数 MAC，不能把此计数外推成所有等变实现的成本下界。状态传递或 checkpoint 可加载不能替代验证。
- 边界：该证据停止当前确定性 selector、全相位物化基线及扩展。训练不能让“对任意权重严格等变”的结构断言重新成立，也不能减少不变计算图的 MAC；但它可能改变近似误差或任务性能，这些并未被本次前向反例否定。
- 证据：`ziyu24/cqc_T1@18df509d3f5e46dedf0f8733c44b6fe5b6716b21` 的 `lab/result.md`、`lab/failed_methods.md`、`src/lattice_det/audit.py`、`src/lattice_det/state.py`。

## 方法族停止索引

下表只索引当前主线 `ziyu24/cqc_T1@a395f8fb2ae20751df9659a22e5f614f107c1ae4` 中仍可回读的总结、报告和实现入口；“停止范围”均为有限否定，不是对整个研究方向的不可能性宣判。

| 方法族 | 最强负证据 | 停止范围 | 当前 main 证据路径 |
| --- | --- | --- | --- |
| WAVE | `256→256` radius-1 固定核最快 `26.832 s`，已是完整检测时限 `14.990019 s` 的 `1.790×`，且尚未包含其余检测链路 | 停止 direct convolution、row-group、stripe/wavefront traversal、cuDNN bit-exact imitation 与该 executor 调优；不否定 6 GiB 整图检测本身 | `lab/result.md`；`lab/failed_methods.md`；`src/scripts/run_wave_det_radius_one_p2_lower_bound.py` |
| LIVE / EBS | LIVE 的两个 full-residency residual operand 需 `7018.250 MiB`；EBS 的 Add-only 虽可 exact，却不能覆盖 finite-radius convolution | 分别停止 full-residency residual 与 Add-only 实现族；不外推到其它生命周期或卷积执行原语 | `lab/discussion.md`；`lab/failed_methods.md`；`src/scripts/audit_live_det_p0_residual_barrier.py`；`src/scripts/audit_ebs_det_p0_barriers.py` |
| PNEE / DPE | PNEE 的 exact 路径成本过高或 GPU 输出不 exact；DPE 仅 trunk 即达 `9965.9 MiB` | 停止当前 FP64/分块 exact backbone 与 streaming dense-head 实现族；不是精确分块计算的一般否定 | `lab/failed_methods.md`；`src/scripts/run_dota10_pnee_p0b2_large_latency.py`；`src/scripts/audit_dota10_dpe_prereg_cost.py` |
| SPEAR | 翻转虽可降到零，但敏感实例 proposal `R@0.3` 仅 `0.737%`，属于表示坍塌 | 停止当前触发器、stride-free proposal 和 sidecar；不否定能力匹配的新提案模型 | `lab/failed_methods.md`；`src/scripts/run_spear_stage_a_eval.py`；`src/scripts/audit_spear_semantic_trigger_headroom.py` |
| merge / MOPR | learned merge 的全 GT 严格 Recall 上限仅 `+0.513` 点；MOPR 使 AP/Recall 分别下降 `0.559/0.274` 点 | 停止当前候选合并与局部相位修正主线；不否定输入或估计对象发生实质变化的新方法 | `lab/failed_methods.md`；`src/scripts/merge_dota10_premerge_recovery.py`；`src/scripts/summarize_dota10_mopr_gate1.py` |
| LatticeDet | 全链路共同坐标最大误差 `81.434`；所需全相位强基线至少 `112.402G / 1.580×` Conv MAC，超过 `1.25×` 成本门 | 停止当前 selector、全相位物化、训练和跨检测器/数据集扩展；不否定所有 lattice/polyphase 理论 | `lab/result.md`；`lab/failed_methods.md`；`src/lattice_det/audit.py`；`src/lattice_det/p0_contract.py` |
| APS-D | 单母图的 306 个 GT×shift 配对总翻转 `3→3`；`75/81` 稠密分支/位移不能整数余类对齐，剩余最大误差 `54.846214` | 停止当前冻结 RTMDet 的 coset 扩展；严格等变有反例，总体改善率未知 | `doc/coset_equiv_p0_result.md`；`lab/result.md`；`lab/failed_methods.md`；`src/coset_equiv/aps.py` |
| Oracle / recrop | 同布局固定候选 Recall 审计仅 `+0.4852` 点；15% GT 贪心定向重裁仅 `+0.1816` AP、crossing Recall `+0.7108` 点 | 项目停止当前 set-decoder/recrop 主线；贪心结果不是所有同预算重裁策略的上界 | `doc/physical_instance_oracle_p0a_result.md`；`doc/physical_instance_oracle_p0b_result.md`；`lab/discussion.md`；`lab/failed_methods.md` |
| ExactRTM | S 相对已 atomized 参考仅降 `1.7286%` 采样峰值；相对 default 多用 `25.08%` 且 321/458 图检测数变化。缺同数值标志未改写对照 | 停止当前 S 型微调及通用/发表主张；不否定所有 atom 改写，不推翻 M 的相等与采样显存正结果 | `doc/RESEARCH_AUDIT_20260905.md`；`doc/exactrtm_project_protocol.md`；`doc/exact_dense_obb_final_report.md`；`src/scripts/audit_saved_predictions.py` |
