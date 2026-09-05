# cqc_P4 科学问题与失败教训

> 使用边界：教训须结合适用条件与原始证据使用，同条件下的有效反证不能忽略，也不能跨条件自动否决新研究；来源不可访问时须注明“未独立核实”，不得将摘要当作已核实的原始证据。

审计基线：当前主线 `ziyu24/cqc_P4@0719847bfbc1b49f4e4d5254685bf0e6b318fb2c`；另比较了比主线多 4 个提交的执行分支 `ziyu24/cqc_P4@ca6a7615605025196f46c39b22bb80c321456133`。次线只新增 OVOD runtime readiness 与阻塞回执，没有训练或性能证据，但暴露了实际模型身份不成立的问题。

快速阅读路径：先读“项目研究什么”→“教训一、二、四、五”→“方法族停止索引”。

## 项目研究什么

项目先研究有限空间支持是否要求面向目标方向的频域自适应感受野，随后转向开放词汇旋转检测中的隐藏标签风险。前者提出频域各向异性模块，后者尝试用严格证据隔离保证标签不被提前使用。

## 领域位置与当前结论

- **事实**：频域模块的论文公式、代码算术和频率坐标不一致，合成 Gate 只证明实现响应异常；参数量从约 3098 万增到 4835 万且无等容量对照，不能支持小目标方向机制。
- **事实**：开放词汇方向的 angle-jitter observable 存在拓扑反例；后续虽建设了大量隔离与 provenance 工具，主线没有真实检测收益。
- **事实**：较新次线的 21 项工程测试通过，但实际配置构造的是本地兼容 `GSDet`，不是需要验证的真实注册 detector；正式 prepare、forward、训练和 AP 均为零。
- **推断**：项目目前最强结论是两个“测量/身份先行”教训，而不是 FAA 或 OVOD 方法有效。
- **未知**：修正数学定义并以真实 detector 做等容量、无泄漏实验后是否存在信号，仓库尚未回答。

## 实际采用过的方法

项目实现并测试了频域自适应聚合模块、合成矩形频谱诊断和检测器消融；后续又设计隐藏标签隔离、静态检查和逐阶段证据协议，但没有形成相应的真实检测性能证据。

## 教训一：论文公式、实现和容量对照必须指向同一机制

- 失败命题：当前实现已经检验了论文所述的径向频谱聚合机制，正结果可归因于该机制。
- 失败原因：文档公式沿半径累加功率，而代码按单频率的加权幅值取最大；频率网格处理也不一致，且模块把参数量从约 3098 万增到 4835 万而缺少等容量对照。
- 后续做法：冻结可执行数学定义，做公式到代码的数值单测，并设置等参数、等计算量和去机制对照后再跑官方训练。
- 边界：已有检测结果仍可说明“这一整套实现”可能有效，但不能归因到声称的频域机制。
- 证据：`ziyu24/cqc_P4@0719847bfbc1b49f4e4d5254685bf0e6b318fb2c` 的 `research/EVIDENCE.md`、`research/FAA_GATE0_RESULTS.md`。

## 教训二：改变短边支持与长宽比不能解释为单一各向异性效应

- 失败命题：合成矩形频谱随形状变化的响应，直接证明检测器需要方向自适应支持。
- 失败原因：实验同时改变短边支持和长宽比，无法区分有限支持、尺度和各向异性；玩具频谱只验证算术响应，没有连接到真实特征或误差。
- 后续做法：采用正交控制，分别固定面积、短边、长宽比和方向，并在真实特征层做干预与性能响应分析。
- 边界：合成矩形仍适合发现实现错误或生成定性假设，不足以确认检测机制。
- 证据：`ziyu24/cqc_P4@0719847bfbc1b49f4e4d5254685bf0e6b318fb2c` 的 `research/EVIDENCE.md`、`research/FAA_GATE0_RESULTS.md`。

## 教训三：总体正结果不能自动支持预设的小目标机制

- 失败命题：模块在 DOTA 上的总体提升证明收益来自小目标的有限空间支持。
- 失败原因：项目没有给出尺寸分层、支持半径干预或目标级中介证据，总体提升还可能来自额外容量或普通特征混合。
- 后续做法：预注册按尺寸与形状的异质效应，报告等容量基线，并检验中介变量是否随干预按预测变化。
- 边界：总体结果可以作为工程候选信号，不能单独确证小目标机制。
- 证据：`ziyu24/cqc_P4@0719847bfbc1b49f4e4d5254685bf0e6b318fb2c` 的 `research/EVIDENCE.md`、`research/FAA_GATE0_RESULTS.md`。

## 教训四：严密的证据协议不能替代最小性能信号

- 失败命题：不断加强隐藏标签隔离、静态检查和验收步骤，本身就能推进开放词汇方向的科学结论。
- 失败原因：这些步骤能保证证据可信，却没有产生候选方法相对强基线的性能信号；协议复杂度最终超过被验证的科学内容。
- 后续做法：先用最小无泄漏实验确认存在值得研究的效应，再为高风险环节增加必要隔离；审计机制只服务于明确主张。
- 边界：涉及真正隐藏测试集或竞赛提交时，严格隔离仍必要；被否定的是用流程完整性替代科学结果。
- 证据：`ziyu24/cqc_P4@0719847bfbc1b49f4e4d5254685bf0e6b318fb2c` 的 `research/ovod_angle_risk/EVIDENCE.md`、`research/OVOD_GATE1A0_RESULTS.md`、`server_result.md`。

## 教训五：测试通过前必须确认运行的是声称的模型

- 失败命题：runtime builder、registry、恢复日志和 21 项测试全绿，就说明真实 GSDet 已具备训练就绪性。
- 失败原因：较新次线的配置实际实例化本地 compatibility `GSDet`，不是待研究的真实注册 detector；因此测试只闭合了替身对象的工程接口。该分支没有正式数据准备、forward、优化步或 AP，不能产生方法结论。
- 后续做法：把模型身份设为最早的可回读断言：记录 registry 来源、类的模块路径、解析后配置和 checkpoint key 覆盖；用一个真实样本做 forward 身份审计后才建设恢复与证据层。
- 边界：替身测试对开发接口仍有价值，但必须明确标为 fake/compatibility fixture，不能作为真实系统 readiness。
- 证据：`ziyu24/cqc_P4@ca6a7615605025196f46c39b22bb80c321456133` 的 `research/ovod_angle_risk/configs/baseonly/main_r2.py`、`research/ovod_angle_risk/results/baseonly_systems_prep_r2_successor_failure.json`、`server_result.md`。

## 方法族停止索引

| 方法族 | 最强负证据或限制 | 停止范围 | 当前证据路径 |
| --- | --- | --- | --- |
| FAA frequency estimator | 论文径向功率和代码单 bin 加权幅值不是同一算子，频率坐标亦有错误 | 停止现有实现的机制归因与训练扩展 | main：`research/FAA_GATE0_RESULTS.md`；`research/gate0/faa_estimators.py` |
| FAA shape probe | 尺度、短边支持和长宽比同时变化，且只在合成矩形上观察 | 停止把玩具响应外推为真实小目标机制 | main：`research/EVIDENCE.md`；`research/FAA_GATE0_RESULTS.md` |
| FAA detector result | 参数增加约 56%，无等容量对照 | 停止把总体差异归因于方向自适应 | main：`research/EVIDENCE.md` |
| angle-jitter variance | 标量 `sin(2θ)` 方差存在 0°/90° 与边界角拓扑反例 | 停止以该 observable 认证方向风险 | main：`research/ovod_angle_risk/GATE0_AJV_TOPOLOGY.md`；`research/ovod_angle_risk/results/ajv_gate0.json` |
| OVOD evidence system | 主线只有隔离/seed 审计；较新次线又实例化本地替身而非真实 detector | 停止把 protocol readiness 当性能或方法证据 | main：`research/OVOD_GATE1A0_RESULTS.md`；次线：`research/ovod_angle_risk/results/baseonly_systems_prep_r2_successor_failure.json` |
