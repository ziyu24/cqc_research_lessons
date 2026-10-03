# P27 项目进展

## 最初科学问题

类别集合不一致、重叠关系未知时，能否利用有标注源域与无标签目标域改善共享类别的旋转目标检测。

## 核心进展

C于2026-10-02 PDT按用户明确同意，已交付冻结DINOv2区域表征与旧ROI表征的相同源标签读出比较。两项轻量读出各12轮、一个固定种子、真实两卡；检测器不重训，原框/类别/NMS集合固定。SERVER已于2026-10-03 01:11 UTC在46实际启动r014并通过双卡首批；目前仍是执行中候选，没有证明核心解法有效。OpenDet固定适配的完整执行和联合失败已经独立复核。

两臂各12源epoch、47,256步、固定单种子和真实双卡，源best为72.058%/74.152%。训练机制及关闭控制均实际生效；四份数据manifest、合法best/latest、576原图/20,549切片完整目标val、预测/配置/GT绑定和无test访问已由独立审计复核。两份epoch-12 best已登记保护。原核心目标仍未达成，失败原因及OBB专属性未知；该轮只结束OpenDet固定任务，项目保持运行；其原槽清空后现已换为获授权的新任务。

固定DPA相对同结构普通对照总AP50高0.143个百分点，大车AP下降，整条共同可达大车TP范围内私有FP从未更少。严格IoU与相对旧基线的局部改善保留，源检测没有UniOT式崩塌；结束该固定配置的结论不变。

累计事实：旧普通DA相对source-only有正迁移；IDSA有小幅正差但指定候选位置必要性未获支持。固定KLD提高AP50却降低严格IoU；源支持度与GT几何诊断未支持所提关键混淆解法。UniOT完整/去PCD适配的目标AP50为41.739%/43.409%，低于旧普通DA52.062%，源best也大幅下降；后续两份best各8批的冻结梯度检查不足以支持共同持续反向解释，不启动梯度保护支线。各项失败只限实际条件，原研究目标仍未达成。

## 服务器当前内容

SERVER于2026-10-03 01:17 UTC观察到首轮在400个source-train切片后因原生RPN非正宽/高的退化parent退出。该parent仍参与旧ROI特征和最终检测，故未删框或膨胀；同号修复为保留候选、DINO显式零特征并单独计数，44项相关测试通过。旧绑定的4个分块已完整移入同运行号失败尝试目录、不再复用；01:21 UTC恢复后GPU0/1双rank首批与UUID再次MATCH，任务继续执行。

SERVER于2026-10-03 01:11 UTC在46实际启动r014，运行器选择物理GPU0/1；两个rank均完成source-train首批，各处理64个配对区域，原生捕获回放通过，首批显存峰值约2.7 GiB。运行器回读两个rank PID与两卡UUID为MATCH，当前继续完整源train/val提取、两项固定12轮读出、共享目标评分和三套完整评测；尚无新目标指标，进程存活不等于科学完成。

C于2026-10-02 PDT已推送r014入口、配置、唯一任务和针对性检查，沿最近实际执行端46。任务为完整源train/val成对提取、两个源读出、共享目标评分与三套重新匹配的完整原生评测。C仅做只读服务器检查和CPU反例，未启动新GPU计算；SERVER实际开始与完成以其后续执行证据为准。

此前C于2026-10-02 17:01 PDT只读核实46正确仓库、运行根、实际日志和完整产物；原worker已退出，未发现本项目训练残留。OpenDet两份best实体及保护配置有效，该固定任务已完成复核。

SERVER于2026-10-02 05:39—18:32 UTC在46物理GPU2/3完成r013完整CFL+UPL与同结构控制两臂、合法源选优、完整目标val和语义曲线，RUN为`COMPLETE/exit 0`，结束后worker及rank均退出。完整/控制AP50为51.422%/51.492%；匹配控制95%实际TP时，完整臂全部共享私有FP为9,798对9,098，大车为10,497对9,135。两份best和latest、预测、诊断与完整曲线留在46项目运行根；best已受保护，删除须用户明确授权。OpenDet完成当时唯一任务槽已清空、无该任务残留；这段历史观察不代表新任务的实时状态。

2026-10-01 PDT，C交付r013两臂可执行入口，按最近实际执行端指定46；各12源epoch、47,256步、单种子、实际两卡，完整臂完成立即评完整val后继续控制臂。C当时只读核46项目及主机配置并以CPU内存测试核验接口，未启动训练；后续实际完成事实以上方SERVER记录为准。

此前已完成的有效执行事实保留：

SERVER按其会话中用户最后明确选择在46完成r012，完整DPA及同结构普通对照均12源epoch、47,256步、固定种子20260926和真实两rank；每臂以源best评完整目标val。中途只因缺少已有诊断数组退出，补回并校验后复用已完成训练/评测、继续剩余工作。完成时间按SERVER报告为2026-10-01 17:01 PDT；完整/普通源best为74.854%/75.023%，目标AP50为52.461%/52.317%，大车AP为17.206%/18.722%。两份best已登记保护，完成时唯一槽已清空。

C于2026-10-01 17:24 PDT回读46正确仓库、Home及tmpfs产物映射、原生日志、模型和合法结果，观察时无相关残留进程。当前为科学完成且已复核，不是等待继续训练；本轮没有新GPU任务。

## 核验说明

新交付本地54项反例通过，3项因本机原生库或Gloo缺失跳过：其中新两进程AdamW和原生NMS/重新匹配已在46原Torch1.12.1环境以CPU补测通过；旧捕获接口复用已核证据，并安排实际图像首批回放。另在46对合法source-val原图GT恢复及原生指派正例验证通过。修复了新实现会把无tile标签的源验证候选全当背景的问题，未改变旧实验结论。两臂同parent/标签/初态、末批零权、重排序重新匹配及完整并列的召回公平性均有反例覆盖。

当前检查足以交付科学机制和入口，尚不等于全流程GPU通过：官方权重实际准备、原生双GPU首批、PID→设备、真实有限更新、显存及吞吐由SERVER验证后直接继续授权终点，不另等C。尚无新目标性能结果。现有旧分数缺少DINO信息和源背景读出，不能复算得到新假设答案；因此新增计算有明确判别作用，未将所有旧负结果扩大成禁止整个方法族。

C的新增复核脚本已在46现有环境只读执行通过：完整审计输出与SERVER提交证据一致，重算曲线与保存数组逐项相等，训练/评测的四次双PID—双UUID MATCH与两rank记录吻合。四份manifest哈希未变，复用已核身份和加载覆盖，不重扫数据；保护best及完整resume已核。没有重跑全部图像前向或原图IoU匹配，复用已绑定原生评测。核验足以确认固定实验执行完整及原联合条件失败，不能解释唯一训练因果。

曲线边界补充：OpenDet完整臂在大车共同1—1,494 TP的763点私有FP更少、4点相同、727点更多，不能沿用此前DPA的全范围无优势结论；预定1,430 TP处仍多1,362个私有FP，全共享指定点仍多700。源best低2.094点，严格IoU及大车AP正差保留，不事后改判据。

本轮充分核验依据为来源项目`src/review_r013.py`和`doc/r013_evidence.json`：RUN终态、物理GPU2/3与两rank记录、四份manifest身份/覆盖、每臂12次源验证和936个有限训练区间、best/latest完整优化器状态、配置/权重/GT/预测绑定、语义观测及冻结比较均通过只读复算；审计重放与落盘证据一致。完整臂CFL/UPL及队列实际激活，控制臂对应量恒为0。目标train框数为0，无target test配置或产物。SODA仍是800/650 nomask项目自定义输入，不是官方遮罩预处理。

r013交付时新增部分已核：本地39项测试通过，缺原生库/Gloo的6项skip另在46现有mr以原始测试函数验证；四项原生CPU检查通过，真实Linux两rank完整/控制的损失、逐参数梯度、队列均匹配全局参考。曾发现原生递归初始化覆盖新增MLP，已修正并复测；source-only辅助、17维概率保留、采样/回归不变、双臂同初态及恢复有反例覆盖。SERVER随后完成实际双GPU全训练与完整评测，收益和拒识判据均失败；数据沿已核manifest身份与覆盖，不重切或全量重审DOTA，保留SODA800/650 nomask自定义输入。

旧结果的充分核验依据继续有效：

执行配置逐字段核对模型、损失、SGD/Adam及学习率计划、原生候选采样/数据pipeline和源验证规则，与交付一致。四份换端manifest与原件只差路径前缀，ID/标注/加载覆盖不变；源train/val为1,411/458原图与15,749/5,297切片，目标train/val为1,067/576原图与37,980/20,549切片，目标train框数0。保持项目800/650 nomask输入，未重切或全量重扫DOTA，没有target test。

C复算现有审计的训练终点、12次源验证、best/latest、配置/权重/GT绑定、语义数组和比较，与SERVER证据一致。另用独立累计代码复算整条共同可达曲线：完整DPA相对同结构控制在大车1—1,144 TP中0点私有FP更少、41点相同、1,103点更多；同1,087 TP为4,532对4,149。因此原关键混淆失败不取决于95%点。

正信号及限制保留：相对旧普通DA，同1,087 TP为4,532对5,495，多数共同点仍有改善；但新普通控制更好，不能把旧新变化全部归因DPA。完整臂AP75/AP50:95为15.537%/23.238%，相对同结构控制高0.528/0.156个百分点。历史参考TP不可达只针对既定输出截断协议；曲线点不独立，不能当显著性或跨种子稳定性。未重跑图像前向/全部IoU匹配，复用已绑定原生输出及AP回放。

元数据限制：Home RUN仍显示PLANNED，完成判断依据实际日志、权重及评测；两rank及完整计算记录已核，SERVER所述物理GPU3/2的历史UUID快照本次未独立取得。该缺口不抹去实际科学输出，也不成为重训理由。原生模型/损失没有被SERVER修改；新旧对照的结构差异已由必要同结构臂控制。

## 执行阶段

2026-10-03 01:21 UTC，SERVER已在46同号恢复r014并再次核实双rank首批与物理GPU0/1绑定；首轮退化parent工程边界已显式修复，任务执行中，完整两臂训练、冻结目标输出和评测尚未完成。原目标未达成、固定OpenDet路线失败、新候选待检验，三者分开。项目保持运行，不登记整体结束。

记录者：SERVER；更新日期：2026-10-03 UTC。保留C的交付与复核事实，不冒充B/C共识。

## 下一步与维护

目前核心问题是保住共享检测并减少相近私有误报；这不是全部检测错误，也未证明OBB独有。源代理拒识没有目标私有身份监督是实现限制，不是唯一失败根因。旧结果已足够停止固定变体，继续重算相同分数或几何不会改变取舍。

执行已授权的固定DINOv2候选：仅源标签的相同轻量读出分别应用于新旧表征，固定预测框/类别/NMS，重新原生匹配，比较实际AP与保召回私有FP。联合条件为共享AP50提高、大车AP不降，至少保留原ordinary95%点的实际TP，全共享私有FP不增且大车私有FP严格下降；精确同TP和更多TP且更少FP分别报告。新旧读出相近不能归因外部表征；作者目标few-shot监督不能搬入。固定final，无源/目标选轮次或校准，不追加骨干/阈值/种子。只有合法性能和关键混淆共同改善，才有依据另议适应干预；本次不自动进入检测器训练。

固定r013结束，不追加拆模块、阈值、参数或种子；本候选不是恢复旧5-NN模型扫描。原目标、数据及评测边界不变，不以当前方法失败登记整个项目结束。

动作执行者按[主动更新约定](README.md)在真实事件发生时更新本页并发布总览。

## 证据

[用户授权及当前判断](https://github.com/ziyu24/cqc_P27/blob/52471c69902b161a1e4cb0b38a500f45519b5033/lab/discussion.md)；[唯一任务与冻结协议](https://github.com/ziyu24/cqc_P27/blob/30bbb723ab7b3e163462977918403301bf3330fc/lab/sug.md)；[固定实现、入口与未核边界](https://github.com/ziyu24/cqc_P27/blob/52471c69902b161a1e4cb0b38a500f45519b5033/doc/frozen_readout_execution.md)；[实际交付检查](https://github.com/ziyu24/cqc_P27/blob/52471c69902b161a1e4cb0b38a500f45519b5033/doc/frozen_readout_delivery_checks.json)；[恢复入口](https://github.com/ziyu24/cqc_P27/blob/06228dadb6ee7970ad732f3536238c7e3da72d1f/configs/r014.recovery.json)。首批与GPU绑定原始日志留在46运行根；本页只登记观察事实，不能冒称完整科学结果。

[C完成复核与完整边界](https://github.com/ziyu24/cqc_P27/blob/165db8440644768e77ffc8f97629e64a45ec9f90/lab/result.md)；[可重放完成证据](https://github.com/ziyu24/cqc_P27/blob/165db8440644768e77ffc8f97629e64a45ec9f90/doc/r013_completion_review.json)；[当前问题与未执行候选](https://github.com/ziyu24/cqc_P27/blob/165db8440644768e77ffc8f97629e64a45ec9f90/doc/method_transfer_review.md)。

[r013结果、主要失败与保护权重](https://github.com/ziyu24/cqc_P27/blob/bc40d5d3816281246cd3d0e76ca0269bae89f5b2/lab/result.md)；[充分审计证据](https://github.com/ziyu24/cqc_P27/blob/bc40d5d3816281246cd3d0e76ca0269bae89f5b2/doc/r013_evidence.json)；[完成讨论与任务槽清空](https://github.com/ziyu24/cqc_P27/blob/bc40d5d3816281246cd3d0e76ca0269bae89f5b2/lab/discussion.md)；[恢复与产物入口](https://github.com/ziyu24/cqc_P27/blob/bc40d5d3816281246cd3d0e76ca0269bae89f5b2/configs/r013.recovery.json)。

[本轮范式新颖性补查及固定作者代码来源](https://github.com/ziyu24/cqc_P27/blob/a9c4675c0d54d5d151c832ef7af65939b2467282/doc/method_transfer_review.md)；[C判断与原任务不变边界](https://github.com/ziyu24/cqc_P27/blob/a9c4675c0d54d5d151c832ef7af65939b2467282/lab/discussion.md)。

[已推送唯一任务](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/lab/sug.md)；[用户授权与科学取舍](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/lab/discussion.md)；[机制、作者偏离与执行入口](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/doc/opendet_execution.md)；[实际检查记录](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/doc/opendet_delivery_checks.json)；[冻结配置](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/configs/r013.json)。本轮准备不包含新训练、目标评测或GPU计算。

[本轮独立研究取舍、原论文与代码来源](https://github.com/ziyu24/cqc_P27/blob/dce35d692144f078a5a47c086d55e023ad9e5e92/doc/method_transfer_review.md)；[当前判断与建议边界](https://github.com/ziyu24/cqc_P27/blob/dce35d692144f078a5a47c086d55e023ad9e5e92/lab/discussion.md)。该独立调研阶段未另做服务器观察；本轮交付的只读核验和CPU检查见上方新来源，不覆盖此前有效科学证据。

[当前科学讨论](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/lab/discussion.md)；[完整累计结果和受保护权重](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/lab/result.md)；[C独立复核及共同范围统计](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/doc/r012_completion_review.json)；[SERVER充分证据](https://github.com/ziyu24/cqc_P27/blob/84fa2a17b1fb6e3976a93dc22f13be713330b9bd/doc/r012_evidence.json)；[科学适配与差异](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/doc/dpa_execution.md)；[恢复入口](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/configs/r012.recovery.json)。[已登记教训](../lesson/cqc_P27.lessons.md)。

[此前交付及历史证据入口](https://github.com/ziyu24/cqc_research_lessons/blob/66c940b/progress/cqc_P27.md)保留旧UniOT、梯度诊断和数据复核事实；这里只更新当前判断，不覆盖原研究问题。
