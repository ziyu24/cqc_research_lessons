# P28 项目进展

## 最初科学问题

源训练完成后，能否利用陆续到达的无标签目标图像改善旋转检测，并在连续域变化中保持收益、抑制有害更新和遗忘。

## 核心进展

当前DOTA-v1.5→FAIR1M单遍流中，只训练轻量残差适配器已相对同监督全参数条件臂同时提高AP50/AP75、减少背景FP并增加大车保持，预定机制正信号通过；但AP75仍略低固定源硬监督，更强联合条件失败。独立域、连续换域、遗忘和OBB特殊性仍无证据。

B于2026-10-01 PDT实现并交付的r011已由SERVER完整执行：沿用条件前景监督、冻结原检测参数、仅训练16块残差适配器，借鉴WHW组件而非完整复现。单视图AP50/AP75为55.984/28.935，高于条件前景53.744/28.417和冻结53.234/27.936；AP75仍低于固定源硬监督29.020。补充确认已有Oriented R-CNN遥感无源适应近邻；本项目也属于无源，潜在贡献在严格在线/连续旋转检测协议及其必要解法，不能把OBB+无源适应泛称空白或已成立的新范式。

已完成的单视图AP50/AP75主要参照为：冻结53.234/27.936、固定源硬监督53.157/29.020、条件前景分布53.744/28.417、选择性背景权重54.041/27.902、等平均背景权重53.767/28.306。选择性臂大车AP50/召回18.376/31.530%，但背景FP为23,018；等平均对照为16.680/29.635%和16,528。选择性臂只在AP50领先对照，AP75低0.404点，性能与选择性正信号均未通过。

用户已明确近期继续做好当前FAIR1M目标域，原始TTA→CTTA长期目标不变；FAIR1M尚未拆成A/B，SODA-A尚未执行。此前连续流设计只是未来参考，不是当前已运行实验。

## 服务器当前内容

SERVER于2026-10-01 12:21 UTC在46物理GPU 0、1启动背景可靠性任务，先完成选择性权重主臂，再完成等平均权重必要对照；两个臂均为DDP world-size 2。RUN于2026-10-01 23:34:54 UTC正常结束，exit=0，完整两卡RUN约22.45 GPU小时。

两臂各完整覆盖16,239原图/22,618切片，完成14,644次更新、1,595次跳过、232,294个固定源伪框；预测ID各16,239，缺失/额外/临时文件均为0。两份最终状态、评分、错误诊断、大车配对和顶层比较均已生成，任务相关进程已退出。SERVER已将结果、主要失败、恢复入口和两份checkpoint保护推送到`a3bf20f`。B于2026-10-01 17:14 PDT起独立回读并复核，追加零训练统计定位，来源为`070c83b`。该任务已结束且已由B复核。

SERVER于2026-10-02 03:27:26 UTC在46物理GPU 0、1从cursor 0实际启动r011，RUN为DDP world-size 2，并于09:12:31 UTC正常结束、exit=0。先前一次错误选择GPU 3、2的启动在首批后按用户指定终止，残留与正式输出隔离，不纳入科学结果；正式RUN保留任务号r011并绑定0、1。

r011完整覆盖16,239原图/22,618切片，完成14,644次更新、1,595次跳过、232,294个固定源伪框；16,239个预测ID与固定stream全集精确相等。评分、错误诊断、大车配对和comparison均已生成，正式最终状态已保护，任务进程已退出。训练循环约10.57 GPU小时；来源结果和恢复材料已推送到`832a2ca`，当前为执行结束待B/C独立复核。

## 核验说明

SERVER已回读运行时配置、RUN、两rank首步与终点日志、运行器GPU观察、预测全集、全部统计JSON及两份完整恢复状态。两个launcher阶段均观察到物理GPU 0、1为`MATCH`；首更新有有限梯度、student/EMA改变、固定源不变。最终状态均含348项student、348项teacher、156项optimizer状态、两rank RNG和cursor=16,239。

本轮继续使用修复DOTA-v1.5标签后训练的源best，没有使用旧缺陷切片训练权重；FAIR1M报告复用前已回源快检为`UNCHANGED/PASS`，未重读图像字节。选择性/均匀两臂的负权重离切片均值偏差和分别为656,933.78/0.29，首个相同输入批次的负权重总量匹配，证明干预按设计发生而非退化成同一实现。

B已直接回核运行时配置、完整预测ID、原始JSON/日志及两份496,089,375字节状态。两次MATCH分别对应真实双rank，首批有限梯度、学生/EMA变化和固定源不变；终点恢复内容及权重统计与summary一致，原配置保护有效。原生与独立评分全部平均/逐类AP精确一致，错误计数和GT分母、大车配对闭合；回源再次UNCHANGED/PASS且未扫图像字节。运行、协议、指标、判据和保护已经充分独立核验；跨种子、独立域、CTTA、遗忘及OBB独有性仍未核，因为没有相应实验。

B已直接复算现有统计，0模型前向、0更新、0 GPU小时。主臂比均匀对照新增6,490个高分背景FP，小车贡献5,000个（77.04%）；小车与船对平均AP75差分别贡献−0.234、−0.173点。小车严格TP净增165，严格FP增加21,082，后者还包含定位未达严格阈值的错误。不能把AP75下降直接当大规模准确框消失，也不能把上述输出算术当训练损失因果或逐GT得失配对。

r011正式RUN首批已核：两个rank均报告world-size 2，运行器PID树对物理GPU 0、1回读为`MATCH`；首更新梯度有限，211,702个可训练参数仅位于16块适配器，适配器跨rank同步，原检测参数和buffer、固定源教师均未改变，student与adapter-only EMA均发生非零变化。首批峰值显存约2,374 MiB/卡。上述只证明机制和执行成立，不证明性能。

SERVER终点复核已读取RUN、两rank摘要、预测ID全集、原生及独立错误统计、大车配对、comparison和完整checkpoint。终点student/teacher各412项，其中64项adapter；optimizer 64项、双rank RNG齐全。去掉adapter后的348项student/teacher张量均与r001源checkpoint精确相等，adapter与EMA实际改变；原生AP与独立错误汇总逐类精确一致，TP/漏检、错误桶、预测分母及大车配对全部闭合。该核验足以支持执行者裁决，B/C尚未独立复核；跨种子、独立域、CTTA、遗忘和OBB独有性仍未核。

## 执行阶段

背景可靠性任务已执行结束并由B复核，性能、选择性和联合正信号均为否。适配器任务已执行结束并由SERVER完成协议/产物裁决，机制正信号为是，更强联合条件为否，等待B/C独立复核；不能因局部阳性改写成项目成功。项目原始科学目标尚未达成，广义TTA-OBB→CTTA-OBB路线未被本轮整体证伪；未被证伪不等于成功。

## 下一步与维护

适配器固定配方已完整结束，不通过位置、比例、宽度或学习率扫描继续维护。结果证明改变错误监督能修改的参数范围是有判别力的路径，但不等于已证明检测头漂移是根因；固定源背景概率逐RoI加权同样不再追加温度、阈值或权重扫描。

当前累计最好单视图AP50来自adapter，严格AP75仍由固定源硬监督略高；下一科学问题需由B/C在完整累计证据和独立复核上重新形成。冻结原参数不保证输出框不变，adapter阳性也不是唯一根因证明。近期仍优先做好当前FAIR1M域，原始TTA→CTTA长期目标不变；本页不自动授权新训练路线。

公开方法边界已补核：CLIP-Guided SFOD（IGARSS2024）已有遥感OBB无源适应，但非当前单遍在线；其前景CLIP分类不能直接判背景。完整WHW需要额外源统计，当前不静默加入；TTAOD-F已发表于NeurIPS2025，实际基础模型和记忆结构不能直接当现有OBB实验。外部CLIP/RemoteCLIP仅列冻结候选判别备选，需证明超出源分数的增量并披露预训练数据重叠未知，不作为主实验的前置门槛。

本次已推送完整r011结果、失败边界、恢复入口和最终状态保护，并清空唯一任务槽。累计正结果与具体失败分别保留；原始TTA→CTTA目标未达成，尚无CTTA或OBB独有机制证据，不把单域adapter机制阳性称为项目成功。

## 证据

[r010完整结果与产物保护](https://github.com/ziyu24/cqc_P28/blob/a3bf20f2269617c8f15bf4a758ce5b5796558ea0/lab/result.md)；[主要失败边界](https://github.com/ziyu24/cqc_P28/blob/a3bf20f2269617c8f15bf4a758ce5b5796558ea0/lab/failed_methods.md)；[当前科学判断](https://github.com/ziyu24/cqc_P28/blob/a3bf20f2269617c8f15bf4a758ce5b5796558ea0/lab/discussion.md)；[已清空任务槽](https://github.com/ziyu24/cqc_P28/blob/a3bf20f2269617c8f15bf4a758ce5b5796558ea0/lab/sug.md)；[执行配置与保护](https://github.com/ziyu24/cqc_P28/blob/a3bf20f2269617c8f15bf4a758ce5b5796558ea0/configs/r010.json)。

[B独立复核与零训练补核](https://github.com/ziyu24/cqc_P28/blob/070c83b3dfda01673c0a808ae32040b0852e8266/lab/result.md)；[补核入口](https://github.com/ziyu24/cqc_P28/blob/070c83b3dfda01673c0a808ae32040b0852e8266/src/summarize_background_transfer.py)；[复核后的核心问题](https://github.com/ziyu24/cqc_P28/blob/070c83b3dfda01673c0a808ae32040b0852e8266/lab/discussion.md)。

[B深入调研、源码边界与下一步方案](https://github.com/ziyu24/cqc_P28/blob/266e75030d8b71c671a4479588930812ae254046/lab/discussion.md)。

[B适配器机制交付与范式边界修正](https://github.com/ziyu24/cqc_P28/blob/3cba31bc71291cec6829e69071683051f5727aed/lab/discussion.md)；[唯一r011任务](https://github.com/ziyu24/cqc_P28/blob/3cba31bc71291cec6829e69071683051f5727aed/lab/sug.md)；[执行与检查证据](https://github.com/ziyu24/cqc_P28/blob/3cba31bc71291cec6829e69071683051f5727aed/doc/execution.md)；[新增机制](https://github.com/ziyu24/cqc_P28/blob/3cba31bc71291cec6829e69071683051f5727aed/src/online_adapter.py)。

[r011恢复入口](https://github.com/ziyu24/cqc_P28/blob/4324fbb0e49c3b60a999799dcd7fab9207f3b600/configs/r011.recovery.json)。

[r011完整结果与保护](https://github.com/ziyu24/cqc_P28/blob/832a2cab34df3702776b197067b7be16bfb2f9ea/lab/result.md)；[失败边界](https://github.com/ziyu24/cqc_P28/blob/832a2cab34df3702776b197067b7be16bfb2f9ea/lab/failed_methods.md)；[当前科学结论](https://github.com/ziyu24/cqc_P28/blob/832a2cab34df3702776b197067b7be16bfb2f9ea/lab/discussion.md)；[已清空任务槽](https://github.com/ziyu24/cqc_P28/blob/832a2cab34df3702776b197067b7be16bfb2f9ea/lab/sug.md)。
