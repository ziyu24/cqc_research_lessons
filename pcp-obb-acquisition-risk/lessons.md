# pcp-obb-acquisition-risk 避坑点

审计基线：`ziyu24/pcp-obb-acquisition-risk@5d6768e0ee4f75c353e37bed7b543984c42af77f`

## ACQ-01 标准 RCPS/LTT 外套 acquisition 层级不产生新方法

- 类型：科学证伪。
- 为何失败：对 acquisition score 直接套风险控制或浓缩界，与既有 RCPS/LTT 的归约没有新的统计障碍；更换样本单位不构成原创。
- 避坑：必须提出 acquisition 依赖导致的新可识别量、算法或界；标准工具只作为分析层。
- 边界：RCPS/LTT 仍可用于有效应用，不能冒领为核心创新。
- 证据：`ziyu24/pcp-obb-acquisition-risk@5d6768e0ee4f75c353e37bed7b543984c42af77f` 的 `lab/failed_methods.md`、`lab/result.md`。
## ACQ-02 同一 acquisition 多帧不能制造独立样本量

- 类型：范围限制。
- 为何失败：帧内相关使有效统计单位仍是 acquisition/session；把帧数当 `n` 会产生过窄置信区间和虚假保证。
- 避坑：在 acquisition 外层做抽样和置信界，帧只在单位内聚合；明确 exchangeability 假设。
- 边界：有可验证独立采样机制时可使用更细单位。
- 证据：`ziyu24/pcp-obb-acquisition-risk@5d6768e0ee4f75c353e37bed7b543984c42af77f` 的 `doc/legacy/T0_LABEL_FREE_FAILURE_CERTIFICATE.md`。

## ACQ-03 无标签一致性只能给否决下界，不能证明安全

- 类型：范围限制。
- 为何失败：多视图高度一致仍可能共同犯错；低 disagreement 只能表示没有观察到矛盾，不能推出自然视图风险小或部署安全。
- 避坑：输出 `REJECT/NOT_FALSIFIED` 而非 `SAFE`；区分 intervention/orbit risk 与自然分布风险，额外不变性假设需单列。
- 边界：高 disagreement 在合法 label-equivariant 变换和完整 metric 下可支持单向风险下界。
- 证据：`ziyu24/pcp-obb-acquisition-risk@5d6768e0ee4f75c353e37bed7b543984c42af77f` 的 `doc/legacy/T0_LABEL_FREE_FAILURE_CERTIFICATE.md`。

## ACQ-04 Fréchet/GOSPA disagreement 的直接组合仍是已有对象

- 类型：科学证伪。
- 为何失败：Fréchet median/dispersion、GOSPA、triangle-inequality 的 `D/2` 下界和 Hoeffding 外层均有直接先验；把 OBB 代入没有形成新的 sharp 算法或理论障碍。
- 避坑：先做一般 metric-space 归约；若定理只是现成结果实例化，归入基线或应用，不继续包装。
- 边界：OBB metric 的工程实现仍可能有用，但不支撑原顶刊方法目标。
- 证据：`ziyu24/pcp-obb-acquisition-risk@5d6768e0ee4f75c353e37bed7b543984c42af77f` 的 `doc/legacy/T0_LABEL_FREE_FAILURE_CERTIFICATE.md`。

## ACQ-05 数据与标注预算不可行时不要进入 FlightShift

- 类型：资产不可用。
- 为何失败：FlightShift-OBB 需要 acquisition/scene 级元数据、独立标注和足够人工复核；当前单研究者、无标注预算无法形成可执行 T1。
- 避坑：概念筛查后立即做数据权利、元数据、独立单位和人工成本审计；不可执行时停止，不用弱 proxy 替代金标准。
- 边界：若未来获得合格 paired acquisitions 与预算，可作为新任务重新评估。
- 证据：`ziyu24/pcp-obb-acquisition-risk@5d6768e0ee4f75c353e37bed7b543984c42af77f` 的 `lab/failed_methods.md`、`lab/result.md`。
