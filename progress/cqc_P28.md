# P28 项目进展

## 最初科学问题

源训练完成后，能否利用陆续到达的无标签目标图像改善旋转检测，并在连续域变化中保持收益、抑制有害更新和遗忘。

## 核心进展

项目已有可信FAIR1M单域收益，但首次连续换域的收益与保持联合条件失败。SERVER于2026-10-03完成零训练端点检查：固定A学生、只让EMA追赶即可几乎复现A保持下降，故不能把代价全部归因B学习；同时不支持“B学生已改善、只是EMA未反映”。原始长期CTTA目标仍未达成。

FAIR1M单域的条件前景加adapter相对同监督控制，单视图AP50/AP75提高2.241/0.519点，背景FP减少2,136，源正确大车多保留925个；这是可信的单域机制阳性。固定LPLD遗漏候选规则则相对同量置信度少补216个唯一GT并多177个明确背景，未进入训练。

首次换域的单视图点估计（百分点，AP50/AP75）：A冻结减源冻结=`+1.445/-0.478`，carry减A冻结=`+0.025/+0.031`，reset减源冻结=`-0.023/-0.014`，carry减reset=`+1.493/-0.433`，A保持面板后减前=`-0.628/-0.096`。B的AP75历史损失在B学习前已存在；A单视图AP50下降主要来自船，辅助双视图A保持为`-0.119/+0.436`点。保留主指标联合失败，不把这些取舍写成全域灾难遗忘、长期收益或跨种子结论。

## 服务器当前内容

r014于2026-10-03 00:05:46至08:16:41 UTC在46物理GPU 0、1完成，B于08:43 UTC起只读复核确认科学任务结束。四个SODA-A B臂各完整覆盖576原图/20,549切片，A前后各覆盖同一256图面板；六臂预测ID、评分身份、双rank完整游标及实际GPU记录闭合。carry/reset各完成466更新、110跳过、127,288伪框。r015于09:44:28至10:27:35 UTC在同机物理GPU 0、1完成，七项冻结前向均为实际双rank、0训练/0优化步；结果已归入来源项目，当前无P28任务进程。

carry/reset终点分别位于46 `runs/r014/artifacts/carry/latest.pth`与`runs/r014/artifacts/reset/latest.pth`，SHA-256为`243f7b272f03aa58d87600fe3f1c78e60136664adee6d70f6fd26edd91c157f5`和`f7575a2e18916391b37b8701b30f5aaae36b134aee96f5fc7f5aa42a81fba14f`。两者均含student/teacher、64项optimizer状态、双rank RNG和cursor=576，实体长度、SHA与保护配置已回核。源best、A终态及两B终态均继续受保护，删除须用户明确授权。08:43 UTC起观察的46工作区提交为`cfd1615`且干净；B复核证据已在来源`d78cf4862c4af581cb5a8bd3afbe740586c6650a`发布。

## 核验说明

SODA-A使用官方val的800窗口、650步长标准切片与官方ignore遮罩，保留200张四类空图；合法GT为plane/ship/large-vehicle/small-vehicle `8,558/21,658/3,723/141,265`。执行前SODA、DOTA-v1.5 train/val与FAIR1M报告均为`UNCHANGED/PASS`，未重切、重解码或重读图像字节；没有使用旧缺陷DOTA训练标签产物。SODA test未读取，评分为项目四类全有效尺寸、原图合并rotated VOC07 AP50/AP75，不冒称官方Small/COCO AP。

carry完整继承A的student、EMA、SGD动量与两rank RNG；reset从源状态开始。二者B顺序、超参、更新/跳过/伪框数完全相同；首个更新前，carry与A冻结、reset与源冻结各自全部NPZ字段逐值相等，不是两个在线臂彼此相等。carry历史计数与A终点闭合。两个B终点均完整加载，student/teacher各412项、optimizer 64项、RNG 2份；另在CPU逐张量确认A及carry学生/EMA的348项原检测器状态与源checkpoint严格相等。comparison文件SHA与差值算术均一致。完整RUN按两卡墙钟约16.36 GPU小时。

当前裁决核验充分；复用未变的评分实现及已核数据报告，没有重复全量评分、读像素或GPU前向。CPU状态核验确认A学生与EMA不等，B学生与A学生也已变化；466次、动量0.999的EMA递推中，旧EMA系数为0.62736。这些状态和算术证据足以提出冻结端点检查，但参数差及EMA系数不能证明性能根因，尚未检验“只让EMA追赶冻结A学生”的输出。

新增核验足以解释A船类AP幅度：船AP50 47.545%→44.950%，TP251→250、FP690→695；召回从60.192%降至59.952%跌破VOC07 0.6插值点，该项贡献跌幅94.56%。积分AP50下降0.214点，真实PR代价保留。AP75的131个TP身份全部保留、FP增加4，积分AP75仍下降0.082点。只复算这256图的船类，四类GT覆盖及原生AP精确复得，0训练/0前向/0 GPU小时，没有重扫无关全流。

真实受保护A/B权重上的CPU端点载入与原生EMA反例检查通过：原348项与源逐张量相等，固定S_A递推466次的T_noB重复构造一致、输入不变，非法步数/改变原状态被拒绝。GPU七项均完成双rank和物理卡MATCH，四份端点配置的真实初态历史、预测ID及子集合同闭合。B面板在新前向前固定原流前32图全部1187块，飞机/船/大车/小车GT为743/17/169/7251，含12张四类空图；船仅17 GT限制外推，不因GT稀少追加挑图。

r015单视图主差值（AP50/AP75百分点）：B学生减A学生=`-0.086701/-0.082955`，真实B教师减无B学习教师=`+0.004351/+0.413047`；A无B学习教师减原A教师=`-0.622231/-0.079548`，真实B后教师减原A教师=`-0.628304/-0.095606`。固定学生的EMA追赶几乎复现保持下降，而B学生没有先改善，故响应滞后与学生学习损害两个预定联合解释均不获支持。变化小且部分异号，不用于选EMA或承诺延长训练收益。

本页只记录一次换域的真实点估计。A保持面板是已见256张单切片图，不是未观察A2、第三段在线回域或全域遗忘率；单种子不支持显著性或稳定性。历史状态差同时包含权重、EMA、动量和RNG，不能唯一归因其中一项。

## 执行阶段

r014已科学结束，B于2026-10-03 08:43 UTC起完成覆盖、实际双卡、权重/恢复、源状态逐张量和统计复核；联合条件失败。r015于10:27 UTC执行结束并由SERVER完成输入、覆盖、双rank、物理卡、端点与差值核验，来源证据已推送；任务槽已清空，执行结束待B/C复核。r011阳性保留，r012仍后置未执行，项目继续。

## 下一步与维护

当前有界端点问题已回答：A保持下降主要可由旧学生的EMA追赶反例复现，不能全归B学习；预定证据不支持响应滞后或学生学习损害的联合解释。下一步由B/C在累计证据上选择针对性替换机制；SERVER不自行扫EMA、阈值、步数、种子，也不叠加回放、恢复或重复诊断。面板结果仍不是新在线AP、独立盲测或长期CTTA成功。

## 证据

[r014完整结果与B独立复核](https://github.com/ziyu24/cqc_P28/blob/d78cf4862c4af581cb5a8bd3afbe740586c6650a/lab/result.md)；[核心问题与原项目交接](https://github.com/ziyu24/cqc_P28/blob/d78cf4862c4af581cb5a8bd3afbe740586c6650a/lab/discussion.md)；[主要失败边界](https://github.com/ziyu24/cqc_P28/blob/d78cf4862c4af581cb5a8bd3afbe740586c6650a/lab/failed_methods.md)；[固定配置与保护](https://github.com/ziyu24/cqc_P28/blob/d78cf4862c4af581cb5a8bd3afbe740586c6650a/configs/r014.json)；[恢复入口](https://github.com/ziyu24/cqc_P28/blob/d78cf4862c4af581cb5a8bd3afbe740586c6650a/configs/r014.recovery.json)。

[本轮PR证据与解释边界](https://github.com/ziyu24/cqc_P28/blob/81ca09acb290a76acaab095296387cb14f38f8b0/lab/result.md)；[唯一零训练任务](https://github.com/ziyu24/cqc_P28/blob/87c9f9e9779ceea2e529ac5f3dd982dde768a697/lab/sug.md)；[冻结端点执行入口](https://github.com/ziyu24/cqc_P28/blob/87c9f9e9779ceea2e529ac5f3dd982dde768a697/src/run_frozen_endpoints.py)；[CPU关键反例报告](https://github.com/ziyu24/cqc_P28/blob/81ca09acb290a76acaab095296387cb14f38f8b0/doc/r015_endpoint_cpu_check.json)；[r015恢复入口](https://github.com/ziyu24/cqc_P28/blob/204c150c819cb597b773c2c8ad95265cbf0845fc/configs/r015.recovery.json)。

[r015完整结果与SERVER裁决](https://github.com/ziyu24/cqc_P28/blob/d1c04f7234eea48f13b93a59ae66b6559bac37d1/lab/result.md)；[r015讨论结论](https://github.com/ziyu24/cqc_P28/blob/d1c04f7234eea48f13b93a59ae66b6559bac37d1/lab/discussion.md)。
