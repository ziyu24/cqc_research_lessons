# pcp-obb-acquisition-risk 科学问题与失败教训

审计基线：`ziyu24/pcp-obb-acquisition-risk@5d6768e0ee4f75c353e37bed7b543984c42af77f`

快速阅读路径：先读“项目研究什么”→“教训一、三、四”→“方法族停止索引”。

## 项目研究什么

项目研究遥感采集批次层级的旋转检测风险控制，试图在少标签或无标签条件下，利用多帧、多检测器或采集元数据判断一次飞行是否安全可用。

## 领域位置与当前结论

- **事实**：项目只完成零训练的新颖性、可识别性与资源审计，没有 GPU 实验。
- **事实**：把完整 acquisition 当独立原子后，RCPS/LTT/CRC 可直接处理任意组内依赖；用帧数增加有效样本则必须引入已有 hierarchical/trajectory 假设。
- **事实**：无标签多检测器风险在 arbitrary common miss/bias 下不可识别；自适应、post-selection 和 structured-output 候选又分别归约到已有工作。
- **事实**：FlightShift 需要多次采集、约万级穷尽 OBB 与双人 QA，和单研究者、零标注预算直接冲突。
- **推断**：该仓库的价值是及时停止伪新颖或不可执行的问题，而不是一个失败算法。
- **未知**：未来资源变化或提出 CSP/CRC 不能表达的新 estimand 时可重新审计，但不得继承旧新颖性主张。

## 实际采用过的方法

项目审查 acquisition-level RCPS/LTT、无标签多检测器一致性、Fréchet 界、GOSPA 集合距离、capture-recapture/随机有限集建模，以及需要大规模新采集与双重标注的 FlightShift 方案。

## 教训一：改变统计单位不自动产生新方法

- 失败命题：把标准 RCPS 或 LTT 从图像层改名为 acquisition 层，就形成新的风险控制理论。
- 失败原因：若损失、交换单位和保证形式没有实质变化，方法仍是既有群组共形或风险控制；应用层名称不构成新定理。
- 后续做法：明确采集层带来的新依赖、干预或决策约束，并证明现有方法不能直接覆盖，才建立新问题。
- 边界：在真实飞行批次上验证已有方法仍可形成重要应用研究，但应准确定位贡献。
- 证据：`ziyu24/pcp-obb-acquisition-risk@5d6768e0ee4f75c353e37bed7b543984c42af77f` 的 `lab/failed_methods.md`、`lab/result.md`。

## 教训二：同一采集中的多帧不是独立样本量

- 失败命题：一次飞行产生许多图像，就可以把它们都当独立样本获得很窄的风险界。
- 失败原因：帧共享天气、传感器、航线和场景，簇内相关使名义样本数远大于有效独立采集数。
- 后续做法：以 acquisition 为交换与划分单位，采用簇级校准或层次模型，并报告采集数而非仅报告帧数。
- 边界：跨采集随机化或能证明条件独立时，可利用帧级信息提高效率，但不能忽略层级结构。
- 证据：`ziyu24/pcp-obb-acquisition-risk@5d6768e0ee4f75c353e37bed7b543984c42af77f` 的 `doc/legacy/T0_LABEL_FREE_FAILURE_CERTIFICATE.md`。

## 教训三：无标签一致性不能证明系统安全

- 失败命题：多个模型或视图高度一致，即可上界真实漏检和总体风险。
- 失败原因：所有系统可以共同漏掉相同对象；同一预测联合分布兼容相反的真实风险。引入条件独立、固定检出率等假设后，问题又落入已有 capture-recapture、记录链接或随机有限集框架。
- 后续做法：把无标签一致性用于发现冲突或风险下界；完整风险需要独立抽样标注、异质传感器或经外部验证的识别假设。
- 边界：强不一致可以证明至少一个预测源有问题，但高一致不等于正确。
- 证据：`ziyu24/pcp-obb-acquisition-risk@5d6768e0ee4f75c353e37bed7b543984c42af77f` 的 `doc/legacy/T0_LABEL_FREE_FAILURE_CERTIFICATE.md`。

## 教训四：数据预算不可行应在方法设计前暴露

- 失败命题：依赖约一万实例与双重标注的新采集基准，可以在单人、零新增预算条件下作为近期主线。
- 失败原因：采集、配准、实例 OBB 和复核成本与资源约束直接冲突；继续优化方法不能补足不存在的识别数据。
- 后续做法：在立项时列出最小样本、标注者、许可、传感器和质控成本，无法满足就缩小 estimand 或选择现有数据能回答的问题。
- 边界：这是项目可行性否决，不是 FlightShift 科学假设的负证据；获得资源后可以重新评估。
- 证据：`ziyu24/pcp-obb-acquisition-risk@5d6768e0ee4f75c353e37bed7b543984c42af77f` 的 `lab/failed_methods.md`、`lab/result.md`。

## 方法族停止索引

| 方法族 | 最强负证据或限制 | 停止范围 | 当前 main 证据路径 |
| --- | --- | --- | --- |
| acquisition-level RCPS/LTT | 完整 acquisition 作为 IID 原子后为现有定理直接应用 | 停止 theorem novelty；可保留应用验证 | `doc/reports/T0_NOVELTY_REVIEW.md` |
| acquisition-aware evaluation | temporal/spatial leakage、cluster bootstrap 与排序敏感性已有直接近邻 | 停止只换 OBB/采集名称的贡献 | `doc/reports/PIVOT_T0_ACQUISITION_AUDIT_REVIEW.md` |
| unlabeled multi-detector risk | 共同漏检、共同偏差与 unknown linkage 导致不可识别 | 停止完整风险点估计 | `doc/reports/T0_UNLABELED_MULTI_DETECTOR_RISK_REVIEW.md` |
| adaptive / post-selection / structured output | 分别归约为 adaptive conformal、selective/weighted control 与 CSP | 停止现有组合路线 | `doc/reports/T0_ADAPTIVE_MODEL_AND_STRUCTURED_OUTPUT_REVIEW.md`；`doc/reports/T0_POST_SELECTION_STRUCTURED_DISCOVERY_REVIEW.md` |
| FlightShift | 采集与双重标注规模和现有资源不相容 | 判当前资源 NO-GO，不裁决科学假设 | `doc/reports/T1_FLIGHTSHIFT_RESOURCE_REVIEW.md` |
