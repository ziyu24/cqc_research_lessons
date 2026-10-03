# P28 项目进展

## 最初科学问题

源训练完成后，能否利用陆续到达的无标签目标图像改善旋转检测，并在连续域变化中保持收益、抑制有害更新和遗忘。

## 核心进展

项目已有FAIR1M单域有效底座，首次FAIR1M→SODA-A连续换域已于2026-10-03 08:43 UTC起由B完成充分复核。完整执行及收益与保持联合条件失败可信，但新增收益近零、已见面板部分指标下降的根因仍未知；优先复用现有状态做有界冻结端点检查，不新增训练。原始长期CTTA目标仍未达成。

FAIR1M单域的条件前景加adapter相对同监督控制，单视图AP50/AP75提高2.241/0.519点，背景FP减少2,136，源正确大车多保留925个；这是可信的单域机制阳性。固定LPLD遗漏候选规则则相对同量置信度少补216个唯一GT并多177个明确背景，未进入训练。

首次换域的单视图点估计（百分点，AP50/AP75）：A冻结减源冻结=`+1.445/-0.478`，carry减A冻结=`+0.025/+0.031`，reset减源冻结=`-0.023/-0.014`，carry减reset=`+1.493/-0.433`，A保持面板后减前=`-0.628/-0.096`。B的AP75历史损失在B学习前已存在；A单视图AP50下降主要来自船，辅助双视图A保持为`-0.119/+0.436`点。保留主指标联合失败，不把这些取舍写成全域灾难遗忘、长期收益或跨种子结论。

## 服务器当前内容

r014于2026-10-03 00:05:46至08:16:41 UTC在46物理GPU 0、1完成，B于08:43 UTC起只读复核确认科学任务结束。四个SODA-A B臂各完整覆盖576原图/20,549切片，A前后各覆盖同一256图面板；六臂预测ID、评分身份、双rank完整游标及实际GPU记录闭合。carry/reset各完成466更新、110跳过、127,288伪框；当前无P28任务进程，唯一任务槽为空，无新训练下发。

carry/reset终点分别位于46 `runs/r014/artifacts/carry/latest.pth`与`runs/r014/artifacts/reset/latest.pth`，SHA-256为`243f7b272f03aa58d87600fe3f1c78e60136664adee6d70f6fd26edd91c157f5`和`f7575a2e18916391b37b8701b30f5aaae36b134aee96f5fc7f5aa42a81fba14f`。两者均含student/teacher、64项optimizer状态、双rank RNG和cursor=576，实体长度、SHA与保护配置已回核。源best、A终态及两B终态均继续受保护，删除须用户明确授权。08:43 UTC起观察的46工作区提交为`cfd1615`且干净；B复核证据已在来源`d78cf4862c4af581cb5a8bd3afbe740586c6650a`发布。

## 核验说明

SODA-A使用官方val的800窗口、650步长标准切片与官方ignore遮罩，保留200张四类空图；合法GT为plane/ship/large-vehicle/small-vehicle `8,558/21,658/3,723/141,265`。执行前SODA、DOTA-v1.5 train/val与FAIR1M报告均为`UNCHANGED/PASS`，未重切、重解码或重读图像字节；没有使用旧缺陷DOTA训练标签产物。SODA test未读取，评分为项目四类全有效尺寸、原图合并rotated VOC07 AP50/AP75，不冒称官方Small/COCO AP。

carry完整继承A的student、EMA、SGD动量与两rank RNG；reset从源状态开始。二者B顺序、超参、更新/跳过/伪框数完全相同；首个更新前，carry与A冻结、reset与源冻结各自全部NPZ字段逐值相等，不是两个在线臂彼此相等。carry历史计数与A终点闭合。两个B终点均完整加载，student/teacher各412项、optimizer 64项、RNG 2份；另在CPU逐张量确认A及carry学生/EMA的348项原检测器状态与源checkpoint严格相等。comparison文件SHA与差值算术均一致。完整RUN按两卡墙钟约16.36 GPU小时。

当前裁决核验充分；复用未变的评分实现及已核数据报告，没有重复全量评分、读像素或GPU前向。CPU状态核验确认A学生与EMA不等，B学生与A学生也已变化；466次、动量0.999的EMA递推中，旧EMA系数为0.62736。这些状态和算术证据足以提出冻结端点检查，但参数差及EMA系数不能证明性能根因，尚未检验“只让EMA追赶冻结A学生”的输出。

本页只记录一次换域的真实点估计。A保持面板是已见256张单切片图，不是未观察A2、第三段在线回域或全域遗忘率；单种子不支持显著性或稳定性。历史状态差同时包含权重、EMA、动量和RNG，不能唯一归因其中一项。

## 执行阶段

r014已科学结束，B于2026-10-03 08:43 UTC起完成覆盖、实际双卡、权重/恢复、源状态逐张量和统计复核；联合条件失败，根因仍未知。项目继续，唯一任务槽为空；后续有界冻结检查尚未下发或执行。r011阳性保留，r012仍后置未执行。

## 下一步与维护

目前核心问题是学生是否学到了有益变化，以及预测EMA是否及时反映这些变化，可靠解法尚未证实。优先复用A船类已保存预测做PR分解，再用已有A/B学生与EMA做一次有界冻结端点比较；必要对照为固定A学生、按原生EMA递推466次的“无B学习EMA”。这能区分新学习影响与旧学生追赶的可能影响，无须先重训。

检查前固定同图面板，禁止按GT或结果选图；B在线过程预测不能冒充终点预测，面板结果不当作新在线AP或独立盲测。学生改善但EMA未体现、冻结旧学生追赶已复现下降、或学生与实际EMA均恶化，会改变后续机制选择；变化小不证明加步数会涨点。以上尚为待核验计划，不是已证根因或新SERVER任务，不扫EMA、阈值、步数或种子，不立即叠加回放/恢复模块。

## 证据

[r014完整结果与B独立复核](https://github.com/ziyu24/cqc_P28/blob/d78cf4862c4af581cb5a8bd3afbe740586c6650a/lab/result.md)；[核心问题与原项目交接](https://github.com/ziyu24/cqc_P28/blob/d78cf4862c4af581cb5a8bd3afbe740586c6650a/lab/discussion.md)；[主要失败边界](https://github.com/ziyu24/cqc_P28/blob/d78cf4862c4af581cb5a8bd3afbe740586c6650a/lab/failed_methods.md)；[已清空任务槽](https://github.com/ziyu24/cqc_P28/blob/d78cf4862c4af581cb5a8bd3afbe740586c6650a/lab/sug.md)；[固定配置与保护](https://github.com/ziyu24/cqc_P28/blob/d78cf4862c4af581cb5a8bd3afbe740586c6650a/configs/r014.json)；[恢复入口](https://github.com/ziyu24/cqc_P28/blob/d78cf4862c4af581cb5a8bd3afbe740586c6650a/configs/r014.recovery.json)。
