# cerq 科学问题与失败教训

审计基线：`ziyu24/cerq@d223bfe8428c2230d64b91d584cc3dce52b22967`

快速阅读路径：先读“项目研究什么”→“教训一、二、三”→“方法族停止索引”。

## 项目研究什么

项目研究不重新训练检测器时，能否利用候选框与预测无关的真值栅格支持、边界和中心证据，对旋转框进行质量重排，弥补分类分数与定位质量不一致。

## 领域位置与当前结论

- **事实**：GT-rIoU oracle 在四组设置有约 `+11.2` 至 `+22.7` AP50:95 的排序空间，证明候选排序并非饱和。
- **事实**：强制 DOTA Oriented R-CNN 上，完整 CERQ 仅比 protocol closure 高约 `0.168` 点，比 absolute-only 高约 `0.009` 点，未过 1 点门。
- **事实**：独立取证复算与冻结结果逐字节一致，未发现足以解释负结果的实现错误。
- **推断**：当前支持/边界/中心特征没有提供强组件之外的独立排序信息；oracle headroom 与 feature learnability 必须分开。
- **未知**：引入新的可观测信息或学习式质量估计后能否利用 oracle 空间，不由本项目裁决。

## 实际采用过的方法

项目先用真值旋转 IoU 做 oracle 重排量化排序 headroom，再构造绝对质量、局部邻域 regret 和曲率等 CERQ 特征，在多个设置及强制 DOTA Oriented R-CNN 条件下复核，并做逐字节实现取证。

## 教训一：oracle 排序空间不等于候选特征能利用该空间

- 失败命题：真值 IoU 重排可提升约 11 至 23 个 AP 点，因此栅格证据重排也应获得显著收益。
- 失败原因：oracle 使用了目标答案，只证明现有候选中存在更优排序；它没有证明支持、边界和中心特征携带足够信息。完整 CERQ 在强制设置上仅比闭包高约 0.168 个点，比 absolute-only 高约 0.009 个点，AP50 还下降。
- 后续做法：把 oracle headroom 与特征可预测性分开，先在独立数据上验证 AUC、校准和 top-regret，再进行最终重排比较。
- 边界：大 oracle headroom 仍说明排序值得研究，但不能为任意重排特征背书。
- 证据：`ziyu24/cerq@d223bfe8428c2230d64b91d584cc3dce52b22967` 的 `docs/reports/CERQ_FINAL_NO_GO.md`、`docs/reports/STOP_2026-07-20_GATE1.md`。

## 教训二：实现缺陷排除后应接受证据特征的科学失败

- 失败命题：多项指标没有改善仍可归因于隐藏实现错误，继续修补就可能出现主效应。
- 失败原因：逐字节取证确认输入、特征、排序和评价路径与协议一致，而 AUC 增量约 0.007、风险—保留曲线无支配，说明当前证据特征没有提供足够独立排序信息。
- 后续做法：在通过实现身份审计后，把负结果归到特征假设，只有引入新的可观测信息或不同机制才重开。
- 边界：结论针对当前特征族和数据，不证明所有无需训练的质量重排都无效。
- 证据：`ziyu24/cerq@d223bfe8428c2230d64b91d584cc3dce52b22967` 的 `docs/reports/C0_FAILURE_FORENSICS.md`、`docs/reports/STOP_2026-07-20.md`。

## 教训三：复杂组合必须击败最强单组件，而不只是命名上的 closure

- 失败命题：支持、曲率和邻域 regret 合并后略高于简化 closure，就证明组合证据互补。
- 失败原因：完整 CERQ 相对 absolute-only 仅约 `+0.009` 点，几乎没有增量；把较弱对照称作 protocol closure 会夸大复杂组件的贡献。
- 后续做法：在预注册主表中加入最强单组件、同自由度组合和 oracle，并以最强可部署组件为增量基线。
- 边界：微小差异可用于误差分析，但未达门时不能支撑新方法主张。
- 证据：`ziyu24/cerq@d223bfe8428c2230d64b91d584cc3dce52b22967` 的 `docs/reports/CERQ_FINAL_NO_GO.md`、`docs/reports/STOP_2026-07-20.md`。

## 方法族停止索引

| 方法族 | 最强负证据或限制 | 停止范围 | 当前 main 证据路径 |
| --- | --- | --- | --- |
| GT-rIoU oracle | 有 `+11.2–22.7` 点 headroom，但使用真值答案 | 仅证明排序空间，不为任何候选特征背书 | `docs/reports/CERQ_FINAL_NO_GO.md` |
| absolute support | 当前最强可部署单组件，组合未显著超过 | 保留为基线，不宣称新组合收益 | `docs/reports/STOP_2026-07-20_GATE1.md` |
| curvature / regret / full CERQ | 相对 absolute-only 仅约 `+0.009` 点 | 停止当前特征族与训练外重排主线 | `docs/reports/CERQ_FINAL_NO_GO.md` |
| forensic rerun | 冻结结果逐字节复现 | 排除“隐藏实现错误”挽救理由 | `docs/reports/C0_FAILURE_FORENSICS.md` |
