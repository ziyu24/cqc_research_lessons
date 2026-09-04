# cqc_P7 避坑点

审计基线：`ziyu24/cqc_P7@6451a708401384a52fd95a0edaf7dcf92e7a9378`

## P7-01 对称退化不能包装成目标非对称反例

- 类型：科学证伪。
- 为何失败：NuWa/CIFAR 的 anchor 与 `prune_40` 分别下降约 `6.05/5.95` 点，masking gap 为零且没有通过点；它没有形成预期的 head-mask 非对称反例。
- 避坑：反例必须直接通过冻结的不对称判据；两个臂一起退化只说明共同脆弱性，不说明目标机制。
- 边界：只限 r009 的模型、数据和 mask 定义。
- 证据：`ziyu24/cqc_P7@6451a708401384a52fd95a0edaf7dcf92e7a9378` 的 `lab/failed_methods.md`、`lab/result.md`。
