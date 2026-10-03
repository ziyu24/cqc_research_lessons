# P29 项目进展

## 最初科学问题

在光学遥感二维 OBB 离线域适应中，仅用两个源模型和无标注目标图像，能否把多源互补转化为单个同容量检测器的收益（MS-01）；额外开放一个源的完整标注数据时，能否获得超过普通源监督相加的收益（MS-02）。

## 核心进展

C已交付正式DOTA＋FAIR→SODA四类主实验，HRSC只保留已有探针，不再执行上版提议的整套HRSC开发训练。r006科学代码、实际输入准备和CPU集成已完成，SERVER已在46实际启动两卡训练。本轮独立补FAIR四类源，再检验普通可见源监督及第二教师的额外作用；不是已经实现新的质量学习方法，原项目目标仍未达成。

已有HRSC负结果保持：相同DOTA初态和预算下，union AP50/AP75为0.399136/0.291599，低于FAIR监督学生0.487296/0.333018和冻结FAIR教师0.506138/0.356322。r005执行完整、固定配方失败，不能外推为正式四类SODA或整个MS-01/MS-02已失败。

新的原因定位证据是：union删除375个原有FAIR训练伪框、纳入840个DOTA框，不能说只是增加互补。最终在IoU0.5相对FAIR监督学生新增11个正确匹配而丢35个，在IoU0.75新增22而丢51个。替换和补充没有分开干预，不能认定唯一因果；没有用train GT把被删或新增框判成对错。

## 服务器当前内容

SERVER于2026-10-01 17:06:47–17:49:35 UTC在46完成三臂：FAIR、union、DOTA伪标签监督；HRSC train436图，每臂实际两卡、12epoch/660优化步、同一初态、一个预定种子；固定epoch12后各评测181图/541GT。DOTA学生为0.323041/0.199333。总墙钟2568.738秒、1.42708 GPU小时。三项终点保存完整优化器/调度器恢复状态，均受保护，删除须用户明确授权。

C于2026-10-02 02:56:13 UTC在46完成r006真实输入CPU集成：SODA无标签窗口37980、DOTA训练15749、FAIR训练18207/源验证4660条均实际加载，四集真实首图变换成功；DOTA权重严格加载且tensor摘要一致。29项协议与原生CPU反例通过，其中包含真实两rank Gloo联合梯度与恢复检查。源码和证据已推送并同步46 Home，唯一任务为r006。本次C没有启动GPU训练或SODA实际评测；GPU首批、显存及吞吐待SERVER实测，不能把CPU检查称为训练成功。未重新清点整机其它项目负载。

SERVER于2026-10-02 04:50:58 UTC在46以同一r006、物理GPU 3/2实际启动。`cqc-run gpu-check`观察到两训练PID与两张预期卡完全匹配；两个rank均记录world size 2、seed 20261001、FAIR训练18207切片和相同初态摘要。首50 iter实际loss 0.8623、grad norm 2.5232，均为有限值；约0.402秒/iter。FAIR第1轮源val `fair/AP50=0.5353`，合法best及完整epoch1 resume已保存并受保护。

SERVER误把用户“抢占，启动”理解为可终止已有任务，于04:49:11 UTC通过`cqc-run stop`停止P23/r030；用户随后明确没有授权杀死别人的任务。P23当时状态已成`STOPPED`，不能把该操作说成正常暂停。用户要求“先暂停”后，SERVER于05:37:31 UTC只终止P29当前torchrun；r006 attempt为`FAILED`以保留同号续接资格，GPU 2/3均已释放。第2轮未完成部分不计结果。用户随后重新明确恢复P29/r006并指定46；SERVER于2026-10-02 23:56:08 UTC从epoch1完整恢复点同号续跑，物理GPU 2/3的两个训练PID已由`gpu-check`核为MATCH。该事件是执行解释错误，不改变科学目标或路线。

SERVER已完成FAIR源12轮训练，合法源验证最佳为epoch12、`fair/AP50=0.7235`；37980张目标图的DOTA、FAIR及union冻结伪标签也已全部生成。两位教师对固定SODA验证集的两rank推理和原生评分均已完整结束：DOTA教师AP50/AP75/mAP为0.532575/0.139914/0.230021，FAIR教师为0.365351/0.104736/0.159706，当前冻结DOTA教师明显更强；两者均覆盖576张原图并保存完整评测产物。首次写DOTA指标参数时仅因NumPy整数不能JSON序列化而退出，工程修复、完整产物检查及反例测试已提交推送，同源重算指标不变。2026-10-03 14:22:32 UTC，SERVER按用户指定在GPU 0/1同号续接。15:01 UTC又在相同两卡启动DOTA学生；两个训练rank经`gpu-check`为MATCH，world size 2、37980张输入、seed 20261001及初态一致，首50优化步约0.496秒/iter，loss 0.1477、grad norm 1.8767。15:05 UTC在已空闲的GPU 2/3并行启动独立FAIR学生；两rank同样经核为MATCH且输入、种子和FAIR初态一致，首50优化步约0.361秒/iter，loss 0.1003、grad norm 2.1374。两臂第1轮完整恢复点均已落盘，以上量均有限，没有终止或迁移其他项目进程。

## 核验说明

**已充分核验这轮限定开发结论。** C检查生成提交和源码/输入身份、双rank初终态、训练日志/学习率/更新步、checkpoint与评测一致性、436图伪标签全集和181图完整预测。独立多边形几何重算全部有效训练标签及六条PR；原NumPy同分排序下逐点与AP均吻合。本机另一NumPy同分顺序只产生约0.00002226的union AP50差，不影响裁决。当前配置仅在执行后加了权重保护，科学参数未改。

训练代码路径不读取目标XML，但没有操作系统文件访问跟踪；不把声明当取证。三臂都有DOTA初始化，FAIR监督学生不是纯FAIR初态单源模型。一个种子不说明跨种子稳定；替换和补充同时变化，不能把失败唯一归因于数量、噪声、背景或容量。完整低分候选下正确匹配减少，固定0.5分数下TP410→392、FP633→769，不能仅怪低分尾部。

原输入审计复用有效，本轮四项受影响数据源端快检均UNCHANGED，没有重切或重哈希图像全集。FAIR249组精确编码重复原图已绑定划分，全部16488原图/22867切片保留；train13190原图、val3298原图。不能把单纯原图ID划分当作去重；重编码、裁幅和地理同景仍未排除。FAIR source val的37个无效多边形显式排除并记数，保留原图全集。DOTA实际共同四类347188框，384677是16类总数，原教师四类过滤未改。

SODA适应使用1067原图/37980个raw无GT掩膜窗口；正式评估固定576原图/20549官方masked val切片、原生101点Small AP50/AP75，补报其他面积与逐类。训练/val原图无交叉，空预测仍计入总体。本次没有打开实际SODA训练或val GT；官方masked评估不代表raw部署。本轮比较后同一val不得再称未见盲测，test保持不访问。HRSC test曾暴露对象计数的旧限制保留。严格FAIR四类权重尚待训练，当前只有配置的独立ImageNet初始化核验。

## 执行阶段

项目继续运行，r006已按用户新指令在46恢复实际执行。r005已执行结束并由C独立复核；r006当前RUN为`RUNNING`，FAIR源训练、三套冻结伪标签和两位教师固定验证评测均已有完整证据。当前DOTA学生在GPU 0/1、FAIR学生在GPU 2/3各自实际两卡训练并已跨过第1轮恢复点；其余四个学生尚未训练，科学完成仍未知。原目标、正式主路线和单容量部署条件不变；教师差异或固定union探针失败均不等于整个问题被证伪。C交付段记录者为C，SERVER执行段记录者为SERVER；没有对端原线程回写，不称跨端共识。

## 下一步与维护

目前核心问题：HRSC异类别头单类探针不能回答共同四类SODA上的多源增量，也没有检验开放一个源真标签后另一个源是否仍有独立价值。核心问题解法：复用DOTA四类源，从ImageNet独立训练FAIR四类源，直接执行SODA主实验；源按本源合法val选best，目标各臂固定12轮，不能用早出的目标结果调参。

全部七项训练：FAIR源，以及SODA的DOTA单教师、FAIR单教师、双教师A、A加DOTA监督B_D、仅DOTA教师加同DOTA监督S_D、A加FAIR监督B_F。原HRSC学生不能当SODA基线复用。每项实际两卡、一个种子、12epoch；源27312优化步，学生各56976步。源分支额外batch8，不减目标batch8；一次联合反传/裁剪。B_D须胜A且胜S_D并超过强单源参照，才能支持隐藏FAIR信息有效，不能只把源GT修复坏A当多源成功。B_F含DOTA初态，方向边界如实报告。

训练原总估计294–442 GPU小时，加冻结前向、评估和首批余量合计324–487 GPU小时，均非硬时限。FAIR源训练已经完成；当前先并行完成两个源教师固定评测，再依既定顺序执行六个学生，每臂结束即固定评估，不按低分删臂或加种子。候选类别/旋转IoU质量学习仍是后续未验证假设，共同ROI、软蒸馏和IoU头本身已有前作；普通源监督结果不能冒充该方法成功。既有产物保护继续有效，当前FAIR best/resume及后续r006终点按配置保护。

## 证据

[完整结果](https://github.com/ziyu24/cqc_P29/blob/46b10fd7d63ac0dd2edc3cd06556e9a2cc2f29ef/lab/result.md#r005)、[C独立复核](https://github.com/ziyu24/cqc_P29/blob/46b10fd7d63ac0dd2edc3cd06556e9a2cc2f29ef/configs/r005.review.json)、[复核实现](https://github.com/ziyu24/cqc_P29/blob/46b10fd7d63ac0dd2edc3cd06556e9a2cc2f29ef/src/review_student_adaptation.py)、[当前科学判断与方案](https://github.com/ziyu24/cqc_P29/blob/066d6ffbbaf7312d87c76c23557ee9de25a78bf0/lab/discussion.md)、[SERVER执行审计](https://github.com/ziyu24/cqc_P29/blob/46b10fd7d63ac0dd2edc3cd06556e9a2cc2f29ef/configs/r005.audit.json)、[失败边界](https://github.com/ziyu24/cqc_P29/blob/46b10fd7d63ac0dd2edc3cd06556e9a2cc2f29ef/lab/failed_methods.md)。

[论文与代码核查](https://github.com/ziyu24/cqc_P29/blob/066d6ffbbaf7312d87c76c23557ee9de25a78bf0/doc/takeover-evidence.md)、[当前唯一任务](https://github.com/ziyu24/cqc_P29/blob/19333fa8b2e7aae45247f4aaf070e781aa536637/lab/sug.md)、[最新科学取舍](https://github.com/ziyu24/cqc_P29/blob/19333fa8b2e7aae45247f4aaf070e781aa536637/lab/discussion.md)、[全部训练清单与预算](https://github.com/ziyu24/cqc_P29/blob/19333fa8b2e7aae45247f4aaf070e781aa536637/doc/server-execution.md)、[46真实CPU集成证据](https://github.com/ziyu24/cqc_P29/blob/19333fa8b2e7aae45247f4aaf070e781aa536637/configs/r006.preflight.json)、[正式两卡科学入口](https://github.com/ziyu24/cqc_P29/blob/19333fa8b2e7aae45247f4aaf070e781aa536637/src/run_main_experiment.py)。

[启动时科学代码](https://github.com/ziyu24/cqc_P29/tree/c41d7ddaee1529d12163d9a19062373220ed4f00)、[修正后的恢复入口](https://github.com/ziyu24/cqc_P29/blob/86db4fb96df76d39d4c34e0104108f6c54a898a1/configs/r006.recovery.json)。

[评测产物序列化修复与完整性检查](https://github.com/ziyu24/cqc_P29/commit/817243f4a1dd34f34df04a66c6e1673e3d8a76c0)。
