# P27 项目进展

## 最初科学问题

类别集合不一致、重叠关系未知时，能否利用有标注源域与无标签目标域改善共享类别的旋转目标检测。

## 核心进展

目前仍卡在保住共享检测能力同时减少主要私有误报，原目标尚未达成。完整DPA相对同结构普通对照的目标val AP50小幅提高0.143个百分点，但源best略低、large-vehicle AP50下降，并且同TP下container主导的私有FP更多；因此只能记总体性能小幅收益，不能称“保检测降混淆”成功。r012已执行结束并归纳，等待B/C科学复核，不启动调参、消融或多种子支线。

本次借鉴UniOT完成目标结构学习PCD与部分匹配CCD的检测适配。完整/去PCD两臂目标val AP50为41.739%/43.409%，均低于普通DA 52.062%；完整臂还低于去PCD 1.669个百分点，并同时损失共享和large-vehicle召回、增加主要私有误报。因此本次固定适配、PCD正贡献和“保召回降混淆”三项主张均失败。去PCD在固定全共享TP点减少私有FP的局部信号保留，但large-vehicle召回不可达参考点，不能称核心问题解决。项目原始目标仍未达成。

## 服务器当前内容

2026-09-30 PDT，C已交付r012：完整DPA及同结构普通对齐两臂，均沿冻结DOTA1.0→SODA nomask、Oriented R-CNN、单种子、12源epoch和真实两卡；每臂完成即以源best评完整目标val。沿最近实际执行端26。05:16 UTC只读核查仓库/工作区及所需旧输入，r012尚不存在；本次只交付，没有启动训练，后续实际状态须由SERVER登记。

SERVER在26完成两臂：各12源epoch、47,256步、固定种子20260926、真实两卡；均以epoch12源best评完整目标val。实际墙钟12小时9分23秒，整段两卡折合24.313 GPU小时，短于C此前46–64 GPU小时估算。步时0.377/0.363秒，原估算依据0.758秒；没有少跑，具体加速因素尚无受控剖析。任务未读取目标train标签或test，两份best继续受保护。

C于2026-09-30 18:43 PDT观察26无残留上一任务进程，随后完成结果复核。SERVER于2026-10-01 02:10 UTC在26以GPU0/1完成有限梯度检查r011；两份best各8批，运行48秒、约0.027 GPU小时，训练更新0，模型状态不变，未产生新checkpoint。

SERVER于2026-10-01 00:47 UTC在46实际启动r012的完整DPA臂，固定种子20260926、真实双卡GPU3/2、12源epoch和47,256步；随后顺序执行同结构普通对齐臂。00:48 UTC已核到两rank `WORLD_SIZE=2`、物理GPU UUID绑定一致、首个优化步梯度有限，并推进至epoch 1的50/3938步。用户明确要求在已有任务占卡时先行复用GPU3/2；启动时GPU2显存余量很小但未OOM，未改batch、预算或科学协议。这是启动时观察，最终状态见下段。

SERVER于2026-10-01 17:01 PDT完成r012两臂、各自源best完整目标val评测、语义诊断和冻结比较。完整/普通臂源best为74.854%/75.023%，目标val AP50为52.461%/52.317%，large-vehicle AP50为17.206%/18.722%；完整臂在相同1,087个大车TP处私有FP为4,532，高于控制4,149。两臂均未达到旧普通DA的共享/大车95%参考TP。一次执行在完整臂评测后因46缺少冻结r008诊断数组退出，SERVER从26原产物补回并核哈希后同号续跑，仅复算诊断和执行剩余臂；已完成训练与评测未重做。任务未访问target test，两个best已登记保护。

## 核验说明

独立审计重读四份实际manifest，确认源train/val为1,411/458原图与15,749/5,297切片，目标train/val为1,067/576原图与37,980/20,549切片，目标train加载框数为0。两臂各936个有限训练记录、12次源验证、best/latest元数据、配置/权重/GT哈希、576原图目标val、语义诊断回放、冻结比较和双PID/双UUID证据全部一致；受影响测试16通过、1跳过。实际SODA仍是800/650无遮罩自定义输入，不是官方遮罩标准。

C复核重算诊断数组、曲线与比较，重读运行/日志/模型及评测绑定，与SERVER证据一致；复用未变manifest报告，没有重新审计数据全集或重新跑全部AP匹配。又到46回读普通DA原两段日志，哈希及源验证逐项吻合。因此执行完整及本固定方法失败已经充分核验；源域下降属新增可靠观察，不能仅归因PCD或某一loss。

普通DA参考共享TP/私有FP为83,560/9,190，large-vehicle为1,469/8,049。完整臂对应82,570/12,626与1,372/11,085；在固定95%共享TP点私有FP也高于参考。去PCD为86,289/9,511，固定全共享TP点私有FP6,425低于参考7,607，但large-vehicle仅1,159 TP，达不到参考95%所需1,396。证据足以结束当前固定配置，但尚不能把下降唯一归因于候选噪声、分类超参、源辅助头、CCD或移除实例对抗。

r011独立审计确认两臂逐批输入与源标签相同、真实双rank、总梯度可加、完整state前后相同，并排除目标标签/val/test访问。源辅助分类两臂8/8同向；CCD负点积为5/8和3/8但投影中位数接近零且符号不一致，PCD仅2/8反向。这不足以支持两臂共同持续冲突的终点解释，也不足以还原早期训练因果。

C于2026-09-30 21:38 PDT回核26真实执行及产物，审计逐字段一致；另从Gram独立计算方向/投影和对称半正定，确认辅助合计完整臂7/8同向、去PCD8/8同向。对固定检查完整结束及不据此训练梯度修复已充分核验；没有新AP结果。输入绑定和训练代码未变，没有必要重复全量数据审核或扩大批次。

C本轮24项本地受影响测试通过；26原生环境内存加载待交付代码，4项原生采样/损失/初始化/优化器续训测试通过，两真实CPU rank的完整/普通臂梯度及原型与全局参考一致，作者PCC/GDPA值和梯度差分通过。CPU前后向用BN替代CUDA专属SyncBN仅限测试；实际CUDA同步BN、首批显存和吞吐尚未实测，由SERVER在原生两卡首批核验后继续。实现检查足够交付，方法有效性仍未知。

SERVER完成审计读取四份实际manifest、两臂936个训练记录和12次源验证，复核best/latest优化器状态、配置/权重/GT绑定、576原图目标val、语义观察数组与固定TP曲线；冻结比较可逐字段重算，未发现target-test产物。环境缺少pytest，因此没有把测试套件声称为本次通过；实际双卡训练、完整评测和独立结果审计均已成功。该证据足以判定r012按固定协议执行结束及联合判据失败；方法族外推、跨种子稳定性和新路线仍未经核验。

## 执行阶段

2026-10-01 PDT，r012在46执行结束待B/C复核：两臂训练、合法源best目标val评测、语义比较、结果归纳、关键best保护和来源项目推送均已完成，唯一任务槽已清空。固定DPA路线未满足核心联合判据，原项目目标尚未达成，不登记项目结束，也不自动追加消融、调参、种子或新路线。

记录者：SERVER；更新日期：2026-10-02 CST。执行结束待B/C复核，项目创新目标未达成，不登记项目结束。

## 下一步与维护

r011按预定阴性分支结束：不套用梯度修复、不追加批次找阳性。末期权重不能还原早期轨迹，原始梯度不含历史momentum；不能把本次阴性改写成根因已解决。

C已核查作者实际GDPA/IDSA/PCC及独立边界Adam，接入原生旋转检测/训练/评测。两臂共用新域头和候选，普通控制只关闭专属选样/权重/PCC；用同结构AP、源检测保持以及大车/全共享实际TP—私有FP裁决，不凭loss或总AP单项宣称核心问题解决。旧权重没有学习这套联合机制，已有冻结检查不能给出新训练收益，因此该训练是必要性能检验，不为补齐论文表格。无目标标签/共享oracle/test，不追加种子或系数搜索。

r012已经按固定比较完成：完整臂只有总体AP和全共享聚合曲线的局部正信号，关键large-vehicle召回—私有FP条件失败。下一步不是SERVER自行扩展实验；由B/C复核累计证据后决定是否有新的直接科学任务，不能把局部曲线或GT辅助诊断改写成核心问题解决。

动作执行者按[主动更新约定](README.md)在真实事件发生时更新本页并发布总览。

## 证据

[r010结果、失败边界与受保护权重](https://github.com/ziyu24/cqc_P27/blob/dec8e4c127a0caede7fc4aa8554cb763e3634599/lab/result.md)；[独立充分证据](https://github.com/ziyu24/cqc_P27/blob/dec8e4c127a0caede7fc4aa8554cb763e3634599/doc/r010_evidence.json)；[当前科学讨论](https://github.com/ziyu24/cqc_P27/blob/dec8e4c127a0caede7fc4aa8554cb763e3634599/lab/discussion.md)；[恢复入口](https://github.com/ziyu24/cqc_P27/blob/dec8e4c127a0caede7fc4aa8554cb763e3634599/configs/r010.recovery.json)。[已登记教训](../lesson/cqc_P27.lessons.md)。

[C完成复核、源验证与耗时](https://github.com/ziyu24/cqc_P27/blob/592e702/lab/result.md)；[唯一后续任务](https://github.com/ziyu24/cqc_P27/blob/592e702/lab/sug.md)；[有限检查实现与边界](https://github.com/ziyu24/cqc_P27/blob/592e702/doc/gradient_probe.md)。

[r011恢复入口](https://github.com/ziyu24/cqc_P27/blob/bc1e2af/configs/r011.recovery.json)。

[r011结果、失败边界与充分证据](https://github.com/ziyu24/cqc_P27/blob/24a329b254a2ccd7f8c0f71beacdf33f4fa47cdd/lab/result.md)。

[C完成复核与路线选择](https://github.com/ziyu24/cqc_P27/blob/6ebbd3f3bc40d92d3ce4a63ed58559fd9d94dc61/lab/discussion.md)；[方法迁移审查和具体比较方案](https://github.com/ziyu24/cqc_P27/blob/6ebbd3f3bc40d92d3ce4a63ed58559fd9d94dc61/doc/method_transfer_review.md)。

[用户授权、核心判断与交付核验](https://github.com/ziyu24/cqc_P27/blob/1ff20e8a0c02b20c2e887e80960db21a3dddf646/lab/discussion.md)；[唯一r012任务](https://github.com/ziyu24/cqc_P27/blob/1ff20e8a0c02b20c2e887e80960db21a3dddf646/lab/sug.md)；[科学实现与已核/未核边界](https://github.com/ziyu24/cqc_P27/blob/1ff20e8a0c02b20c2e887e80960db21a3dddf646/doc/dpa_execution.md)。

[46执行恢复入口与路径绑定](https://github.com/ziyu24/cqc_P27/blob/a575fe9b0f6325c60078381e58d4dfba110180b8/configs/r012.recovery.json)。

[r012结果、失败边界、独立证据与受保护权重](https://github.com/ziyu24/cqc_P27/tree/84fa2a1c/lab)；[r012充分证据](https://github.com/ziyu24/cqc_P27/blob/84fa2a1c/doc/r012_evidence.json)；[恢复入口](https://github.com/ziyu24/cqc_P27/blob/84fa2a1c/configs/r012.recovery.json)。
