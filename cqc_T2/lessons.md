# cqc_T2 避坑点

审计基线：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e`

## T2-01 开发期正 headroom 必须接受冻结轨迹外验证

- 类型：科学证伪。
- 为何失败：Oracle V3 开发期 dynamic headroom 为 `+0.005633` mAP 且 CI 跨零；冻结后的 trajectory-3 上最佳固定动作反而为 `-0.028984`，没有候选通过双 replay 与 equal-wall 合取门。
- 避坑：开发结果只用于冻结候选，最终裁决必须来自未用于选择的轨迹和等墙钟终点；局部正点不能覆盖整体负结果。
- 边界：不否定所有动态控制，只停止该候选集合。
- 证据：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 的 `lab/result.md`、`work_dirs/oracle_v3/ORACLE_V3_DECISION.md`。

## T2-02 DDP 提前结束时 rank-0 单独保存会破坏 collective 顺序

- 类型：工程失败。
- 为何失败：首个 equal-wall hook 仅 rank 0 直接保存原始 state_dict，缩短 loop 后不同 rank 的 teardown/collective 顺序不一致，造成非科学退出。
- 避坑：所有 rank 广播同一 stop decision，并走框架 collective-safe checkpoint 路径；工程失败不计入科学矩阵。
- 边界：适用于 DDP 缩短循环，不要求单卡任务增加分布式同步。
- 证据：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 的 `lab/failed_methods.md`。

## T2-03 局部融合单测通过不能证明完整 detector exact

- 类型：协议/实现无效。
- 为何失败：partition-transparent 路线的局部/融合测试 bit-exact，但真实 detector 的普通 tile 六条件 final set 均不等于 native，完整 L1--L4 结果为零。
- 避坑：exact compiler 必须在真实完整图和最终 boxes/scores/order 上验证，不以模块单测替代端到端等价。
- 边界：单测仍能定位组件，不是方法结论。
- 证据：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 的 `lab/result.md`、`work_dirs/partition_transparent_closure/TOP_JOURNAL_DECISION.md`。

## T2-04 显存下降但输出不等价且延迟暴增不构成有效 compiler

- 类型：科学证伪。
- 为何失败：完整 global barrier 后 regional PAFPN 仍有 shape-dependent FP32 差异，8/8 L3/L4 不相等；虽峰值显存降约 73%，decode/NMS 前最低单次已慢 `6.08×`。
- 避坑：精确性、显存、端到端速度和完整图均为合取门；禁止只报最有利资源指标。
- 边界：只否定冻结 RTMDet exact partition 实现。
- 证据：`ziyu24/cqc_T2@2a5998027fd06309a345beb08820194bea26a98e` 的 `lab/result.md`、`work_dirs/rtmdet_full_global_barrier/FULL_GLOBAL_BARRIER_DECISION.md`。
