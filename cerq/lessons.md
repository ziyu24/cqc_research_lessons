# cerq 避坑点

审计基线：`ziyu24/cerq@d223bfe8428c2230d64b91d584cc3dce52b22967`

## CERQ-01 Oracle headroom 不是候选方法的有效性

- 类型：科学证伪。
- 为何失败：Gate 0 证明检测分数存在明显质量排序余量，但冻结的 CERQ 在 DOTA × Oriented R-CNN 上相对最强 closure 只增 `+0.168` AP50:95 点，远低于 `+1.0`，相对 absolute-only 仅 `+0.009`；尾部和 risk-retention 门也未同时通过。
- 避坑：把“问题有上界空间”和“具体方法兑现空间”设为独立门；oracle 通过绝不能为候选方法背书。
- 边界：否定的是固定框、quality-only、冻结证据与邻域下的 CERQ，不否定质量排序问题或 box refinement。
- 证据：`ziyu24/cerq@d223bfe8428c2230d64b91d584cc3dce52b22967` 的 `docs/reports/CERQ_FINAL_NO_GO.md`、`docs/reports/STOP_2026-07-20_GATE1.md`。

## CERQ-02 已排除实现缺陷的多门失败不得降格续命

- 类型：科学证伪。
- 为何失败：有界法证复算使特征生成与评估逐字节一致，且 AP、排序、低质高分尾部和风险保留同时失败；没有足以跨过预注册阈值的实现缺陷。
- 避坑：失败法证只排查能改变裁决的实现问题；确认科学失败后，不把项目改名为 PQA+local search，不加新 head/loss、不在确认集扩大邻域或放宽阈值。
- 边界：早期 baseline 路径缺失是已解决的非科学阻塞，不得与最终 Gate 1 NO-GO 混为一谈。
- 证据：`ziyu24/cerq@d223bfe8428c2230d64b91d584cc3dce52b22967` 的 `docs/reports/C0_FAILURE_FORENSICS.md`、`docs/reports/STOP_2026-07-20.md`。
