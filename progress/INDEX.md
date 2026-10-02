# 当前项目核心进展

本页由各项目进展页生成；只展示最后已观察的事实，不是实时监控，也不改变[项目级状态](../PROJECT_STATUS.md)。任务下发不等于已启动，执行结束不等于已充分核验。维护方式见[主动更新约定](README.md)。

## 存活项目

| 项目 | 当前最核心进展 | 执行阶段（带观察时间） |
| --- | --- | --- |
| [P12](cqc_P12.md) | 原“相邻目标比孤立目标额外容易失败”的投入依据，经组级统计复算不成立；后续研究改为训练时扩展找证据的位置、仍预测原物体紧框，尚未完成DOTA同预算比较。 | 用户暂停；2026-09-30 03:50 UTC在46未观察到本项目训练进程，旧RUN失败状态不覆盖后来的原生续训与暂停历史。 |
| [P18](cqc_P18.md) | 选择性放大在DOTA与DIOR-R已有约2个AP点收益及部分真实成本证据，但数量选区相对同预算不确定性选区仅领先0.187/0.054点，尚未建立独立机制贡献。单尺度学生没有可靠联合改进，项目整体目标未达成，当前不足以支撑明确顶刊竞争力。 | 执行结束且C已复核；2026-10-02 05:51 UTC在46无任务、未观察到本项目进程，无新增实验结果。 |
| [P20](cqc_P20.md) | 未知目标的排序与误检仍未解决：SPWOOD上的末端高斯未知AP为0.6571%，前移筛选退至0.5113%；已有局部增益，但尚无有效完整方法或顶刊贡献证据。 | 执行结束且C已作有边界复核；2026-10-01 23:03 PDT（10月2日06:03 UTC）观察时无任务、无本项目计算进程，新方案尚未下发。 |
| [P21](cqc_P21.md) | DOTA当前最强数量模型的原图VOC07 AP50已提高到37.7601、面积AP36.8639，可靠缺席类负监督相对原35.7140/34.4634通过既定联合条件，且13/15类AP提高。C已充分独立复核；收益主要表现为误报减少和排序改善，全部正确检出仅净增7，正实例供给/空间标签质量仍有改进空间。它不是精确正数量值或U的独立收益，也不代表项目总体或顶刊目标完成。 | 上一轮可靠负监督已执行结束并由C充分复核，37.7601强参照继续保留。当前唯一任务r057的两次训练前工程退出已修复并保留attempt记录；accurate已执行结束且主联合门槛失败，实际双AP正增量保留。permuted现正以seed42、实际2卡执行12轮/47256更新，完成后立即评测；新增数量对应贡献仍未知。项目总体目标、U独立价值、跨seed稳定性及顶刊创新证据仍未完成，没有真实B端讨论或双方共识。 |
| [P22](cqc_P22.md) | 稀疏带噪弱框仍未学成可靠旋转检测：目标发现不足与几何误差并存。修正候选层边界后，排除分类冲突使teacher AP50比原生对照低1.0095个百分点，AP75均为4.5455%；目前没有支撑顶刊方法贡献的有效机制证据。 | r014已完成并经C复核；r015已交付但在26无启动记录。C最新观察为2026-10-01 23:08 PDT；本轮仅汇报与制定方案，没有新训练下发。 |
| [P23](cqc_P23.md) | 用同一SAM物理框约束旋转几何，在HRSC带噪条件有较大性能收益，无标签学习也有增量；独立创新和多类通用性仍未完成。 | 服务器执行异常结束；2026-10-02 04:49 UTC在46核到r030于96000/120000评测期间被SIGTERM终止并标记STOPPED。96000步完整恢复点有效、此前物理GPU 2、3绑定持续MATCH，但命令退出不是科学完成，尚缺24000步训练及96000步起的既定评测。 |
| [P24](cqc_P24.md) | 固定教师下同步减半两类训练计算，在HRSC固定终点保持AP并节省约17.8%总成本；不是所有质量目标都更快，也还没证明自适应或普遍收益。 | 服务器执行中；2026-09-30 03:51 UTC在星湖楼核到r022 RUN和相关计算进程。 |
| [P25](cqc_P25.md) | 内部强弱、域内参照诊断与作者原生模块核验已完成。C已交付r022完整单源旋转适配及语言机制开/关两臂，按用户要求并行且每臂实际两卡；CPU实际权重、全部L/U加载和两臂相同初态通过。尚无新训练AP，外部SSDG匹配性能参照和弱标注成本问题仍未解决。 | 主/辅卡均衡已实际落实：复用B反序零更新CUDA检查及两臂3200步严格完整恢复证据，不重复等待确认。用户明确允许下一完整保存核验后外部受控退出并接受少量在途/未保存更新回退；两臂各在06:01:19/24 UTC核完整12800保存后退出，旧训练/worker及已识别加载子进程均已退出，再于06:01:53 UTC同r022续接。A/B实际新PID分别2394328/2394329，UUID顺序0/1与1/0，两个gpu-check均MATCH、两卡实际前后向及步数增长通过。原日志、完整恢复状态和旧attempt记录保留，未用更早checkpoint、未重训；全局4L+2U、采样、seed42、归约、优化器/LR/EMA、120k及冻结评测未变。原生DataLoader预取不保存，实际未保存/在途回退步数未观察，不能宣称位级batch轨迹连续。 |
| [P26](cqc_P26.md) | 旧子集上删除伪框回归提高了源旋转检测，但目标域绝对能力仍低；当前先建立全源图像、完整与稀疏弱框的可信参照，尚无跨域因果特征证据。 | 服务器执行中；2026-09-30 15:23 UTC在26实际启动r016完整HBB臂，双卡与全15749切片覆盖已核；后续评测与汇总已接入同一任务恢复入口。 |
| [P27](cqc_P27.md) | 用户点名CLIP-Guided SFOD后，已补核其OBB闭集适应，以及遥感OSSOD的跨库类别不一致训练、SS-OWFormer的开放世界OBB。完整UniDA＋目标域OBB同条件工作本轮仍未找到，但创新主张须限定为既有Universal设定的旋转遥感任务/基准扩展，不能把普通DA-OBB或未知OBB称首次。原r013方法试验不变，方法收益仍待实际结果。 | 2026-10-02 05:39 UTC，SERVER在46的GPU2/3实际启动r013；完整臂已完成首个双rank优化步，任务处于执行中，尚未形成性能或拒识结论。固定DPA已科学结束并复核，原项目仍运行，目标与成功边界不变。 |
| [P28](cqc_P28.md) | 当前DOTA-v1.5→FAIR1M单遍流中，只训练轻量残差适配器已相对同监督全参数条件臂同时提高AP50/AP75、减少背景FP并增加大车保持，预定机制正信号通过；但AP75仍略低固定源硬监督，更强联合条件失败。独立域、连续换域、遗忘和OBB特殊性仍无证据。 | 背景可靠性任务已执行结束并由B复核，性能、选择性和联合正信号均为否。适配器任务已执行结束并由SERVER完成协议/产物裁决，机制正信号为是，更强联合条件为否，等待B/C独立复核；不能因局部阳性改写成项目成功。项目原始科学目标尚未达成，广义TTA-OBB→CTTA-OBB路线未被本轮整体证伪；未被证伪不等于成功。 |
| [P29](cqc_P29.md) | C已交付正式DOTA＋FAIR→SODA四类主实验，HRSC只保留已有探针，不再执行上版提议的整套HRSC开发训练。r006科学代码、实际输入准备和CPU集成已完成，SERVER已在46实际启动两卡训练。本轮独立补FAIR四类源，再检验普通可见源监督及第二教师的额外作用；不是已经实现新的质量学习方法，原项目目标仍未达成。 | 项目继续运行但执行已按用户要求暂停。r005已执行结束并由C独立复核；r006已正式交付，2026-10-02 04:50:58–05:37:31 UTC在46实际执行到FAIR源第1轮完成，当前无P29训练进程。原目标、正式主路线和单容量部署条件不变；固定union探针失败不等于整个问题被证伪。C交付段记录者为C，SERVER执行段记录者为SERVER；没有对端原线程回写，不称跨端共识。 |
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
