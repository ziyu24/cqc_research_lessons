# cqc_factory 避坑点

审计基线：`ziyu24/cqc_factory@feb685b757cbabb046eb8e93c2f40278a12532fd`

## FACTORY-01 工作树分支不是科研状态或第二权威源

- 类型：范围限制。
- 为何失败：Codex 为并行隔离创建的 `codex/*` 分支或 worktree 会让 `git switch main` 因 main 已被其他 worktree 占用而失败；把它解释成项目设计的专属科研分支，会制造不存在的流程状态。
- 避坑：用提交对象和 `origin/main` 判断权威性。隔离分支可以执行修改，但完成必须回到远端 `main` 可回读的提交；若当前 worktree 已在同一提交，不能仅因无法切分支判定项目异常。
- 边界：Git 自身的 worktree 占用与锁仍需遵守；本条不允许把未合入分支冒充完成。
- 证据：`ziyu24/cqc_factory@feb685b757cbabb046eb8e93c2f40278a12532fd` 的 `AGENTS.md`、`global/POLICY.md`、`doc/SIMPLE_PROJECT_SYSTEM.md`。

## FACTORY-02 最近一轮状态不能覆盖整个项目累计证据

- 类型：历史结论已推翻。
- 为何失败：接手聊天时只读取最新任务或最新失败，曾把“当前无结果/一次资产不可用”误写成整个项目没有成熟成果，导致重复研究和错误期刊判断。
- 避坑：先读项目范围、累计 `lab/result.md`、唯一当前 `lab/sug.md`，再按问题回查讨论、失败路线和提交；明确区分项目总裁决与单轮状态。
- 边界：不要求每轮扫描全部历史；已有摘要足够定位时只读相关证据。
- 证据：`ziyu24/cqc_factory@feb685b757cbabb046eb8e93c2f40278a12532fd` 的 `templates/simple/v1/files/AGENTS.md.tmpl`、`doc/SIMPLE_PROJECT_SYSTEM.md`。

## FACTORY-03 工程失败、资产缺失和科学证伪必须分型

- 类型：协议/实现无效。
- 为何失败：一次进程退出、错误数据接线、无资产或无效协议不含方法效果信息；若直接结束科学任务，会把可修工程问题永久传播成错误观点。
- 避坑：普通工程退出在同一任务内修复并重开；资产缺失只记录可用性；只有执行有效且触发冻结科学门才写科学失败。
- 边界：用户 `STOP`、结构不可实现和真实外部阻塞仍可停止，不要求无休止重试。
- 证据：`ziyu24/cqc_factory@feb685b757cbabb046eb8e93c2f40278a12532fd` 的 `global/POLICY.md`、`templates/simple/v1/files/AGENTS.md.tmpl`。

## FACTORY-04 tmpfs 可删性取决于持久重建材料而非摘要

- 类型：协议/实现无效。
- 为何失败：只在 `/dev/shm` 留代码、配置或运行入口，或只在 Home 留项目级摘要，删除后无法重建具体轮次；“Git 忽略、零进程、方法停止”都不证明可删。
- 避坑：同名 Home 主项目及远端 main 必须保存源提交、精确配置、脚本、结论和可执行重建命令；无 `RUN.json` 的遗留树默认不可删。
- 边界：可重建不要求 checkpoint 逐位相同，但必须恢复同一科学用途；无需恢复的已归档最终结果可按其证据边界处理。
- 证据：`ziyu24/cqc_factory@feb685b757cbabb046eb8e93c2f40278a12532fd` 的 `global/POLICY.md`、`doc/SIMPLE_PROJECT_SYSTEM.md`。
## FACTORY-05 checkpoint 的训练身份由精确配置决定

- 类型：历史结论已推翻。
- 为何失败：把 SHA-256 当成训练等价判据会把同配置重跑的不同权重误判为不同训练，也可能忽略不同配置的语义差异；文件哈希只能证明字节完整性。
- 避坑：用 `source_commit` 可取回的精确训练配置判断 `pth_data` 是否覆盖；配置不同必须分别保留。SHA-256 仅用于复制后和现存文件回读。
- 边界：当前归档标准保留 best 而非 last；best 无法识别时停止删除，不猜测。
- 证据：`ziyu24/cqc_factory@feb685b757cbabb046eb8e93c2f40278a12532fd` 的 `global/POLICY.md`、`doc/SIMPLE_PROJECT_SYSTEM.md`。
