# cqc_P5 科学问题与失败教训

审计基线：当前主线 `ziyu24/cqc_P5@1093b8b57a9a8dc13a8e520376caa9b826a9fb33`；另比较了比主线多 1 个提交的执行分支 `ziyu24/cqc_P5@8fc035ddb9827c21f56fefd9c3b3bdae2f93602c`。次线仅记录外部资源/权限与 GPU 占用导致的 preflight 阻塞，优化步为零，不改变科学结论。

快速阅读路径：先读“项目研究什么”→“教训二、三、四、五”→“方法族停止索引”。

## 项目研究什么

项目研究异构标注空间下的旋转检测，尤其是不同数据源存在类别层级、漏标或粗粒度标注时，如何训练统一检测器。广义统一标签空间路线因先验工作拥挤，后续收窄到尺寸相关标注政策与隐变量分配。

## 领域位置与当前结论

- **事实**：统一标签空间与匹配检测器路线和 UFO2、Omni-DETR、OpenSeeD、Wholly-WOOD、PWOOD/SPWOOD、UniconDet 等直接重叠。
- **事实**：现有 oracle-ignore 正结果因 IoF 方向和零正样本旁路而无效；修正后的资格门又因边界框几何与 `allowed_border=0` 冲突，在训练前停止。
- **事实**：当前尺寸相关策略保留全部实例，研究的是 annotation granularity policy，不再是 MNAR；较新次线只证明资源未就绪，没有方法失败。
- **推断**：真正可研究的对象应是明确的数据生成/标注机制，而不是“异构标注”这个过宽标签。
- **未知**：在忠实 Wholly 两阶段基线、MCAR 与匹配控制齐全时，尺寸相关粒度政策是否有效仍未知。

## 实际采用过的方法

项目审查了统一标签空间、匹配检测器、漏标实例 oracle-ignore、覆盖约束和利用隐藏真值诊断分配差异等方案，并通过配置与样本级审计检查实现是否真的产生预期训练信号。

## 教训一：统一标签空间加匹配检测器不足以构成新科学主线

- 失败命题：把异构数据集映射到统一类别空间，再使用匹配式检测器，就是新的通用学习问题。
- 失败原因：UFO2、Omni-DETR、OpenSeeD 等工作已覆盖相近的异构监督与统一空间；原方案没有提出新的可识别矛盾或可验证机制。
- 后续做法：先定位现有方法无法处理的具体标注政策，并将贡献收窄为可测的缺失机制、粒度机制或部署约束。
- 边界：新的大规模数据和系统整合可有工程价值，但不能仅凭组合结构宣称方法新颖性。
- 证据：`ziyu24/cqc_P5@1093b8b57a9a8dc13a8e520376caa9b826a9fb33` 的 `research/PROJECT_STATUS.md`、`research/EVIDENCE.md`。

## 教训二：漏标与粗粒度标注是不同缺失机制

- 失败命题：未标注的小实例与被标成上位类别的实例可以由同一个统一策略处理。
- 失败原因：前者缺少正标签且可能被当作背景，后者有观测标签但语义分辨率较低；二者的似然、分配和评价偏差不同。
- 后续做法：分别定义缺失概率和标签映射过程，设计不同对照与可识别假设，避免把两种问题合并后无法解释收益来源。
- 边界：若数据生成过程明确规定二者共享同一潜变量，可联合建模，但需给出并验证该生成模型。
- 证据：`ziyu24/cqc_P5@1093b8b57a9a8dc13a8e520376caa9b826a9fb33` 的 `research/PROJECT_STATUS.md`、`research/EVIDENCE.md`。

## 教训三：无效的 oracle-ignore 不能给出性能上界

- 失败命题：利用隐藏真值忽略漏标小目标后得到的小幅提升，可视为方法可达到的 oracle 上界。
- 失败原因：实现中的 IoF 方向与预期相反，零正样本分支又绕过了关键逻辑，因此处理并未稳定作用于目标样本；约 0.488 的变化没有 oracle 含义。
- 后续做法：用手工构造的正、负和零正样本验证匹配方向与损失路径，确认干预确实改变目标样本后再解释上界。
- 边界：修复并通过样本级因果检查的 oracle 仍只能说明潜在 headroom，不是可部署方法。
- 证据：`ziyu24/cqc_P5@1093b8b57a9a8dc13a8e520376caa9b826a9fb33` 的 `research/EVIDENCE.md`、`research/R1_RESULT_REVIEW.md`。

## 教训四：资格条件不能与数据几何天然冲突

- 失败命题：要求旋转框完全落在图像内的覆盖条件，可以公平筛选边界截断样本。
- 失败原因：边界拟合标注天然贴近或越过图像边缘，在 `allowed_border=0` 下大量合法样本永远不合格，筛选结果反映规则冲突而非方法能力。
- 后续做法：在运行前用真实标注计算条件可满足率，并让覆盖定义与截断数据的生成机制一致。
- 边界：对明确禁止截断且标注有安全边距的数据，严格内含条件仍可使用。
- 证据：`ziyu24/cqc_P5@1093b8b57a9a8dc13a8e520376caa9b826a9fb33` 的 `research/EVIDENCE.md`、`research/R1A_STAGE_A_REVIEW.md`。

## 教训五：尺寸相关标注粒度不等于 MNAR，必须匹配正确对照

- 失败命题：按目标大小决定保留细类还是粗类，就可以直接解释为 missing-not-at-random 并与随机漏标比较。
- 失败原因：当前政策保留全部实例，只改变标签粒度；它没有产生“实例是否被观测”的缺失机制。若缺少 MCAR 粒度退化与相同标签预算对照，收益无法归因于尺寸信息。
- 后续做法：把实例缺失、类别粗化、点/HBox/OBB 几何降级分别建模；对尺寸政策设置同预算随机政策和 matched control。
- 边界：标注是否出现若确实依赖不可观测真值，可属于 MNAR；必须由数据生成过程而不是方法名称决定。
- 证据：`ziyu24/cqc_P5@1093b8b57a9a8dc13a8e520376caa9b826a9fb33` 的 `experiments/p5_r2a/frozen_config_contract.json`、`research/PROJECT_STATUS.md`。

## 教训六：复现分阶段训练不能压成一个看似相同的单阶段配置

- 失败命题：把 Wholly 的预训练与微调参数合并进一次训练，就可作为忠实强基线。
- 失败原因：原方法是具有不同数据、全局 batch 与优化状态的两阶段流程；单阶段近似改变了学习路径和比较预算，结果无论正负都不能裁决原方法。
- 后续做法：按作者阶段边界复现并记录每阶段初始化、数据、batch、schedule 与 checkpoint lineage；若资源不足，只标记基线不可比较。
- 边界：单阶段变体可以作为新工程基线，但必须改名并停止声称作者方法复现。
- 证据：`ziyu24/cqc_P5@1093b8b57a9a8dc13a8e520376caa9b826a9fb33` 的 `research/R6_CORPUS_AUDIT.md`、`research/SURVEY.md`。

## 方法族停止索引

| 方法族 | 最强负证据或限制 | 停止范围 | 当前证据路径 |
| --- | --- | --- | --- |
| unified annotation space | 与多项异构/弱监督检测工作直接重叠 | 停止以统一空间+匹配器作为独立创新 | main：`research/SURVEY.md`；`research/PROJECT_STATUS.md` |
| missing / coarse / point / HBox | 观测机制不同，合并后 estimand 不清 | 停止单一“异构标签”处理和归因 | main：`research/BRIEF.md`；`research/EVIDENCE.md` |
| original oracle-ignore | IoF 方向、零 GT 旁路和弱训练破坏 oracle 语义 | 停止引用约 0.488 的变化为上界 | main：`research/R1_RESULT_REVIEW.md` |
| corrected eligibility gate | 边界 HBox 使最大 IoF 约 0.499989，规则在训练前不可满足 | 停止当前覆盖门；不是方法性能负结果 | main：`research/R1A_STAGE_A_REVIEW.md`；`experiments/p5_r1a/results/stage_a_gate.json` |
| size-dependent granularity | 保留全部实例，不是 MNAR；缺 MCAR 与 matched control | 只有对照和预算闭合后才可研究 | main：`research/PROJECT_STATUS.md`；`experiments/p5_r2a/frozen_config_contract.json` |
| Wholly reproduction | 原方案为两阶段，单阶段拼装不忠实 | 停止用假复现裁决强基线 | main：`research/R6_CORPUS_AUDIT.md` |
| newer execution preflight | 外部 Wholly 根/authority 缺失且 GPU 忙，零优化步 | 仅记资源阻塞，不写成科学失败 | 次线：`experiments/p5_r2a/results/server/001/report.md` |
