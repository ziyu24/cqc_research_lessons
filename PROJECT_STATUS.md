# 项目状态总表

更新日期：2026-09-24。维护者：B。本页是项目级状态的统一入口，每个精确仓库名只占一行。

## 当前口径

- 按用户2026-09-19明确指定：**P12、P18–P23、OrientDA、orientbench正在运行；其余既有科研项目均登记为失败。**“正在运行”表示项目仍在推进，不是本次逐台核验GPU进程的结论。
- 本次初始化共69项（含历史科研计划/占位仓库）：9项正在运行，60项失败。基础设施、知识库、第三方上游、学习与非科研仓库不列入科研成败统计。
- “失败”按用户的项目结项/汇报口径填写，不等于所有方法、原科学命题均被证伪；已验证正结果、局部失败与未知仍以对应教训和来源证据为准。不得以“尚未证伪”把失败改成运行或成功。
- 下表写最初科学问题，不用后来诊断、替代路线或最近一轮任务覆盖它；后续获授权的变化另记在来源项目。问题据本库已登记的早期研究问题及来源README/讨论页提炼，本次不重新裁决各项目的科学成败。未立题或缺原始文字时如实注明，不凭仓库名推测。
- 本次登记不启动、停止、清理或恢复维护任何项目；旧项目的停止维护边界继续有效。`INDEX.md`里的“已登记”只指教训收录，不是本页的项目状态。

## 已有研究问题的项目

本表“初始化依据”统一为用户本次状态指令；最后一列给出原始问题的文字来源。后续结束时，由来源项目将该列补为结束原因及已推送的结果证据，同时保留问题来源。

| 项目／精确仓库 | 最初科学问题 | 当前状态 | 更新日期 | 结论／依据 |
| --- | --- | --- | --- | --- |
| P1（`cqc_P1`） | 遥感旋转检测是否依赖上下文捷径，以及这种依赖如何影响分布外泛化并与竞争解释区分。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_P1/blob/f17d92fc94897cc39549053ee0a41e409cd7bb96/README.md)。 |
| P2（`cqc_P2`） | 旋转检测基准是否有效测量了宣称的能力，角度定义、样本分配与排行榜是否可比。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P2.lessons.md)。 |
| P3（`cqc_P3`） | 遥感目标检测中哪些候选科学问题兼具新颖性、可识别性和可验证的竞争解释。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P3.lessons.md)。 |
| P4（`cqc_P4`） | 有限空间支持是否需要面向目标方向的频域自适应感受野。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P4.lessons.md)。 |
| P5（`cqc_P5`） | 不同来源只提供mask、OBB、HBox或point时，如何学习统一的旋转检测目标。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P5.lessons.md)。 |
| P6（`cqc_P6`） | 旋转检测器能否按任务条件进行容量专门化，尺度与方向扰动能否揭示可利用的组件机制。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P6.lessons.md)。 |
| P7（`cqc_P7`） | NuWa/DeiT-Tiny在CIFAR-10类别2/8任务中，输出头掩码是否会颠倒20%与40%剪枝的精度判断。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P7.lessons.md)。 |
| P8（`cqc_P8`） | 采集条件与旋转几何能否解释压缩/量化损伤，并形成推理时可用的旋转检测压缩方法。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P8.lessons.md)。 |
| P9（`cqc_P9`） | 能否擦除非目标类别身份信息而保留目标召回，实现按类别层级的任务特异旋转检测压缩。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P9.lessons.md)。 |
| P10（`cqc_P10`） | 样本与非目标标签的价值是否随模型容量和监督用途变化，能否联合选择训练内容与最终网络。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P10.lessons.md)。 |
| P11（`cqc_P11`） | 真实遥感成像处理链中，哪些产品处理对检测有条件收益，能否跨卫星选择满足漏检风险约束的最低成本路径。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P11.lessons.md)。 |
| P12（`cqc_P12`） | 相邻遥感目标在模糊与采样退化下，是否存在超出匹配孤立目标普通漏检的实例分解错误。 | 正在运行 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P12.lessons.md)。 |
| P13（`cqc_P13`） | 查询同时参与参考对齐与分类是否给错误类别带来乐观拟合，空间交叉拟合能否改善细粒度旋转目标识别。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P13.lessons.md)。 |
| P14（`cqc_P14`） | 原生高分辨率PAN与较粗MS联合检测时，无法分清实例的MS观测能否提供组级语义约束，同时保持逐实例检测。 | 失败 | 2026-09-19 | 用户要求结束项目；固定组级代理与相对光谱传播均未达预定联合门，有限PAN/MS正证据保留，原命题未被完全证伪。[结束记录](https://github.com/ziyu24/cqc_P14/blob/0414b3addbcd30f2093f9a7869c617f8d6308a31/lab/discussion.md)。 |
| P15（`cqc_P15`） | 检测器对象错误历史能否在当前难度之外预测再次训练的泛化收益，并改善计入观测成本的等时间检测精度。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P15.lessons.md)。 |
| P16（`cqc_P16`） | Impostor式局部图像编辑能否提供可信检测监督，服务不完整标签学习与专用检测轻量化。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_P16/blob/60e4cc731bddb61726679a0575f682f42ec48868/README.md)。 |
| P17（`cqc_P17`） | 能否预测图像编辑相对原图续训的检测收益与能力退化，并据训练阶段、时长和预算作编辑决策。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P17.lessons.md)。 |
| P18（`cqc_P18`） | PWOOD在DOTA-v1.5、10%水平框标注的部分弱监督旋转检测协议下，作者权重与独立完整训练能否复现。 | 正在运行 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P18.lessons.md)。 |
| P19（`cqc_P19`） | 少量图像仅给已知类Point/HBox、其余无标签时，如何检测已知/未知OBB、区分难已知与新类，并在弱标签揭示后增量学习。 | 失败 | 2026-09-20 | 固定同源外部对象正支持及固定候选冻结排序均未过低误报投入门槛；[来源结果](https://github.com/ziyu24/cqc_P19/blob/3be33d61f8c06ec1400d7fd4460f9132b716374e/lab/result.md)。 |
| P20（`cqc_P20`） | 稀疏已知类Point/HBox与大量无标签图像能否支持已知/未知OBB检测及少量新类弱标签下的增量学习。 | 正在运行 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P20.lessons.md)。 |
| P21（`cqc_P21`） | 部分图像只提供逐类完整人工数量、其余无标签时，能否学到多实例旋转框检测。 | 正在运行 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P21.lessons.md)。 |
| P22（`cqc_P22`） | 少量图像中只有部分实例带Point/HBox且位置或类别可能出错、其余图像无标签时，如何学习OBB检测。 | 正在运行 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_P22/blob/52f950da077023611b84d7ce43c682ed1728417a/README.md)。 |
| P23（`cqc_P23`） | 少量图像保留每个实例、但Point/HBox可能出错，结合大量无标签图像如何学习OBB检测。 | 正在运行 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_P23.lessons.md)。 |
| P24（`cqc_P24`） | 在部分弱监督旋转检测中，区分继续学习、刷新监督与暂时跳过的边际收益，降低达到同等检测质量的总计算成本。 | 正在运行 | 2026-09-24 | 成熟状态三动作及图像敏感性已核验：逐一删图排序不变，配对整图重采样范围跨零，不能判训练稳定性。用户已授权夜间扩充，较早同12800父态新增四臂补齐教师来源×计算量及关闭控制，旧半量复用；新任务尚无结果，三条教训不变。自适应路线尚未实现，原同质量总成本目标未达成。[原问题与计划](https://github.com/ziyu24/cqc_P24/blob/628c099e130929ae218317d453b76a5724eb6cee/lab/discussion.md)；[已有证据](https://github.com/ziyu24/cqc_P24/blob/628c099e130929ae218317d453b76a5724eb6cee/lab/result.md)。 |
| P25（`cqc_P25`） | 没有完整OBB标注源域，仅有部分HBox或Point图像与完全无标签图像，如何学习对训练不可见目标域泛化的旋转检测器。 | 正在运行 | 2026-09-24 | 用户已授权继续研究。共同初态的普通多尺度续训获得源/诊断域有限正收益，完整PR及覆盖已回读；L/U分流消融已冻结但未执行。目标未达成，新机制、跨种子和严格盲域未验证；旧占位失败不代表原命题被证伪。[问题与授权](https://github.com/ziyu24/cqc_P25/blob/30a8eef387808eca66b9d58eceef085bfcc1628e/lab/discussion.md)、[已核结果](https://github.com/ziyu24/cqc_P25/blob/f2d3c0a1755a854c2b63715a61adf0841806c93d/lab/result.md)。 |
| P26（`cqc_P26`） | 待用户确定科学问题、核心路线和成功标准。 | 已创建 | 2026-09-23 | 按用户要求初始化；尚未下达科研任务，无实验结论。[初始项目说明](https://github.com/ziyu24/cqc_P26/blob/a0d25d02fffd012d445266236b40ead808301afa/README.md)。 |
| P27（`cqc_P27`） | 待用户确定科学问题、核心路线和成功标准。 | 已创建 | 2026-09-23 | 按用户要求初始化；尚未下达科研任务，无实验结论。[初始项目说明](https://github.com/ziyu24/cqc_P27/blob/7d19a91c41b11e9ab586b0ecd8b36f1d3a19a02b/README.md)。 |
| P28（`cqc_P28`） | 待用户确定科学问题、核心路线和成功标准。 | 已创建 | 2026-09-23 | 按用户要求初始化；尚未下达科研任务，无实验结论。[初始项目说明](https://github.com/ziyu24/cqc_P28/blob/56009d13f2844ae585120ded97e5a4d550888e8c/README.md)。 |
| P29（`cqc_P29`） | 待用户确定科学问题、核心路线和成功标准。 | 已创建 | 2026-09-23 | 按用户要求初始化；尚未下达科研任务，无实验结论。[初始项目说明](https://github.com/ziyu24/cqc_P29/blob/585430d995912782db7c90be462152d7b7453893/README.md)。 |
| P30（`cqc_P30`） | 待用户确定科学问题、核心路线和成功标准。 | 已创建 | 2026-09-23 | 按用户要求初始化；尚未下达科研任务，无实验结论。[初始项目说明](https://github.com/ziyu24/cqc_P30/blob/4afdb95df3ffeeb6302c3bfccf1bf201f777bab7/README.md)。 |
| bgc_obb（`bgc_obb`） | 弱监督旋转检测中，中心与形状参数块的几何梯度冲突能否预测定位错误，并用于实例重加权。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/bgc_obb.lessons.md)。 |
| cerq（`cerq`） | 不重训检测器时，真值栅格支持、边界与中心证据能否揭示旋转框质量重排空间。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cerq.lessons.md)。 |
| cqc_naood（`cqc_naood`） | 旋转框中心、尺度、角度的真值替换及交互能暴露多少可信的AP提升空间，能否转化为部署可见特征的重排收益。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_naood.lessons.md)。 |
| cqc_T1（`cqc_T1`） | 只改变超大遥感图像的切片网格原点，同一物理目标的检出、类别和几何为何变化，如何在保留检测能力和预算下减小变化。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_T1.lessons.md)。 |
| cqc_T2（`cqc_T2`） | 训练状态与历史能否预测样本难度、类别或分辨率调整的后续收益，并在等成本和新轨迹上改进动态训练控制。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/cqc_T2.lessons.md)。 |
| D7_pcp_obb_foundation（`D7_pcp_obb_foundation`） | 角度π周期、近方形弱可识别及图内目标相关时，如何为旋转框方向构造有限样本覆盖的预测弧与选择性拒绝。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/D7_pcp_obb_foundation.lessons.md)。 |
| DG-OBB（`DG-OBB`） | 多尺度训练能否缓解数据集、尺度和细长形状域差，是否需要比简单缩放更复杂的旋转检测域泛化机制。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/DG-OBB.lessons.md)。 |
| dgobb-synthprobe（`dgobb-synthprobe`） | 源域与目标域的尺度关系能否决定跨域旋转检测多尺度训练的方向。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/dgobb-synthprobe.lessons.md)。 |
| GeoPDE-OBB（`GeoPDE-OBB`） | 特征结构张量的局部方向与定向各向异性扩散能否改善旋转目标几何表征。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/GeoPDE-OBB.lessons.md)。 |
| GeoStructDOTA（`GeoStructDOTA`） | 地图、DSM及语义分割等地理结构先验能否为旋转目标检测提供有效弱监督。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/GeoStructDOTA.lessons.md)。 |
| orientbench（`orientbench`） | 旋转检测的方向质量是否被框指标掩盖，方向测量能否为独立下游决策提供可迁移增量价值。 | 正在运行 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/orientbench.lessons.md)。 |
| OrientDA（`OrientDA`） | 源域有旋转框、目标域只有水平框时，如何实现弱监督跨域旋转目标检测适应。 | 正在运行 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/OrientDA.lessons.md)。 |
| pcp-obb（`pcp-obb`） | 如何给匹配旋转框构造尊重π周期、具有有限样本覆盖的角度集合，并检查边界与条件覆盖。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/pcp-obb.lessons.md)。 |
| pcp-obb-acquisition-risk（`pcp-obb-acquisition-risk`） | 少标签或无标签时，能否用多帧、多检测器或采集元数据控制采集批次的旋转检测风险。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/pcp-obb-acquisition-risk.lessons.md)。 |
| pcp-obb-beyond（`pcp-obb-beyond`） | 切片相关性和NMS阈值变化破坏交换性时，旋转框共形覆盖能否保持稳健或得到校准修正。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/pcp-obb-beyond.lessons.md)。 |
| pcp-obb-score-study（`pcp-obb-score-study`） | 旋转框训练几何能否成为兼顾合法覆盖、短角度弧及最差条件覆盖的共形分数。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/pcp-obb-score-study.lessons.md)。 |
| SynDOTAForge（`SynDOTAForge`） | 能否生成可控旋转框、俯视几何和真实遥感外观的合成DOTA数据，用于低数据检测与机制研究。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/SynDOTAForge.lessons.md)。 |
| TAOS（`TAOS`） | 截断感知监督和融合能否在不损伤完整目标的前提下改善切片边界截断目标的旋转定位。 | 失败 | 2026-09-19 | 按用户指令登记；[问题来源](https://github.com/ziyu24/cqc_research_lessons/blob/1e30234490f59dce9ecc891067110252aa18c643/lesson/TAOS.lessons.md)。 |

## 历史科研计划与占位仓库

以下同样按用户指令登记为失败，不能把“计划开源”“占位”继续汇报为正在运行。逐库读取现有README后，仅3项存在可提炼的计划范围，其余没有明确科学问题文字；缺失项等待有原始材料时补充，不虚构实验失败原因。`cqc-P1`与`cqc_P1`是不同仓库。

| 项目／精确仓库 | 最初科学问题 | 当前状态 | 更新日期 | 结论／依据 |
| --- | --- | --- | --- | --- |
| `axial-conformal-inference` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/axial-conformal-inference/blob/27ffcb628fdb4565651e2179e516f378953f9e61/README.md)。 |
| `Censored-OBB-Base` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/Censored-OBB-Base/blob/07ec912fa7a730c9ec5eacab1f4e95988fa4b7c6/README.md)。 |
| `CensoredTile-OBB` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/CensoredTile-OBB/blob/2f22a527b303042024f883f6d0e9be97becd4225/README.md)。 |
| `cods-obb` | 计划构造旋转目标检测的共形预测集合；只有占位范围，未形成已验证研究。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/cods-obb/blob/3298ac026dee6a94819bb7ab5752627b1fa23370/README.md)。 |
| `conformal-mmrotate` | 计划为MMRotate实现周期共形预测、条件校准与旋转IoU风险校准封装；尚为工具计划。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/conformal-mmrotate/blob/b55f7a4873d6d57130b8ba98083893a131971419/README.md)。 |
| `cqc-P1` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/cqc-P1/blob/3259108256af0949f17e699991a32a9c63a05704/README.md)。 |
| `D17_FragmentStitch-OBB` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/D17_FragmentStitch-OBB/blob/73d025241602a7a280652b003c2959c000ad8390/README.md)。 |
| `D17_TileBoundary-OBB-Benchmark` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/D17_TileBoundary-OBB-Benchmark/blob/0964c97735d115d44aa90243002c9f3e09f0da59/README.md)。 |
| `DenseOBB-B1C3` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/DenseOBB-B1C3/blob/9566c7fa1b6184a5ffbe8b9924aadef82a4c6786/README.md)。 |
| `frozen-query-obb` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/frozen-query-obb/blob/c248ec3c00f159a1f71d8b85ae82c47ec5c9c7d6/README.md)。 |
| `geosense-obb` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/geosense-obb/blob/5baea7197fceb4cda88e9539f237f89d22e33a40/README.md)。 |
| `GeoSupport-OBB-LT` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/GeoSupport-OBB-LT/blob/21046132142c1756fdd9005463f0370567e983e6/README.md)。 |
| `HoML-OBB` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/HoML-OBB/blob/22aa31c9ff1764764634203fa1fa6f11695de074/README.md)。 |
| `iev-obb` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/iev-obb/blob/37e1018128a4834344529026bf6343b006dcb82d/README.md)。 |
| `kappagate-obb` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/kappagate-obb/blob/e8b55d090ce1f09c52e6f15a6285ef339a8477d3/README.md)。 |
| `longfpn-obb` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/longfpn-obb/blob/2818fb049abc0fbeb84384be44561bbb48b620cc/README.md)。 |
| `lspassign` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/lspassign/blob/636dc6b809366db901d09412fa2e7aec8e72cce0/README.md)。 |
| `mobiusobb` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/mobiusobb/blob/438a6ff190942824fc3116f3f6cf20a0d7995ef0/README.md)。 |
| `obb-input-aligned-distill` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/obb-input-aligned-distill/blob/1d12ca7b9f953d18b5c07cd31e565929f168c366/README.md)。 |
| `oriented-detection-risk-control` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/oriented-detection-risk-control/blob/db85aa22742f7afebbd748af80465700106397a7/README.md)。 |
| `OVShape-OBB` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/OVShape-OBB/blob/6cc6b8f31ae4d12600ac855dce271d65419f9f6a/README.md)。 |
| `pcb-obb` | 计划为光学遥感旋转框方向参数提供有限样本覆盖保证；尚无验证结论。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/pcb-obb/blob/8ac7244fe52e771042b7605c2606a1989b39fbe5/README.md)。 |
| `Phase-Tiny-OBB` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/Phase-Tiny-OBB/blob/0ce606acbdddda3564b783ba0bb1cb69fb29d813/README.md)。 |
| `retrieval-obb` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/retrieval-obb/blob/6813eccd5751e287c67bb6bb6798ed0aa969f986/README.md)。 |
| `SuppressionRank-OBB` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/SuppressionRank-OBB/blob/4cd3ebc41faffc33b5df28f6a467af1d27d33b4c/README.md)。 |
| `symq-obb` | 原始科学问题未载明：README仅有项目名或内部编号，不能据名称推断。 | 失败 | 2026-09-19 | 按用户指令登记；[已核README](https://github.com/ziyu24/symq-obb/blob/9ccf306deb645bf4859327380cb166e42d97af55/README.md)。 |

## 项目结束时怎么填写

1. **更新本项目这一行，不新增另一份状态表。**先拉取本库最新main，以精确仓库名定位；没有该项目行时补一行。保留原始科学问题，有原始材料才能补正，不能用后来的路线换掉它。
2. 先将来源项目的结果、主要失败和恢复入口提交推送。再填写本页的当前状态、更新日期、一两句结束原因，并链接来源提交中的`lab/result.md`或`lab/failed_methods.md`；“原目标是否达成、实际路线结果、原命题是否证伪”分别据实说清，不用内部运行器COMPLETE代替项目结论。
3. **项目结束而用户没有特别说明其他状态时，填“失败”。**成功或恢复运行等特别状态须有用户明确说明及相应依据；已有用户说明不重复申请。本次9项运行名单只是初始化快照，不是永远不能结束的白名单。
4. 本页只更新自己的项目行；可复用科学教训另按README原流程更新对应`lesson/`文件，不能把一条状态登记当作完整失败教训。
5. 提交推送本页并回读远端；并发修改时保留其他项目更新。推送失败如实报告“来源已结束，状态表尚未更新”，不得宣称登记完成。无需新增审批、锁、后台同步或运行状态机，也不为维护此表启动科研实验。

后续用户明确恢复或调整项目状态时，同样更新原行。旧状态和文字由Git历史保留，本页不追加聊天流水账。
