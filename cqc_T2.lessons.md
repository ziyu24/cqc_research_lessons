# cqc_T2 科学问题与失败教训

审计基线：当前主线 `ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e`。全部历史执行分支均已确认是该主线祖先；本文以当前主线中的最终决策和机器可读结果为准，不把较早的阶段性 GO、运行状态或内部任务编号当成最终科学结论。

快速阅读路径：先读“项目研究什么”→“教训一、四、六、七、九”→“方法族停止索引”。

## 项目研究什么

T2 实际包含两个独立的高风险问题，不能用一条“训练与推理优化”笼统概括：

1. **动态训练控制**：从训练中途的模型状态出发，改变样本难度、类别构成或输入分辨率，能否比正常训练获得稳定的后续精度收益；训练状态和历史信号能否预测当下应选择哪种 action，并在等训练步数、等墙钟和新轨迹上泛化。
2. **分区透明执行**：对固定的大图旋转检测 DAG，能否改变空间分块、执行顺序和张量驻留位置，同时保持母图坐标中的最终规范检测集合不变，并自动满足 GPU 显存预算和可接受延迟。

## 领域位置与当前结论

按损失、难度或不确定性动态选择训练样本并不是 T2 首次提出，已有 online batch selection、Active Bias 和 data-driven curriculum 等工作。精确 tile/out-of-core 推理与 DNN tile compiler 也已有公开研究。T2 可能有区分度的对象，分别是“在旋转检测训练状态上用成对反事实 replay 估计 action 的 baseline-relative utility”，以及“把旋转检测候选、RoI、top-k、NMS 等全局集合运算纳入 canonical final-set equality 契约”；仓库没有证据证明这两种表述已经获得同行共同体认可。

- **事实**：早期开发轨迹存在动作差异和可预测 headroom，但历史状态模型未达到绝对决策门槛；最终冻结的独立轨迹上，开发期最优 action 由正转负，等墙钟结果也没有形成跨阶段、双 replay 的稳定正收益，动态控制路线最终停止。
- **事实**：局部算子和合成 FPN 子图通过了精确性测试，但当时没有真实检测器的分区运行。补齐 RTMDet 的四个全局 ChannelAttention barrier 后，区域 neck 的 shape-dependent FP32 convolution 首先失配，最终候选与检测集合仍不相等。
- **事实**：最终 RTMDet 分区执行把 P1854 峰值显存从 6.674 GiB 降到约 1.8 GiB，但在 decode/NMS 前已至少慢 6.08 倍，且没有满足严格输出等价；这不是有效的精确低显存 compiler 结果。
- **推断**：T2 最有复用价值的是把开发选择、独立确认、等墙钟因果效用和多级执行等价分开的审计框架，而不是已经闭合的方法贡献。
- **未知**：动态 action 家族没有进入完整 DOTA validation，因为没有候选通过预注册触发门；分区 compiler 没有在第二检测器或外部数据集上形成可执行结果。若放宽为容差等价或近似离线推理，收益边界尚未被本项目系统研究。

相关先验工作：[Online Batch Selection](https://arxiv.org/abs/1511.06343)、[Active Bias](https://proceedings.neurips.cc/paper/2017/hash/2f37d10131f2a483a8dd005b3d14b0d9-Abstract.html)、[MentorNet](https://proceedings.mlr.press/v80/jiang18c.html)、[NIST Exact Tile-Based Segmentation Inference](https://www.nist.gov/publications/exact-tile-based-segmentation-inference-images-larger-gpu-memory)、[Welder](https://www.usenix.org/conference/osdi23/presentation/shi)。

## 实际采用过的方法

- **动作价值探测**：从多个训练阶段 checkpoint 分叉，短程执行高损失、低损失、随机、小目标/稀有类倾向和不同分辨率 action，比较 ΔmAP、单位训练时间收益、动作排序及 oracle-static headroom。
- **状态与控制器估计**：用瞬时 loss、正样本数、梯度/参数更新、训练进度和多尺度历史特征训练 Ridge、Logistic 与 RandomForest 预测器，评价 leave-one-trajectory regret、排序反转准确率和 headroom capture。
- **冻结因果确认**：开发只使用两条轨迹并做 replay cross-fitting；第三条轨迹冻结 action 后，以 canonical fork state、成对 Control/Treatment、双 replay、等步数和端到端等墙钟重新估计 baseline-relative utility。
- **分区语义与规划**：定义母图坐标、halo/stride phase、Add/Concat 对齐、全局候选屏障和 L1–L4 等价层级；实现局部算子、合成 toy-FPN、legality-first planner 及普通独立切片敏感性基线。
- **真实检测器门控**：冻结 RTMDet native reference，先诊断全局 ChannelAttention，再实现 full-feature native global barrier 并接回 regional backbone、PAFPN、head、decode 与 NMS，联合测等价、物理显存和延迟。

## 教训一：动作之间有差异，不等于动态控制相对正常训练有正收益

- 失败命题：oracle 比随机 action 好，或 action 间 ΔmAP 方差明显大于重复噪声，就证明存在值得部署的动态训练控制空间。
- 失败原因：早期小型探测的 signal-to-noise 为 `22.772`、oracle 相对 random 高 `0.033588` mAP，后续开发矩阵也得到 `0.010762` 的动态 headroom；这些量主要比较候选 action 之间的排序。即使所有干预都比正常 Control 差，事后选择“最不差”的 action 仍会产生 oracle headroom。最终 baseline-relative 确认正是出现了这种情况。
- 后续做法：先估计每个 action 相对“不改变训练”的配对因果效应，再讨论 action 之间的 oracle 或 controller headroom；把“存在异质性”“可选择”和“绝对有益”作为三个独立命题。
- 边界：早期结果仍证明当前 action 在短程 probe 中存在异质性；被否定的是从相对排序直接跳到可部署正收益，而不是所有自适应采样都无效。
- 证据：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 的 `work_dirs/oracle_gain_test/ORACLE_DECISION.md`、`work_dirs/oracle_gain_test_v2/ORACLE_V2_DECISION.md`、`work_dirs/oracle_v3/ORACLE_V3_DECISION.md`。

## 教训二：相关性和相对 regret 改善不能代替可用的决策精度

- 失败命题：某些 proxy 与未来增益强相关，或预测器比一个较弱基线降低 regret，就足以进入在线控制器。
- 失败原因：较长 probe 与短 probe 的 action 排序 Spearman 中位数只有 `0.619`，跨阶段仅 `0.381`；早期 leave-one-trajectory 模型的中位 R² 仅 `0.102`。Controller V1 的 history Ridge 虽比瞬时 Ridge 把 top-1 regret 降低 `28.3%`，绝对 regret 仍为 `0.008992`、高于 `0.004350` 门，稳定反转 pair accuracy 为 `0.239`，还低于两阶段同时猜对的 `0.25` 基线。
- 后续做法：控制器必须同时报告新轨迹上的绝对 regret、反转决策准确率、相对 best-static 的 capture 和最终效用；相关系数或相对百分比改善只能用于筛选特征，不能单独授权在线部署。
- 边界：这些结果限制当前两条开发轨迹、特征和 action 集上的预测器，不是否定训练状态中可能存在其它可预测信息。
- 证据：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 的 `work_dirs/oracle_gain_test_v2/ORACLE_V2_DECISION.md`、`work_dirs/oracle_gain_test_v2/horizon_rank_agreement.csv`、`work_dirs/oracle_controller_v1/CONTROLLER_V1_DECISION.md`。

## 教训三：更高频、更长的训练历史不自动构成有用状态

- 失败命题：只要增加 loss、梯度、置信度和参数更新的历史窗口，控制器就会比瞬时特征更准确。
- 失败原因：State V2 在开发集选中的 AP 模型只使用 progress/lr，没有选择 history；5-step 高频与冻结 50-step 下采样的最终 regret 同为 `0.018276`。该模型还劣于瞬时 Logistic 基线的 `0.014294`，headroom capture 为 `-0.067`，稳定反转准确率 `0.417` 也低于 `0.60` 门槛。更多观测没有转化为跨轨迹决策信息。
- 后续做法：把历史特征的价值定义为在同一冻结模型选择协议下对新轨迹的增量收益，并与瞬时、progress-only 和 best-static 同时比较；没有增量就停止扩充窗口和模型复杂度。
- 边界：该负结果受限于现有记录频率、三条轨迹和监督标签；它不证明优化器历史在其它任务中没有作用，也不支持继续在本项目堆叠历史特征。
- 证据：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 的 `work_dirs/controller_state_v2/STATE_V2_DECISION.md`、`work_dirs/controller_state_v2/state_v2_metrics.csv`、`work_dirs/controller_state_v2/stable_reversal_predictions.csv`。

## 教训四：开发期 headroom 必须通过冻结新轨迹和等墙钟因果确认

- 失败命题：开发轨迹上的最佳 action 或 cross-fitted dynamic headroom 为正，就可以继续设计 controller 或直接做完整验证。
- 失败原因：开发期 `high_loss_1024` 的平均 baseline-relative utility 为 `+0.029207` mAP，但动态 headroom 仅 `+0.005633`，95% CI `[-0.005033,+0.016985]` 已跨零；冻结到第三条轨迹后，`high_loss_1024` 变为 `-0.028984`，95% CI `[-0.051767,-0.002603]`。端到端等墙钟下三个冻结 action 的总体均值也均不为稳定正值，没有任何 action×stage 同时通过双 replay probe 与双 replay wall-clock 门。
- 后续做法：开发阶段只用于冻结 action、终点和模型选择；最终判断只看未参与选择的新轨迹、成对 Control 和包含选择开销的等墙钟效用。触发门失败时不再用局部正 stage 或更长 horizon 重启路线。
- 边界：完整 DOTA validation 因无合格候选而未运行，所以结论是停止当前 action/controller 家族，不是宣称任何数据集、模型和训练预算上的动态课程都无效。历史 checkpoint 缺少原 RNG/AMP/sampler 状态，canonical fork 支持分支内公平比较，但不是原历史轨迹的逐状态重建。
- 证据：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 的 `work_dirs/oracle_v3/ORACLE_V3_DECISION.md`、`work_dirs/oracle_v3/oracle_v3_summary.json`、`work_dirs/oracle_v3/equalwall_summary.json`、`work_dirs/oracle_v3/state_restore_audit.json`。

## 教训五：局部算子和合成子图精确不能推出真实检测器精确

- 失败命题：Conv、MaxPool、Add、Concat 等局部算子通过逐位测试，toy-FPN 和全局 NMS/RoI 单测也通过，就已经得到可组合的真实检测器 compiler。
- 失败原因：项目完成的是 18/18 个随机局部算子测试和 7 个语义单测；真实 RTMDet/Oriented R-CNN 的 FPN/PAN、head、RPN/RoI、候选流、liveness 和 postprocess 当时都没有接入 regional runtime，L1–L4 的有效检测器结果为零。数学上的算子闭包只有在实际 DAG 的全部节点、坐标映射和全局屏障都覆盖后才能组合。
- 后续做法：先从冻结真实 DAG 反向建立算子覆盖表和首个不支持节点，再以完整 L1→L4 数据流逐级闭合；合成测试只作为实现单元证据，不能承担方法结论。
- 边界：已通过的局部语义和 toy-FPN 测试仍是可复用实现资产；被否定的是把它们外推为真实检测器或跨架构的端到端等价。
- 证据：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 的 `work_dirs/partition_transparent_closure/OPERATOR_EQUIVALENCE_REPORT.md`、`work_dirs/partition_transparent_closure/TOP_JOURNAL_DECISION.md`、`work_dirs/partition_transparent_closure/END_TO_END_EQUIVALENCE.csv`。

## 教训六：非法 DAG 的拒绝是能力缺口，不是等价性实验失败

- 失败命题：八个计划都没有达到最终集合精确，便可把它们记为八次方法失败，甚至证明 halo 分区无法处理该检测器。
- 失败原因：最初八个计划全部在执行前被 legality gate 拒绝，因为四个 ChannelAttention 含全局空间平均而 executor 没有 global-reduction lowering；有效执行次数其实是 `0/8`，L1–L4 都是 N/A。后续加入原生全局 barrier 后，这四处 attention 的 input、GAP、weight 和 output 均可逐位相等，说明早期结果定位的是缺失算子语义，不是全模型不可能。
- 后续做法：明确区分 rejected、executed-but-mismatched 和 exact；遇到全局算子先建立合法 gather/reduction barrier 和独立单测，再继续寻找实际首个失配节点。
- 边界：普通有限 halo 确实不能直接替代全局平均；但这只要求显式全局归约，不代表加入 barrier 后的整个检测器会自动精确。
- 证据：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 的 `doc/rtmdet_exact_gate/RTMDET_EXACT_GATE_DECISION.md`、`doc/rtmdet_exact_gate/EXACT_GATE_RESULTS.csv`、`work_dirs/rtmdet_full_global_barrier/FULL_GLOBAL_BARRIER_DECISION.md`。

## 教训七：数学算子相同也可能因执行形状改变而失去 FP32 逐位等价

- 失败命题：全局 attention 已精确、halo 和母图坐标也正确，区域 PAFPN 中相同权重的 convolution 就应与整图执行逐位相同。
- 失败原因：四个 attention barrier 接回 regional backbone 后仍精确，但区域 CSPNeXtPAFPN 首先失配：P0897/P1854 最大差分别为 `6.002×10⁻⁵` 和 `7.558×10⁻⁵`。全尺寸 native neck+head control 可以精确，说明根因不是 attention、坐标、decode 或 NMS，而是输入形状变化触发的 FP32 convolution reduction 路径差异；随后 8/8 的候选与最终集合都不相等。
- 后续做法：声称 bit-exact 时必须把算子实现、输入形状、kernel/reduction plan 和归约顺序纳入参考函数；从首个失配张量定位，不以“数学卷积相同”跳过数值执行审计。
- 边界：该结果否定当前 regional PAFPN 在严格逐位契约下的透明性，不说明误差必然影响所有任务指标，也不否定预先冻结数值计划或采用容差契约的其它方案。
- 证据：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 的 `work_dirs/rtmdet_full_global_barrier/FULL_GLOBAL_BARRIER_DECISION.md`、`lab/result.md`、`src/partition_runtime/neck_head_regional_executor.py`。

## 教训八：显存、语义正确性和延迟必须在同一执行上同时成立

- 失败命题：分区执行把峰值显存降低约 73%，就足以证明 compiler 或 runtime 成功。
- 失败原因：P1854 的峰值确实从 native `6.674 GiB` 降到 `1.779–1.796 GiB`，但 L3/L4 均失败；并且在 decode/NMS 之前单次已耗时至少 `9.005 s`，是 native `1.481517 s` 的 `6.08×`。节省显存的执行既没有保持目标语义，也没有达到实用延迟。
- 后续做法：为同一个冻结执行联合设置 L1–L4、物理峰值和端到端延迟接受域；正确性失败时不把资源数字单独宣传为方法收益，性能测量也必须包括完整后处理和重复运行。
- 边界：在允许近似、极端内存受限且可接受慢速的离线场景，这一折中可能有工程价值；但必须改变“精确且高效”的主张并重新定义误差预算。
- 证据：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 的 `work_dirs/rtmdet_full_global_barrier/FULL_GLOBAL_BARRIER_DECISION.md`、`lab/result.md`。

## 教训九：不可追溯结果和不可执行计划都不能进入科学结论

- 失败命题：旧聊天或摘要中的大样本 exact 计数，以及 synthetic planner 的峰值/延迟预测，可以共同补足真实 compiler 的经验结果。
- 失败原因：旧称的 `1734/1734`、`180/180` 没有来源提交、命令、配置、输入或权重 provenance，仓库、分支、reflog 与可用历史均无法恢复，只能标为 UNVERIFIED。planner 也只在未绑定检测器 DAG 的 `6144×4096` synthetic shape 上预测 `1,153,351,680` bytes 和 `41.914624 ms`；没有可执行 runtime、实测峰值或 hand-tuned/static/offload 对照。
- 后续做法：经验结论必须绑定来源提交、冻结输入/权重、可重建命令和机器可读输出；planner 只有在同一真实 DAG 上执行并与强基线比较后，才能报告预算满足或性能优势。找不到证据时保留未知，不用新实验替旧数字补 provenance。
- 边界：旧主张不可验证不等于它必然为假；synthetic cost model 也可作为设计原型。二者都不能被引用为已完成的科学结果。
- 证据：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 的 `doc/rtmdet_exact_gate/EVIDENCE_RECONCILIATION.md`、`work_dirs/partition_transparent_closure/PLANNER_EVALUATION.csv`、`work_dirs/partition_transparent_closure/TOP_JOURNAL_DECISION.md`。

## 方法族停止索引

下表只索引当前主线 `ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 中可回读的最终决策、机器结果和实现入口。较早的阶段性 GO 若与后续冻结确认冲突，以后者为准。

| 方法族 | 最强负证据或限制 | 停止范围 | 当前 main 证据路径 |
| --- | --- | --- | --- |
| Oracle Gain / Oracle V2 | 动作差异与开发 headroom 存在，但短/长 horizon 排序中位相关仅 `0.619`、跨阶段仅 `0.381`，且没有证明相对正常 Control 的稳定正收益 | 停止把相对 action 排序直接解释为在线 controller；保留为开发期异质性证据 | `work_dirs/oracle_gain_test/ORACLE_DECISION.md`；`work_dirs/oracle_gain_test_v2/ORACLE_V2_DECISION.md`；`work_dirs/oracle_gain_test_v2/horizon_rank_agreement.csv` |
| Controller V1 | history 模型 regret `0.008992>0.004350`，稳定反转准确率 `0.239<0.25` 随机联合基线 | 停止当前离线 history controller 进入第三轨迹或在线部署 | `work_dirs/oracle_controller_v1/CONTROLLER_V1_DECISION.md`；`work_dirs/oracle_controller_v1/reversal_prediction.csv` |
| State V2 | 最终 regret `0.018276`，劣于瞬时基线 `0.014294`；capture `-0.067`，反转准确率 `0.417<0.60` | 停止继续堆叠当前高频/长窗口状态特征；不否定其它状态定义 | `work_dirs/controller_state_v2/STATE_V2_DECISION.md`；`work_dirs/controller_state_v2/state_v2_metrics.csv` |
| Oracle V3 | 开发最优 action `+0.029207`，冻结第三轨迹变为 `-0.028984`；等墙钟无稳定正 action，完整验证候选为空 | `STOP DYNAMIC CONTROL`：停止当前 action、状态估计和 controller 设计，不外推到所有动态课程 | `work_dirs/oracle_v3/ORACLE_V3_DECISION.md`；`work_dirs/oracle_v3/oracle_v3_summary.json`；`work_dirs/oracle_v3/equalwall_summary.json` |
| independent-tile baseline | 两个检测器的 6 个真实条件 final set 全部不等于 native；RTMDet P0897 的 retained-set rate 随布局为 `0.9324–0.9461` | 只作为分区敏感性动机；停止把普通切片+合并当作 transparent compiler 结果 | `work_dirs/partition_transparent_closure/PARTITION_SENSITIVITY_REPORT.md`；`work_dirs/partition_transparent_closure/PARTITION_SENSITIVITY_BENCHMARK.csv` |
| regional operators / toy-FPN | 局部测试 18/18、语义单测 7 个通过，但真实两类 detector 的 L1–L4 均未执行 | 停止从单元/合成子图外推端到端 compiler；保留已闭合局部语义 | `work_dirs/partition_transparent_closure/OPERATOR_EQUIVALENCE_REPORT.md`；`work_dirs/partition_transparent_closure/END_TO_END_EQUIVALENCE.csv` |
| legality-first planner | 只有未绑定 DAG 的 synthetic 预测；实测峰值/延迟为空，所有强基线均不可用 | 停止自动预算满足、优于手工或 offload 的性能主张 | `work_dirs/partition_transparent_closure/PLANNER_EVALUATION.csv`；`work_dirs/partition_transparent_closure/planner_plan.json` |
| RTMDet halo-only exact gate | 四个全局 ChannelAttention 未支持，8 个计划均执行前拒绝，合法 L4 样本为零 | 停止当前 halo-only executor；只证明需 global-reduction lowering，不是八次等价失败 | `doc/rtmdet_exact_gate/RTMDET_EXACT_GATE_DECISION.md`；`doc/rtmdet_exact_gate/EXACT_GATE_RESULTS.csv`；`doc/rtmdet_exact_gate/runtime_legality.json` |
| Full Global Barrier | attention 全部 exact 后 regional PAFPN 首先失配，8/8 L3/L4 不等；虽降显存 73%，decode/NMS 前已慢 `6.08×` | `STOP_PARTITION_TRANSPARENT_PROJECT`：停止当前严格 bit-exact regional runtime、planner 和跨模型扩展 | `work_dirs/rtmdet_full_global_barrier/FULL_GLOBAL_BARRIER_DECISION.md`；`lab/result.md`；`src/partition_runtime/full_global_barrier.py` |
| legacy alleged exact runtime | `1734/1734`、`180/180` 无提交、命令或 provenance，全面搜索后仍不可追溯 | 禁止引用为结果或用新运行补写旧 provenance；状态保持 UNVERIFIED | `doc/rtmdet_exact_gate/EVIDENCE_RECONCILIATION.md`；`doc/rtmdet_exact_gate/native_reference_manifest.json` |
