# P29 项目进展

## 最初科学问题

在光学遥感二维 OBB 离线域适应中，仅用两个源模型和无标注目标图像，能否把多源互补转化为单个同容量检测器的收益（MS-01）；额外开放一个源的完整标注数据时，能否获得超过普通源监督相加的收益（MS-02）。

## 核心进展

C已实际核清学生初始化监督：局部正/背景冲突存在，但平均检测头梯度同向，且约70%的冲突涉及错误伪框，不能直接拿冲突判标签质量或投入全局梯度投影。SERVER随后完成r005真实学生训练；union学生AP50/AP75为0.399136/0.291599，低于FAIR学生0.487296/0.333018，也低于冻结FAIR教师0.506138/0.356322。当前固定union学生路线未把互补转成最佳单源之上的收益。

原冻结控制已确认类别概率事件修正有效；当前ProbEn后验和置信度框平均失败。固定输出集合复算证明主要损失来自排序和坐标平均，NMS选择改变不足以解释。此结论保留，停止当前分支的阈值/先验扫描。

## 服务器当前内容

SERVER于2026-10-01 17:06:47–17:49:35 UTC在46完整执行r005：同一DOTA源初态，HRSC无标签train 436图，依次训练FAIR、union sum、DOTA监督三个同容量学生；每臂实际两卡、12 epoch/660更新、一个种子。三臂两个DDP rank、学习率节点、有限损失/梯度、固定epoch12终点和181图评测均齐全，GPU UUID为MATCH，结束后相关进程为0。DOTA学生AP50/AP75为0.323041/0.199333；union虽高于DOTA，但低于FAIR学生0.088160/0.041419，两个预定支持条件均失败。墙钟2568.738秒、两卡累计1.42708 GPU小时。

五项针对性反例及46原生CPU数据检查通过：空图保留、四类头ship索引、qbox转rbox与缩放、完整436样本覆盖、两rank采样模拟各220、恢复到本臂学生checkpoint。实际训练中每臂1320微迭代/660优化步，双rank终态摘要一致；三项epoch12终点已列为受保护权重。实际总成本低于事前1.5–3.0 GPU小时估计。

以下保留已完成证据：

C按用户授权直接在46完成r004，2026-10-01 15:21:07–15:22:04 UTC实际两张A30、91/90图，57.621秒、0.03201 GPU小时；实际PID→GPU UUID为MATCH。181次学生前向、0优化步，无新权重。该旧任务已执行结束并由C独立复核；r005随后已完成，未改写r004的限定结论。

三臂共362000个原RPN、各92672个采样ROI；两个rank模型状态前后不变。2026-10-01 15:43:20 UTC观察时相关PID退出，两源实体存在，既有P28源best保护不变。新产物368文件、64,346,052字节，原始分配/梯度、日志和恢复材料保留。

SODA输入修复也已在46验证：仅按原图尺寸生成1067图/37980窗口，集合缺失/额外0，四个实际边界裁块与原图像素一致，未读目标标注。原官方切片依赖GT掩膜，保留原数据并新增图像独立读取方式，没有批量重切或修改正式评估。代码、结论、索引及恢复材料已推送并同步46 Home仓库。

## 核验说明

**r004限定结论已由C充分复核；r005已由SERVER充分核验执行与产物完整性，尚不是B/C独立科学复算。** r005训练未打开train GT，三份伪标签各覆盖436图；三臂各181份预测，双rank评测91/90图，六条PR长度均等于检测数。三个权重哈希与评测记录一致，student summary联合支持为false。

r004梯度检查仍只限于DOTA源初态、预定0.5门槛、原生ROI监督及最后共享FC/分类/回归层；r005补上了完整训练与学生AP，但没有等数量伪框或噪声分型对照。union正框更多且空图更少而性能更低，与错误正框/漏监督并存相容，却不能唯一识别因果。单种子不称跨种子稳定。

回源快检DOTA、FAIR、SODA五份报告均UNCHANGED/PASS，复用清单和摘要，无全集新解码/重哈希。十对数据集及HRSC val未发现精确编码重复，DOTA/SODA各自train-val原图ID无交叉；**重编码、裁幅和地理同景未排除**。FAIR37类到四类及TXT别名已核，other-vehicle保留ignore，空图保留；旧源train_only/val路径不存在，不能把标准总体当成已核源划分或冒用37类权重。HRSC test曾暴露对象数量的旧边界仍保留。

## 执行阶段

项目继续运行。r005已在46执行结束并由SERVER完成运行/产物审计，等待B/C按需独立科学复核；当前任务槽为空。原目标未达成，固定union学生路线失败；严格四类SODA主实验尚未开始，MS-01/MS-02未被证伪不等于成功。

本次执行收尾记录者：SERVER；2026-10-01。未续接B/C原线程或获得其对端回写，不称独立复核或跨端共识。

## 下一步与维护

r005已经表明当前固定union学习没有可靠双源增量。停止继续扫描union门槛、普通后处理或无依据的框数平衡；后续机制须用合法无标签依据同时处理错误正框与漏监督，并直接相对r005 FAIR/union学生终点检验，而不是只优化冲突率或候选潜力。

三臂都含DOTA初态知识，“FAIR监督学生”不是纯FAIR初态对照；本轮不分离标签数量与互补因果，不替代严格四类SODA主实验。FAIR四类教师/源划分与SODA正式评估条件仍保留，暂不先花约18 GPU小时补源模型；新机制尚未被证明。后续MS-02和SODA不自动启动。

当前不自动启动后续SODA/MS-02训练。更新仍沿现有任务/进展规则，不增审批或状态。

## 证据

[完整结果](https://github.com/ziyu24/cqc_P29/blob/c283314cd4fc1f94252d7bbea538e5c6703566bc/lab/result.md#r004)；[当前取舍](https://github.com/ziyu24/cqc_P29/blob/c283314cd4fc1f94252d7bbea538e5c6703566bc/lab/discussion.md)；[真实执行](https://github.com/ziyu24/cqc_P29/blob/c283314cd4fc1f94252d7bbea538e5c6703566bc/configs/r004.audit.json)；[独立监督/梯度复核](https://github.com/ziyu24/cqc_P29/blob/c283314cd4fc1f94252d7bbea538e5c6703566bc/configs/r004.review.json)；[输入清单审计](https://github.com/ziyu24/cqc_P29/blob/c283314cd4fc1f94252d7bbea538e5c6703566bc/configs/input_audit.json)；[SODA真实读取验证](https://github.com/ziyu24/cqc_P29/blob/c283314cd4fc1f94252d7bbea538e5c6703566bc/configs/soda_input_check.json)；[图像独立入口](https://github.com/ziyu24/cqc_P29/blob/c283314cd4fc1f94252d7bbea538e5c6703566bc/src/soda_unlabeled.py)。

r005收尾：[完整结果](https://github.com/ziyu24/cqc_P29/blob/ec3e70810e425f7bde0d0c6a34b8fc3ffe6bfbb6/lab/result.md#r005)、[执行与产物审计](https://github.com/ziyu24/cqc_P29/blob/ec3e70810e425f7bde0d0c6a34b8fc3ffe6bfbb6/configs/r005.audit.json)、[失败边界](https://github.com/ziyu24/cqc_P29/blob/ec3e70810e425f7bde0d0c6a34b8fc3ffe6bfbb6/lab/failed_methods.md)、[当前取舍](https://github.com/ziyu24/cqc_P29/blob/ec3e70810e425f7bde0d0c6a34b8fc3ffe6bfbb6/lab/discussion.md)。
