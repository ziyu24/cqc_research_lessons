# D7_pcp_obb_foundation 科学问题与失败教训

> 使用边界：教训须结合适用条件与原始证据使用，同条件下的有效反证不能忽略，也不能跨条件自动否决新研究；来源不可访问时须注明“未独立核实”，不得将摘要当作已核实的原始证据。

审计基线：当前主线 `ziyu24/D7_pcp_obb_foundation@1aeb4e5339d1ecd71966d565b9de5802e8f4408e`。已抓取并检查全部远端分支，没有更新更晚的次线。最新证据补齐同尺度基线及计数查询的端点等价/分数支配证明，进一步削弱 global 简化臂的独有几何解释；旧原型保持停止，尚无通过新颖性与效用审查的新方法。已有开发样本上的新复算是事后诊断，不是独立确认。

快速阅读路径：先读“项目研究什么”→“教训十三、十四”→“教训一、二、三、八、九、十、十一、十二”→“方法族停止索引”。

## 项目研究什么

项目研究旋转框方向不确定性的共形预测：在角度具有 π 周期、近方形目标方向弱可识别且同一图像多对象相关时，如何给出有限样本覆盖保证、有效预测弧和选择性拒绝。

后续转向冻结检测输出下的整图区域盘点：构造类别×空间格的非负整数计数集合，同时考虑候选空间归属、删除与补漏，用整图校准支持看结果后选择网格区域的计数查询。它是新的计数 estimand，不恢复已停止的单框表示或阈值后选择路线。

## 领域位置与当前结论

- **事实**：π 周期分数、匹配条件覆盖和图像簇交换性已得到较充分审计，但分数单调等价、匹配选择偏差和对象伪重复显著收缩了可主张范围。
- **事实**：phase-capture 路线中，真正输入暴露切换虽有 464 个样本，和检测 discordance 重叠仅 30 个；全局 discordance 也只有 38 个，无法支撑预注册分析。
- **事实**：阈值后选择 benchmark 在 3 个架构中有 2 个无法在 `FPI≤2` 下提供至少 5 个阈值，故没有 coverage 结果；一个要求不存在 adapter 的强基线协议同样无效。
- **事实**：完整 1024 方向的 symKLD 存档存在四个严格可行框越过所称外界的反例；表观面积 gap 小于 1% 不构成有效数值证书，当前自定义效率/表示 benchmark 已按协议停止。
- **事实**：旧 C2 虽 polygon 等价，却不是所称 le135 长边约定；真正 le90/le135 下，本项目绝对残差数学不变，冻结样本差仅约 1e-16。四个 Bonferroni 校准折均有分位秩溢出，本地 MaxRank-like 的覆盖与面积边界也不一致，旧有效漂移/公平效率解释已撤回。
- **事实**：旧 DOTA 指标使用矩形化 GT 和 difficulty>=100，不能称为官方 Task1 评测。保持原匹配和操作点、改用原四边形与非零 difficulty 后，两个关键架构在全部五个开发切分仍超过原 FP 预算，定义更正没有恢复已停止的后选择支持区间；正式官方 AP 尚未复现。
- **事实**：区域计数主方法在 DOTA 91 图、两个架构上均未体现预定的方向与局部配额增量；去方向的逐图 membership 相同、宽度略小，去局部配额后更紧。原图等权纠正不改变负结果，补漏项占原始平均宽度约 72%/76%。12 个校准配置中 9 个的分位已由 root/类别计数缺口下界决定，任意同类空间移动都不能降低这些分位。
- **事实与未知**：global 对原整数运输的开发归一化宽度优势仍可复现，但给运输加入同一预测计数尺度与整数约定后，一架构优势仅余 0.158%，另一架构变为 global 宽 10.25%。更简单的全子集误差基线比 global 窄 15.50%/14.91%，逐图 membership 相同；这些是事后结果，未完成 global 无方向对照与独立确认。
- **事实**：在当前单位搬移、删补成本下，运输与全子集误差集合虽不同，对全部普通区域计数却有相同端点；后者分数更小，同尺度分别校准后所有此类区间确定性包含于运输区间。该支配不扩展到有符号区域差值，已有小型严格反例。
- **推断**：单独的数值失败不能证明物理方法普遍无效；这次另有独立的基线/命题定义问题，不能再概括为“只差算力闭合”。
- **未知**：有效物理方法与正确定义基线的公平效率比较仍未获得；停止当前路线不是证明所有 OBB 可靠性问题没有研究价值。

## 实际采用过的方法

项目比较线性角度残差、π 商空间残差、wrapped-π 分数、协方差几何分数、按图像聚类的共形校准、形状条件化与局部化校准，并评估近方形诊断和选择性 abstention。后续实际采用了五维 coordinate Bonferroni、本地 MaxRank-like、rIoU/GWD/symKLD/log-SPD 标量集合，以及方向支撑/凸包面积；最新审计核对其真正 chart、有限样本分位、集合 predicate 和外界定义，不将方法名当作实现有效的证明。

区域计数实验复用已有 ORCNN/ARS 输出与原四边形标注，固定 4×4 网格和 15 类，以整数流定义 OBB 可达几何及 laminar 补漏/删除容量。对比逐叶最大残差、两种树计数 CP、联合椭球、整数非平衡运输，以及同面积无方向、global-only 两消融；未训练、下载、新推理或新增标注。查询区间从整数集的精确支持计算，不使用旧面积估计器。

后续只读既有充分统计，加入与 global 相同尺度的运输及全子集计数误差基线。数学上，global 成员关系可写成可达图最大匹配 `K≥max(M−D,N−B)`，并由全部区域的 Hall 上下界刻画；这种预测依赖的部分匹配形式不能直接宣称新度量。另用有限穷举核对普通计数和有符号差值的解析支撑，未运行新的真实数据验证。

## 教训一：单调等价分数不是两个独立方法

- 失败命题：π 商空间角度分数与 wrapped-π 分数是两个可比较优劣的新方法。
- 失败原因：两者在有效域上是单调变换，产生相同排序和等价共形集合；数值差异不能支撑独立方法或优越性主张。
- 后续做法：先证明候选分数之间的序关系和集合等价性；若单调等价，就作为同一表示族，只研究计算、解释或校准便利性。
- 边界：正确处理周期边界本身仍有价值，但贡献应表述为表示与校准研究，而非两个算法的竞争。
- 证据：`ziyu24/D7_pcp_obb_foundation@84da96973a464562cd965fbb0c9759a25bae5a58` 的 `lab/result.md`、`doc/reports/FINAL_PROJECT_REPORT.md`。

## 教训二：匹配框的角度覆盖不等于完整检测风险覆盖

- 失败命题：在预测框与真值已匹配的样本上达到角度覆盖，就说明检测系统整体可靠。
- 失败原因：条件样本排除了漏检、误检、分类错误和匹配失败；这些错误不会进入角度区间，整体风险被系统性截断。
- 后续做法：明确报告“条件于成功匹配”的 estimand，并为检测存在性、类别和匹配不确定性建立单独风险分解。
- 边界：在应用只关心已确认对象的方向测量时，匹配条件覆盖仍是合法目标。
- 证据：`ziyu24/D7_pcp_obb_foundation@84da96973a464562cd965fbb0c9759a25bae5a58` 的 `lab/result.md`、`doc/reports/FINAL_PROJECT_REPORT.md`。

## 教训三：对象级样本数会夸大多对象图像的有效证据

- 失败命题：把同一图像中的所有匹配对象当作独立校准样本，可以直接使用对象级置信区间。
- 失败原因：图像聚类 bootstrap 与对象 iid bootstrap 的区间宽度比在两个多对象配置中约为 `2.42`、`2.55`，而 HRSC 配置约为 `0.95`，不是所有条件都膨胀。图像不交叉重划分后的覆盖有升有降，不能概括成统一下降一至两个百分点；核心问题是对象 iid 推断缺少交换性依据。
- 后续做法：以图像或采集事件作为交换单元，使用簇级校准、留图验证或层次模型，并报告对象级与簇级结果差异。
- 边界：每图只有一个对象或能证明条件独立时，对象级处理可接近合理。
- 证据：`ziyu24/D7_pcp_obb_foundation@84da96973a464562cd965fbb0c9759a25bae5a58` 的 `doc/reports/B0_image_cluster_exchangeability_audit.md`、`doc/reports/FINAL_PROJECT_REPORT.md`。

## 教训四：继承的分数负结果也要核对集合与表示定义

- 失败命题：旧 score-study 的大弧长与低分桶 coverage 足以证明所有协方差角度集合效率差，或物理近方形方向完全不可识别。
- 失败原因：追溯上游代码发现，coverage 使用真实形状，弧长反演使用预测形状，评价的不是同一集合。这里的零均值协方差分数混合尺度与角度，并不包含中心；方形协方差的连续旋转不变性也是有损表示性质，不能等同于真实正方形的离散旋转对称性。
- 后续做法：先核对集合 membership、长度和部署信息是否一致，再继承负结果；严格区分物理表示与高斯近似，不从有损表示退化推出物理不可能性。
- 边界：撤回旧表支撑的同覆盖效率裁决，不据此宣称协方差更优。该限制不影响独立成立的周期分数单调等价结论；当前物理表示比较仍未知。
- 证据：`ziyu24/D7_pcp_obb_foundation@fb71ec02c97a48d16e66710d8caec83d0646e457` 的 `lab/result.md`；上游 `ziyu24/pcp-obb-score-study@0df97a23936c0893704f8cf03c652625522060f9` 的 `src/scripts/run_score_comparison.py`、`src/scripts/s1_constructive_solution.py`、`src/pcbobb_score/scores/_common.py`。

## 教训五：形状诊断、局部校准和拒绝策略不能被包装成普适规律

- 失败命题：形状折叠指标能稳定预测区间质量，按其局部校准或拒绝即可普遍提高效率且不伤害总体结果。
- 失败原因：该指标虽数值稳定，却只弱预测角度弧和最差条件覆盖；局部化方案与既有 localized conformal prediction 同构且无稳定优势，拒绝近方形虽改善保留集覆盖，却牺牲全对象效率。
- 后续做法：把诊断的预测效度、方法新颖性、保留集收益和总体效用分开评估，预先报告拒绝率及被拒样本代价。
- 边界：在允许人工复核或不必覆盖所有对象的选择性任务中，拒绝仍可能合理；不能宣称无代价普适改进。
- 证据：`ziyu24/D7_pcp_obb_foundation@84da96973a464562cd965fbb0c9759a25bae5a58` 的 `lab/failed_methods.md`、`doc/reports/FINAL_PROJECT_REPORT.md`。

## 教训六：中介候选很多但目标事件太少时，机制检验没有统计支撑

- 失败命题：大量 core-state switching 就足以证明输入相位切换解释检测 discordance。
- 失败原因：core switching 不是目标中介。按真实输入暴露定义后有 464 个切换样本，但与检测 discordance 重叠仅 30 个，全局 discordance 也只有 38 个，达不到冻结的有效样本门。
- 后续做法：在立项时先用目标事件定义计算可用交集样本数；中介必须与干预和结果同一单位配对，不能用更宽 proxy 扩充分母。
- 边界：这是当前数据/协议的统计不可用，不证明相位机制不存在。
- 证据：`ziyu24/D7_pcp_obb_foundation@1f4092fd5ebb8ea0f4479b5e1e01a28f27aacece` 的 `lab/result.md`、`lab/failed_methods.md`。

## 教训七：阈值后选择研究必须先存在共同、非退化的操作区间

- 失败命题：对多个架构扫描阈值，就能研究选择后的 coverage 或效率。
- 失败原因：在冻结的 `FPI≤2` 条件下，3 个架构中有 2 个无法给出至少 5 个合格阈值；候选集合在统计校准前已经退化，因此没有可解释的 post-selection 结果。
- 后续做法：先在所有架构上验证共同操作区间和候选数量，再冻结选择规则；操作区间不存在时停止，不删难例或放松阈值补齐表格。
- 边界：放宽部署约束可以形成新问题，但必须重新预注册，不得沿用原门后的保证。
- 证据：`ziyu24/D7_pcp_obb_foundation@1f4092fd5ebb8ea0f4479b5e1e01a28f27aacece` 的 `lab/result.md`、`lab/failed_methods.md`。

## 教训八：可行的局部支撑不是全局外界证书

- 失败命题：全部方向计算完成、候选可行且内外面积 gap 足够小，就证明半平面交是有效外包络；或者反过来，数值失败便证明物理方法无效。
- 失败原因：局部最大化只给最优支撑的下界，将其作为半平面阈值可能排除合法框。完整 177,152 个方向结果中，四个见证框越过其他存档半平面；将它们向预测收缩后，原 score-q 均低于 -2.9e-7，仍越界约 .01265–.36780，不能归因于 feasibility 容差。所谓小于 1% 的面积 gap 因外界不真而失去证书意义。
- 后续做法：区分可行点、最优值下界、全局上界与离散方向误差；优先用已有见证框做跨半平面必要检查，但“未检出反例”也不能冒充全局认证。数值证书未成立不比较科学效率。
- 边界：当前求解与自定义效率路线已按预先约束止损；不授权继续加方向或换求解器挽救。它不是对所有全局算法的不可能性证明，也不说明所有物理方法无效。此条取代旧版“高方向数仍待定”的过时边界。
- 证据：`ziyu24/D7_pcp_obb_foundation@9c04d0a6325f4df91a1f894f0ef22a5a64c088c8` 的 `src/r011_archive_integrity.py`、`src/r012_validity_audit.py`、`doc/2026-09-06-validity-evidence.json`、`lab/result.md`。

## 教训九：几何等价不能代替坐标约定与效应的代数检查

- 失败命题：只要转换前后 polygon 相同，所测漂移就是合法 le90/le135 基线的表示敏感性。
- 失败原因：旧转换按角度条件交换 w/h，分别使 42/172 和 24/174 个 development 框违反长边约定。真正 le90/le135 只改角度的整数 pi 代表，在共同方形轴约定下，中心绝对残差、log 尺度与 wrapped-pi 距离逐点不变；复算误差约 1e-16。旧巨大/临界面积差不能支持声称的机制。
- 后续做法：同时验证 polygon、角范围、长边/tie 规则和 score/predicate 变换规律；在投入高维集合体积计算之前，先推导差异是否代数上可能存在。
- 边界：条件换轴编码可以几何等价且导致不同 coordinate 区域，但不能误称另一正式约定；该证据不证明所有表示、所有有符号/非对称残差或不同方形轴规范都不敏感。
- 证据：`ziyu24/D7_pcp_obb_foundation@9c04d0a6325f4df91a1f894f0ef22a5a64c088c8` 的 `src/r009_p1_freeze.py`、`src/r009_methods.py`、`src/r012_validity_audit.py`、`doc/2026-09-06-literature-review.md`、`doc/2026-09-06-validity-evidence.json`。

## 教训十：有限样本校准与集合反演必须使用同一个有效定义

- 失败命题：函数名是 Bonferroni/Max-Rank 且能返回有限阈值，就可以进入同覆盖率的物理效率比较。
- 失败原因：五维 Bonferroni 在总 alpha=.10、每维 .02 时，四个 n=43/43/44/43 的校准折所需秩为 44/44/45/44，均溢出；旧实现却截成样本最大值。正确语义为全支持集，不具备旧有限面积。另一本地秩实现采用 1+count(cal<=x)，面积侧却包含第 k 秩坐标边界，四个拟合的边界 membership 均不一致。
- 后续做法：先验证空样本、秩溢出、有限分位首次可达样本量、重复分数与阈值两侧；集合反演和 coverage 使用同一个 predicate，无法获得有限有效集合时如实记为不可用，不事后改 split 挽救。
- 边界：分位溢出破坏所称分布无关保证，并不意味着每份数据的经验 coverage 必然失败；秩/product 边界失配也尚不能解释全部面积差，更不构成已发表 Max-Rank 理论的反例。
- 证据：`ziyu24/D7_pcp_obb_foundation@9c04d0a6325f4df91a1f894f0ef22a5a64c088c8` 的 `src/r009_methods.py`、`src/r010_coordinate.py`、`src/r012_validity_audit.py`、`src/test_r012_validity_audit.py`、`doc/2026-09-06-validity-evidence.json`、`lab/result.md`。

## 教训十一：官方标注输入不等于官方评测，纠错也不等于结论反转

- 失败命题：使用官方数据集标注，就可以把矩形化、困难目标阈值和自定义匹配后的指标称为官方结果；或者发现口径错误就认为旧负结论已被推翻。
- 失败原因：项目先把原四边形转成矩形，以 difficulty>=100 处理 ignore；官方 DOTA Task1 保留原四边形、非零 difficulty 和 score-greedy。原图共有 1,909 条 difficulty=1，定义差异真实存在。对原五个开发切分的 314 张并集进行二因素复算，旧逐图计数精确复现；原四边形/非零 difficulty 下两关键架构 FPI 分别为 5.604–11.132 和 2.264–3.769，仍全部超过预算 2。只改 difficulty 没改变这些操作点的 FP，不代表所有指标都不变。
- 后续做法：分别锁定标注几何、困难目标语义、匹配顺序、IoU 边界与 AP 积分规则，再声称复现官方指标；发现错误后保持原 split/操作点做可归因诊断，区分名称撤回、数值变化和科学判定是否反转。
- 边界：这次核查保留原最大基数与预删除 ignore，四边形交并使用 Shapely，仍不是官方 Task1 AP 复现；不把新口径混入旧预注册结果，也不因停止未反转而保留错误的“官方评测”名称。停止仅针对现有后选择协议，不是对所有可靠性研究的否定。
- 证据：`ziyu24/D7_pcp_obb_foundation@af7bb4c2fcaa9f8d668c45922e56ef71ba0353a0` 的 `src/r006_original_eval.py`、`src/r007_dota_fpi_gate.py`、`src/dota_semantics_probe.py`、`doc/2026-09-06-dota-semantics-evidence.json`、`lab/result.md`；官方定义见 [DOTA Task1 源码](https://raw.githubusercontent.com/CAPTAIN-WHU/DOTA_devkit/master/dota_evaluation_task1.py)。

## 教训十二：同参数下的集合收缩不保证分别校准后的效率，几何不能消除基数缺口

- 失败命题：给整数计数场景集增加类别/空间局部配额，并加入 OBB 方向可达约束，就会比全局预算或通用计数/运输集更紧。
- 失败原因：同一标量同时放大几何范围与全部补漏/删除容量，局部难例抬高校准分位后，原本更小的集合可能整体更宽。两个架构去方向后无所需收益，去局部配额则更紧；主方法宽度主要来自补漏。对 root/类别，`ceil(160*abs(y_v-m_v)/max(10,m_v))` 是与同类移动几何无关的层级必要下界，12 个校准配置中 9 个下界分位等于实际分位。一个校准图的小车真计数/预测为 237/13，单是净计数差就强制层级至少 2757；改变框方向不能消除它。
- 后续做法：先分析不同误差来源对校准分位的必要下界，再分解查询宽度；比较各方法独立校准后的效率而非只比较同一膨胀参数下的集合包含关系。预留方向与预算消融，严格按原图权重汇总，同时保留消融的真实正信号。
- 边界：结论仅针对固定输出、类别不变移动、局部容量定义及开发样本；不证明所有几何或区域计数方法无效。global 比原未缩放运输更紧，但新增同尺度对照已削弱该机制解释，见教训十三、十四；尚缺对应方向消融和独立确认。此处净计数差不是经实例配对确定的 FN 数，事后选择消融也不能算原主方法通过。
- 证据：`ziyu24/D7_pcp_obb_foundation@c8bc18bb70e5c0d17ac42830ae5a93b68ae82255` 的 `doc/r013-b-scientific-review.md`、`doc/r013-b-image-weighted-review.json`、`src/r013_result_review.py`、`src/r013_scene_count_flow.py`、`lab/result.md`。

## 教训十三：集合更精细不等于对实际查询更有信息

- 失败命题：空间运输球排除了更多计数直方图，所以对所有区域盘点必然优于只控制计数误差的集合。
- 失败原因：当前非负整数直方图、一步搬移与删补均为单位成本、可在任意格补入时，运输成本 T 的任意非空区域端点恒为 `[max(0,m(A)−q),m(A)+q]`。令 `E=sup_A|y(A)−m(A)|=max(正残差总量,负残差总量)`，则 `E≤T≤2E`，而同预算 E 球的全部区域端点与运输相同。两个分数按相同正尺度、同校准样本与合法秩分别标定后，E 的分位不大于 T，故每个普通计数区间都包含于运输区间。独立公式复现 50,232 个存档区间，小型穷举也验证集合并不相等。
- 后续做法：先固定真实查询族，推导集合的查询支撑及分数序关系，再评价新增结构；检查是否已有计算更简单、查询等价但校准分数更小的基线。证明依赖的是端点和序关系，不因使用 CP 就成为新通用定理。
- 边界：仅针对该单位编辑成本与普通 0/1 子集查询。三格预测 `(1,0,0)`、预算 1 时，差值 `z1−z3` 在运输球为 `[0,2]`，在 E 球为 `[-1,2]`，所以不能宣称对任意线性决策也支配。非均匀补入成本、受限补入位置或分数移动成本须重新推导；E 对 global 的经验优势不是普遍支配定理。
- 证据：`ziyu24/D7_pcp_obb_foundation@1aeb4e5339d1ecd71966d565b9de5802e8f4408e` 的 `doc/2026-09-07-count-query-theory-and-review.md`、`src/count_query_mechanism_review.py`、`src/test_count_query_mechanisms.py`、`doc/2026-09-07-count-query-mechanism-evidence.json`。

## 教训十四：几何归因须控制尺度，归一化宽度也须对应部署效用

- 失败命题：global 集合相对原运输的归一化宽度优势，已经证明独有几何机制且能支持有用盘点。
- 失败原因：原两种分数使用不同的输入计数尺度。继承 global 的尺度与整数约定后，其在 90% 名义覆盖下对运输的开发优势由约 32%/16% 变为 0.158%/负 10.25%；更简单的全子集误差又比 global 窄 15.50%/14.91%，逐图 membership 相同，95% 名义设置同向。global 的原始平均宽度却大于原运输，且约 98%/99% 的主查询下界为零，平均归一化宽度较小不等于能认证非零库存或比较关系。
- 后续做法：保证新方法与强基线使用同一部署信息、尺度和离散化合同；同时报告逐图覆盖、归一化/原始宽度及实际决策证书。尺度匹配是归因对照，不能沿用未控制表格宣称几何贡献；应为新增信息提供同信息的朴素基线。
- 边界：这些数值来自同一份已反复观察的 91 图开发集，只是事后诊断，不是独立科学确认或各因素的唯一因果分解；global 无方向对照仍未知。下界为零不等于所有上界无价值，但部署收益尚未证实。已知匹配近邻和初等支撑公式也不构成独立的新颖性证明。
- 证据：`ziyu24/D7_pcp_obb_foundation@1aeb4e5339d1ecd71966d565b9de5802e8f4408e` 的 `doc/2026-09-07-count-query-theory-and-review.md`、`doc/2026-09-07-count-query-mechanism-evidence.json`、`doc/2026-09-07-primary-literature-audit.md`、`lab/result.md`。

## 方法族停止索引

| 方法族 | 最强负证据或限制 | 停止范围 | 当前 main 证据路径 |
| --- | --- | --- | --- |
| linear / π-quotient / wrapped-π | π-quotient 与 wrapped-π 在有效域单调等价 | 停止把二者包装为独立方法 | `lab/result.md`；`doc/reports/S_score_geometry_report.md` |
| matched-pair CP | 不覆盖漏检、误检、分类和匹配失败 | 只允许“条件于成功匹配”的主张 | `doc/reports/FINAL_PROJECT_REPORT.md` |
| object-level exchangeability | 两配置聚类区间约 `2.42/2.55×`，HRSC 约 `0.95×`；不能统一外推 | 停止无依据的对象 iid 推断 | `doc/reports/B0_image_cluster_exchangeability_audit.md` |
| covariance | 上游 coverage 与长度集合不一致，旧效率排序未获合法比较支持 | 撤回继承的普适负结论；先修集合定义 | `lab/result.md`；上游 score-study 的 `src/scripts/run_score_comparison.py` |
| localized / abstention | 现有局部路线未显稳定优势；拒绝牺牲保留率 | 停止无代价普适改进主张 | `lab/failed_methods.md`；`lab/result.md` |
| phase capture | 目标中介与 discordance 交集仅 30，事件总数不足 | 停止当前 phase-capture 检验；机制保持未知 | `lab/result.md`；`lab/failed_methods.md` |
| threshold post-selection | 2/3 架构没有共同非退化阈值集 | 停止当前 benchmark，不产生 coverage 结论 | `lab/result.md` |
| no-pose strong baseline | 协议要求的 adapter 不存在 | 判协议无效，不裁决方法 | `lab/failed_methods.md` |
| physical support numerics | 严格可行框越过所称外界，小面积 gap 无证书效力 | 当前自定义效率路线止损，不作所有物理方法无效的推断 | `lab/result.md`；`doc/2026-09-06-validity-evidence.json` |
| le90/le135 drift | 旧转换不满足长边 chart，正确绝对残差代数不变 | 撤回错误约定支撑的漂移机制，不泛化到所有表示 | `src/r012_validity_audit.py`；`lab/result.md` |
| finite coordinate baselines | Bonf 分位秩溢出被截断；本地 rank 与 product 边界不一致 | 撤回旧有效性/公平效率解释，不归咎已发表方法 | `src/r009_methods.py`；`src/r010_coordinate.py`；`lab/result.md` |
| DOTA evaluator equivalence | 矩形化与困难目标规则非官方合同；二因素诊断未恢复旧操作区间 | 撤回官方 AP 称谓，不重开原后选择协议；真实官方 AP 未验证 | `src/dota_semantics_probe.py`；`doc/2026-09-06-dota-semantics-evidence.json`；`lab/result.md` |
| OBB-local scene-count flow | 方向消融无增量、局部配额抬高 q；计数缺口在多数配置决定几何无关分位下界 | 停止固定主原型，不改阈值/网格/尺度/数据族挽救 | `doc/r013-b-scientific-review.md`；`doc/r013-b-image-weighted-review.json`；`src/r013_result_review.py` |
| global geometry attribution | 同尺度运输及查询充分误差基线削弱旧 W 优势，绝大多数查询下界为零 | 停止从旧比较升级独有机制/部署效用；不是所有 global 几何失败的定理 | `doc/2026-09-07-count-query-theory-and-review.md`；`doc/2026-09-07-count-query-mechanism-evidence.json` |
| unit-cost transport for indicator counts | 与 E 球普通计数端点等价且分数更大，同尺度校准后区间被 E 包含 | 不把该运输球的额外结构当普通计数增益；不扩展到有符号查询或其他编辑合同 | `src/test_count_query_mechanisms.py`；`doc/2026-09-07-count-query-theory-and-review.md` |
