# P23 项目进展

## 最初科学问题

少量图像保留每个实例、但Point/HBox可能出错，结合大量无标签图像如何学习OBB检测。

## 核心进展

用同一SAM物理框约束旋转几何，在HRSC带噪条件有较大性能收益，无标签学习也有增量；独立创新和多类通用性仍未完成。

## 服务器当前内容

按用户指定在十五类DOTA上训练新完整方案的带噪、干净两臂；带噪臂已跑满120000步。干净臂在46使用物理GPU 2、3推进到96000步完整恢复点后，于2026-10-02 04:49 UTC收到SIGTERM并被运行器记为STOPPED；96000步评测尚未落盘，当前没有残留P23进程。本轮不自动补旧方案对照。

## 核验说明

旧结果和分配不可表示问题已有源码/真实增强反例；DOTA身份快检UNCHANGED，实际加载与13个原实例未映射边界已核。带噪臂38个既定评测点已生成；干净臂已有至92800步的29个完整评测点，92800步AP50/AP75为59.7722/23.0299，双rank、458原图/5297切片及产物哈希均已核。96000步恢复文件含优化器状态，但该步评测缺失；完整双臂结论仍须等干净臂到120000步，不能用中途指标或结构修正保证涨点。

## 执行阶段

服务器执行异常结束；2026-10-02 04:49 UTC在46核到r030于96000/120000评测期间被SIGTERM终止并标记STOPPED。96000步完整恢复点有效、此前物理GPU 2、3绑定持续MATCH，但命令退出不是科学完成，尚缺24000步训练及96000步起的既定评测。

记录者：B；初始化日期：2026-09-30。来源中的B/C核验与本次只读观察分开表述；未取得对端新回写，不称本轮共识。

## 下一步与维护

SERVER分别汇报带噪和干净完成事实；B/C据完整结果说明核验范围、同条件对照缺口和实际方法贡献。

动作执行者按[主动更新约定](README.md)在真实事件发生时更新本页并发布总览。

## 证据

[范围与最初立题](https://github.com/ziyu24/cqc_P23/blob/06c5b85d7c3d2d80f48fcd5dfafc073ac4dff52a/README.md)；[当前讨论](https://github.com/ziyu24/cqc_P23/blob/06c5b85d7c3d2d80f48fcd5dfafc073ac4dff52a/lab/discussion.md)；[结果依据](https://github.com/ziyu24/cqc_P23/blob/06c5b85d7c3d2d80f48fcd5dfafc073ac4dff52a/lab/result.md)；[主线任务](https://github.com/ziyu24/cqc_P23/blob/06c5b85d7c3d2d80f48fcd5dfafc073ac4dff52a/lab/sug.md)；[恢复入口](https://github.com/ziyu24/cqc_P23/blob/06c5b85d7c3d2d80f48fcd5dfafc073ac4dff52a/configs/r030.recovery.json)。 [已登记教训](../lesson/cqc_P23.lessons.md)。
