# D7_pcp_obb_foundation 科学问题与失败教训

> 使用边界：教训须结合适用条件与原始证据使用，同条件下的有效反证不能忽略，也不能跨条件自动否决新研究；来源不可访问时须注明“未独立核实”，不得将摘要当作已核实的原始证据。

审计基线：当前主线 `ziyu24/D7_pcp_obb_foundation@fb71ec02c97a48d16e66710d8caec83d0646e457`。最新提交只修改数值实现，尚无新增已提交结果；不凭任务单推断实时运行状态，也不让旧归档稿覆盖已重开的物理表示审计。

快速阅读路径：先读“项目研究什么”→“教训一、二、三、八”→“方法族停止索引”。

## 项目研究什么

项目研究旋转框方向不确定性的共形预测：在角度具有 π 周期、近方形目标方向弱可识别且同一图像多对象相关时，如何给出有限样本覆盖保证、有效预测弧和选择性拒绝。

## 领域位置与当前结论

- **事实**：π 周期分数、匹配条件覆盖和图像簇交换性已得到较充分审计，但分数单调等价、匹配选择偏差和对象伪重复显著收缩了可主张范围。
- **事实**：phase-capture 路线中，真正输入暴露切换虽有 464 个样本，和检测 discordance 重叠仅 30 个；全局 discordance 也只有 38 个，无法支撑预注册分析。
- **事实**：阈值后选择 benchmark 在 3 个架构中有 2 个无法在 `FPI≤2` 下提供至少 5 个阈值，故没有 coverage 结果；一个要求不存在 adapter 的强基线协议同样无效。
- **事实**：最新物理表示数值审计已修复稀疏 Sobol/rejection 实现，但 256 个方向的 inner/outer gap 仍为约 `1.199%–1.557%`，超过 `<1%` 门；当前更高方向数任务尚无结果。
- **推断**：数值支持未收敛只说明计算证书未闭合，不能作为某个科学方法的负证据。
- **未知**：物理表示相对基线的效率/覆盖比较尚未运行，最终科学效果未知。

## 实际采用过的方法

项目比较线性角度残差、π 商空间残差、wrapped-π 分数、协方差几何分数、按图像聚类的共形校准、形状条件化与局部化校准，并评估近方形诊断和选择性 abstention。

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

## 教训八：数值支持未收敛不是科学负结果

- 失败命题：方向离散、Sobol 候选或 hull 边界误差超过阈值，说明物理表示方法本身无效。
- 失败原因：早期 rejection 平均只接受约 2.60–3.55 个候选/图，面积变化达约 2.73%–6.02% 且命中边界，数值支撑不合法；改用直接支持和解析乘积后 synthetic truth 通过，但 256 方向的 inner/outer gap 仍约 `1.199%–1.557%`，只表明误差证书尚未闭合，物理比较根本没有运行。
- 后续做法：先通过冻结的数值误差与边界门，再比较表示效率；不得靠删难例、只报 aggregate 或把方向数增加本身写成方法改进。
- 边界：最新任务单要求检验更高方向数和保守区间端点，但尚无已提交结果；按冻结误差标准增加数值分辨率是合法修复，不是规避门槛。方法效果保持未知。
- 证据：`ziyu24/D7_pcp_obb_foundation@1f4092fd5ebb8ea0f4479b5e1e01a28f27aacece` 的 `lab/result.md`、`lab/failed_methods.md`、`lab/sug.md`。

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
| physical support numerics | 早期 sparse hull 非法；修复后 256 方向误差仍超 1% | 数值门未闭合，不得写成科学负结果；当前任务待定 | `lab/result.md`；`lab/sug.md` |
