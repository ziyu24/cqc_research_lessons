# cqc_P8 避坑点

审计基线：`ziyu24/cqc_P8@f15635f7a79386b5bf3628d2fead559bc19b7892`

## P8-01 专门化编译必须胜过同预算通用剪枝

- 类型：科学证伪。
- 为何失败：r004 Task-Compile 的 mAP50 `0.5149`，低于 Generic-Prune `0.5293`，同时参数更多、速度略慢；零训练取证不能补足这个强对照缺口。
- 避坑：专门化方法至少与同预算通用方法比较准确率、参数和延迟；被全面支配时停止。
- 边界：只否定该静态 Task-Compile 实现，不否定所有任务条件压缩。
- 证据：`ziyu24/cqc_P8@f15635f7a79386b5bf3628d2fead559bc19b7892` 的 `lab/failed_methods.md`、`lab/result.md`。

## P8-02 采集条件分数负相关时不进入压缩阶段

- 类型：科学证伪。
- 为何失败：r005 ACOR Stage-A 的 Spearman 为 `-0.161` 且 hidden-tail gate 失败，说明冻结分数没有形成所需排序信号。
- 避坑：先在无训练准入中验证排序和尾部，再授权结构搜索；信号门失败不靠后续模型调参补救。
- 边界：只限 ACOR 当前观测量和冻结数据。
- 证据：`ziyu24/cqc_P8@f15635f7a79386b5bf3628d2fead559bc19b7892` 的 `lab/failed_methods.md`、`lab/result.md`。

## P8-03 局部 fake-quant NO-GO 不能外推整机量化

- 类型：范围限制。
- 为何失败：r006 只做 bbox-head W4A4 fake quant，`weight_updates=0`；它触发 `QUOTIENT_PTQ_NO_GO`，但没有覆盖 backbone、真实硬件或迁移训练。
- 避坑：量化结论必须与实际量化范围、是否训练和硬件执行一致，不用局部零训练结果代表全模型部署。
- 边界：当前结果仍足以停止同一 quotient bbox-head 筛查。
- 证据：`ziyu24/cqc_P8@f15635f7a79386b5bf3628d2fead559bc19b7892` 的 `lab/failed_methods.md`、`lab/result.md`。

## P8-04 证据修补不是新的科学贡献

- 类型：范围限制。
- 为何失败：补齐哈希、日志、配置和取证链只能恢复结论可信度，不产生新的机制、效果或新颖性。
- 避坑：把 evidence repair 写成工程工作；科学主张仍须由有效对照和结果单独支持。
- 边界：证据完整性仍是完成条件，只是不能计作方法贡献。
- 证据：`ziyu24/cqc_P8@f15635f7a79386b5bf3628d2fead559bc19b7892` 的 `lab/failed_methods.md`。
