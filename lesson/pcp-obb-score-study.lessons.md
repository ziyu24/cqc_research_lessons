# pcp-obb-score-study 科学问题与失败教训

审计基线：`ziyu24/pcp-obb-score-study@0df97a23936c0893704f8cf03c652625522060f9`

快速阅读路径：先读“项目研究什么”→“教训一、二”→“方法族停止索引”。本次复核修正的是比较协议与外推，不把旧表格换成新的方法胜负。

## 项目研究什么

项目研究训练损失使用的旋转框几何是否也适合作为共形 nonconformity score，目标是同时获得合法覆盖、短角度弧和较好的最差条件覆盖。

## 领域位置与当前结论

- **事实**：旧表报告四类协方差分数的 Mean Arc 比 `s_π` 大约 `75%–1378%`，KL 约大 `256%`，最佳固定混合约大 `63%`。这些是原程序输出，不等于已验证的同覆盖效率比较。
- **事实**：主比较与构造性修正代码用真实宽高计算 calibration/validation score，却用预测宽高固定两侧来计算角度弧；所报 coverage 与 Mean Arc 不是同一个集合的两个指标。形状分桶只作事后 coverage 诊断，主程序并非逐桶校准。
- **推断**：此前据此停止所有 angle-only 协方差路线的表述过强；当前首先失效的是集合定义与评价的一致性。
- **未知**：统一可部署集合、校准和覆盖事件后，各分数的实际效率排序未知；原数字不能裁决完整 angle-shape 集合。

## 实际采用过的方法

项目比较周期角度分数、协方差距离、KL 类分数，以及尺度归一化、回归混合和按形状调整的构造，评估平均弧长与近方形目标的条件覆盖。

## 教训一：coverage 与长度必须评价同一个预测集合

- 失败命题：对真实框 score 做共形校准，再固定预测形状反演角度弧，就自动得到了具有同一覆盖保证的 angle-only 集合。
- 失败原因：校准和 coverage 含真实形状误差，弧的 membership 却去掉该误差。可直接用源码复算：Frobenius 分数在预测 `(w,h,θ)=(2,1,0)`、真值 `(3,1,0)`、阈值 `q=1` 时为 `5>q`，被 coverage 计为未覆盖；同一真值角在所报弧中分数为 `0≤q`，却被包含。因而 coverage 与弧长不能配对解释；后续三种修正沿用这一问题。
- 后续做法：先写出只依赖部署可用输入的集合 `C(x)`，再以 `真值∈C(x)` 计算覆盖并以同一 `C(x)` 计算长度。可以研究联合框集合及其角度投影，也可以定义真正的 angle-only score，但不能在校准和反演间悄悄替换未知形状。
- 边界：此反例否定指标对应关系，不是重跑后的排序结论。用真实形状构造的 oracle 只能诊断形状混杂，不能替代部署保证；旧表暂不能支持“同覆盖下某类分数必然更差”。
- 证据：`ziyu24/pcp-obb-score-study@0df97a23936c0893704f8cf03c652625522060f9` 的 `src/scripts/run_score_comparison.py`、`src/scripts/s1_constructive_solution.py`、`src/scripts/p1_1_oracle_12cfg.py`、`src/pcbobb_score/scores/sigma_frobenius.py`。

## 教训二：协方差表示的退化不等于物理方向完全不可识别

- 失败命题：近方形的协方差角度敏感度退化，足以证明物理方框的所有角度都无区别；名称含 Bures 的实现也自然等同于 Bures/W2 距离。
- 失败原因：`Σ=R diag(w²,h²) Rᵀ` 在 `w=h` 时对任意旋转不变，但真实正方形只对 90° 整数倍旋转等价，45° 通常改变其占据区域。丢失的是该表示的信息，不能直接上升为物理不可识别定理。此外源码 `sigma_bures` 实际计算平方根矩阵的 Frobenius 距离，一般不等于另行实现的 Bures/W2 距离。
- 后续做法：区分标注参数对称性、真实几何对称性与有损表示不变性；以公式和构造样本核对方法身份，再讨论分数对角度、尺度的耦合。
- 边界：近方形方向敏感度弱仍是有用诊断，但其物理、统计含义取决于目标定义和观测噪声；不据此否定所有协方差方法。
- 证据：`ziyu24/pcp-obb-score-study@0df97a23936c0893704f8cf03c652625522060f9` 的 `src/pcbobb_score/scores/_common.py`、`src/pcbobb_score/scores/sigma_bures.py`、`src/pcbobb_score/scores/sigma_frobenius.py`。

## 教训三：重复划分、分桶诊断与不显著差异不能扩大保证

- 失败命题：12 配置×5 seed、形状分桶和未显著不同的 WSC，足以分别证明独立复现、条件覆盖保证及两方法等效。
- 失败原因：这里的 seed 主要重划分固定预测文件，不是独立训练；配置共享数据或检测器，也不能当作完全独立重复。主程序用全局分位数后按形状报最差桶，未提供每桶的校准保证；KL 的差异不显著更不等于通过等效检验。
- 后续做法：明确重复来自训练、数据采集还是划分，按相应单位配对；条件覆盖另行定义和验证；等效性须预先给容差及相应区间。首先修复教训一，再比较简单周期分数与复杂构造的覆盖、长度和代价。
- 边界：多配置和重复划分仍能描述当前固定资产上的稳定性；旧表可以作为需复核的线索，不能当作修复后方法的负证据。
- 证据：`ziyu24/pcp-obb-score-study@0df97a23936c0893704f8cf03c652625522060f9` 的 `src/scripts/run_score_comparison.py`、`src/scripts/s1_constructive_solution.py`、`doc/paper/paper_zh_v5.md`。

## 方法族停止索引

| 方法族 | 最强负证据或限制 | 停止范围 | 当前 main 证据路径 |
| --- | --- | --- | --- |
| Frobenius / square-root Frobenius / W2 | coverage 与角度弧反演使用不同形状；存在 membership 反例 | 撤回同覆盖效率优劣裁决；先统一集合后再评估 | `src/scripts/run_score_comparison.py`；`src/pcbobb_score/scores/_common.py` |
| KL score | 历史弧长约 `+256%`，但同样受集合不一致限制；不显著不是等效 | 不以旧表裁决整体优劣或条件覆盖保证 | `src/scripts/run_score_comparison.py`；`doc/paper/paper_zh_v5.md` |
| normalized / regularized covariance | 旧程序无更紧配对，但继承同一评价问题 | 停止当前效率主张，不扩大为方法族不可能 | `src/scripts/s1_constructive_solution.py` |
| r-aware fixed mixing | 历史最好约 `+63%`，不是已验证的同覆盖代价 | 与其他候选一起修复协议后才能裁决 | `src/scripts/s1_constructive_solution.py` |
| true-shape oracle | 使用部署时未知的真实形状 | 仅作诊断，不继承可部署覆盖保证 | `src/scripts/p1_1_oracle_12cfg.py` |
