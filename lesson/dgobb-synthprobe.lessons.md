# dgobb-synthprobe 科学问题与失败教训

审计基线：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed`

快速阅读路径：先读“项目研究什么”→“教训一、五、六、八”→“方法族停止索引”。

## 项目研究什么

项目先研究跨域旋转检测中“源域与目标域尺度关系能否决定多尺度训练方向”，形成了 bounded scale-axis 证据；随后寻找无需大规模重训的新路线，包括单图伪标签适配、旋转轨道一致性、物理/数字探针、分布形状处方和无标签多视图风险估计。

## 领域位置与当前结论

- **事实**：固定干预在若干域对上显示 directed scale policy 可优于 uniform，但 label-free V5 方向估计只命中 2/4 可用 pair，band-response 也只命中 4/5 directed pair 并在边界失效。
- **事实**：SCM 的三种子 oracle 矩阵结果混合；DIOR-R→FAIR1M 的 SCM-global 相对 uniform 三个 paired delta 全负，不能升级为普适处方。
- **事实**：normalized factor response 的 scale/angle 原始幅度约 14.67×，但 angle 缺 matched-lineage 位移，跨因素比较门失败，原“15×机制”已撤回。
- **事实**：单图适配、无新观测的融合以及多个物理/数字载体在性能、直接归约、可识别性或数据资格上停止。
- **推断**：项目能保留的是“尺度轴存在条件性可控响应”的有限诊断，不是无标签预测方向的自动 DG 方法。
- **未知**：在新载体和独立物理观测下是否存在可识别风险路线未被一般否定；项目已停止维护，不自动重开。

## 实际采用过的方法

项目测试单图梯度适配和四视图 TTA，构造 orbit-consensus、RIVE、RayLift、Spin2、FiberID、DPIRT 与多视图风险界，并逐一审计它们是否引入了新观测、可识别假设和可执行数据载体。

## 教训一：单图伪标签梯度适配不能靠筛选超参数挽救

- 失败命题：从单张无标签目标图生成伪标签并做一步梯度更新，会比纯测试时增强更稳健。
- 失败原因：适配性能显著低于四视图 TTA，商空间直通估计的置信区间也完全为负；继续调同类阈值没有改变监督自举的核心弱点。
- 后续做法：把无需训练的强 TTA 作为最低基线，并要求伪标签适配在独立域和风险指标上提供稳定增量。
- 边界：有多帧、外部教师或少量标签时，测试时适配的信息条件不同，不能由本结果直接否定。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `lab/failed_methods.md`。

## 教训二：没有新观测的轨道融合仍是测试时增强

- 失败命题：把同一图像的旋转视图预测做轨道一致性或加权框融合，就构成新的物理或统计问题。
- 失败原因：orbit-consensus、RIVE、RayLift 和 Spin2 都只重组同一模型在确定变换下的输出，与 TTA/WBF 的已有对象直接同构，没有新增信息源或新识别结果。
- 后续做法：新路线必须指出额外可观测量、不同干预或新的理论保证；仅重新命名组合算子不作为科学贡献。
- 边界：更好的融合实现仍可能有工程收益，但新颖性需按已有 TTA 文献评价。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `lab/failed_methods.md`。

## 教训三：物理采集设想必须有可审计的数据载体

- 失败命题：把偏振、多光谱等物理变量写进框架，就足以形成可验证的跨域方法。
- 失败原因：FiberID 等方案没有闭合场景到标签的生成链，也没有可获得、可配对、可许可的数据载体；数学结构退化为已有随机有限集与鲁棒 Bayes 组合。
- 后续做法：先锁定传感器、采集协议、配对单位、标签生成和许可，再证明新观测改变了可识别集。
- 边界：未来若获得真实、配对的多物理量数据，相关问题可重新成立；当前结论是证据条件未闭合。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `doc/legacy/audits/dg_obb_2_h000005_final_scientific_decision.md`、`lab/failed_methods.md`。

## 教训四：数字探针不经过传感器链只能做合成模型选择

- 失败命题：在数字图像上施加模拟扰动并观察模型响应，可以证明真实采集条件下的行动风险。
- 失败原因：DPIRT 没有建模光学、姿态、噪声、压缩和标注过程，也没有 probe 响应到真实风险的外部桥接；结论停留在模型对人工变换的敏感性。
- 后续做法：用真实采集配对或校准实验估计数字扰动与物理变量的映射，并在独立真实域验证风险预测。
- 边界：数字探针仍适合筛选模型或发现脆弱性，不能直接当作物理因果证据。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `lab/failed_methods.md`。

## 教训五：无标签多视图输出不能识别共同漏检

- 失败命题：多个视图或检测器的预测联合分布足以估计完整真实风险。
- 失败原因：它们可能同时漏掉同一对象；相同预测分布可对应不同真值风险。条件独立假设在跨视图同源模型中不可验证，现有 RarePlanes 条件也不能补足独立金标准。
- 后续做法：报告部分识别界，或引入概率抽样人工标注和异质传感器；若使用独立性假设，必须给出外部证据和敏感性分析。
- 边界：无标签一致性可发现明确矛盾或给出风险下界，不能证明系统安全。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `lab/failed_methods.md`。

## 教训六：有方向的训练干预有效，不等于方向可由无标签 proxy 决定

- 失败命题：既然某些域对上 directed scale policy 优于 uniform，就能从目标预测分布自动选出正确方向。
- 失败原因：固定干预回答“若方向已知会怎样”，无标签选择器回答“方向能否识别”，是两个问题。V5 top-K 估计只命中 2/4 可用 pair并漏掉 FAIR1M-source 反转；band-response 也有关键错判。
- 后续做法：把 oracle intervention 与 direction estimator 分开报告；部署方法必须在未参与设计的域对上先选方向，再一次性验证结果。
- 边界：有监督或元数据明确给出尺度关系时，oracle 干预仍可作为条件策略。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `doc/legacy/audits/final_claim_consistency_099.md`、`doc/legacy/audits/label_free_sign_final_decision_101.md`。

## 教训七：跨因素“倍率”必须有共同位移单位和 matched lineage

- 失败命题：scale probe 幅度约为 angle 的 14.67 倍，因此尺度是约 15 倍更强的因果机制。
- 失败原因：scale 位移可在有效 log-sqrt-area 单位追踪，angle 却没有 matched-lineage 的目标位移；分子响应和分母干预强度不可比，倍率没有统一物理含义。
- 后续做法：比较因素前冻结同一响应、可追溯干预位移和匹配数据 lineage；任一因素缺项就只报告各自响应，不排序机制强弱。
- 边界：原始响应幅度仍可说明当前 probe 中 scale 变化更大，但不能解释为机制倍率。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `doc/legacy/audits/normalized_factor_response_decision_098.md`。

## 教训八：oracle 分布处方结果混合时不能替换更窄但稳健的结论

- 失败命题：SCM 根据尺度分布形状给出若干正结果，因此可以升级为跨域普适 prescription，并取代 bounded scale-axis 诊断。
- 失败原因：三种子矩阵不是全局支配；DIOR-R→FAIR1M 的 SCM-global 相对 uniform 三个 paired delta 均为负，另有 pair 的符号混合。选择正 cell 会忽略明确反例。
- 后续做法：报告 pair-level 矩阵和反例，把 SCM 定位为 oracle stress test；只有预注册跨域成功率与最坏情况门均通过才升级处方。
- 边界：SCM 在若干 pair 上可能有效，负结论针对 universal upgrade，不抹去条件正结果。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `doc/legacy/audits/scm/scm_final_decision.md`、`doc/legacy/audits/final_claim_consistency_099.md`。

## 方法族停止索引

| 方法族 | 最强负证据或限制 | 停止范围 | 当前 main 证据路径 |
| --- | --- | --- | --- |
| single-image adaptation | 明显低于 four-view TTA，quotient-ST 区间为负 | 停止当前伪标签一步适配与阈值微调 | `lab/failed_methods.md` |
| orbit-consensus / RIVE | 无新增观测，只是 TTA/pullback/WBF 重组 | 停止方法新颖性主张 | `lab/failed_methods.md` |
| RayLift / Spin2 / FiberID / DPIRT | 直接组合、90° 歧义、载体不闭合或数字到物理风险不可识别 | 停止当前物理/数字探针路线 | `lab/failed_methods.md` |
| MV-Risk | 相同预测联合分布兼容相反真值风险 | 停止无标签完整风险点估计 | `lab/failed_methods.md` |
| label-free scale direction | V5 仅 2/4，band probe 关键 pair 失败 | 停止自动方向选择主张 | `doc/legacy/audits/final_claim_consistency_099.md` |
| normalized factor ranking | angle 缺 matched-lineage 位移 | 撤回“约 15×机制倍率” | `doc/legacy/audits/normalized_factor_response_decision_098.md` |
| SCM prescription | 三种子 oracle 结果混合且有全负反例 | 停止普适处方升级；保留 bounded 诊断 | `doc/legacy/audits/scm/scm_final_decision.md` |
