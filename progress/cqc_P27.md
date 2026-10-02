# P27 项目进展

## 最初科学问题

类别集合不一致、重叠关系未知时，能否利用有标注源域与无标签目标域改善共享类别的旋转目标检测。

## 核心进展

用户已同意普通DA上的OpenDet式类别判别和拒识学习，C已实现并下发r013完整机制与同结构控制两臂。新增模块、背景/unknown映射、原生回归、双rank全局梯度和结果裁决的针对性检查已通过；有效性尚未验证，未观察到新训练启动。原核心目标未达成，已定位的语义混淆不是全部错误或已证明的OBB特有根因。

固定DPA相对同结构普通对照总AP50高0.143个百分点，大车AP下降，整条共同可达大车TP范围内私有FP从未更少。严格IoU与相对旧基线的局部改善保留，源检测没有UniOT式崩塌；结束该固定配置的结论不变。

累计事实：旧普通DA相对source-only有正迁移；IDSA有小幅正差但指定候选位置必要性未获支持。固定KLD提高AP50却降低严格IoU；源支持度与GT几何诊断未支持所提关键混淆解法。UniOT完整/去PCD适配的目标AP50为41.739%/43.409%，低于旧普通DA52.062%，源best也大幅下降；后续两份best各8批的冻结梯度检查不足以支持共同持续反向解释，不启动梯度保护支线。各项失败只限实际条件，原研究目标仍未达成。

## 服务器当前内容

2026-10-01 PDT，C已交付r013两臂可执行入口，按最近实际执行端指定46；各12源epoch、47,256步、单种子、实际两卡，完整臂完成立即评完整val后继续控制臂。首批真实GPU/加载/吞吐由SERVER核验后直接执行。C本轮只读核46项目及主机配置，并以CPU内存测试核验接口，未在服务器写文件、启动训练或改动在跑任务；当前记录为已下发，实际训练尚未观察。

此前已完成的有效执行事实保留：

SERVER按其会话中用户最后明确选择在46完成r012，完整DPA及同结构普通对照均12源epoch、47,256步、固定种子20260926和真实两rank；每臂以源best评完整目标val。中途只因缺少已有诊断数组退出，补回并校验后复用已完成训练/评测、继续剩余工作。完成时间按SERVER报告为2026-10-01 17:01 PDT；完整/普通源best为74.854%/75.023%，目标AP50为52.461%/52.317%，大车AP为17.206%/18.722%。两份best已登记保护，完成时唯一槽已清空。

C于2026-10-01 17:24 PDT回读46正确仓库、Home及tmpfs产物映射、原生日志、模型和合法结果，观察时无相关残留进程。当前为科学完成且已复核，不是等待继续训练；本轮没有新GPU任务。

## 核验说明

本轮新增部分已核：本地39项测试通过，缺原生库/Gloo的6项skip另在46现有mr以原始测试函数验证；四项原生CPU检查通过，真实Linux两rank完整/控制的损失、逐参数梯度、队列均匹配全局参考。曾发现原生递归初始化覆盖新增MLP，已修正并复测；source-only辅助、17维概率保留、采样/回归不变、双臂同初态及恢复有反例覆盖。尚未核实际双GPU首批和真实训练收益，CPU结果不代替GPU计算。数据沿已核manifest身份与覆盖，不重切或全量重审DOTA；保留SODA800/650 nomask自定义输入。

旧结果的充分核验依据继续有效：

执行配置逐字段核对模型、损失、SGD/Adam及学习率计划、原生候选采样/数据pipeline和源验证规则，与交付一致。四份换端manifest与原件只差路径前缀，ID/标注/加载覆盖不变；源train/val为1,411/458原图与15,749/5,297切片，目标train/val为1,067/576原图与37,980/20,549切片，目标train框数0。保持项目800/650 nomask输入，未重切或全量重扫DOTA，没有target test。

C复算现有审计的训练终点、12次源验证、best/latest、配置/权重/GT绑定、语义数组和比较，与SERVER证据一致。另用独立累计代码复算整条共同可达曲线：完整DPA相对同结构控制在大车1—1,144 TP中0点私有FP更少、41点相同、1,103点更多；同1,087 TP为4,532对4,149。因此原关键混淆失败不取决于95%点。

正信号及限制保留：相对旧普通DA，同1,087 TP为4,532对5,495，多数共同点仍有改善；但新普通控制更好，不能把旧新变化全部归因DPA。完整臂AP75/AP50:95为15.537%/23.238%，相对同结构控制高0.528/0.156个百分点。历史参考TP不可达只针对既定输出截断协议；曲线点不独立，不能当显著性或跨种子稳定性。未重跑图像前向/全部IoU匹配，复用已绑定原生输出及AP回放。

元数据限制：Home RUN仍显示PLANNED，完成判断依据实际日志、权重及评测；两rank及完整计算记录已核，SERVER所述物理GPU3/2的历史UUID快照本次未独立取得。该缺口不抹去实际科学输出，也不成为重训理由。原生模型/损失没有被SERVER修改；新旧对照的结构差异已由必要同结构臂控制。

## 执行阶段

2026-10-01 PDT，用户明确“可行，给出服务器执行方案”后，C完成r013实现、针对性检查及源仓库推送，正式交付两臂任务。SERVER尚未回报实际启动；此页不把代码就绪说成训练进行中。固定DPA已科学结束并复核，原项目仍运行，目标与成功边界不变。

记录者：C；更新日期：2026-10-01 PDT。此前SERVER有效执行事实及C独立复核结论继续保留。

## 下一步与维护

目前核心问题是如何改善共享检测，同时避免把相近私有物体自信判为已知类。已有预测确认它有AP损失，也排除了原分数阈值能修复同结构大车曲线的解释；旧权重不能回答新表征训练效果，因此必要的下一步是已经实现的训练干预，不再追加宽泛冻结诊断。

核心问题解法仍待验证：只对源合法ROI施加OpenDet式类别对比和未知条件概率，目标保留普通DA，不给共享名单/目标私有身份。两臂同新头，只开关CFL+UPL。总AP50增量与预定同TP私有FP拒识证据分开裁决；大车误报减少但真实检测受损不算成功，全曲线和不可达范围同时报告。source best及严格IoU如实保留，不将旧任务的所有辅助条件自动升级为新成功门槛。

source背景不是真unknown，学出的边界可能不跨域、拒掉真大车或继续接收container；科学有效性未知。固定两臂结束后按结果收尾，不自动扫参/加种子/换路线。即使阳性，也不自动证明OBB专属性、跨种子稳定或算法原创。两臂best作为实验和控制证据须在收尾登记保护。

动作执行者按[主动更新约定](README.md)在真实事件发生时更新本页并发布总览。

## 证据

[已推送唯一任务](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/lab/sug.md)；[用户授权与科学取舍](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/lab/discussion.md)；[机制、作者偏离与执行入口](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/doc/opendet_execution.md)；[实际检查记录](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/doc/opendet_delivery_checks.json)；[冻结配置](https://github.com/ziyu24/cqc_P27/blob/69b0d7e9100ddb7c1a3db123eb9ddbbf23b4e852/configs/r013.json)。本轮准备不包含新训练、目标评测或GPU计算。

[本轮独立研究取舍、原论文与代码来源](https://github.com/ziyu24/cqc_P27/blob/dce35d692144f078a5a47c086d55e023ad9e5e92/doc/method_transfer_review.md)；[当前判断与建议边界](https://github.com/ziyu24/cqc_P27/blob/dce35d692144f078a5a47c086d55e023ad9e5e92/lab/discussion.md)。该独立调研阶段未另做服务器观察；本轮交付的只读核验和CPU检查见上方新来源，不覆盖此前有效科学证据。

[当前科学讨论](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/lab/discussion.md)；[完整累计结果和受保护权重](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/lab/result.md)；[C独立复核及共同范围统计](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/doc/r012_completion_review.json)；[SERVER充分证据](https://github.com/ziyu24/cqc_P27/blob/84fa2a17b1fb6e3976a93dc22f13be713330b9bd/doc/r012_evidence.json)；[科学适配与差异](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/doc/dpa_execution.md)；[恢复入口](https://github.com/ziyu24/cqc_P27/blob/a6b9499da2c074f4e53aaa3aecda8a025005264d/configs/r012.recovery.json)。[已登记教训](../lesson/cqc_P27.lessons.md)。

[此前交付及历史证据入口](https://github.com/ziyu24/cqc_research_lessons/blob/66c940b/progress/cqc_P27.md)保留旧UniOT、梯度诊断和数据复核事实；这里只更新当前判断，不覆盖原研究问题。
