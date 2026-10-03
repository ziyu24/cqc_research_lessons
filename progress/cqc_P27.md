# P27 项目进展

## 最初科学问题

类别集合不一致、重叠关系未知时，能否利用有标注源域与无标签目标域改善共享类别的旋转目标检测。

## 核心进展

C已于2026-10-02 PDT完成OpenDet固定适配的服务器独立复核：两臂完整，性能与指定高召回拒识联合条件失败。关键混淆现象已确认，唯一训练根因、OBB专属性和有效核心解法仍未找到。候选方案为冻结外部DINOv2区域表征与旧ROI表征的相同源标签读出比较；这是待用户明确选择的新路线，尚未下发或执行。

两臂各12源epoch、47,256步、固定单种子和真实双卡，源best为72.058%/74.152%。训练机制及关闭控制均实际生效；四份数据manifest、合法best/latest、576原图/20,549切片完整目标val、预测/配置/GT绑定和无test访问已由独立审计复核。两份epoch-12 best已登记保护。原核心目标仍未达成，失败原因及OBB专属性未知；本轮只结束当前任务，项目保持运行且唯一任务槽已清空。

固定DPA相对同结构普通对照总AP50高0.143个百分点，大车AP下降，整条共同可达大车TP范围内私有FP从未更少。严格IoU与相对旧基线的局部改善保留，源检测没有UniOT式崩塌；结束该固定配置的结论不变。

累计事实：旧普通DA相对source-only有正迁移；IDSA有小幅正差但指定候选位置必要性未获支持。固定KLD提高AP50却降低严格IoU；源支持度与GT几何诊断未支持所提关键混淆解法。UniOT完整/去PCD适配的目标AP50为41.739%/43.409%，低于旧普通DA52.062%，源best也大幅下降；后续两份best各8批的冻结梯度检查不足以支持共同持续反向解释，不启动梯度保护支线。各项失败只限实际条件，原研究目标仍未达成。

## 服务器当前内容

C于2026-10-02 17:01 PDT只读核实46正确仓库、运行根、实际日志和完整产物；原worker已退出，未发现本项目训练残留。两份best实体及保护配置有效；当前任务已完成复核，槽仍为空，本轮没有新GPU前向或训练。

SERVER于2026-10-02 05:39—18:32 UTC在46物理GPU2/3完成r013完整CFL+UPL与同结构控制两臂、合法源选优、完整目标val和语义曲线，RUN为`COMPLETE/exit 0`，结束后worker及rank均退出。完整/控制AP50为51.422%/51.492%；匹配控制95%实际TP时，完整臂全部共享私有FP为9,798对9,098，大车为10,497对9,135。两份best和latest、预测、诊断与完整曲线留在46项目运行根；best已受保护，删除须用户明确授权。唯一任务槽已清空，没有在跑的P27任务。

2026-10-01 PDT，C交付r013两臂可执行入口，按最近实际执行端指定46；各12源epoch、47,256步、单种子、实际两卡，完整臂完成立即评完整val后继续控制臂。C当时只读核46项目及主机配置并以CPU内存测试核验接口，未启动训练；后续实际完成事实以上方SERVER记录为准。

此前已完成的有效执行事实保留：

SERVER按其会话中用户最后明确选择在46完成r012，完整DPA及同结构普通对照均12源epoch、47,256步、固定种子20260926和真实两rank；每臂以源best评完整目标val。中途只因缺少已有诊断数组退出，补回并校验后复用已完成训练/评测、继续剩余工作。完成时间按SERVER报告为2026-10-01 17:01 PDT；完整/普通源best为74.854%/75.023%，目标AP50为52.461%/52.317%，大车AP为17.206%/18.722%。两份best已登记保护，完成时唯一槽已清空。

C于2026-10-01 17:24 PDT回读46正确仓库、Home及tmpfs产物映射、原生日志、模型和合法结果，观察时无相关残留进程。当前为科学完成且已复核，不是等待继续训练；本轮没有新GPU任务。

## 核验说明

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

2026-10-02 17:01 PDT，C完成r013独立复核；SERVER实际两臂和全部预定输出已结束，合法best保护与任务槽清空已核。原目标未达成、固定OpenDet路线失败、普遍科学命题未被此单次结果完全否定，三者分开。项目保持运行，尚无下一项已下发任务。

记录者：C；更新日期：2026-10-02 PDT。保留SERVER的实际执行事实，不冒充SERVER启动或B/C共识。

## 下一步与维护

目前核心问题是保住共享检测并减少相近私有误报；这不是全部检测错误，也未证明OBB独有。源代理拒识没有目标私有身份监督是实现限制，不是唯一失败根因。旧结果已足够停止固定变体，继续重算相同分数或几何不会改变取舍。

下一候选具体检验冻结DINOv2能否提供当前检测器缺少的视觉区分证据：仅源标签的相同轻量读出分别应用于新旧表征，固定预测框/类别/NMS，重新进行原生重打分匹配，比较实际AP与同TP私有FP。只在主候选实际AP和同TP混淆同时改善时再讨论下一适应干预；新旧读出相近不能归因外部表征。相关遥感论文具有目标少样本标注，不能直接沿用其目标原型或背景监督。外部预训练与原路线不同，方案等待用户明确选择；未改唯一sug、未新建任务号、未启动计算，也不把候选称为有效解法。正式交付前还须固定训练/采样/校准预算和真实两卡入口。

固定r013结束，不追加拆模块、阈值、参数或种子；本候选不是恢复旧5-NN模型扫描。原目标、数据及评测边界不变，不以当前方法失败登记整个项目结束。

动作执行者按[主动更新约定](README.md)在真实事件发生时更新本页并发布总览。

## 证据

[C完成复核与完整边界](https://github.com/ziyu24/cqc_P27/blob/165db8440644768e77ffc8f97629e64a45ec9f90/lab/result.md)；[可重放完成证据](https://github.com/ziyu24/cqc_P27/blob/165db8440644768e77ffc8f97629e64a45ec9f90/doc/r013_completion_review.json)；[当前问题与未执行候选](https://github.com/ziyu24/cqc_P27/blob/165db8440644768e77ffc8f97629e64a45ec9f90/doc/method_transfer_review.md)。

[r013结果、主要失败与保护权重](https://github.com/ziyu24/cqc_P27/blob/bc40d5d3816281246cd3d0e76ca0269bae89f5b2/lab/result.md)；[充分审计证据](https://github.com/ziyu24/cqc_P27/blob/bc40d5d3816281246cd3d0e76ca0269bae89f5b2/doc/r013_evidence.json)；[完成讨论与任务槽清空](https://github.com/ziyu24/cqc_P27/blob/bc40d5d3816281246cd3d0e76ca0269bae89f5b2/lab/discussion.md)；[恢复与产物入口](https://github.com/ziyu24/cqc_P27/blob/bc40d5d3816281246cd3d0e76ca0269bae89f5b2/configs/r013.recovery.json)。

[本轮范式新颖性补查及固定作者代码来源](https://github.com/ziyu24/cqc_P27/blob/a9c4675c0d54d5d151c832ef7af65939b2467282/doc/method_transfer_review.md)；[C判断与原任务不变边界](https://github.com/ziyu24/cqc_P27/blob/a9c4675c0d54d5d151c832ef7af65939b2467282/lab/discussion.md)。

[已推送唯一任务](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/lab/sug.md)；[用户授权与科学取舍](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/lab/discussion.md)；[机制、作者偏离与执行入口](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/doc/opendet_execution.md)；[实际检查记录](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/doc/opendet_delivery_checks.json)；[冻结配置](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/configs/r013.json)。本轮准备不包含新训练、目标评测或GPU计算。

[本轮独立研究取舍、原论文与代码来源](https://github.com/ziyu24/cqc_P27/blob/dce35d692144f078a5a47c086d55e023ad9e5e92/doc/method_transfer_review.md)；[当前判断与建议边界](https://github.com/ziyu24/cqc_P27/blob/dce35d692144f078a5a47c086d55e023ad9e5e92/lab/discussion.md)。该独立调研阶段未另做服务器观察；本轮交付的只读核验和CPU检查见上方新来源，不覆盖此前有效科学证据。

[当前科学讨论](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/lab/discussion.md)；[完整累计结果和受保护权重](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/lab/result.md)；[C独立复核及共同范围统计](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/doc/r012_completion_review.json)；[SERVER充分证据](https://github.com/ziyu24/cqc_P27/blob/84fa2a17b1fb6e3976a93dc22f13be713330b9bd/doc/r012_evidence.json)；[科学适配与差异](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/doc/dpa_execution.md)；[恢复入口](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/configs/r012.recovery.json)。[已登记教训](../lesson/cqc_P27.lessons.md)。

[此前交付及历史证据入口](https://github.com/ziyu24/cqc_research_lessons/blob/66c940b/progress/cqc_P27.md)保留旧UniOT、梯度诊断和数据复核事实；这里只更新当前判断，不覆盖原研究问题。
