# P27 项目进展

## 最初科学问题

类别集合不一致、重叠关系未知时，能否利用有标注源域与无标签目标域改善共享类别的旋转目标检测。

## 核心进展

C已完成固定语义秩门的独立复核：相同79,382个真检出下，语义秩门少1,584个私有相关误报，却多8,303个其他误报，净增6,719个误报；总体AP50由52.062%降至47.083%。额外拒识信息存在，但当前乘法破坏了类内检测排序，原目标未达成，可靠兼容解法尚未找到。

高召回正信号仍真实存在：全共享79,382 TP处，ordinary/源文本秩门/TASC秩门私有FP为7,607/8,566/6,023；大车1,396 TP处为7,667/7,617/5,724，大车AP50升至19.331%。因此r015证明“有额外信息”，r016证明“当前全局秩乘法不能保住总体排序”；两者不矛盾，项目原始目标仍未达成。

C在SERVER审计基础上复核r016完整经验秩、分数乘积、曲线和判据，并用独立101点精度实现精确重算21个逐类AP50，三臂总AP50最大误差1.11e-16。137,251个TP/private-FP结果不变的检测ID中，储罐TP对其余FP的AUC由0.90479降至0.59942，表明正确框也被类内误压；固定集合且无新截断时，按类乘正常数不能改变该类AP。这不识别唯一表征或训练根因，其余FP也不能直接称为背景或定位错误。

此前冻结DINO区域特征加源类别读出已完整执行并经C独立复核：总体AP50从52.062%升至52.656%，但大车从16.138%降至14.537%，保住同样真检出时私有误报增加。这个固定源读出候选失败，与当前目标发现语言信号的正结果并不矛盾：两者使用的信息条件不同。

新增缓存诊断将问题收紧：固定原检测身份的大车TP/私有误报上，DINO接受分数自身AUC仅0.47903，私有误报的接受度中位数反而更高；没有证据仅靠改乘法或阈值挽回。源val读出有效，但源其他类/背景与目标已被检测器接受的私有难例不同，不能据AUC差唯一识别域移位。可靠解法尚未找到。

累计正结果保留：普通DA相对source-only有正迁移，IDSA有小幅正差但指定候选位置必要性未获支持；固定KLD提高AP50却降低严格IoU。UniOT固定适配连源检测都明显下降，终点梯度复算不支持共同持续冲突；DPA有总体AP和聚合曲线局部正差，但大车未改善；OpenDet固定适配的性能与拒识联合条件也失败。各结论只约束实际配置，项目仍运行。

## 服务器当前内容

SERVER于2026-10-03 14:31—15:06 UTC在46完成r016，配置选择物理GPU3/2；C于16:01—16:06 UTC只读回核正确仓库、实际产物和保护实体。两个rank实际处理61,609个校准区域与184,159个验证候选，CUDA张量代码路径、各22.09 MiB非零峰值及分工缓存支持真实双rank CUDA计算；但日志UUID来自CUDA_VISIBLE_DEVICES环境串，不是独立设备观测。启动和结束外部快照均为`UNOBSERVED`，缺少短评分阶段的历史PID→UUID MATCH，物理卡外部观测核验不完整。随后CPU完成两项全量原生AP重匹配。评分零目标标签、零优化步、零新编码器前向或搜索，worker已退出；不为补快照重跑已有效科学产物。

C于2026-10-03 13:53—13:54 UTC只读回核46的正确仓库、实际运行根、六阶段双rank/PID—GPU UUID和所有候选身份，相关worker已退出；r015完整执行且诊断通过，已复核。目标发现中心与完整轨迹新增为受保护下游依赖，删除须用户明确授权。当时已交付r016代码、固定配置及反例检查；这是历史交付记录，后续实际完成和C复核以上述最新记录为准。

SERVER于2026-10-03 09:37—12:41 UTC在46物理GPU2/3完成固定语言语义任务。首次命令在GPU计算前因默认PyPI镜像TLS失败；固定版本依赖改从官方PyPI装入既有`mr`环境后同号续接，不改变科学输入或复算不存在的有效GPU步骤。有效尝试六个阶段均有两rank进度和PID—双GPU UUID `MATCH`，墙时3.073小时；计入失败attempt共约6.154 GPU小时。

完整执行覆盖target train 1,067原图/37,980切片和target val固定预测576原图/20,549切片；编码67,191个文本、12,094,380条提示，完成2,000次离散坐标更新并冻结184,159个验证候选的两套分数。目标train加载框数0，test未访问，零优化步。当前worker已经退出，但诊断完成由覆盖、冻结输出、联合裁决及独立核验共同证明，不由退出码单独证明。

SERVER已在46完成r014两项固定读出，各12轮、2,304步、单种子、真实两rank；完整目标val为576原图/20,549切片。用户指定迁卡后，源train合法复用了修复后旧卡生成的11,900切片，同绑定新增3,849切片；源val、两读出及目标val在迁卡后完成。最终命令2026-10-03 07:01 UTC结束，含失败与迁卡前尝试累计约11.497 GPU小时。

C于2026-10-03 07:49—08:04 UTC只读核验正确仓库、实际产物、训练/前向进度与日志；观察时原训练worker已退出。r014科学执行结束且已复核。旧普通DA best与两个读出final实体和保护配置有效，均受保护，删除须用户明确授权；大型缓存和模型仍在原项目运行根。

首轮退化parent修复保留候选及原几何，仅显式置零DINO特征；不同旧绑定缓存未混用。源train最后一次退化计数1仅涵盖新增部分，不是全量；完整源train/val零特征347/95全部是源背景，但零特征不等于退化几何。此更正不改变候选失败。

## 核验说明

原SERVER审计复核精确manifest/加载覆盖、原图合并与两级NMS/哈希采样、全部区域/文本特征、评分身份、完整曲线及裁决。C追加从完整冻结向量按独立float64公式复算两分数，最大绝对差约6.34e-6/3.75e-5，与保存GPU FP32结果在数值容差内一致；全部曲线逐项相等。按种子重建2,000次抽样/候选流及状态，所选词均合法，源槽保护有效、K最低14。没有重新计算每次候选目标值，不能称重新优化搜索。复用未变的输入与NMS绑定证据，没有新图像前向或训练。

审计确认三种分数均精确达到全共享79,382 TP及大车1,396 TP。UniMS相对ordinary在预定高召回共同范围的全共享4,173点、大车74点全部私有FP更少；相对MS-s分别4,150点和74点也全部更少，不是单一锚点或并列拆分造成。验证有6个无效区域，r015按固定协议保留身份且两种分数置零；r016明确这些没有可用语义，权重为1，不能把占位值当测量。

充分核验执行完整和固定裁决：全源缓存的tile/parent/label身份、两臂特征哈希、类数及加载覆盖与训练报告完全一致；读出完整更新、优化器及双rank RNG、五个末次阶段的PID—双GPU UUID匹配已核。目标分数乘积、语义数组全部裁决和拒识曲线重算一致，复用哈希绑定的原生AP及一对一匹配输出。没有重复图像前向、全量IoU或test，也没有新训练。

固定79,382共享TP处，原分数/ROI/DINO私有FP为7,607/7,679/7,935；固定1,396大车TP处为7,667/7,693/7,871。各评分保留原命中83,560个GT身份，但ROI/DINO各有2个TP检测布尔值变化，不能把GT身份不变说成TP框身份不变。完整大车曲线仍有7个同TP点DINO私有FP更少，保留局部正差而不改预定高召回裁决。

新增核验：r016源文本/TASC分别改变12/14个TP检测身份、1/2个ignore身份和14/16个GT分配，命中GT集合均无增减。完整经验秩、6个无效区域门值1、float64乘积、全部曲线与原判据再次复算一致；另以独立计数核257个固定身份位置。三臂21个逐类AP50独立复算逐项误差0，三臂总AP50最大误差1.11e-16，几何面积精度变化引起Small边界成员变化为0。原科学源码和评分未改；r002 ordinary best、r014两份final和r015 discovery四份保护实体SHA均匹配登记，删除须用户明确授权。定向测试61项通过、1项按环境跳过。

核验足以接受固定接法失败及类内排序损伤；当前缓存已经回答最有判别力问题，不再追加诊断。未重算IoU，AP75/AP50:95复用绑定原生结果，没有称为独立复算；历史PID→UUID MATCH缺失，不能称物理卡外部核验完整。仍无HBB、官方遮罩SODA或跨种子证据，16个发现槽不等于16个真实类别。

## 执行阶段

r016于2026-10-03 15:06 UTC在46科学执行结束，C于16:01—16:06 UTC完成执行与保护复核，随后完成AP50与类内排序复算；固定接法联合判据失败。sug为空，没有r017，没有新增训练；项目仍在运行，原始目标未达成。此前r015诊断阳性继续保留。

## 下一步与维护

固定全局经验秩乘法按原判据停止：拒识阳性不足以抵消其他错误排序损失，不扫描融合、词表、温度、阈值、幂次、类别映射、校准或追加训练，也不把同一误抑制TP的门搬入loss就称解决。下一核心方向是区分类别语义证据与检测质量，但尚无可靠且信息条件兼容的解法；已查公开论文和作者代码只提供候选依据，不构成新任务。若改路线，须先明确新假设、信息条件、必要对照和成功标准，再取得用户授权，本次未编派下一实验。

原目标、DOTA→SODA无遮罩输入、AP50主指标和不默认增加unknown输出均未改变。当前无SERVER科学任务，不以局部正信号改写失败，也不把本接法失败扩大为全部语言语义失败。

记录者：C；更新日期：2026-10-03 PDT。保留SERVER执行事实及此前C有效核验，不冒充跨端共识。动作执行者按[主动更新约定](README.md)在真实事件发生时维护本页。

## 证据

[C完成复核与科学边界](https://github.com/ziyu24/cqc_P27/blob/a5439e31c137ce77044ea12e0ceec49d643032d8/lab/result.md)；[执行与四保护实体核验](https://github.com/ziyu24/cqc_P27/blob/a5439e31c137ce77044ea12e0ceec49d643032d8/doc/r016_execution_review.json)；[21项逐类AP50独立复算](https://github.com/ziyu24/cqc_P27/blob/a5439e31c137ce77044ea12e0ceec49d643032d8/doc/r016_metric_review.json)；[私有及其他FP与类内排序诊断](https://github.com/ziyu24/cqc_P27/blob/a5439e31c137ce77044ea12e0ceec49d643032d8/doc/r016_signal_review.json)；[下一机制与停止边界](https://github.com/ziyu24/cqc_P27/blob/a5439e31c137ce77044ea12e0ceec49d643032d8/lab/discussion.md)。无新训练、前向、评分或IoU重算。

[r016完成结果与失败边界](https://github.com/ziyu24/cqc_P27/blob/c6e34687e8f82217f245cb8e5aac9d7959d13d85/lab/result.md)；[独立复算证据](https://github.com/ziyu24/cqc_P27/blob/c6e34687e8f82217f245cb8e5aac9d7959d13d85/doc/r016_evidence.json)；[只读复算入口](https://github.com/ziyu24/cqc_P27/blob/c6e34687e8f82217f245cb8e5aac9d7959d13d85/src/review_r016.py)；[固定协议](https://github.com/ziyu24/cqc_P27/blob/c6e34687e8f82217f245cb8e5aac9d7959d13d85/configs/r016.json)。完整预测、原生匹配、曲线和日志留在46项目运行根。

[C完成复核与保护](https://github.com/ziyu24/cqc_P27/blob/09d482d8bb6de3069dcadfc8b2d3f4d218d34b25/lab/result.md)；[独立公式/曲线复算](https://github.com/ziyu24/cqc_P27/blob/09d482d8bb6de3069dcadfc8b2d3f4d218d34b25/doc/r015_completion_review.json)；[实际执行复核](https://github.com/ziyu24/cqc_P27/blob/09d482d8bb6de3069dcadfc8b2d3f4d218d34b25/doc/r015_execution_review.json)；[搜索轨迹边界](https://github.com/ziyu24/cqc_P27/blob/09d482d8bb6de3069dcadfc8b2d3f4d218d34b25/doc/r015_mechanism_review.json)；[当时交付的任务](https://github.com/ziyu24/cqc_P27/blob/09d482d8bb6de3069dcadfc8b2d3f4d218d34b25/lab/sug.md)；[固定推理入口与检查](https://github.com/ziyu24/cqc_P27/blob/09d482d8bb6de3069dcadfc8b2d3f4d218d34b25/doc/text_semantics_execution.md)；[原生匹配CPU反例](https://github.com/ziyu24/cqc_P27/blob/09d482d8bb6de3069dcadfc8b2d3f4d218d34b25/doc/r016_native_cpu_review.json)。

[固定语义信号结果与边界](https://github.com/ziyu24/cqc_P27/blob/ed4ac503b35041a26f87baddebe80f38446f4020/lab/result.md)；[完整审计摘要](https://github.com/ziyu24/cqc_P27/blob/ed4ac503b35041a26f87baddebe80f38446f4020/doc/r015_evidence.json)；[可重跑只读审计](https://github.com/ziyu24/cqc_P27/blob/ed4ac503b35041a26f87baddebe80f38446f4020/src/review_r015.py)；[恢复入口](https://github.com/ziyu24/cqc_P27/blob/ed4ac503b35041a26f87baddebe80f38446f4020/configs/r015.recovery.json)。原始分块、日志和大模型产物留在来源项目运行根，不复制到公共库。

[本次结果、纠正与保护产物](https://github.com/ziyu24/cqc_P27/blob/f8c185198e9b1fb29ad55319977382307d900e24/lab/result.md)；[完整完成复算](https://github.com/ziyu24/cqc_P27/blob/f8c185198e9b1fb29ad55319977382307d900e24/doc/r014_completion_review.json)；[接受信号及全曲线诊断](https://github.com/ziyu24/cqc_P27/blob/f8c185198e9b1fb29ad55319977382307d900e24/doc/r014_signal_review.json)；[原始论文、代码及下一路线边界](https://github.com/ziyu24/cqc_P27/blob/f8c185198e9b1fb29ad55319977382307d900e24/doc/method_transfer_review.md)；[当前讨论与授权范围](https://github.com/ziyu24/cqc_P27/blob/f8c185198e9b1fb29ad55319977382307d900e24/lab/discussion.md)。

[SERVER完成证据及恢复入口](https://github.com/ziyu24/cqc_P27/tree/4daba29f7bf996ef013042a04e1787171409325a)；[此前交付、实际启动、工程修复及旧路线复核历史](https://github.com/ziyu24/cqc_research_lessons/blob/c425c63/progress/cqc_P27.md)；[已登记科学教训](../lesson/cqc_P27.lessons.md)。原始数据、模型和日志留在来源项目，不复制至公共进展页。
