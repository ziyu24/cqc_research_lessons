# pcp-obb 科学问题与失败教训

审计基线：`ziyu24/pcp-obb@f9a241f0b4c77f47b92b5559e10aef705e397175`

快速阅读路径：先读“项目研究什么”→“教训一、二、三、四”→“方法族停止索引”。

## 项目研究什么

项目研究旋转框角度的共形预测，目标是在有限样本下为已匹配预测框给出尊重 π 周期的角度集合，并检查边界与条件覆盖。

## 领域位置与当前结论

- **事实**：12 个配置中 11 个边际 coverage 位于 `[0.87,0.93]`，π 周期处理在高 fold-back 条件明显避免朴素弧退化。
- **事实**：保证仅针对成功匹配的 detection–GT pair，不覆盖漏检、误检、类别错和匹配失败；HRSC 尾部 bin 样本稀少，WSC 不稳定。
- **事实**：`s_π` 与 wrapped-π 在标准 split-CP 下单调等价。表格 AMB 路径实际退化成 split-CP 分位数，其他 CRC/LTT 命名路径主要给该阈值加罚项；不能继承原论文保证或据此宣称严格优势。
- **推断**：可保留的是一套周期安全、匹配条件明确的框架与适用域诊断，不是“首个 OBB-CP”或完整检测风险证书。
- **未知**：未匹配对象和完整场景级风险的有效联合保证尚未由该项目解决。

## 实际采用过的方法

项目比较普通线性角度残差与周期/商空间残差，在多个配置上检查边际覆盖、预测弧长度和按形状或难度分桶的最差覆盖。

## 教训一：线性角度残差不适用于周期边界

- 失败命题：把角度当作实数做绝对差，可以直接用于旋转框共形校准。
- 失败原因：等价方向在 π 边界两侧会产生接近 π 的虚假大残差，排序和预测集合因此折返或膨胀。
- 后续做法：先定义旋转框的等价类，再在商空间上计算最短周期距离，并用跨边界构造样本单测。
- 边界：若角度定义有真实有向头尾且周期为 2π，应使用相应圆周距离，而不是机械采用 π 周期。
- 证据：`ziyu24/pcp-obb@f9a241f0b4c77f47b92b5559e10aef705e397175` 的 `lab/failed_methods.md`、`lab/result.md`。

## 教训二：边际覆盖不能掩盖条件样本与小分桶问题

- 失败命题：多数配置达到总体覆盖，就足以说明所有形状和难度下都可靠。
- 失败原因：校准先按 IoU 和真值角度条件选择 matched pairs，筛选本身排除了部分大角误差；结论只对该选择条件成立。某些分桶有效样本过少，最差条件覆盖也不稳定。
- 后续做法：明确匹配条件，按图像或对象簇报告有效样本数、置信区间和条件覆盖；样本不足时不作稳定最差组结论。
- 边界：边际共形保证本来不承诺任意子群覆盖；它仍可作为清楚限定后的合法结果。
- 证据：`ziyu24/pcp-obb@f9a241f0b4c77f47b92b5559e10aef705e397175` 的 `lab/result.md`、`doc/notes/wsc_failure_hrsc_per_bin.md`。

## 教训三：单调等价的 score 不能重复计作方法贡献

- 失败命题：余弦型 π-score 与 wrapped-π 距离得到相似结果，说明提出了两个互相验证的新算法。
- 失败原因：在有效域内二者保持同一排序，split conformal 的分位数集合等价；公式不同没有产生新的统计对象。
- 后续做法：先证明 score 的序等价、集合等价和极限行为；单调等价者合并为一个方法族，只比较数值与解释性。
- 边界：可微性或计算便利仍可能影响训练和实现，但不改变标准 split-CP 的集合。
- 证据：`ziyu24/pcp-obb@f9a241f0b4c77f47b92b5559e10aef705e397175` 的 `doc/notes/c_plus_v3_5_final.md`、`doc/PROJECT_HANDOFF_REPORT_20260613.md`。

## 教训四：基线名称和罚项阶数不能代替算法与保证

- 失败命题：给 split-CP 分数阈值添加 `2/n` 或 Hoeffding 罚项，就可称为官方 CRC/LTT，并用弧长更短证明新方法严格优越。
- 失败原因：生成主表的 `amb_crc()` 直接返回 split-CP 分位数；`angelopoulos_crc()` 加 `2/n`，`ltt_crc()` 加一个平方根项，并未执行 LTT 的逐候选有效检验与多重控制。库中的另一 AMB 路径又使用 Hoeffding 项，和表格不是同一实现。风险松弛、分数阈值差与角度弧差也不同：`arc(q)=acos(1−q)` 在零附近按 `sqrt(2q)` 变化，因此 `O(1/n)` 阈值差不自动给出同阶弧长差。
- 后续做法：以真实调用链确认基线身份，逐项匹配损失、概率量词、置信水平和选择规则，再比较效率。CRC 的边际期望风险与 LTT 的高概率风险控制不能不加区分地比松紧；自定义保守基线应如实命名。
- 边界：保留周期 split-CP 的描述性结果与单调等价事实；撤回未经推导的 `O(B/n)` 弧长等价及对原始 CRC/LTT 的优越性。没有重跑合法原算法，修复后的排序未知。
- 证据：`ziyu24/pcp-obb@f9a241f0b4c77f47b92b5559e10aef705e397175` 的 `src/tools/e2_amb_crc_grid.py`、`src/pcp_obb/baselines/amb_crc.py`、`doc/notes/ambcrc_table4_data_source_verification.md`；保证形式见 [Conformal Risk Control](https://arxiv.org/abs/2208.02814) 与 [Learn then Test](https://arxiv.org/abs/2110.01052)。

## 方法族停止索引

| 方法族 | 最强负证据或限制 | 停止范围 | 当前 main 证据路径 |
| --- | --- | --- | --- |
| linear absolute angle CP | π 边界把等价方向变成近 π 残差 | 停止在线性角度轴直接校准 | `lab/failed_methods.md` |
| π-score / wrapped-π | 单调等价，产生同序集合 | 停止作为两个独立方法计贡献 | `doc/notes/c_plus_v3_5_final.md` |
| AR-Mondrian | 提高条件覆盖但稀疏 HRSC bin 方差大，弧长可能放松 | 限定到样本充足分桶，不宣称任意子群保证 | `doc/notes/wsc_failure_hrsc_per_bin.md` |
| AMB-CRC / named CRC/LTT baselines | 表格是 split-CP 与手工分数罚项，库实现另有不同；风险阶数不等于弧长阶数 | 停止对原论文算法的优势及弧长等价主张，先核算法身份 | `src/tools/e2_amb_crc_grid.py`；`src/pcp_obb/baselines/amb_crc.py` |
| matched-pair framework | 不覆盖 unmatched detection/GT 与完整场景风险 | 只允许条件 matched-pair 主张 | `doc/notes/c_plus_v3_5_final.md` |
