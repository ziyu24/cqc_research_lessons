# cqc_naood 科学问题与失败教训

> 使用边界：教训须结合适用条件与原始证据使用，同条件下的有效反证不能忽略，也不能跨条件自动否决新研究；来源仓库为私有，无法访问时须注明“未独立核实”，不得把本摘要当作原始证据或把诊断性 oracle 当作可部署结果。

审计基线：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e`。该提交是迁移后项目的 V2 脱敏证据 successor：保留完整 canonical oracle/factorial/null/Observer 表、48 条相关证书视图、失败协议和再生脚本，不含数据集、逐检测预测、权重、主机路径或未公开稿件。初始 V1 仍由 Git 历史保留，未就地改数。

快速阅读路径：先读“项目研究什么”→“关键 oracle 数据”→“教训四、十、十一、十二”→“方法族停止索引”。

## 项目研究什么

NAOOD 实际研究了三个必须分开的科学问题：

1. **诊断问题**：把旋转框的中心、尺度和角度替换为真值时，哪些替换及交互能提高 AP，观察到的 oracle gap 是否具有可信的样本身份和评价语义。
2. **转化问题**：冻结现有旋转检测器后，部署时可见的分数、几何、上下文或条件质量特征，能否利用 oracle 暴露的排序空间，而不是只在有真值时成立。
3. **泛化问题**：一种结果前冻结、限制匹配破坏并允许拒绝动作的重排规则，能否跨检测器和数据集提高 AP75，同时不伤 AP50。

## 领域位置与当前结论

检测集合上下文重打分、matching-aware target、pairwise detection ranking、duplicate-aware calibration 和一般 abstaining ranking 都已有公开研究。NAOOD 不能把任一部件单独宣称为首次。其已经成立的贡献是受限的测量与证伪：修复旋转检测 oracle 的身份/表示/评价污染，给出可独立复算的多因子 replacement 与 matched-null，并系统记录 oracle headroom 为什么没有直接转化为部署收益。matching-aware MI-PAR 约束组合仍只是未完成候选。

- **事实**：经显式键和独立复算认证的 DOTA-v1.5 全量 replacement oracle 有 8,704 个 metric rows；主口径 `full` 总增益为 26.83--31.16 pp，而主导二阶残差是 `xy-wh`，不是旧称的 `wh-theta`。
- **事实**：DIOR-R 与 DOTA-v1.0 两检测器 factorial 都得到正的预注册 interaction contrast，但效应大小依赖数据集；这是一个外部数据集确认加一个同图 annotation/checkpoint sensitivity，不是两个独立外部复现。
- **事实**：GCRR 六路线中只有两条超过 matched-noise null；多条正 bootstrap 区间仍低于 null q95，跨域正向机制已 STOP。
- **事实**：Corrected Observer 中中心/尺度残差的跨模型 OOF R² 为中等到较高，`dtheta` 线性 OOF R² 仅约 .0004--.0362；旧 angle/routing/collapse 机制不能恢复。
- **事实**：修正 native matching 与 SODA 坐标系后，五个源环境均存在可受益、有害和中性相邻 pair；合计有害 pair 比可受益 pair 更多，说明重排问题存在但安全选择并不容易。
- **事实**：质量混合、条件质量 meta-model、SPIR、ORQ、PQA、训练式排序和旧 pairwise reranking 均未通过各自冻结门，不能作为正向方法贡献。
- **推断**：当前最有信息量的创新是“oracle 诊断怎样失真、如何用 factorial/null 证伪、为何难以转化”的审计方法学；它可支撑 JSTARS 型审计论文，但不是已经成功的 TGRS/IJCV/TPAMI 新检测方法。
- **未知**：现有证据没有完成五源域 outer-LOO、独立 clean method replay 或 DIOR 双架构 prospective 验证，也没有证明该约束组合已被同行共同体认可。

相关先验工作：[Pato 等的 contextual AP rescoring](https://openaccess.thecvf.com/content_CVPR_2020/html/Pato_Seeing_without_Looking_Contextual_Rescoring_of_Object_Detections_for_AP_CVPR_2020_paper.html)、[Xu 等的 adaptive ranking pair selection](https://openaccess.thecvf.com/content/CVPR2022/html/Xu_Revisiting_AP_Loss_for_Dense_Object_Detection_Adaptive_Ranking_Pair_CVPR_2022_paper.html)、[Gilg 等的 duplicate-aware calibration](https://openaccess.thecvf.com/content/WACV2024/html/Gilg_Do_We_Still_Need_Non-Maximum_Suppression_Accurate_Confidence_Estimates_and_WACV_2024_paper.html)、[Mao 等的 abstaining pairwise ranking](https://proceedings.mlr.press/v202/mao23a.html)。

## 实际采用过的方法

- **oracle 分解**：对中心、宽高、角度及其组合做真值替换，使用原生 AP50/AP75、不同 GT 口径和 forced-identity 对照检查主效应与交互。
- **随机化与审计**：构造 matched-null、bootstrap、显式键 prediction/GT 对账和协议隔离的独立复算，区分观察差值、随机基线与可签证结果。
- **可部署质量建模**：测试条件质量 meta-model、原生分数与质量分数混合、训练式排序和多种消融；这些路线均保留原生检测器并在后处理阶段改变排序。
- **匹配不变的选择性交换**：对全局同类排序中的跨图相邻 pair 学习 benefit/harm/neutral，只交换 detection identity 所占的 score slot，保持每图同类访问顺序和每类 score multiset。

## 关键 oracle 数据

### 已认证的 DOTA-v1.5 全量 replacement oracle

口径为 DOTA-v1.5 全 5,297 图、16 类、all-GT、match IoU 0.3、AP75、VOC07 macro。`baseline` 为 AP fraction，其余为百分点。候选与 clean 对 8,704 个 metric keys、1,088 个 interaction keys 和 737,696 个 assignment rows 对账，登记失败数均为 0。

| detector | baseline | Δxy | Δwh | Δtheta | Δxy-wh | Δxy-theta | Δwh-theta | Δfull |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Oriented R-CNN | .376179 | 8.8318 | 11.5833 | 1.9739 | 26.2683 | 11.4347 | 15.5640 | 31.1605 |
| Strip R-CNN | .418869 | 8.3274 | 11.0192 | 2.0592 | 25.2265 | 10.4103 | 15.7570 | 29.8217 |
| ARS-DETR | .352013 | 7.0563 | 9.5166 | 2.3696 | 23.2402 | 10.1750 | 14.2936 | 28.4503 |
| RTMDet-R | .445901 | 6.6210 | 10.1160 | 1.8703 | 22.2707 | 8.4506 | 13.6793 | 26.8335 |

对应 `inc(xy,wh)` 为 5.5337--6.6673 pp，`inc(wh,theta)` 为 1.6930--2.6785 pp。`Δwh-theta` 是组合替换总增益，`inc(wh,theta)=Δwh-theta-Δwh-Δtheta` 是非加性交互残差；V1 只列 residual，因而造成 oracle 很少的错觉。完整 CSV 还覆盖 16 类+macro、matching 0.3/0.5、AP50/AP75、all/easy-GT、VOC07/all-point 和 8 个 replacement modes。`theta` 是完整 GT-angle substitution，不是角度 bin sweep；历史 angle/aspect-ratio partition 受污染，不能当作缺失的 canonical 表补入。

证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/canonical/t11/t11_full_l2_v4_clean_v1_canonical_metrics.csv`、`evidence/canonical/t11/t11_full_l2_v4_clean_v1_interactions.csv`、`evidence/EXPORT_MANIFEST_V2.csv`、`evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md`。

### 跨数据集确认性 factorial

相同主口径下，预注册 contrast `C=Shapley I_xy,wh-I_wh,theta`：

| dataset / detector | Δxy | Δwh | Δtheta | Δxy-wh | Δwh-theta | Δfull | C | 95% CI(C) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| DIOR-R / Oriented R-CNN | 4.2561 | 9.3209 | 2.6173 | 24.0274 | 12.8285 | 31.0057 | 9.5601 | [8.1532, 10.3949] |
| DIOR-R / Strip R-CNN | 4.6290 | 9.4458 | 1.5651 | 24.3461 | 12.5228 | 29.6540 | 8.7594 | [7.4237, 9.8472] |
| DOTA-v1.0 / Oriented R-CNN | 8.9601 | 11.5169 | 1.1711 | 26.2278 | 14.9500 | 30.0498 | 3.4888 | [1.0993, 4.6600] |
| DOTA-v1.0 / Strip R-CNN | 7.5472 | 12.7200 | 1.2659 | 25.6392 | 16.3319 | 29.3468 | 3.0260 | [.9177, 4.5023] |

四条 route 都支持 `xy-wh` interaction 更强，但 DIOR-R 的 paired mean C 为 9.1598 pp、DOTA-v1.0 为 3.2574 pp，不能称数据集不变常数。DIOR-R 是独立外部数据集确认；DOTA-v1.0 与 DOTA-v1.5 共享图像身份，只能作为 annotation/checkpoint sensitivity。

证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/canonical/factorial_geometry/paired_bootstrap_summary.csv`、`evidence/canonical/factorial_geometry/t12_dior_r_oriented_rcnn_factorial_attribution.csv`、`evidence/canonical/factorial_geometry/t12_dior_r_strip_rcnn_factorial_attribution.csv`、`evidence/canonical/factorial_geometry/t13_dota_v10_oriented_rcnn_factorial_attribution.csv`、`evidence/canonical/factorial_geometry/t13_dota_v10_strip_rcnn_factorial_attribution.csv`。

### matched-null 与六路线 GCRR

普通 D2 在两个检测器、三个数据集的六个 cells 均未超过 matched-noise q95。GCRR 六路线的 observed gap/route gate 为：DOTA-v1.5 Oriented R-CNN 1.0593 pp/PASS、Strip .6918/PASS；DIOR-R Oriented 2.5090/FAIL、Strip 1.4988/FAIL；DOTA-v1.5 ReDet .6692/FAIL；DOTA-v1.0 ReDet 1.3224/FAIL。后三条中的 DIOR 双路线和 DOTA-v1.0 ReDet bootstrap CI 均排除零，但仍低于 null q95。正 CI 因而不能替代 matched-null gate，跨域正向机制 STOP。

证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/canonical/phase3/phase3_observed_primary_rescoring_v2.csv`、`evidence/canonical/phase3/phase3_primary_macro_null_v2.csv`、`evidence/canonical/phase3/jstars_gcrr_r1_r6_combined_presentation_v1.csv`、`evidence/registries/audit_certificate_events_v1.csv`。

### Corrected Observer

认证点统计有 780 rows。中心/尺度 components 的跨模型 OOF R² 范围为 `.2105--.7125`；`dtheta` 只有 `.0004--.0362`，尽管其 Spearman 为 `.5231--.6860`。这提示角度周期秩关系与线性可预测性必须分开，不支持旧的 angle routing/collapse 因果叙事。结构化 null 又发现 77,222 rows 中 23,645 rows 不可置换，16 类中 14 类超过冻结 fixed-block gate；successor 只能对结果前限定的 53,577 eligible rows 推断，完整 population 仅作描述。

证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/canonical/observer/t18_corrected_observer_canonical_point_statistics_v1.csv`、`evidence/canonical/observer/t18_corrected_observer_canonical_corrected_null_summary_v1.csv`、`evidence/canonical/observer/observer_null_feasibility_summary_v2.json`、`evidence/protocols/T18_CORRECTED_OBSERVER_PROMOTION_PROTOCOL_V1.md`。

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

证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/protocols/ISSUES_V40_144_SODA_RESCALE_20260820.md`、`evidence/protocols/IQU_MIPAR_SODA_RESCALED_MATCHING_LABEL_PROTOCOL_V11_20260820.md`、`evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md`。

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

证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/reports/mipar_rescaled_lineage_pair_population_v12.report.json`、`evidence/source/analyze_mipar_rescaled_lineage_pair_population_v12.py`。

## 教训一：跨文件等长数组不能代替稳定样本身份

- 失败命题：预测、GT、alignment 或缓存长度一致，并各自排序后按位置连接，就足以对应同一图像和检测。
- 失败原因：预测 PKL 是各模型推理序，GT loader 是字典序；历史消费者仍按整数位置绑定。由此曾出现三模型每个约 5,296/5,297 图错位、零 AP 行和被 tie-breaking 伪造的主导交互，另一路仅 1/5,297 图同 rank。错误可生成整齐表格，因而不能靠输出形状发现。
- 后续做法：跨文件一律以完整 `image_id`、`source_key`、`class_id` 显式连接，并断言 key set、几何、类别、分数和数量守恒；forced-identity 必须在 oracle 读数前通过。
- 边界：位置访问可用于同一函数内部已冻结的局部数组；被否定的是没有跨文件身份契约的位置 join，不是数组运算本身。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md`、`evidence/reports/t11_full_l2_v4_candidate_execution_report_v1.json`。

## 教训二：单框最大 IoU 不能冒充原生 greedy-matching oracle

- 失败命题：用每个候选的 maximum IoU 是否超过 0.50/0.75，就能定义 AP50/AP75 的逐检测 TP/FP，并安全地训练相邻交换。
- 失败原因：greedy matching 受分数访问顺序和 GT 占用影响。高分框 IoU 0.60、低分框 IoU 0.80 且共享一个 GT 时，高分框在 0.50 是 TP、低分框是 duplicate FP；在 0.75 则身份反转。因此逐检测 `TP75⇒TP50` 不成立，raw-IoU 标签不能支持 matching-aware 或 AP-safe 主张。
- 后续做法：在每个阈值分别调用冻结的原生 matcher，把 TP/FP/ignored 立即映射回显式 detection key；pair label 先判任一阈值的 harm，再判 AP75 benefit 与 AP50 safe。
- 边界：maximum IoU 仍可作局部几何诊断或特征；失效的是把它等同于评价器最终 TP/FP 身份。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/protocols/IQU_MIPAR_NATIVE_MATCHING_CORRECTION_V2_20260819.md`、`evidence/protocols/IQU_MIPAR_MATCHING_AWARE_SOURCE_LABEL_PROTOCOL_V3_20260819.md`。

## 教训三：oracle 匹配前必须显式证明预测与标注处于同一坐标系

- 失败命题：检测框和 annotation 都表示同一张图，就可以直接计算 IoU；极低 TP 只说明模型失效或数据域太难。
- 失败原因：SODA 的两个适配器以 `rescale=False` 保存 1024×1024 网络坐标，而 tile 与 annotation 是 800×800。直接匹配把 M04/M05 的 TP50 压到 420/454；只做预定义的 `25/32` 坐标变换后，TP50 恢复到 31,000/44,644。模型、分数、角度和特征没有变化，变化来自评价坐标错误。
- 后续做法：在任何 IoU/oracle 统计前冻结并校验 `ori_shape`、`img_shape`、scale factor、框表示和逆变换；用图像 header、显式键和变换前后 digest 做守恒检查。
- 边界：这说明旧 SODA label 无效，不说明所有低 TP 都来自坐标错误，也不构成 MI-PAR 的效果证据。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/protocols/ISSUES_V40_144_SODA_RESCALE_20260820.md`、`evidence/protocols/IQU_MIPAR_SODA_RESCALED_MATCHING_LABEL_PROTOCOL_V11_20260820.md`。

## 教训四：大的 replacement oracle gap 不等于可学习、可部署的重排收益

- 失败命题：中心—尺度 oracle 在四检测器上有约 5.53–6.67 pp 的非加性交互残差、22.27–26.27 pp 的组合总增益，就意味着质量模型能从部署输入恢复同量级 AP。
- 失败原因：oracle 直接读取目标答案，只证明候选和替换动作中存在更优结果。部署模型还要分别证明可观测特征含有增量信息、动作能被稳定选择、错误选择的 harm 可控、原生 AP 真正改善且跨环境迁移。项目的 QAnchor、R-MetaDetect、NTSR-OBB 和旧 MI-PAR 正是在这些转化环节停止。
- 后续做法：把 oracle headroom、特征可预测性、策略可选择性、原生 AP 因果效果和跨域 transport 作为连续而独立的门；任何一步失败都只停止相应外推。
- 边界：认证的 replacement oracle 仍是有效瓶颈诊断，也能指导新假设；它不为任意质量分数或学习器背书。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md`、`evidence/reports/source_alpha_selection_v1.report.json`、`evidence/protocols/NTSR_OBB_TOP_JOURNAL_ROUTE_CLOSEOUT_V1_20260819.md`。

## 教训五：排序空间同时含 benefit 与 harm，不能只统计可改善 pair

- 失败命题：发现大量 `FP75→TP75` 相邻反转，就足以说明重排有稳定正期望，或只需提高 benefit 分类准确率。
- 失败原因：修正后的五环境中，0.10 logit budget 合计有 18,199 个 safe-benefit pair，却有 31,698 个 harm pair和 243,102 个 neutral pair；harm 比 benefit 多约 74%，且类别严重不平衡。只报告 benefit 会隐藏错误动作更常见这一事实。
- 后续做法：把 harm 设为优先标签并单独建模，使用单侧 harm threshold 和 abstention；最终以 held-environment AP50 non-harm、AP75 positive 和 paired image-cluster bootstrap 裁决，不能用 pair AUC 替代。
- 边界：population 不是策略结果；harm 更常见不证明一个充分保守的学习器必然失败，也不证明所有预算和特征下比例相同。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/reports/mipar_rescaled_lineage_pair_population_v12.report.json`、`evidence/protocols/IQU_MIPAR_RESCALED_LINEAGE_PAIR_POPULATION_V12_20260820.md`。

## 教训六：结构不变量只能限制破坏方式，不能证明策略有效

- 失败命题：跨图同类相邻交换保持每图 matching 顺序和 class score multiset，因此预测交换天然 AP-safe 或必然增益。
- 失败原因：固定每图同类访问顺序确实能保持指定阈值下的 greedy TP/FP 身份，交换已知相邻 `(FP,TP)` 也不会降低对应 AP；但部署模型并不知道真实身份。错误预测仍可能把 `(TP,FP)` 交换成有害顺序，score multiset 守恒也不控制全局 AP 排序方向。
- 后续做法：把顺序、分数多重集、tie、rank displacement 和显式 receipt 当机械不变量；把预测正确性、AP50 non-harm、AP75 gain 和 uncertainty 当独立经验命题。
- 边界：在已知真实 TP/FP 且固定 matcher 的数学条件下，相邻交换非下降结论仍成立；被否定的是把结构定理转移给未知标签预测器。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/protocols/IQU_MIPAR_NATIVE_MATCHING_CORRECTION_V2_20260819.md`、`evidence/protocols/IQU_MIPAR_MATCHING_AWARE_OUTER_LOO_METHOD_V8_20260820.md`。

## 教训七：设计集已被观察后，不能再把它包装成 prospective 验证

- 失败命题：训练不使用某个验证环境的标签，就足以称该环境为未见测试，即使研究者已经看过旧方法结果并据此改设计。
- 失败原因：M02 的 outcome 已在旧路线中被观察，后续即使不进入 fit，也只能作 post-result diagnostic；阈值、特征和规则可能已受到结果知识影响。已有 DIOR trainval checkpoint 同样见过 validation，不能充当 prospective 主结果。
- 后续做法：先用源环境冻结全部规则、模型输入、score candidates 和 swap receipts并哈希，再打开目标 validation annotation；prospective detector 只用 official train 训练，official test labels 永久封存。
- 边界：已观察验证集仍可用于诊断、消融和方法开发；失去的是确认性或 prospective 身份，不是所有科学用途。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/protocols/IQU_MIPAR_MATCHING_AWARE_OUTER_LOO_METHOD_V8_20260820.md`、`evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md`。

## 教训八：组合方法的新颖性必须逐部件做先例排除

- 失败命题：把 matching-aware、pairwise、calibration、abstention 和旋转检测组合起来，就可以声称首次提出上述任一概念。
- 失败原因：contextual AP rescoring、AP ranking pairs、duplicate-aware calibration 和 abstaining pairwise ranking 都已有直接先例。仅换成遥感旋转框或给既有部件换名，不能形成可靠新颖性。
- 后续做法：把主张限定为尚待验证的约束组合：冻结旋转检测器、跨图同类相邻交换、保持每图匹配顺序与 score multiset、多源 outer-LOO、单侧 harm control、未见双架构验证；继续做正式引用追踪，避免使用未经证明的 `first`。
- 边界：先例排除限制的是宽泛首创叙事，不证明该组合已经新颖，也不否定组合在充分实验后可能有方法价值。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/protocols/IQU_MIPAR_NOVELTY_BOUNDARY_V25_20260820.md`、`evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md`。

## 教训九：工程可复现、独立复算和科学有效性是三种不同结论

- 失败命题：哈希一致、forced-identity 通过、独立实现复算一致或产物有证书，就自动证明研究命题成立。
- 失败原因：这些检查能证明输入、实现或再现范围内的一致性，却不能修复错误 estimand、错误坐标系、错误 oracle 标签或不足的跨域效果。项目中既出现过可稳定复现的污染表，也出现过工程链完整但 AP75 近零、bootstrap 跨零的训练式排序结果。
- 后续做法：按“身份与实现正确→估计对象正确→统计不确定性→跨环境效果→新颖性”分层给权限；证书只覆盖列明 artifact 和 scope，不能外推到方法有效或期刊级别。
- 边界：严格工程审计仍是可信科研的必要基础；本教训反对的是以它替代科学效果，而不是降低复现要求。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md`、`evidence/reports/NTSR_OBB_N1_A6_VS_A0_KEYED_EVALUATION_V1_20260819.json`。

## 教训十：组合替换总增益与非加性交互残差不能混称 oracle gap

- 失败命题：`wh+theta` 替换带来的总 AP 增益和 `wh-theta` interaction 是同一读数；摘要只列 interaction 已足以代表完整 oracle。
- 失败原因：总增益是 `Δwh-theta`，二阶残差是 `inc(wh,theta)=Δwh-theta-Δwh-Δtheta`。主口径下前者为 13.68--15.76 pp，后者仅 1.69--2.68 pp；同理 `Δxy-wh` 为 22.27--26.27 pp，而其残差为 5.53--6.67 pp。混称会让读者既低估完整 headroom，又误解“协同”的定义。
- 后续做法：factorial 报告同时列 baseline、所有单臂、组合臂、full、pairwise residual 和 three-way；表头写明 estimand、单位和公式，机器摘要直接从 canonical CSV 生成。
- 边界：总增益和残差都可作为诊断量；本教训不规定哪一个更重要，只禁止在没有公式时互换名称或用局部摘要冒充全表。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md`、`evidence/canonical/t11/t11_full_l2_v4_clean_v1_canonical_metrics.csv`、`evidence/canonical/t11/t11_full_l2_v4_clean_v1_interactions.csv`。

## 教训十一：正 bootstrap 区间不能代替 matched-noise 反事实

- 失败命题：observed gap 的 bootstrap 置信区间排除零，就足以支持重打分机制，或至少证明它超过随机扰动能产生的改善。
- 失败原因：bootstrap 回答相对零的不确定性，matched-null 回答同约束噪声能产生多大的假阳性空间。六路线 GCRR 中，DIOR-R 两路线与 DOTA-v1.0 ReDet 的区间都为正，却仍低于各自 null q95；最终只有两条路线通过，跨域机制 STOP。
- 后续做法：预先冻结 observed effect、cluster bootstrap、matched-null、multiplicity 与 effect-size gate，并使用联合决策；不得在结果后只选择最容易通过的一种不确定性描述。
- 边界：bootstrap CI 对估计精度仍然必要；它失效的是“超过零即可证明机制”的外推，而不是 bootstrap 方法本身。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/canonical/phase3/jstars_gcrr_r1_r6_combined_presentation_v1.csv`、`evidence/canonical/phase3/phase3_primary_macro_null_v2.csv`、`evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md`。

## 教训十二：相关性、统计显著和相对原生分数的增量效用是三层命题

- 失败命题：一个 proxy 与真实定位质量高度相关、AUC 很高或 permutation p 很小，就足以把它称为有用的新质量分数。
- 失败原因：ORQ 的 orbit residual 在四个有效 arms 都有明显相关和纯 proxy AUC，但相对 native score 的冻结增量只有一个 arm 过门；PQA 在三十多万 records 上 p=.01，AUC 增量却只有 .000033，远低于 .01 materiality gate。相关信息可能已被原生分数吸收，大样本也可使微小效应显著。
- 后续做法：依次检验 association、conditional increment、practical materiality 和 native AP；每层使用独立指标与门槛，并允许“有结构但无部署增量”的结论。
- 边界：相关性和显著性可用于机制探索或筛选假设；被否定的是直接把它们写成排序收益或顶刊方法效果。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/protocols/ORQ_TOP_JOURNAL_ROUTE_CLOSEOUT_20260818.md`、`evidence/protocols/IQU_PQA_Q3_L1_FINAL_CLOSEOUT_V1_20260818.md`、`evidence/FORENSIC_FINDINGS_V2.md`。

## 教训十三：结构化 null 的可置换性必须在推断前通过

- 失败命题：先在全样本上运行置换检验，遇到 singleton 或固定 block 后再丢掉不可置换行，仍可把结果称为原计划的 full-population inference。
- 失败原因：Observer full population 的 77,222 rows 中有 23,645 rows 在冻结 block 下不可置换，14/16 classes 超过 5% gate；事后删除会改变 estimand，并可能按结果选择更有利 population。
- 后续做法：把 block support、derangement feasibility、fixed fraction 和 per-class gate 放进 preflight；失败即保存 receipt，另建 append-only successor，在读统计结果前冻结 eligible population。full population 可继续作描述，但不能共享推断标签。
- 边界：限定到 53,577 eligible rows 的 successor 推断在其范围内有效；它不能外推回被排除行，也不能把 exclusion 本身解释为机制。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/canonical/observer/observer_null_feasibility_summary_v2.json`、`evidence/protocols/T18_CORRECTED_OBSERVER_PROMOTION_PROTOCOL_V1.md`、`evidence/FORENSIC_FINDINGS_V2.md`。

## 教训十四：近 tie 排序实验必须冻结数值执行上下文

- 失败命题：checkpoint 和图像相同，就能认为 score 完全相同；float32 尾差、batch composition 或等价角度分支不会改变 AP 结论。
- 失败原因：等价候选曾因尾差让 argmax 偏向看似特定的角度分支；同一网络在不同 batch context 下也可产生足以交换 near-tie rank 的尾差。AP 依赖全局次序，极小 score 差并不保证极小 ranking 影响。
- 后续做法：冻结 batch size、padding/grouping、dtype、device/kernel、tie equivalence class 和 canonical representative；比较时同时核对 score bytes、tie policy、rank displacement 与 native AP。
- 边界：多数非近 tie 检测可能对这些尾差不敏感；本教训要求证明稳定性，不声称所有 GPU/批次变化都会改变结果。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/FORENSIC_FINDINGS_V2.md`、`evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md`。

## 教训十五：总数和宏观指标一致不能证明语义键一致

- 失败命题：candidate/clean 的 macro AP、dominance count、行数或表形状一致，就足以证明逐样本、逐类别实现相同。
- 失败原因：项目曾在 aggregate 计数完全不变时发生四个 class labels 置换；只修 image key 后，class tuple 仍可能按 positional slot 错绑。不同 assignment 可偶然得到相同汇总，同一错误协议也可被两份实现稳定复现。
- 后续做法：比较完整 `(dataset_version,image_id,class_id,detection_id,row_id)` semantic keys、逐 assignment digest 和 matching identity，再比较 aggregate；clean implementation 还必须只读协议，避免复制同一 bug。
- 边界：aggregate agreement 仍是有用的快速 gate；它只能提供必要条件，不能单独授予逐样本或科学有效性权限。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/FORENSIC_FINDINGS_V2.md`、`evidence/reports/t11_full_l2_v4_clean_v1_summary.json`、`evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md`。

## 教训十六：数据版本、模型绑定、匹配器与 AP 口径共同定义 estimand

- 失败命题：图像 ID 相同、checkpoint 能加载、都叫 AP75，就可以跨运行直接比较；小的口径差异只影响实现细节。
- 失败原因：项目曾把 DOTA-v1.5 GT 绑定给 DOTA-v1.0、混用 match 0.5/0.3、VOC07/all-point、macro/GT-weighted，并出现 duplicate 当 TP 和 per-image normalization 改写全局排序；另有 checkpoint/config head 缺失的 arm。它们分别改变数据、模型和评价对象，不是可忽略噪声。
- 后续做法：receipt 同时绑定 dataset/version/annotation digest、class schema、checkpoint/config/coder、coordinate frame、matcher occupancy、ignored policy、eval IoU、integration、aggregation 和 tie policy；binding 失败记 invalid，不算科学 PASS/FAIL。
- 边界：不同 estimand 都可能有研究价值；只有在标签清楚时才能并列报告，不能把一个口径的结论搬到另一个口径。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/FORENSIC_FINDINGS_V2.md`、`evidence/protocols/TOP_JOURNAL_FACTORIAL_GEOMETRY_CONFIRMATION_PROTOCOL_V8.md`、`evidence/protocols/ORQ_TOP_JOURNAL_ROUTE_CLOSEOUT_20260818.md`。

## 教训十七：单调校准改善 ECE 不会自动改善 ranking AP

- 失败命题：isotonic 或其它单调 calibration 让置信度更接近经验正确率，就可以作为 AP 改善或 oracle headroom 被回收的证据。
- 失败原因：同类内严格单调映射保持排序，而 AP 主要由排序决定；因此 ECE 可下降而 AP 不变。项目早期的 score collapse/recovery 还依赖被污染的 cell，不能用校准结果恢复。
- 后续做法：分别报告 calibration metric、排序改变数量、tie 处理、native AP 与 paired uncertainty；若目标是 AP，方法必须说明它如何合法改变排序以及如何控制 harmful swaps。
- 边界：calibration 对概率解释、阈值决策和风险控制仍可能有价值；本教训只否定用 calibration improvement 代替 ranking-effect 证据。
- 证据：`ziyu24/cqc_naood@5439b0cb4872b971a59e2e4bc0dfbc9a78ad285e` 的 `evidence/FORENSIC_FINDINGS_V2.md`、`evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md`。

## 方法族停止索引

下表只陈述当前证据提交中的有限停止范围；MI-PAR matching-aware successor 尚未被判定成功或失败。

| 方法族 | 最强负证据 | 停止范围 | 证据路径 |
| --- | --- | --- | --- |
| 历史 `wh-theta` oracle 叙事 | 位置错配与混合框表示；显式键复算改为四检测器一致的 `xy-wh` 主导 | 停止旧 10–31 pp、35/64 dominant 和 `wh-theta` 机制主张；保留认证后的 replacement oracle | `evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md`；`evidence/FORENSIC_FINDINGS_V2.md` |
| GCRR 跨域机制 | 六路线只有两条超过 matched null，四条失败 | 停止跨域正向机制；保留 DOTA-v1.5 指定条件下的局部反例与审计方法 | `evidence/canonical/phase3/jstars_gcrr_r1_r6_combined_presentation_v1.csv` |
| R-MetaDetect | 条件质量的局部信号没有形成跨域机制与冻结 coverage 的联合支持 | 停止当前 meta-quality TGRS 正向路线；不否定所有条件质量特征 | `evidence/SCIENTIFIC_EVIDENCE_BASELINE_V2.md` |
| QAnchor | 三个冻结 alpha 均未实现全环境 AP50/AP75 non-inferiority | 停止当前原生分数—质量分数混合规则；不否定其它校准目标 | `evidence/reports/source_alpha_selection_v1.report.json` |
| SPIR | 固定点只过一部分核心路线，训练 successor 首门失败 | 停止当前 score-source/fixed-point 方法族的多种子和 test 扩展 | `evidence/protocols/SPIR_TOP_JOURNAL_ROUTE_CLOSEOUT_20260816.md` |
| ORQ | proxy 相关但相对 native score 的增量覆盖不够，理论最大 PASS 数也达不到冻结门 | 停止当前 orbit-quality reranking；不否定 orbit residual 的诊断价值 | `evidence/protocols/ORQ_TOP_JOURNAL_ROUTE_CLOSEOUT_20260818.md` |
| PQA | 大样本显著但 AUC 增量远低于 materiality gate | 停止下一阶段质量头训练；不把 p 值包装成实际效用 | `evidence/protocols/IQU_PQA_Q3_L1_FINAL_CLOSEOUT_V1_20260818.md` |
| NTSR-OBB | AP75 delta 为 `-0.00004897`，paired interval 跨零且未过 materiality | 停止当前训练式 near-tie 排序及其消融扩展；不是排序学习的一般否定 | `evidence/protocols/NTSR_OBB_TOP_JOURNAL_ROUTE_CLOSEOUT_V1_20260819.md` |
| 旧 MI-PAR | 三个冻结规则全部 0 swap、0 AP delta，且训练标签后来被证明不是 native matching identity | 停止旧 raw-IoU 实现；不能外推到 matching-aware successor | `evidence/reports/mi_pairwise_abstaining_m02_v2.report.json`；`evidence/protocols/IQU_MIPAR_NATIVE_MATCHING_CORRECTION_V2_20260819.md` |
| matching-aware MI-PAR | 五源环境 pair population 结构 gate 通过，但尚无 outer-LOO、clean 或 prospective AP | 继续验证，当前不得写成正向方法或顶刊完成 | `evidence/reports/mipar_rescaled_lineage_pair_population_v12.report.json`；`evidence/protocols/IQU_MIPAR_MATCHING_AWARE_OUTER_LOO_METHOD_V8_20260820.md` |
