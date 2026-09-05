# pcp-obb-beyond 科学问题与失败教训

审计基线：`ziyu24/pcp-obb-beyond@439e415ce3ded5fd1336bc2703160f7fa40c09c9`

快速阅读路径：先读“项目研究什么”→“教训一、二、三”→“方法族停止索引”。

## 项目研究什么

项目研究切片相关性和 NMS 阈值变化下的旋转框共形覆盖：标准交换性被图像切片与后处理依赖破坏时，能否得到稳健覆盖或校准修正。

## 领域位置与当前结论

- **事实**：5 数据集×9 切片协议和 6 配置×7 NMS 阈值共 435 个 calibration cells 的覆盖漂移分别不超过约 2.2/1.6 点，属于观测范围内的经验稳定性。
- **事实**：早期 IoU 密度上界假设被数据否定，后改用从同一批数据拟合的两参数指数 path X；最小 `R²=0.9111`，样本内 envelope 435/435 通过。
- **事实**：多类 raw+re-NMS 与旧 V7 pipeline 仍有约 `±2.6–3.3` 点差异；LSKNet 还曾因 image id 顺序错位使匹配数由 21/93 修复到 17722/30380。
- **推断**：现有 path X 是有用的经验包络和算法稳定性假说，但“样本内全覆盖”不能升级为 distribution-free 定理或未知部署保证。
- **未知**：独立确认集、预冻结函数族和严格有限样本选择后保证尚未完成；项目已停止维护。

## 实际采用过的方法

项目按母图/瓦片聚类评估覆盖，改变 NMS 阈值并拟合密度—覆盖关系，构造经验 envelope 与稳健系数，同时审计预测数组的 image_id 对齐和重跑 NMS 后的基线一致性。

## 教训一：同一批校准单元上的经验包络不是分布无关定理

- 失败命题：在 210 个校准单元上拟合密度与覆盖关系并实现百分之百样本内包络，就获得了对未知 NMS 变化的稳健理论保证。
- 失败原因：原密度假设已被数据否定，后续包络和系数仍由同一批样本选择并验证；约 0.911 的拟合优度与样本内全覆盖没有控制选择后的外推误差。
- 后续做法：把它明确标为经验模型，使用独立确认集或有限样本统一界，并预先冻结函数族和超参数。
- 边界：这是基于证据结构的推断；经验包络仍可用于已观测阈值范围内的工程敏感性分析，不能宣称 distribution-free。
- 证据：`ziyu24/pcp-obb-beyond@439e415ce3ded5fd1336bc2703160f7fa40c09c9` 的 `lab/failed_methods.md`、`lab/result.md`。

## 教训二：后处理改变时必须重建同一评价对象

- 失败命题：重跑 NMS 后的预测可以直接与旧 baseline 数字比较，并把差异归因于阈值。
- 失败原因：多类 NMS 的类内/类间处理、tie-breaking 和 image_id 顺序都可能改变候选集合；项目观察到覆盖可变化约正负 2.6 至 3.3 个百分点，自洽新流水线与历史流水线不是同一对象。
- 后续做法：保存原始候选、显式 image_id、类别和稳定排序键，在每个阈值下从同一 pre-NMS 输入重建成对基线。
- 边界：自洽流水线可以支持内部趋势，不能无校准地复现或覆盖历史数字。
- 证据：`ziyu24/pcp-obb-beyond@439e415ce3ded5fd1336bc2703160f7fa40c09c9` 的 `doc/notes/decision_log.md`、`doc/notes/bidirectional_sanity_dota_v10_r50_FAIL.json`。

## 教训三：处理切片依赖会改变保证的统计单位

- 失败命题：把瓦片按母图聚类后仍可宣称原来的逐瓦片交换性与覆盖保证。
- 失败原因：簇级校准把独立单位改成母图，可能更保守且 estimand 不同；瓦片数不再等于有效样本数。
- 后续做法：明确保证是对母图、瓦片还是对象成立，按同一单位划分校准/测试并报告簇大小和有效样本数。
- 边界：簇级方法可以正确处理依赖，但不能沿用逐瓦片保证的表述与样本量。
- 证据：`ziyu24/pcp-obb-beyond@439e415ce3ded5fd1336bc2703160f7fa40c09c9` 的 `lab/result.md`、`doc/notes/decision_log.md`。

## 方法族停止索引

| 方法族 | 最强负证据或限制 | 停止范围 | 当前 main 证据路径 |
| --- | --- | --- | --- |
| IoU-density bound | 原假设不满足真实 marginal/NMS-conditional 密度 | 停止原 A2 路线 | `lab/failed_methods.md`；`doc/notes/decision_log.md` |
| path-X exponential envelope | 函数与参数在同一网格拟合并验证，虽 435/435 cover、最小 R² `0.9111` | 仅作经验 envelope；停止 distribution-free 外推 | `doc/proofs/bound_report_v5_X.md`；`lab/result.md` |
| raw + re-NMS | 多类基线相对旧 pipeline 漂移约 `±2.6–3.3` 点 | 只支持同一 pipeline 横向阈值趋势 | `doc/notes/decision_log.md` |
| LSKNet alignment | image id 顺序错位曾使 matched pairs 几乎清空 | 停止任何未冻结 ID 映射的比较 | `doc/notes/decision_log.md` |
| tile clustering | 独立单位从 tile 改为母图 | 允许簇级保证；停止沿用 tile 样本量和措辞 | `doc/collaborator_handoff/01_research_question.md` |
