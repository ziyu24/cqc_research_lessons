# 当前项目核心进展

本页由各项目进展页生成；只展示最后已观察的事实，不是实时监控，也不改变[项目级状态](../PROJECT_STATUS.md)。任务下发不等于已启动，执行结束不等于已充分核验。维护方式见[主动更新约定](README.md)。

## 存活项目

| 项目 | 当前最核心进展 | 执行阶段（带观察时间） |
| --- | --- | --- |
| [P12](cqc_P12.md) | 原“相邻目标比孤立目标额外容易失败”的投入依据，经组级统计复算不成立；后续研究改为训练时扩展找证据的位置、仍预测原物体紧框，尚未完成DOTA同预算比较。 | 用户暂停；2026-09-30 03:50 UTC在46未观察到本项目训练进程，旧RUN失败状态不覆盖后来的原生续训与暂停历史。 |
| [P18](cqc_P18.md) | 原生PWOOD的复现与改进尚无整体目标达成证据；最新同起点比较中，全部删除无标签损失反而降低整体和小目标AP，不能把局部错误监督推成整条分支有害。 | 执行结束且C已复核；2026-09-30 03:50 UTC在46任务槽无任务、未观察到训练进程。 |
| [P20](cqc_P20.md) | 开放世界检测的主要短板仍是未知目标误检；复用DPOD作者权重得到55.01%未知召回，但未知AP仅2.01%，高召回并未解决可用性。 | 执行结束且C已复核；2026-09-30 03:50 UTC在26无任务、无本项目计算进程。 |
| [P21](cqc_P21.md) | 数量约束有条件正增益，但当前数量检测29.34 AP50仍低于公开点教师43.05；正在借鉴可学习区域分类，直接解决候选几何存在却认错类别的问题。 | 服务器执行中；2026-09-30 03:50 UTC在46核到r053 RUN及固定评分对照的双rank训练进程。 |
| [P22](cqc_P22.md) | 稀疏带噪弱框仍未学成可靠旋转检测；修正候选层边界后，排除分类冲突的teacher主指标未改善，不能再靠旧实现极小正差推进。 | B/C已下发，实际启动未确认；2026-09-30 03:50 UTC在26未观察该臂进程，主线任务与服务器旧槽有差异。 |
| [P23](cqc_P23.md) | 用同一SAM物理框约束旋转几何，在HRSC带噪条件有较大性能收益，无标签学习也有增量；独立创新和多类通用性仍未完成。 | 服务器执行中；2026-09-30 03:50 UTC在46核到r030 RUN及项目计算进程。 |
| [P24](cqc_P24.md) | 固定教师下同步减半两类训练计算，在HRSC固定终点保持AP并节省约17.8%总成本；不是所有质量目标都更快，也还没证明自适应或普遍收益。 | 服务器执行中；2026-09-30 03:51 UTC在星湖楼核到r022 RUN和相关计算进程。 |
| [P25](cqc_P25.md) | C于2026-09-30按用户授权交付五项零训练诊断：SODA/FAIR/HRSC已有域内模型评测、P27固定纯源全OBB参照、P19 H/O候选阶段核验。代码、唯一r020任务、配置、关键反例与执行入口已推送；锁定16个域内候选，合计28个模型域组合，限定26物理GPU 0、1，每项实际两卡，资源允许时并行。尚未实际启动GPU评测，没有本轮新指标；当前接口不能向另一SERVER聊天发送消息，交付明确执行指令，由SERVER登记实际启动。内部强弱诊断已完成，外部SSDG匹配参照仍缺，本轮不能替代它。 | 上一任务执行结束且C复核完成。当前唯一r020已交付任务单、代码及SERVER指令，GPU实际执行尚未启动/观察；不是执行结束。精确P25强参照和完整缩放训练仍未执行，不自动恢复。 |
| [P26](cqc_P26.md) | 旧子集上删除伪框回归提高了源旋转检测，但目标域绝对能力仍低；当前先建立全源图像、完整与稀疏弱框的可信参照，尚无跨域因果特征证据。 | 服务器执行中；2026-09-30 03:50 UTC在26实际执行根核到r016相关训练进程；旧Home RUN不代表当前实际任务。 |
| [P27](cqc_P27.md) | 已从冻结预测确认有实际AP损失的类别混淆：普通DA把大量集装箱报成large-vehicle、把风车报成helicopter。large-vehicle命中数增加但AP下降，GT辅助删除私有相关误检后比较方向反转；这确认了输出问题，尚未证明训练成因、可实现收益或OBB特异性。 | 固定源支持度任务已结束并经C复核。用户授权的冻结取样几何诊断已由SERVER执行结束并完成独立审计，未新增训练或种子；任务槽为空。保留B于2026-09-30 03:51 UTC对更早定位对照的观察；当前新结果待B/C作后续科学取舍，不把SERVER执行结束冒充跨端共识或项目目标达成。 |
| [P28](cqc_P28.md) | 固定源模型提供伪标签后，朴素在线退化明显缓解；剩余AP50缺口集中在大车类别。已抓到当前单域配方的错误反馈和类别保持问题，还不能称为已查清CTTA-OBB的主要科学问题：连续换域、遗忘和OBB特殊性尚无实验。 | 已复核（2026-09-30，B）。r007执行完整但未满足预定单视图联合条件，局部及双视图正结果保留；原始项目目标未达成，主线未被整体证伪。没有新的训练任务。 |
| [P29](cqc_P29.md) | 仅完成项目初始化，尚未登记科学问题或形成实验进展。 | 已创建、尚未下发；依据2026-09-30读取的当前主线，未声称服务器实时状态。 |
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
