# cqc_P5 避坑点

审计基线：`ziyu24/cqc_P5@1093b8b57a9a8dc13a8e520376caa9b826a9fb33`

## P5-01 Oracle 分支实现无效时小增益没有科学含义

- 类型：协议/实现无效。
- 为何失败：R1 报告 `ORACLE-IGNORE - NAIVE = +0.488 AP_tiny`，但 MMDetection 的 ignore IoF 参数方向与项目假设不一致，部分 hidden GT 没有被正确处理；随机初始化、单 seed 和错误 bootstrap 又放大了不可解释性。
- 避坑：先用构造性 anchor 反例验证 assigner 语义，再允许训练；oracle 若未精确实现，结果只能记无效，不与科学阈值比较。
- 边界：不否定 missing-instance 负监督问题，只否定 R1 的实现和数值。
- 证据：`ziyu24/cqc_P5@1093b8b57a9a8dc13a8e520376caa9b826a9fb33` 的 `research/EVIDENCE.md`、`research/R1_RESULT_REVIEW.md`。

## P5-02 几何覆盖门不得与数据边界天然冲突

- 类型：协议/实现无效。
- 为何失败：R1A 要求 inside anchor 对每个 hidden fitted box 的 IoF 达到 `0.5`，边界实例最大值却为 `0.499989837`；裁剪 hidden 分母会改变标签几何，豁免边界又改变目标总体，导致门本身不成立，训练前即停止。
- 避坑：冻结门前用边界构造例验证可满足性；若目标是 assignment 变化，直接比较 stock assignment delta，不用不可达的覆盖代理。
- 边界：这是门定义失败，不是 MNAR 效应为零，也没有任何训练结果。
- 证据：`ziyu24/cqc_P5@1093b8b57a9a8dc13a8e520376caa9b826a9fb33` 的 `research/EVIDENCE.md`、`research/R1A_STAGE_A_REVIEW.md`。

## P5-03 “统一标签空间+匹配检测器”不足以构成新主线

- 类型：科学证伪。
- 为何失败：现有 LAE、Wholly-WOOD、UniconDet 等已覆盖大部分统一标签/粒度和检测器适配对象；原主线因直接近邻撞车停止，不能靠加入遥感数据或换名称恢复。
- 避坑：新路线必须改变可识别的政策风险或推断对象，并正面超过当前强基线；基础集成只作工程底座。
- 边界：这不否定统一数据工具的复用价值。
- 证据：`ziyu24/cqc_P5@1093b8b57a9a8dc13a8e520376caa9b826a9fb33` 的 `research/PROJECT_STATUS.md`、`research/EVIDENCE.md`。
## P5-04 缺失政策与标注粒度政策不能混称

- 类型：范围限制。
- 为何失败：DOTA v1.0/v1.5 的同图补标可研究 size-dependent missingness，而固定实例只把 Point/HBox 粒度改变的是 annotation-granularity stress；二者的处理、基线和风险估计不同。
- 避坑：固定每条路线的实例集合和政策变量；缺实例、弱标签与潜在物理轮廓分别命名和估计。
- 边界：两类政策可在后续共同框架中比较，但不能用一类实验支持另一类结论。
- 证据：`ziyu24/cqc_P5@1093b8b57a9a8dc13a8e520376caa9b826a9fb33` 的 `research/PROJECT_STATUS.md`、`research/EVIDENCE.md`。
