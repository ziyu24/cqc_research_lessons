# P27 项目进展

## 最初科学问题

类别集合不一致、重叠关系未知时，能否利用有标注源域与无标签目标域改善共享类别的旋转目标检测。

## 核心进展

普通DA上的OpenDet式CFL+UPL完整臂与同结构关闭控制均已在46完成。完整/控制目标val AP50为51.422%/51.492%，完整臂没有性能增量；在控制95%实际TP点，完整臂全部共享及大车的私有相关FP分别多700和1,362，因此指定拒识和联合假设也失败。AP75、AP50:95和部分逐类正差保留，但不能替代预定条件。固定适配结束，不拆模块、扫参或追加种子。

两臂各12源epoch、47,256步、固定单种子和真实双卡，源best为72.058%/74.152%。训练机制及关闭控制均实际生效；四份数据manifest、合法best/latest、576原图/20,549切片完整目标val、预测/配置/GT绑定和无test访问已由独立审计复核。两份epoch-12 best已登记保护。原核心目标仍未达成，失败原因及OBB专属性未知；本轮只结束当前任务，项目保持运行且唯一任务槽已清空。

固定DPA相对同结构普通对照总AP50高0.143个百分点，大车AP下降，整条共同可达大车TP范围内私有FP从未更少。严格IoU与相对旧基线的局部改善保留，源检测没有UniOT式崩塌；结束该固定配置的结论不变。

累计事实：旧普通DA相对source-only有正迁移；IDSA有小幅正差但指定候选位置必要性未获支持。固定KLD提高AP50却降低严格IoU；源支持度与GT几何诊断未支持所提关键混淆解法。UniOT完整/去PCD适配的目标AP50为41.739%/43.409%，低于旧普通DA52.062%，源best也大幅下降；后续两份best各8批的冻结梯度检查不足以支持共同持续反向解释，不启动梯度保护支线。各项失败只限实际条件，原研究目标仍未达成。

## 服务器当前内容

SERVER于2026-10-02 05:39—18:32 UTC在46物理GPU2/3完成r013完整CFL+UPL与同结构控制两臂、合法源选优、完整目标val和语义曲线，RUN为`COMPLETE/exit 0`，结束后worker及rank均退出。完整/控制AP50为51.422%/51.492%；匹配控制95%实际TP时，完整臂全部共享私有FP为9,798对9,098，大车为10,497对9,135。两份best和latest、预测、诊断与完整曲线留在46项目运行根；best已受保护，删除须用户明确授权。唯一任务槽已清空，没有在跑的P27任务。

2026-10-01 PDT，C交付r013两臂可执行入口，按最近实际执行端指定46；各12源epoch、47,256步、单种子、实际两卡，完整臂完成立即评完整val后继续控制臂。C当时只读核46项目及主机配置并以CPU内存测试核验接口，未启动训练；后续实际完成事实以上方SERVER记录为准。

此前已完成的有效执行事实保留：

SERVER按其会话中用户最后明确选择在46完成r012，完整DPA及同结构普通对照均12源epoch、47,256步、固定种子20260926和真实两rank；每臂以源best评完整目标val。中途只因缺少已有诊断数组退出，补回并校验后复用已完成训练/评测、继续剩余工作。完成时间按SERVER报告为2026-10-01 17:01 PDT；完整/普通源best为74.854%/75.023%，目标AP50为52.461%/52.317%，大车AP为17.206%/18.722%。两份best已登记保护，完成时唯一槽已清空。

C于2026-10-01 17:24 PDT回读46正确仓库、Home及tmpfs产物映射、原生日志、模型和合法结果，观察时无相关残留进程。当前为科学完成且已复核，不是等待继续训练；本轮没有新GPU任务。

## 核验说明

本轮充分核验依据为来源项目`src/review_r013.py`和`doc/r013_evidence.json`：RUN终态、物理GPU2/3与两rank记录、四份manifest身份/覆盖、每臂12次源验证和936个有限训练区间、best/latest完整优化器状态、配置/权重/GT/预测绑定、语义观测及冻结比较均通过只读复算；审计重放与落盘证据一致。完整臂CFL/UPL及队列实际激活，控制臂对应量恒为0。目标train框数为0，无target test配置或产物。SODA仍是800/650 nomask项目自定义输入，不是官方遮罩预处理。

本轮新增部分已核：本地39项测试通过，缺原生库/Gloo的6项skip另在46现有mr以原始测试函数验证；四项原生CPU检查通过，真实Linux两rank完整/控制的损失、逐参数梯度、队列均匹配全局参考。曾发现原生递归初始化覆盖新增MLP，已修正并复测；source-only辅助、17维概率保留、采样/回归不变、双臂同初态及恢复有反例覆盖。SERVER随后完成实际双GPU全训练与完整评测，收益和拒识判据均失败；数据沿已核manifest身份与覆盖，不重切或全量重审DOTA，保留SODA800/650 nomask自定义输入。

旧结果的充分核验依据继续有效：

执行配置逐字段核对模型、损失、SGD/Adam及学习率计划、原生候选采样/数据pipeline和源验证规则，与交付一致。四份换端manifest与原件只差路径前缀，ID/标注/加载覆盖不变；源train/val为1,411/458原图与15,749/5,297切片，目标train/val为1,067/576原图与37,980/20,549切片，目标train框数0。保持项目800/650 nomask输入，未重切或全量重扫DOTA，没有target test。

C复算现有审计的训练终点、12次源验证、best/latest、配置/权重/GT绑定、语义数组和比较，与SERVER证据一致。另用独立累计代码复算整条共同可达曲线：完整DPA相对同结构控制在大车1—1,144 TP中0点私有FP更少、41点相同、1,103点更多；同1,087 TP为4,532对4,149。因此原关键混淆失败不取决于95%点。

正信号及限制保留：相对旧普通DA，同1,087 TP为4,532对5,495，多数共同点仍有改善；但新普通控制更好，不能把旧新变化全部归因DPA。完整臂AP75/AP50:95为15.537%/23.238%，相对同结构控制高0.528/0.156个百分点。历史参考TP不可达只针对既定输出截断协议；曲线点不独立，不能当显著性或跨种子稳定性。未重跑图像前向/全部IoU匹配，复用已绑定原生输出及AP回放。

元数据限制：Home RUN仍显示PLANNED，完成判断依据实际日志、权重及评测；两rank及完整计算记录已核，SERVER所述物理GPU3/2的历史UUID快照本次未独立取得。该缺口不抹去实际科学输出，也不成为重训理由。原生模型/损失没有被SERVER修改；新旧对照的结构差异已由必要同结构臂控制。

## 执行阶段

2026-10-02 18:32 UTC，SERVER在46的GPU2/3完成r013两臂及全部预定评测；科学审计、失败归档、best保护和任务槽清空均已完成。固定OpenDet适配未通过性能、拒识或联合判据；原项目仍运行，目标与成功边界不变。

记录者：SERVER；更新日期：2026-10-02 UTC。此前SERVER有效执行事实及C独立复核结论继续保留。

## 下一步与维护

目前核心问题仍是如何改善共享检测，同时避免把相近私有物体自信判为已知类；已有普通DA正迁移，但OpenDet式源监督类别边界未在当前条件兑现性能或拒识收益。现有结果不足以唯一识别域偏移、unknown竞争、检测适配或OBB几何中的哪一项造成失败，也没有经证据支持的自动下一训练路线。

固定r013已按终点结束，不追加拆模块、阈值、参数、种子或换一个现成方法。后续若形成新任务，须提出能直接改变核心取舍、且兼容无目标标签信息条件的可证伪假设；不能把AP75/部分逐类正差改写成当前路线成功，也不能外推OpenDet或所有拒识方法无效。项目保持运行、任务槽为空，等待新的科学取舍而非服务器续跑。

动作执行者按[主动更新约定](README.md)在真实事件发生时更新本页并发布总览。

## 证据

[r013结果、主要失败与保护权重](https://github.com/ziyu24/cqc_P27/blob/bc40d5d3816281246cd3d0e76ca0269bae89f5b2/lab/result.md)；[充分审计证据](https://github.com/ziyu24/cqc_P27/blob/bc40d5d3816281246cd3d0e76ca0269bae89f5b2/doc/r013_evidence.json)；[完成讨论与任务槽清空](https://github.com/ziyu24/cqc_P27/blob/bc40d5d3816281246cd3d0e76ca0269bae89f5b2/lab/discussion.md)；[恢复与产物入口](https://github.com/ziyu24/cqc_P27/blob/bc40d5d3816281246cd3d0e76ca0269bae89f5b2/configs/r013.recovery.json)。

[本轮范式新颖性补查及固定作者代码来源](https://github.com/ziyu24/cqc_P27/blob/a9c4675c0d54d5d151c832ef7af65939b2467282/doc/method_transfer_review.md)；[C判断与原任务不变边界](https://github.com/ziyu24/cqc_P27/blob/a9c4675c0d54d5d151c832ef7af65939b2467282/lab/discussion.md)。

[已推送唯一任务](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/lab/sug.md)；[用户授权与科学取舍](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/lab/discussion.md)；[机制、作者偏离与执行入口](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/doc/opendet_execution.md)；[实际检查记录](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/doc/opendet_delivery_checks.json)；[冻结配置](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/configs/r013.json)。本轮准备不包含新训练、目标评测或GPU计算。

[本轮独立研究取舍、原论文与代码来源](https://github.com/ziyu24/cqc_P27/blob/dce35d692144f078a5a47c086d55e023ad9e5e92/doc/method_transfer_review.md)；[当前判断与建议边界](https://github.com/ziyu24/cqc_P27/blob/dce35d692144f078a5a47c086d55e023ad9e5e92/lab/discussion.md)。该独立调研阶段未另做服务器观察；本轮交付的只读核验和CPU检查见上方新来源，不覆盖此前有效科学证据。

[当前科学讨论](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/lab/discussion.md)；[完整累计结果和受保护权重](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/lab/result.md)；[C独立复核及共同范围统计](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/doc/r012_completion_review.json)；[SERVER充分证据](https://github.com/ziyu24/cqc_P27/blob/84fa2a17b1fb6e3976a93dc22f13be713330b9bd/doc/r012_evidence.json)；[科学适配与差异](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/doc/dpa_execution.md)；[恢复入口](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/configs/r012.recovery.json)。[已登记教训](../lesson/cqc_P27.lessons.md)。

[此前交付及历史证据入口](https://github.com/ziyu24/cqc_research_lessons/blob/66c940b/progress/cqc_P27.md)保留旧UniOT、梯度诊断和数据复核事实；这里只更新当前判断，不覆盖原研究问题。
