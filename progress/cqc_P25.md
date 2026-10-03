# P25 项目进展

## 最初科学问题

没有完整OBB标注源域，仅有部分HBox或Point图像与完全无标签图像，如何学习对训练不可见目标域泛化的旋转检测器。

## 核心进展

内部强弱、域内参照诊断与作者原生模块核验已完成。C已交付r022完整单源旋转适配及语言机制开/关两臂，按用户要求并行且每臂实际两卡；CPU实际权重、全部L/U加载和两臂相同初态通过。A完整训练及四域冻结评价已完成并通过CPU输出核验，B仍训练；尚无完整两臂比较，外部SSDG匹配性能参照和弱标注成本问题仍未解决。

r020已独立复核：域内HRSC/SODA/FAIR的VOC07 AP50为87.867/71.638/73.862，P27纯源为40.619/47.350/45.405，P25弱基线为25.476/31.337/37.518。框架、初始化、标注条件和参照选优不同，差值不能全部归为强标注或域偏移因果。H/O共同缺失对象有大量可被域内模型支持；跨域类别筛选损失和SODA小车早期几何覆盖不足并存，候选丢失阶段不是已知训练根因。

r022两臂固定同一DOTA1.0的195-L真实OBB及1216-U、RegionCLIP初态、源内风格、完整120k预算和seed42，只切换图像/区域语言一致性与描述蒸馏。它是CDDMSL核心机制的单源旋转适配：PWOOD分类器、EMA预测区域及源内FDA分别区别于作者文本分类器、RPN及双源CycleGAN，不宣称原方法完整复现。原标注成本问题保留，本轮不追加HBox第三臂。

## 服务器当前内容

r020、r021均已执行结束且通过C独立复核。r021为四张固定DOTA源图、双卡零更新原生语言模块核验，没有检测器训练或新AP。

C于2026-10-01 UTC交付并推送r022，SERVER于02:24:45 UTC在26实际启动同号入口并完成真实CUDA首批。现已于06:01:53 UTC从两臂各自12800步完整恢复点同号续接，A主0辅1、B主1辅0，各自实际双卡且继续并行，不使用2/3。06:05:07 UTC正式日志A12900/B12850，已进入原生U及B语言训练；没有final或新AP。既有DOTA快检仍UNCHANGED且image_bytes_read=0，L/U为2846/12903切片、195/1216原图，缺失/额外/交叉均零；没有重复像素核验、重切或改变科学机制/预算。各120k终点立即冻结四域评价，无需确认。

2026-10-03 02:23 UTC已观察到A正式日志120000步及完整final（与最新resume同一实体），原生终点检查通过，训练PID已退出；其原臂父进程立即启动冻结评价。03:30 UTC确认A四域评价结束、原臂父进程及评价PID退出。HRSC/SODA/FAIR/DOTA val的VOC07 AP50为48.660/35.967/41.719/80.215，连续AP50为47.134/34.797/41.091/83.218；SODA仍为原自定义1024/824，不标官方基准。03:32 UTC B原训练PID仍在0/1双卡继续、已到72150步；没有暂停B、重训或改变协议。A对照完成不是语言收益证据，B尚未到终点，不称r022结束。

SERVER另外已回写46旧重复缓存清理；本次交付保留该回写，未改清理范围或受保护权重。r022资产和源输入不依赖被清理的重复缓存。

## 核验说明

r020独立复算248个AP单元、全部阶段计数及支持交集，覆盖15份报告、30分片，H/O原生输出一致。r021资产SHA、九份作者源文件、四图身份、两rank记录与输入绑定已独立回读；仅证明原生模块可运行。既有冻结IoU/原生阶段重放和数据审计在未变范围复用，不重复GPU推理或全量像素检查。

本轮C在26既有环境通过只读CPU检查：严格加载实际公开视觉骨干和冻结映射，作者特征最大误差4.25e-5、末token映射相同、activation checkpoint梯度差0；语言梯度非零、冻结分支无梯度。完整2846-L/12903-U加载、同34380个L实例及1158空L通过，未读取U标注或目标图；两臂完整参数初态SHA相同，优化器/EMA/U及采样配置不变。独立损失、错误配对、FDA算式、空候选、旋转包络、私有RNG和并行启动模拟通过。

实际源图预览呈明显低频色斑及局部饱和，不能证明严格语义保持或有利风格；它是两臂共用适配条件，不按目标表现调参数。SERVER真实CUDA检查已通过，反序续跑后两臂均有正式学生两卡前向/非零反向与教师两卡前向；早期burn-in后50步平均A约1.49/B2.98秒，只作已观测吞吐，不外推全程收敛或最终收益。

目标评测保持HRSC453、SODA870自定义1024/824、FAIR3298、DOTA val458原图。域内FAIR参照有训练/选优暴露，HRSC参照曾按test选best，三目标已有研究观察，不称全过程盲测。候选支持可复用，不是TP或可实现AP；单seed不称跨种子稳定。

A输出已CPU只读核验4报告、8分片、52逐类AP单元和全部保存PR、阶段支持/丢失/候选计数；原图身份/顺序及GT分母等于冻结输入，两卡互斥覆盖、不同GPU UUID、正CUDA时间和共31013次实际前向通过，AP重放误差最大7.586e-6个百分点。复用原生IoU及数据证据，不重复图像解码或GPU推理；此核验不是独立IoU重算或科学因果验证。A固定final已在来源result/recovery及原保护配置中明确保护，删除须用户明确授权。

## 执行阶段

主/辅卡均衡已实际落实：复用B反序零更新CUDA检查及两臂3200步严格完整恢复证据，不重复等待确认。用户明确允许下一完整保存核验后外部受控退出并接受少量在途/未保存更新回退；两臂各在06:01:19/24 UTC核完整12800保存后退出，旧训练/worker及已识别加载子进程均已退出，再于06:01:53 UTC同r022续接。A/B实际新PID分别2394328/2394329，UUID顺序0/1与1/0，两个gpu-check均MATCH、两卡实际前后向及步数增长通过。原日志、完整恢复状态和旧attempt记录保留，未用更早checkpoint、未重训；全局4L+2U、采样、seed42、归约、优化器/LR/EMA、120k及冻结评测未变。原生DataLoader预取不保存，实际未保存/在途回退步数未观察，不能宣称位级batch轨迹连续。

r022已在26实际启动；02:26 UTC已核两臂真实CUDA首批通过，并已自动进入正式120k训练。A/B各自PID绑定物理GPU 0、1为MATCH，两卡均观察到学生实际前向和非零反向；采用原生等价双卡特征并行与完整batch头/归约，不冒称DDP。初态相同、空L/冻结分支/正ROI梯度及真实语言开关检测损失隔离通过，无优化器首批更新。现A训练/评价执行结束，B训练继续，整个任务仍在执行；内部诊断/r021成功或A到终点不代表r022机制或P25目标成功。

记录者：SERVER（保留C核验与交付）；更新日期：2026-10-03 03:32 UTC。

## 下一步与维护

SERVER按交付入口完成两臂，每臂关键终点立即评测，同次正式前向保留AP/PR及既定候选阶段统计。B−A的AP和同类保留共同改善才支持干预有效；几何覆盖同时变化则报告联合效应，只有支持率或源域分提高不算解决。完整结果决定如何推进匹配HBox臂回答成本问题，不追阈值、步数或种子，不恢复r018/r017和旧停止搜索。

训练只有两臂各120k、4L+2U、seed42、实际两卡。基于旧日志及原生分支耗时，无争用估计A60–100、B120–200 GPU小时，检查/评价另8–20，合计188–320；共享同两卡会增加墙钟及按每臂卡数累加的占用时，需实际并发首批校正，不是硬限时。保护final及完整恢复依赖，代码、配置及恢复材料留Home Git，大产物归本项目。

动作执行者按[主动更新约定](README.md)在实际启动、异常或执行结束时更新本页并推送；无需等待用户轮询，不新增监控或审批。执行结束仍待C科学复核。

## 证据

[A完整四域输出、CPU复算和保护权重结果](https://github.com/ziyu24/cqc_P25/blob/39902ae/lab/result.md)；[A核验摘要与输出绑定](https://github.com/ziyu24/cqc_P25/blob/39902ae/doc/r022_execution.json)；[可重放CPU检查](https://github.com/ziyu24/cqc_P25/blob/39902ae/src/review_language_outputs.py)。

[A完整120000步终点与立即双卡冻结评价、B继续执行证据](https://github.com/ziyu24/cqc_P25/blob/776af5b/doc/r022_execution.json)。

[A部分HRSC指标、冻结终点绑定与两卡实际前向证明](https://github.com/ziyu24/cqc_P25/blob/27fd910/doc/r022_execution.json)。

[12800完整保存核验、受控退出和实际反序双卡增长证据](https://github.com/ziyu24/cqc_P25/blob/92b8f7e/doc/r022_device_order_review.json)；[已推送同号反序恢复材料](https://github.com/ziyu24/cqc_P25/blob/92b8f7e/configs/r022.recovery.json)；[一次性下一完整保存核验与精确PID退出入口](https://github.com/ziyu24/cqc_P25/blob/7c59352/src/pause_language_checkpoint.py)。

[反序GPU与3200步完整恢复检查及此前暂停限制](https://github.com/ziyu24/cqc_P25/blob/479ca1d/doc/r022_device_order_review.json)；[完整恢复核验入口](https://github.com/ziyu24/cqc_P25/blob/de76cd5/src/check_language_resume_order.py)。

[SERVER UUID绑定修正](https://github.com/ziyu24/cqc_P25/commit/62d4b1f685310e2d780b50fe7ff1222ed09e5d63)；[已推送实际恢复入口](https://github.com/ziyu24/cqc_P25/blob/c17fd3e3730d99d1b82cc29d886c23baca566ff1/configs/r022.recovery.json)。

[SERVER两臂真实首批、初态及正式训练绑定证据](https://github.com/ziyu24/cqc_P25/blob/main/doc/r022_execution.json)。

[r020独立复核](https://github.com/ziyu24/cqc_P25/blob/5cbd1ed275c561facae133a7f27ccb81d1755885/doc/r020_independent_review.json)；[r021独立复核](https://github.com/ziyu24/cqc_P25/blob/f62c99923ce8e021db6dc069dfaad9027d32a36b/doc/r021_independent_review.json)；[已登记教训](../lesson/cqc_P25.lessons.md)。

[r022唯一科学任务](https://github.com/ziyu24/cqc_P25/blob/4d6ed34/lab/sug.md)；[完整实现及方法边界](https://github.com/ziyu24/cqc_P25/blob/4d6ed34/doc/cddmsl_adaptation.md)；[C实际资产/初态检查](https://github.com/ziyu24/cqc_P25/blob/4d6ed34/doc/language_control_review.json)；[并行执行入口](https://github.com/ziyu24/cqc_P25/blob/4d6ed34/doc/server.md)；[当前科学讨论](https://github.com/ziyu24/cqc_P25/blob/4d6ed34/lab/discussion.md)。
