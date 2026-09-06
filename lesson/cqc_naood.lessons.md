# cqc_naood 科学问题与失败教训

> 使用边界：教训须结合适用条件与原始证据使用，同条件下的有效反证不能忽略，也不能跨条件自动否决新研究；来源仓库为私有，无法访问时须注明“未独立核实”，不得把本摘要当作原始证据或把诊断性 oracle 当作可部署结果。

审计基线：`ziyu24/cqc_naood@fd264e7f2bae4b7faa2b9687b4793ab96be32d15`。该提交是迁移后项目的脱敏证据快照，保留关键协议、机器报告和实现入口，不含数据、逐检测预测、权重、主机路径或未公开稿件。

快速阅读路径：先读“项目研究什么”→“关键 oracle 数据”→“教训二、三、四、五”→“方法族停止索引”。

## 项目研究什么

NAOOD 实际研究了三个必须分开的科学问题：

1. **诊断问题**：把旋转框的中心、尺度和角度替换为真值时，哪些替换及交互能提高 AP，观察到的 oracle gap 是否具有可信的样本身份和评价语义。
2. **转化问题**：冻结现有旋转检测器后，部署时可见的分数、几何、上下文或条件质量特征，能否利用 oracle 暴露的排序空间，而不是只在有真值时成立。
3. **泛化问题**：一种结果前冻结、限制匹配破坏并允许拒绝动作的重排规则，能否跨检测器和数据集提高 AP75，同时不伤 AP50。

## 领域位置与当前结论

检测集合上下文重打分、matching-aware target、pairwise detection ranking、duplicate-aware calibration 和一般 abstaining ranking 都已有公开研究。NAOOD 不能把任一部件单独宣称为首次；当前仍可检验的差异，是把跨图同类相邻交换、每图匹配顺序不变、分数多重集不变、多源环境 outer-LOO 和单侧 harm abstention 组合到冻结的旋转检测器上，并做未见数据集的 prospective 验证。这个组合目前只是候选假设。

- **事实**：经显式键和独立复算认证的全量 replacement oracle 仍显示明显结构，但主导交互从旧称的 `wh-theta` 改为四检测器一致的 `xy-wh`；旧大效应不能引用。
- **事实**：修正 native matching 与 SODA 坐标系后，五个源环境均存在可受益、有害和中性相邻 pair；合计有害 pair 比可受益 pair 更多，说明重排问题存在但安全选择并不容易。
- **事实**：质量混合、条件质量 meta-model、训练式排序和旧 pairwise reranking 均未通过各自冻结门，不能作为正向方法贡献。
- **推断**：当前最有信息量的贡献是“oracle 诊断怎样失真、为何难以转化”的受限审计结论；MI-PAR 只有完成跨环境 AP 和未见数据验证后，才可能形成正向方法贡献。
- **未知**：现有证据没有完成五源域 outer-LOO、独立 clean method replay 或 DIOR 双架构 prospective 验证，也没有证明该约束组合已被同行共同体认可。

相关先验工作：[Pato 等的 contextual AP rescoring](https://openaccess.thecvf.com/content_CVPR_2020/html/Pato_Seeing_without_Looking_Contextual_Rescoring_of_Object_Detections_for_AP_CVPR_2020_paper.html)、[Xu 等的 adaptive ranking pair selection](https://openaccess.thecvf.com/content/CVPR2022/html/Xu_Revisiting_AP_Loss_for_Dense_Object_Detection_Adaptive_Ranking_Pair_CVPR_2022_paper.html)、[Gilg 等的 duplicate-aware calibration](https://openaccess.thecvf.com/content/WACV2024/html/Gilg_Do_We_Still_Need_Non-Maximum_Suppression_Accurate_Confidence_Estimates_and_WACV_2024_paper.html)、[Mao 等的 abstaining pairwise ranking](https://proceedings.mlr.press/v202/mao23a.html)。

## 实际采用过的方法

- **oracle 分解**：对中心、宽高、角度及其组合做真值替换，使用原生 AP50/AP75、不同 GT 口径和 forced-identity 对照检查主效应与交互。
- **随机化与审计**：构造 matched-null、bootstrap、显式键 prediction/GT 对账和协议隔离的独立复算，区分观察差值、随机基线与可签证结果。
- **可部署质量建模**：测试条件质量 meta-model、原生分数与质量分数混合、训练式排序和多种消融；这些路线均保留原生检测器并在后处理阶段改变排序。
- **匹配不变的选择性交换**：对全局同类排序中的跨图相邻 pair 学习 benefit/harm/neutral，只交换 detection identity 所占的 score slot，保持每图同类访问顺序和每类 score multiset。

## 关键 oracle 数据

### 已认证的全量 replacement oracle

口径为 DOTA-v1.5 全 5,297 图、16 类、all-GT、match IoU 0.3、AP75、VOC07 macro，单位为百分点；候选与 clean 对 8,704 个 metric keys、1,088 个 interaction keys 和 737,696 个 assignment rows 对账，登记失败数均为 0。

| detector | `inc_wh_theta` | `inc_xy_wh` | 主导项 |
| --- | ---: | ---: | --- |
| Oriented R-CNN | 2.0068384763 | 5.8532185142 | `xy-wh` |
| Strip R-CNN | 2.6784937689 | 5.8798935750 | `xy-wh` |
| ARS-DETR | 2.4074575602 | 6.6673281572 | `xy-wh` |
| RTMDet-R | 1.6929846288 | 5.5336636848 | `xy-wh` |

证据：`ziyu24/cqc_naood@fd264e7f2bae4b7faa2b9687b4793ab96be32d15` 的 `evidence/SCIENTIFIC_EVIDENCE_BASELINE.md`、`evidence/reports/t11_full_l2_v4_candidate_execution_report_v1.json`。

### native matching oracle 标签

每个源环境使用 2,048 张显式键图像；TP 是各 IoU 阈值原生 greedy matcher 的身份，不是单框 maximum-IoU 阈值。

| source environment | TP50 | TP75 | 边界 |
| --- | ---: | ---: | --- |
| M01 | 18,730 | 10,470 | accepted source label |
| M03 | 19,602 | 14,150 | accepted source label |
| M04 | 31,000 | 13,992 | SODA 1024→800 exact rescale |
| M05 | 44,644 | 25,739 | SODA 1024→800 exact rescale |
| M06 | 31,737 | 17,048 | literal-correction successor |

M04 错误坐标 lineage 的 TP50/TP75 仅为 420/18，M05 为 454/20；精确缩放 `(cx,cy,w,h)` 为 `25/32` 后得到上表结果，angle、score、key 和 feature 不变。该修复证明旧标签失效，不是方法增益。

证据：`ziyu24/cqc_naood@fd264e7f2bae4b7faa2b9687b4793ab96be32d15` 的 `evidence/protocols/ISSUES_V40_144_SODA_RESCALE_20260820.md`、`evidence/protocols/IQU_MIPAR_SODA_RESCALED_MATCHING_LABEL_PROTOCOL_V11_20260820.md`、`evidence/SCIENTIFIC_EVIDENCE_BASELINE.md`。

### 修正后的相邻 pair population

口径为跨图同类相邻、support 内、singleton score、native logit gap `0<gap<=0.10`，并令 `HARM_ANY` 优先。这些是 `scientific_authority=false` 的 source-development 统计。

| source environment | eligible | benefit75_safe50 | harm_any | neutral |
| --- | ---: | ---: | ---: | ---: |
| M01 | 72,404 | 2,877 | 4,764 | 64,763 |
| M03 | 14,646 | 1,745 | 2,262 | 10,639 |
| M04 | 117,895 | 5,520 | 10,329 | 102,046 |
| M05 | 39,936 | 4,198 | 7,382 | 28,356 |
| M06 | 48,118 | 3,859 | 6,961 | 37,298 |
| aggregate | 292,999 | 18,199 | 31,698 | 243,102 |

合计约为 benefit 6.21%、harm 10.82%、neutral 82.97%。五个环境都有三类支持，只说明问题非空；harm 比 benefit 多约 74%，不能把 oracle population 写成预期 AP 增益。

证据：`ziyu24/cqc_naood@fd264e7f2bae4b7faa2b9687b4793ab96be32d15` 的 `evidence/reports/mipar_rescaled_lineage_pair_population_v12.report.json`、`evidence/source/analyze_mipar_rescaled_lineage_pair_population_v12.py`。

## 教训一：跨文件等长数组不能代替稳定样本身份

- 失败命题：预测、GT、alignment 或缓存长度一致，并各自排序后按位置连接，就足以对应同一图像和检测。
- 失败原因：预测 PKL 是各模型推理序，GT loader 是字典序；历史消费者仍按整数位置绑定。由此曾出现三模型每个约 5,296/5,297 图错位、零 AP 行和被 tie-breaking 伪造的主导交互，另一路仅 1/5,297 图同 rank。错误可生成整齐表格，因而不能靠输出形状发现。
- 后续做法：跨文件一律以完整 `image_id`、`source_key`、`class_id` 显式连接，并断言 key set、几何、类别、分数和数量守恒；forced-identity 必须在 oracle 读数前通过。
- 边界：位置访问可用于同一函数内部已冻结的局部数组；被否定的是没有跨文件身份契约的位置 join，不是数组运算本身。
- 证据：`ziyu24/cqc_naood@fd264e7f2bae4b7faa2b9687b4793ab96be32d15` 的 `evidence/SCIENTIFIC_EVIDENCE_BASELINE.md`、`evidence/reports/t11_full_l2_v4_candidate_execution_report_v1.json`。

## 教训二：单框最大 IoU 不能冒充原生 greedy-matching oracle

- 失败命题：用每个候选的 maximum IoU 是否超过 0.50/0.75，就能定义 AP50/AP75 的逐检测 TP/FP，并安全地训练相邻交换。
- 失败原因：greedy matching 受分数访问顺序和 GT 占用影响。高分框 IoU 0.60、低分框 IoU 0.80 且共享一个 GT 时，高分框在 0.50 是 TP、低分框是 duplicate FP；在 0.75 则身份反转。因此逐检测 `TP75⇒TP50` 不成立，raw-IoU 标签不能支持 matching-aware 或 AP-safe 主张。
- 后续做法：在每个阈值分别调用冻结的原生 matcher，把 TP/FP/ignored 立即映射回显式 detection key；pair label 先判任一阈值的 harm，再判 AP75 benefit 与 AP50 safe。
- 边界：maximum IoU 仍可作局部几何诊断或特征；失效的是把它等同于评价器最终 TP/FP 身份。
- 证据：`ziyu24/cqc_naood@fd264e7f2bae4b7faa2b9687b4793ab96be32d15` 的 `evidence/protocols/IQU_MIPAR_NATIVE_MATCHING_CORRECTION_V2_20260819.md`、`evidence/protocols/IQU_MIPAR_MATCHING_AWARE_SOURCE_LABEL_PROTOCOL_V3_20260819.md`。

## 教训三：oracle 匹配前必须显式证明预测与标注处于同一坐标系

- 失败命题：检测框和 annotation 都表示同一张图，就可以直接计算 IoU；极低 TP 只说明模型失效或数据域太难。
- 失败原因：SODA 的两个适配器以 `rescale=False` 保存 1024×1024 网络坐标，而 tile 与 annotation 是 800×800。直接匹配把 M04/M05 的 TP50 压到 420/454；只做预定义的 `25/32` 坐标变换后，TP50 恢复到 31,000/44,644。模型、分数、角度和特征没有变化，变化来自评价坐标错误。
- 后续做法：在任何 IoU/oracle 统计前冻结并校验 `ori_shape`、`img_shape`、scale factor、框表示和逆变换；用图像 header、显式键和变换前后 digest 做守恒检查。
- 边界：这说明旧 SODA label 无效，不说明所有低 TP 都来自坐标错误，也不构成 MI-PAR 的效果证据。
- 证据：`ziyu24/cqc_naood@fd264e7f2bae4b7faa2b9687b4793ab96be32d15` 的 `evidence/protocols/ISSUES_V40_144_SODA_RESCALE_20260820.md`、`evidence/protocols/IQU_MIPAR_SODA_RESCALED_MATCHING_LABEL_PROTOCOL_V11_20260820.md`。

## 教训四：大的 replacement oracle gap 不等于可学习、可部署的重排收益

- 失败命题：中心—尺度 oracle 在四检测器上有约 5.53–6.67 pp 的交互空间，就意味着质量模型能从部署输入恢复同量级 AP。
- 失败原因：oracle 直接读取目标答案，只证明候选和替换动作中存在更优结果。部署模型还要分别证明可观测特征含有增量信息、动作能被稳定选择、错误选择的 harm 可控、原生 AP 真正改善且跨环境迁移。项目的 QAnchor、R-MetaDetect、NTSR-OBB 和旧 MI-PAR 正是在这些转化环节停止。
- 后续做法：把 oracle headroom、特征可预测性、策略可选择性、原生 AP 因果效果和跨域 transport 作为连续而独立的门；任何一步失败都只停止相应外推。
- 边界：认证的 replacement oracle 仍是有效瓶颈诊断，也能指导新假设；它不为任意质量分数或学习器背书。
- 证据：`ziyu24/cqc_naood@fd264e7f2bae4b7faa2b9687b4793ab96be32d15` 的 `evidence/SCIENTIFIC_EVIDENCE_BASELINE.md`、`evidence/reports/source_alpha_selection_v1.report.json`、`evidence/protocols/NTSR_OBB_TOP_JOURNAL_ROUTE_CLOSEOUT_V1_20260819.md`。

## 教训五：排序空间同时含 benefit 与 harm，不能只统计可改善 pair

- 失败命题：发现大量 `FP75→TP75` 相邻反转，就足以说明重排有稳定正期望，或只需提高 benefit 分类准确率。
- 失败原因：修正后的五环境中，0.10 logit budget 合计有 18,199 个 safe-benefit pair，却有 31,698 个 harm pair和 243,102 个 neutral pair；harm 比 benefit 多约 74%，且类别严重不平衡。只报告 benefit 会隐藏错误动作更常见这一事实。
- 后续做法：把 harm 设为优先标签并单独建模，使用单侧 harm threshold 和 abstention；最终以 held-environment AP50 non-harm、AP75 positive 和 paired image-cluster bootstrap 裁决，不能用 pair AUC 替代。
- 边界：population 不是策略结果；harm 更常见不证明一个充分保守的学习器必然失败，也不证明所有预算和特征下比例相同。
- 证据：`ziyu24/cqc_naood@fd264e7f2bae4b7faa2b9687b4793ab96be32d15` 的 `evidence/reports/mipar_rescaled_lineage_pair_population_v12.report.json`、`evidence/protocols/IQU_MIPAR_RESCALED_LINEAGE_PAIR_POPULATION_V12_20260820.md`。

## 教训六：结构不变量只能限制破坏方式，不能证明策略有效

- 失败命题：跨图同类相邻交换保持每图 matching 顺序和 class score multiset，因此预测交换天然 AP-safe 或必然增益。
- 失败原因：固定每图同类访问顺序确实能保持指定阈值下的 greedy TP/FP 身份，交换已知相邻 `(FP,TP)` 也不会降低对应 AP；但部署模型并不知道真实身份。错误预测仍可能把 `(TP,FP)` 交换成有害顺序，score multiset 守恒也不控制全局 AP 排序方向。
- 后续做法：把顺序、分数多重集、tie、rank displacement 和显式 receipt 当机械不变量；把预测正确性、AP50 non-harm、AP75 gain 和 uncertainty 当独立经验命题。
- 边界：在已知真实 TP/FP 且固定 matcher 的数学条件下，相邻交换非下降结论仍成立；被否定的是把结构定理转移给未知标签预测器。
- 证据：`ziyu24/cqc_naood@fd264e7f2bae4b7faa2b9687b4793ab96be32d15` 的 `evidence/protocols/IQU_MIPAR_NATIVE_MATCHING_CORRECTION_V2_20260819.md`、`evidence/protocols/IQU_MIPAR_MATCHING_AWARE_OUTER_LOO_METHOD_V8_20260820.md`。

## 教训七：设计集已被观察后，不能再把它包装成 prospective 验证

- 失败命题：训练不使用某个验证环境的标签，就足以称该环境为未见测试，即使研究者已经看过旧方法结果并据此改设计。
- 失败原因：M02 的 outcome 已在旧路线中被观察，后续即使不进入 fit，也只能作 post-result diagnostic；阈值、特征和规则可能已受到结果知识影响。已有 DIOR trainval checkpoint 同样见过 validation，不能充当 prospective 主结果。
- 后续做法：先用源环境冻结全部规则、模型输入、score candidates 和 swap receipts并哈希，再打开目标 validation annotation；prospective detector 只用 official train 训练，official test labels 永久封存。
- 边界：已观察验证集仍可用于诊断、消融和方法开发；失去的是确认性或 prospective 身份，不是所有科学用途。
- 证据：`ziyu24/cqc_naood@fd264e7f2bae4b7faa2b9687b4793ab96be32d15` 的 `evidence/protocols/IQU_MIPAR_MATCHING_AWARE_OUTER_LOO_METHOD_V8_20260820.md`、`evidence/SCIENTIFIC_EVIDENCE_BASELINE.md`。

## 教训八：组合方法的新颖性必须逐部件做先例排除

- 失败命题：把 matching-aware、pairwise、calibration、abstention 和旋转检测组合起来，就可以声称首次提出上述任一概念。
- 失败原因：contextual AP rescoring、AP ranking pairs、duplicate-aware calibration 和 abstaining pairwise ranking 都已有直接先例。仅换成遥感旋转框或给既有部件换名，不能形成可靠新颖性。
- 后续做法：把主张限定为尚待验证的约束组合：冻结旋转检测器、跨图同类相邻交换、保持每图匹配顺序与 score multiset、多源 outer-LOO、单侧 harm control、未见双架构验证；继续做正式引用追踪，避免使用未经证明的 `first`。
- 边界：先例排除限制的是宽泛首创叙事，不证明该组合已经新颖，也不否定组合在充分实验后可能有方法价值。
- 证据：`ziyu24/cqc_naood@fd264e7f2bae4b7faa2b9687b4793ab96be32d15` 的 `evidence/protocols/IQU_MIPAR_NOVELTY_BOUNDARY_V25_20260820.md`、`evidence/SCIENTIFIC_EVIDENCE_BASELINE.md`。

## 教训九：工程可复现、独立复算和科学有效性是三种不同结论

- 失败命题：哈希一致、forced-identity 通过、独立实现复算一致或产物有证书，就自动证明研究命题成立。
- 失败原因：这些检查能证明输入、实现或再现范围内的一致性，却不能修复错误 estimand、错误坐标系、错误 oracle 标签或不足的跨域效果。项目中既出现过可稳定复现的污染表，也出现过工程链完整但 AP75 近零、bootstrap 跨零的训练式排序结果。
- 后续做法：按“身份与实现正确→估计对象正确→统计不确定性→跨环境效果→新颖性”分层给权限；证书只覆盖列明 artifact 和 scope，不能外推到方法有效或期刊级别。
- 边界：严格工程审计仍是可信科研的必要基础；本教训反对的是以它替代科学效果，而不是降低复现要求。
- 证据：`ziyu24/cqc_naood@fd264e7f2bae4b7faa2b9687b4793ab96be32d15` 的 `evidence/SCIENTIFIC_EVIDENCE_BASELINE.md`、`evidence/reports/NTSR_OBB_N1_A6_VS_A0_KEYED_EVALUATION_V1_20260819.json`。

## 方法族停止索引

下表只陈述当前证据提交中的有限停止范围；MI-PAR matching-aware successor 尚未被判定成功或失败。

| 方法族 | 最强负证据 | 停止范围 | 证据路径 |
| --- | --- | --- | --- |
| 历史 `wh-theta` oracle 叙事 | 位置错配与混合框表示；显式键复算改为四检测器一致的 `xy-wh` 主导 | 停止旧 10–31 pp、35/64 dominant 和 `wh-theta` 机制主张；保留认证后的 replacement oracle | `evidence/SCIENTIFIC_EVIDENCE_BASELINE.md`；`evidence/reports/t11_full_l2_v4_candidate_execution_report_v1.json` |
| R-MetaDetect | 条件质量的局部信号没有形成跨域机制与冻结 coverage 的联合支持 | 停止当前 meta-quality TGRS 正向路线；不否定所有条件质量特征 | `evidence/SCIENTIFIC_EVIDENCE_BASELINE.md` |
| QAnchor | 三个冻结 alpha 均未实现全环境 AP50/AP75 non-inferiority | 停止当前原生分数—质量分数混合规则；不否定其它校准目标 | `evidence/reports/source_alpha_selection_v1.report.json` |
| NTSR-OBB | AP75 delta 为 `-0.00004897`，paired interval 跨零且未过 materiality | 停止当前训练式 near-tie 排序及其消融扩展；不是排序学习的一般否定 | `evidence/protocols/NTSR_OBB_TOP_JOURNAL_ROUTE_CLOSEOUT_V1_20260819.md` |
| 旧 MI-PAR | 三个冻结规则全部 0 swap、0 AP delta，且训练标签后来被证明不是 native matching identity | 停止旧 raw-IoU 实现；不能外推到 matching-aware successor | `evidence/reports/mi_pairwise_abstaining_m02_v2.report.json`；`evidence/protocols/IQU_MIPAR_NATIVE_MATCHING_CORRECTION_V2_20260819.md` |
| matching-aware MI-PAR | 五源环境 pair population 结构 gate 通过，但尚无 outer-LOO、clean 或 prospective AP | 继续验证，当前不得写成正向方法或顶刊完成 | `evidence/reports/mipar_rescaled_lineage_pair_population_v12.report.json`；`evidence/protocols/IQU_MIPAR_MATCHING_AWARE_OUTER_LOO_METHOD_V8_20260820.md` |
