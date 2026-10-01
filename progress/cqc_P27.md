# P27 项目进展

## 最初科学问题

类别集合不一致、重叠关系未知时，能否利用有标注源域与无标签目标域改善共享类别的旋转目标检测。

## 核心进展

目前仍卡在保住共享检测能力同时减少私有误报，原目标尚未达成。用户已同意以完整DPA检测方法替换失败的固定UniOT适配；C已实现三个核心模块及同结构普通对齐控制，完成实现检查并下发r012，新性能结果尚无。已有末期梯度阴性不足以定位旧失败根因，不启动梯度保护支线。

本次借鉴UniOT完成目标结构学习PCD与部分匹配CCD的检测适配。完整/去PCD两臂目标val AP50为41.739%/43.409%，均低于普通DA 52.062%；完整臂还低于去PCD 1.669个百分点，并同时损失共享和large-vehicle召回、增加主要私有误报。因此本次固定适配、PCD正贡献和“保召回降混淆”三项主张均失败。去PCD在固定全共享TP点减少私有FP的局部信号保留，但large-vehicle召回不可达参考点，不能称核心问题解决。项目原始目标仍未达成。

## 服务器当前内容

2026-09-30 PDT，C已交付r012：完整DPA及同结构普通对齐两臂，均沿冻结DOTA1.0→SODA nomask、Oriented R-CNN、单种子、12源epoch和真实两卡；每臂完成即以源best评完整目标val。沿最近实际执行端26。05:16 UTC只读核查仓库/工作区及所需旧输入，r012尚不存在；本次只交付，没有启动训练，后续实际状态须由SERVER登记。

SERVER在26完成两臂：各12源epoch、47,256步、固定种子20260926、真实两卡；均以epoch12源best评完整目标val。实际墙钟12小时9分23秒，整段两卡折合24.313 GPU小时，短于C此前46–64 GPU小时估算。步时0.377/0.363秒，原估算依据0.758秒；没有少跑，具体加速因素尚无受控剖析。任务未读取目标train标签或test，两份best继续受保护。

C于2026-09-30 18:43 PDT观察26无残留上一任务进程，随后完成结果复核。SERVER于2026-10-01 02:10 UTC在26以GPU0/1完成有限梯度检查r011；两份best各8批，运行48秒、约0.027 GPU小时，训练更新0，模型状态不变，未产生新checkpoint。

SERVER于2026-10-01 00:47 UTC在46实际启动r012的完整DPA臂，固定种子20260926、真实双卡GPU3/2、12源epoch和47,256步；随后将顺序执行同结构普通对齐臂。00:48 UTC已核到两rank `WORLD_SIZE=2`、物理GPU UUID绑定一致、首个优化步梯度有限，并推进至epoch 1的50/3938步。用户明确要求在已有任务占卡时先行复用GPU3/2；启动后GPU2显存余量很小，当前尚未OOM，不改batch、预算或科学协议。r012正在实际执行，不以进程存活提前判定科学完成。

## 核验说明

独立审计重读四份实际manifest，确认源train/val为1,411/458原图与15,749/5,297切片，目标train/val为1,067/576原图与37,980/20,549切片，目标train加载框数为0。两臂各936个有限训练记录、12次源验证、best/latest元数据、配置/权重/GT哈希、576原图目标val、语义诊断回放、冻结比较和双PID/双UUID证据全部一致；受影响测试16通过、1跳过。实际SODA仍是800/650无遮罩自定义输入，不是官方遮罩标准。

C复核重算诊断数组、曲线与比较，重读运行/日志/模型及评测绑定，与SERVER证据一致；复用未变manifest报告，没有重新审计数据全集或重新跑全部AP匹配。又到46回读普通DA原两段日志，哈希及源验证逐项吻合。因此执行完整及本固定方法失败已经充分核验；源域下降属新增可靠观察，不能仅归因PCD或某一loss。

普通DA参考共享TP/私有FP为83,560/9,190，large-vehicle为1,469/8,049。完整臂对应82,570/12,626与1,372/11,085；在固定95%共享TP点私有FP也高于参考。去PCD为86,289/9,511，固定全共享TP点私有FP6,425低于参考7,607，但large-vehicle仅1,159 TP，达不到参考95%所需1,396。证据足以结束当前固定配置，但尚不能把下降唯一归因于候选噪声、分类超参、源辅助头、CCD或移除实例对抗。

r011独立审计确认两臂逐批输入与源标签相同、真实双rank、总梯度可加、完整state前后相同，并排除目标标签/val/test访问。源辅助分类两臂8/8同向；CCD负点积为5/8和3/8但投影中位数接近零且符号不一致，PCD仅2/8反向。这不足以支持两臂共同持续冲突的终点解释，也不足以还原早期训练因果。

C于2026-09-30 21:38 PDT回核26真实执行及产物，审计逐字段一致；另从Gram独立计算方向/投影和对称半正定，确认辅助合计完整臂7/8同向、去PCD8/8同向。对固定检查完整结束及不据此训练梯度修复已充分核验；没有新AP结果。输入绑定和训练代码未变，没有必要重复全量数据审核或扩大批次。

C本轮24项本地受影响测试通过；26原生环境内存加载待交付代码，4项原生采样/损失/初始化/优化器续训测试通过，两真实CPU rank的完整/普通臂梯度及原型与全局参考一致，作者PCC/GDPA值和梯度差分通过。CPU前后向用BN替代CUDA专属SyncBN仅限测试；实际CUDA同步BN、首批显存和吞吐尚未实测，由SERVER在原生两卡首批核验后继续。实现检查足够交付，方法有效性仍未知。

## 执行阶段

2026-09-30 PDT，用户明确授权完整DPA适配及同结构普通控制；本轮r012现已在46实际执行完整DPA臂。两臂训练、各自源best目标val评测、语义比较和结果归纳均尚未完成。旧r011已充分复核完成，本轮不是重跑r010，也未增加消融、调参或种子；原项目目标尚未达成，不登记项目结束。

记录者：C；更新日期：2026-09-30 PDT（UTC为10月1日）。保留SERVER已验证输出，项目创新目标未达成，不登记项目结束。

## 下一步与维护

r011按预定阴性分支结束：不套用梯度修复、不追加批次找阳性。末期权重不能还原早期轨迹，原始梯度不含历史momentum；不能把本次阴性改写成根因已解决。

C已核查作者实际GDPA/IDSA/PCC及独立边界Adam，接入原生旋转检测/训练/评测。两臂共用新域头和候选，普通控制只关闭专属选样/权重/PCC；用同结构AP、源检测保持以及大车/全共享实际TP—私有FP裁决，不凭loss或总AP单项宣称核心问题解决。旧权重没有学习这套联合机制，已有冻结检查不能给出新训练收益，因此该训练是必要性能检验，不为补齐论文表格。无目标标签/共享oracle/test，不追加种子或系数搜索。

r012固定比较完整DPA与同结构普通对齐，以源best合法评目标val；须分别裁决完整检测收益、关键类别召回和私有误报，不能把局部曲线或GT辅助诊断当作检测成功。

动作执行者按[主动更新约定](README.md)在真实事件发生时更新本页并发布总览。

## 证据

[r010结果、失败边界与受保护权重](https://github.com/ziyu24/cqc_P27/blob/dec8e4c127a0caede7fc4aa8554cb763e3634599/lab/result.md)；[独立充分证据](https://github.com/ziyu24/cqc_P27/blob/dec8e4c127a0caede7fc4aa8554cb763e3634599/doc/r010_evidence.json)；[当前科学讨论](https://github.com/ziyu24/cqc_P27/blob/dec8e4c127a0caede7fc4aa8554cb763e3634599/lab/discussion.md)；[恢复入口](https://github.com/ziyu24/cqc_P27/blob/dec8e4c127a0caede7fc4aa8554cb763e3634599/configs/r010.recovery.json)。[已登记教训](../lesson/cqc_P27.lessons.md)。

[C完成复核、源验证与耗时](https://github.com/ziyu24/cqc_P27/blob/592e702/lab/result.md)；[唯一后续任务](https://github.com/ziyu24/cqc_P27/blob/592e702/lab/sug.md)；[有限检查实现与边界](https://github.com/ziyu24/cqc_P27/blob/592e702/doc/gradient_probe.md)。

[r011恢复入口](https://github.com/ziyu24/cqc_P27/blob/bc1e2af/configs/r011.recovery.json)。

[r011结果、失败边界与充分证据](https://github.com/ziyu24/cqc_P27/blob/24a329b254a2ccd7f8c0f71beacdf33f4fa47cdd/lab/result.md)。

[C完成复核与路线选择](https://github.com/ziyu24/cqc_P27/blob/6ebbd3f3bc40d92d3ce4a63ed58559fd9d94dc61/lab/discussion.md)；[方法迁移审查和具体比较方案](https://github.com/ziyu24/cqc_P27/blob/6ebbd3f3bc40d92d3ce4a63ed58559fd9d94dc61/doc/method_transfer_review.md)。

[用户授权、核心判断与交付核验](https://github.com/ziyu24/cqc_P27/blob/1ff20e8a0c02b20c2e887e80960db21a3dddf646/lab/discussion.md)；[唯一r012任务](https://github.com/ziyu24/cqc_P27/blob/1ff20e8a0c02b20c2e887e80960db21a3dddf646/lab/sug.md)；[科学实现与已核/未核边界](https://github.com/ziyu24/cqc_P27/blob/1ff20e8a0c02b20c2e887e80960db21a3dddf646/doc/dpa_execution.md)。

[46执行恢复入口与路径绑定](https://github.com/ziyu24/cqc_P27/blob/a575fe9b0f6325c60078381e58d4dfba110180b8/configs/r012.recovery.json)。
