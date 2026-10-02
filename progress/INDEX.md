# 当前项目核心进展

本页由各项目进展页生成；只展示最后已观察的事实，不是实时监控，也不改变[项目级状态](../PROJECT_STATUS.md)。任务下发不等于已启动，执行结束不等于已充分核验。维护方式见[主动更新约定](README.md)。

## 存活项目

| 项目 | 当前最核心进展 | 执行阶段（带观察时间） |
| --- | --- | --- |
| [P12](cqc_P12.md) | 原“相邻目标比孤立目标额外容易失败”的投入依据，经组级统计复算不成立；后续研究改为训练时扩展找证据的位置、仍预测原物体紧框，尚未完成DOTA同预算比较。 | 用户暂停；2026-09-30 03:50 UTC在46未观察到本项目训练进程，旧RUN失败状态不覆盖后来的原生续训与暂停历史。 |
| [P18](cqc_P18.md) | 原生PWOOD的复现与改进尚无整体目标达成证据；最新同起点比较中，全部删除无标签损失反而降低整体和小目标AP，不能把局部错误监督推成整条分支有害。 | 执行结束且C已复核；2026-09-30 03:50 UTC在46任务槽无任务、未观察到训练进程。 |
| [P20](cqc_P20.md) | 开放世界检测的主要短板仍是未知目标误检；复用DPOD作者权重得到55.01%未知召回，但未知AP仅2.01%，高召回并未解决可用性。 | 执行结束且C已复核；2026-09-30 03:50 UTC在26无任务、无本项目计算进程。 |
| [P21](cqc_P21.md) | DOTA当前最强数量模型的原图VOC07 AP50已提高到37.7601、面积AP36.8639，可靠缺席类负监督相对原35.7140/34.4634通过既定联合条件，且13/15类AP提高。C已充分独立复核；收益主要表现为误报减少和排序改善，全部正确检出仅净增7，正实例供给/空间标签质量仍有改进空间。它不是精确正数量值或U的独立收益，也不代表项目总体或顶刊目标完成。 | 上一轮可靠负监督已执行结束并由C充分复核，37.7601强参照继续保留。用户已认可强教师更新L及必要数量对应控制，当前唯一任务r057已正式下发，等待SERVER实际执行；没有把交付完成写成训练已开始。每臂完成立即评测，再自动继续下一臂，无需等用户在线。实际涨点与新阶段数量对应收益均未知；项目总体目标、U独立价值、跨seed稳定性及顶刊创新证据仍未完成，没有真实B端讨论或双方共识。 |
| [P22](cqc_P22.md) | 稀疏带噪弱框仍未学成可靠旋转检测；修正候选层边界后，排除分类冲突的teacher主指标未改善，不能再靠旧实现极小正差推进。 | B/C已下发，实际启动未确认；2026-09-30 03:50 UTC在26未观察该臂进程，主线任务与服务器旧槽有差异。 |
| [P23](cqc_P23.md) | 用同一SAM物理框约束旋转几何，在HRSC带噪条件有较大性能收益，无标签学习也有增量；独立创新和多类通用性仍未完成。 | 服务器执行中；2026-10-02 00:21 UTC在46核到r030由80800步恢复后推进至80900/120000，物理GPU 2、3均有同一训练PID的计算与显存记录。 |
| [P24](cqc_P24.md) | 固定教师下同步减半两类训练计算，在HRSC固定终点保持AP并节省约17.8%总成本；不是所有质量目标都更快，也还没证明自适应或普遍收益。 | 服务器执行中；2026-09-30 03:51 UTC在星湖楼核到r022 RUN和相关计算进程。 |
| [P25](cqc_P25.md) | 内部强弱、域内参照诊断与作者原生模块核验已完成。C已交付r022完整单源旋转适配及语言机制开/关两臂，按用户要求并行且每臂实际两卡；CPU实际权重、全部L/U加载和两臂相同初态通过。尚无新训练AP，外部SSDG匹配性能参照和弱标注成本问题仍未解决。 | 主/辅卡均衡已实际落实：复用B反序零更新CUDA检查及两臂3200步严格完整恢复证据，不重复等待确认。用户明确允许下一完整保存核验后外部受控退出并接受少量在途/未保存更新回退；两臂各在06:01:19/24 UTC核完整12800保存后退出，旧训练/worker及已识别加载子进程均已退出，再于06:01:53 UTC同r022续接。A/B实际新PID分别2394328/2394329，UUID顺序0/1与1/0，两个gpu-check均MATCH、两卡实际前后向及步数增长通过。原日志、完整恢复状态和旧attempt记录保留，未用更早checkpoint、未重训；全局4L+2U、采样、seed42、归约、优化器/LR/EMA、120k及冻结评测未变。原生DataLoader预取不保存，实际未保存/在途回退步数未观察，不能宣称位级batch轨迹连续。 |
| [P26](cqc_P26.md) | 旧子集上删除伪框回归提高了源旋转检测，但目标域绝对能力仍低；当前先建立全源图像、完整与稀疏弱框的可信参照，尚无跨域因果特征证据。 | 服务器执行中；2026-09-30 15:23 UTC在26实际启动r016完整HBB臂，双卡与全15749切片覆盖已核；后续评测与汇总已接入同一任务恢复入口。 |
| [P27](cqc_P27.md) | 完整DPA固定适配未达原联合目标，独立调研后已提出下一候选：保留普通DA，用源标签学习已知类别判别表征及显式拒识边界，优先借鉴OpenDet的CFL+UPL。当前只形成有依据的方案，尚未实现或下发，更没有验证有效。已确认的是有AP损失的语义混淆子问题，尚未确认唯一训练根因或OBB特有机制；大车—container不能代替整个七共享类检测目标。 | 2026-10-01 PDT，C已完成r012科学复核；随后按用户要求完成独立文献/作者代码与累计证据复查，提出新的边界学习候选，未实施或派发。固定DPA适配按原终点结束，任务槽保持空。现有曲线能回答的阈值疑点已查清，不再以调阈值、系数、模块拆分或追加种子延长本任务；原项目继续运行，针对性方法与完整研究结论尚未形成，不登记项目结束。 |
| [P28](cqc_P28.md) | 当前DOTA-v1.5→FAIR1M单遍流已观察到条件前景目标相对冻结的双AP正差约0.5点。最新背景概率加权提高大车保持，却不如同量统一降权保持AP75和背景精度，联合命题失败；B独立复核已完成。零训练补核定位到新增高分背景误检主要来自小车，不能直接归因于准确框大量消失。独立域、连续换域、遗忘和OBB特殊性仍无证据。 | 背景可靠性任务已执行结束并由B复核。性能正信号、选择性正信号及联合正信号均为否；局部大车改善保留为事实，但不改判整体失败。适配器任务已交付、尚无实际GPU运行/性能证据。项目原始科学目标尚未达成，广义TTA-OBB→CTTA-OBB路线未被本轮整体证伪；未被证伪不等于成功。 |
| [P29](cqc_P29.md) | C已独立核实：相同DOTA初态和预算下，直接合并两个教师的伪标签训练学生，反而比只用FAIR伪标签低8.82个AP50百分点。union AP50/AP75为0.399136/0.291599，FAIR监督学生为0.487296/0.333018，冻结FAIR教师为0.506138/0.356322。本轮执行完整、固定配方失败，原项目目标尚未达成。C已根据论文与实际源码形成下一方案：补齐真实四类源教师，先检验普通可见源监督及第二教师的额外作用，再判断候选质量学习的必要性；方案已发布，未下发训练。 | 项目继续运行。r005已执行结束并由C独立复核；2026-10-01（C本地日期）完成深度调研和方案发布，尚未下发新任务，未启动新训练。SODA主实验和MS-02尚未执行。固定union路线失败不等于整个问题被证伪。记录者C，没有对端原线程回写，不称跨端共识。 |
| [P30](cqc_P30.md) | 仅完成项目初始化，尚未登记科学问题或形成实验进展。 | 已创建、尚未下发；依据2026-09-30读取的当前主线，未声称服务器实时状态。 |
| [orientbench](orientbench.md) | 此前标签版本和集合技术检查没有建立新的评价推断方法；当前转为检验少量整图查询能否估计完整AP差，不新增人工标注或网络训练。 | B已下发，实际执行未确认；2026-09-30 03:50 UTC在26未观察到当前任务进程，服务器副本落后。 |
| [OrientDA](OrientDA.md) | 更强UCR候选把旧方案AP75从6.26提高到18.29，但仍低于直接UCR的23.30；当前没有超过强目标弱框对照的证据。 | 执行结束；2026-09-30 03:50 UTC在46任务槽无任务、无项目计算进程。 |

## 已结束及历史项目

以下仅保留本库已有登记与来源摘要；建立页面不恢复维护，也不进入停止维护仓库。

- [P1](cqc_P1.md)：失败。
- [P2](cqc_P2.md)：失败。
- [P3](cqc_P3.md)：失败。
- [P4](cqc_P4.md)：失败。
- [P5](cqc_P5.md)：失败。
- [P6](cqc_P6.md)：失败。
- [P7](cqc_P7.md)：失败。
- [P8](cqc_P8.md)：失败。
- [P9](cqc_P9.md)：失败。
- [P10](cqc_P10.md)：失败。
- [P11](cqc_P11.md)：失败。
- [P13](cqc_P13.md)：失败。
- [P14](cqc_P14.md)：失败。
- [P15](cqc_P15.md)：失败。
- [P16](cqc_P16.md)：失败。
- [P17](cqc_P17.md)：失败。
- [P19](cqc_P19.md)：失败。
- [bgc_obb](bgc_obb.md)：失败。
- [cerq](cerq.md)：失败。
- [cqc_naood](cqc_naood.md)：失败。
- [cqc_T1](cqc_T1.md)：失败。
- [cqc_T2](cqc_T2.md)：失败。
- [D7_pcp_obb_foundation](D7_pcp_obb_foundation.md)：失败。
- [DG-OBB](DG-OBB.md)：失败。
- [dgobb-synthprobe](dgobb-synthprobe.md)：失败。
- [GeoPDE-OBB](GeoPDE-OBB.md)：失败。
- [GeoStructDOTA](GeoStructDOTA.md)：失败。
- [pcp-obb](pcp-obb.md)：失败。
- [pcp-obb-acquisition-risk](pcp-obb-acquisition-risk.md)：失败。
- [pcp-obb-beyond](pcp-obb-beyond.md)：失败。
- [pcp-obb-score-study](pcp-obb-score-study.md)：失败。
- [SynDOTAForge](SynDOTAForge.md)：失败。
- [TAOS](TAOS.md)：失败。
- [axial-conformal-inference](axial-conformal-inference.md)：失败。
- [Censored-OBB-Base](Censored-OBB-Base.md)：失败。
- [CensoredTile-OBB](CensoredTile-OBB.md)：失败。
- [cods-obb](cods-obb.md)：失败。
- [conformal-mmrotate](conformal-mmrotate.md)：失败。
- [cqc-P1](cqc-P1.md)：失败。
- [D17_FragmentStitch-OBB](D17_FragmentStitch-OBB.md)：失败。
- [D17_TileBoundary-OBB-Benchmark](D17_TileBoundary-OBB-Benchmark.md)：失败。
- [DenseOBB-B1C3](DenseOBB-B1C3.md)：失败。
- [frozen-query-obb](frozen-query-obb.md)：失败。
- [geosense-obb](geosense-obb.md)：失败。
- [GeoSupport-OBB-LT](GeoSupport-OBB-LT.md)：失败。
- [HoML-OBB](HoML-OBB.md)：失败。
- [iev-obb](iev-obb.md)：失败。
- [kappagate-obb](kappagate-obb.md)：失败。
- [longfpn-obb](longfpn-obb.md)：失败。
- [lspassign](lspassign.md)：失败。
- [mobiusobb](mobiusobb.md)：失败。
- [obb-input-aligned-distill](obb-input-aligned-distill.md)：失败。
- [oriented-detection-risk-control](oriented-detection-risk-control.md)：失败。
- [OVShape-OBB](OVShape-OBB.md)：失败。
- [pcb-obb](pcb-obb.md)：失败。
- [Phase-Tiny-OBB](Phase-Tiny-OBB.md)：失败。
- [retrieval-obb](retrieval-obb.md)：失败。
- [SuppressionRank-OBB](SuppressionRank-OBB.md)：失败。
- [symq-obb](symq-obb.md)：失败。
