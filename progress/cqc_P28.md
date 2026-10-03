# P28 项目进展

## 最初科学问题

源训练完成后，能否利用陆续到达的无标签目标图像改善旋转检测，并在连续域变化中保持收益、抑制有害更新和遗忘。

## 核心进展

项目已有FAIR1M单域有效底座，并完成第一次FAIR1M→SODA-A真实连续换域。r014执行本身完整，但“新域双AP超过两个冻结参照且旧域双AP不降”的联合条件失败；原始长期CTTA目标仍未达成，广义路线未被整体证伪也不等于成功。

FAIR1M单域的条件前景加adapter相对同监督控制，单视图AP50/AP75提高2.241/0.519点，背景FP减少2,136，源正确大车多保留925个；这是可信的单域机制阳性。固定LPLD遗漏候选规则则相对同量置信度少补216个唯一GT并多177个明确背景，未进入训练。

首次换域的单视图点估计（百分点，AP50/AP75）：A冻结减源冻结=`+1.445/-0.478`，carry减A冻结=`+0.025/+0.031`，reset减源冻结=`-0.023/-0.014`，carry减reset=`+1.493/-0.433`，A保持面板后减前=`-0.628/-0.096`。直接迁移和历史影响均为双IoU取舍，新域更新相对自身初态接近零，已见旧域面板双指标下降；不能称长期收益、稳定更新或跨种子结论。

## 服务器当前内容

r014于2026-10-03 00:05:46至08:16:41 UTC在46物理GPU 0、1完成，RUN为`COMPLETE/exit 0`。四个SODA-A B臂各完整覆盖576原图/20,549切片，A前后各覆盖同一256图面板；预测ID均无缺失、额外或重复。carry/reset各完成466更新、110跳过、127,288伪框，实际双rank及PID→GPU UUID为`MATCH`，原检测器状态保持不变。

carry/reset终点分别位于46 `runs/r014/artifacts/carry/latest.pth`与`runs/r014/artifacts/reset/latest.pth`，SHA-256为`243f7b272f03aa58d87600fe3f1c78e60136664adee6d70f6fd26edd91c157f5`和`f7575a2e18916391b37b8701b30f5aaae36b134aee96f5fc7f5aa42a81fba14f`。两者均含student/teacher、64项optimizer状态、双rank RNG和cursor=576，已在原配置标记“受保护，删除须用户明确授权”。源best与r011 A终点也继续受原保护。当前无P28运行进程，46工作区已同步到来源提交`cfd1615`。

## 核验说明

SODA-A使用官方val的800窗口、650步长标准切片与官方ignore遮罩，保留200张四类空图；合法GT为plane/ship/large-vehicle/small-vehicle `8,558/21,658/3,723/141,265`。执行前SODA、DOTA-v1.5 train/val与FAIR1M报告均为`UNCHANGED/PASS`，未重切、重解码或重读图像字节；没有使用旧缺陷DOTA训练标签产物。SODA test未读取，评分为项目四类全有效尺寸、原图合并rotated VOC07 AP50/AP75，不冒称官方Small/COCO AP。

carry完整继承A的student、EMA、SGD动量与两rank RNG；reset从源状态开始。二者B顺序、超参、更新/跳过/伪框数完全相同，首个更新前预测相等；carry历史计数与r011终点闭合。两个终点均完整加载，student/teacher各412项、optimizer 64项、RNG 2份；固定源和原检测器摘要不变。完整RUN按两卡墙钟约16.36 GPU小时，相关进程均已退出。

本页只记录一次换域的真实点估计。A保持面板是已见256张单切片图，不是未观察A2、第三段在线回域或全域遗忘率；单种子不支持显著性或稳定性。历史状态差同时包含权重、EMA、动量和RNG，不能唯一归因其中一项。

## 执行阶段

r011完成并复核；r012后置未执行；r013完成并复核；r014已执行结束并由SERVER完成协议、覆盖、指标、恢复状态与保护核验。项目仍在运行，当前SERVER任务槽为空，等待B/C基于累计证据形成下一科学任务。

## 下一步与维护

当前已确认的问题是：一次A→B中历史迁移在AP50/AP75间取舍，B更新相对自身初态近零，并出现已见A面板保持代价。尚未知这些小差异是否可重复、未观察回域是否同样下降，以及多域继续时会否累积。下一步应由B/C决定是优先验证不重复回域/多域序列，还是提出直接针对保持代价的可证伪替代；SERVER不自行追加回放、随机恢复、参数扫描或新模块。

## 证据

[r014完整结果与裁决](https://github.com/ziyu24/cqc_P28/blob/cfd1615ebdc00d0492f062a3dbbe9568a4b79822/lab/result.md)；[当前科学结论与未知](https://github.com/ziyu24/cqc_P28/blob/cfd1615ebdc00d0492f062a3dbbe9568a4b79822/lab/discussion.md)；[主要失败边界](https://github.com/ziyu24/cqc_P28/blob/cfd1615ebdc00d0492f062a3dbbe9568a4b79822/lab/failed_methods.md)；[已清空任务槽](https://github.com/ziyu24/cqc_P28/blob/cfd1615ebdc00d0492f062a3dbbe9568a4b79822/lab/sug.md)；[固定配置与保护](https://github.com/ziyu24/cqc_P28/blob/cfd1615ebdc00d0492f062a3dbbe9568a4b79822/configs/r014.json)；[恢复入口](https://github.com/ziyu24/cqc_P28/blob/cfd1615ebdc00d0492f062a3dbbe9568a4b79822/configs/r014.recovery.json)。
