# cqc_P4 避坑点

审计基线：`ziyu24/cqc_P4@0719847bfbc1b49f4e4d5254685bf0e6b318fb2c`

## P4-01 合成算术复现不能直接裁决真实检测机制

- 类型：范围限制。
- 为何失败：NumPy 对 FAA 发布算术的扫描发现发布实现与论文公式差异，并触发 `FAIL_RELEASED_IMPLEMENTATION`；但它没有运行真实 MMRotate 模型或遥感特征，因此不能证明 FAA 在真实微小目标上退化，也不能否定论文检测结果。
- 避坑：分别命名“发布实现算术”“论文公式控制”“真实模型效果”，只把每项证据用于它实际覆盖的层级。
- 边界：合成扫描仍可作为实现准入和反例生成器。
- 证据：`ziyu24/cqc_P4@0719847bfbc1b49f4e4d5254685bf0e6b318fb2c` 的 `research/EVIDENCE.md`、`research/FAA_GATE0_RESULTS.md`。

## P4-02 工程可辨识或静态 PASS 不是方法收益

- 类型：协议/实现无效。
- 为何失败：若干门只证明 proposal seed 会改变输出集合、接口可运行或工程量可辨识；它们没有完成 base-only 模型、held-out AP、C1/C2 或论文主张所需的真实训练与评估。
- 避坑：每个前置门都明确“只授权下一步”，禁止把可执行、可区分、测试通过写成科学增益。
- 边界：前置门可以淘汰实现，但通过不代表后续门也通过。
- 证据：`ziyu24/cqc_P4@0719847bfbc1b49f4e4d5254685bf0e6b318fb2c` 的 `research/ovod_angle_risk/EVIDENCE.md`、`research/OVOD_GATE1A0_RESULTS.md`。

## P4-03 临时产物和同源自报不能形成独立验收

- 类型：协议/实现无效。
- 为何失败：部分运行把事件、标签实体或 JUnit 留在临时目录并在异常后清理；接收端只能看到汇总字段，无法绑定实际命令、测试集合和原始事件。主实现与“独立验证”复用同一候选表也不能形成独立性。
- 避坑：先持久化最小原始事件、输入/实现提交和测试 provenance，再生成汇总；独立验证必须重建关键集合而非只验输出格式。
- 边界：不要求提交大型运行产物，但决定裁决的小证据必须可回读。
- 证据：`ziyu24/cqc_P4@0719847bfbc1b49f4e4d5254685bf0e6b318fb2c` 的 `research/ovod_angle_risk/EVIDENCE.md`、`CODEX_HANDOFF.md`。

## P4-04 隐藏标签隔离必须在首次读取前结构化成立

- 类型：协议/实现无效。
- 为何失败：仅由样例函数或结果字段自报“C 不可达”，而真实 resolver 仍能访问隐藏标注；先读取再写 ledger、失败后删除临时 claim，也不能证明 single-use test 未泄漏。
- 避坑：在 open 前建立 denyset/broker、持久 claim 与 attempt journal；把读取权限、对象 lineage 和失败路径纳入可重放测试。
- 边界：该要求针对会影响确认性结论的隐藏标签，不扩展成普通开发数据的审批流程。
- 证据：`ziyu24/cqc_P4@0719847bfbc1b49f4e4d5254685bf0e6b318fb2c` 的 `research/ovod_angle_risk/EVIDENCE.md`、`server_result.md`。
