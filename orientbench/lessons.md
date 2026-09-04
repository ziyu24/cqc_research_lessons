# orientbench 避坑点

审计基线：`ziyu24/orientbench@ea337b2d6df813c5460f1a3db844ce2802b8ba09`

## ORIENTBENCH-01 单轮状态不能覆盖项目累计成果

- 类型：历史结论已推翻。
- 为何失败：近期 r007--r011 多为资产/执行审计，但项目早已建立六个受控扰动单元、几何风险、人工双标和评价器闭环；把最新 `ASSET_UNAVAILABLE` 或 `INCONCLUSIVE` 写成“项目没有成果”会抹掉有效主结果。
- 避坑：接手先读 `lab/result.md` 的全项目总裁决，再定位当前轮；裸 `rNNN` 还需区分归档序列与当前序列。
- 边界：累计成果不自动让新方法或顶刊扩展通过。
- 证据：`ziyu24/orientbench@ea337b2d6df813c5460f1a3db844ce2802b8ba09` 的 `lab/result.md`、`lab/discussion.md`。

## ORIENTBENCH-02 AP50 不变不能说明方向误差无害

- 类型：范围限制。
- 为何失败：只改变方向的构造扰动在六单元 AP50 完全不变，却令 AP75 下降约 `0.176--0.398`、角误差增加约 29--32°；低 IoU 指标会掩盖方向质量。
- 避坑：方向研究至少报告高 IoU、轴向角误差和独立下游终点，不能只看 AP50。
- 边界：这是构造性几何后果，不等于现实独立决策损失已成立。
- 证据：`ziyu24/orientbench@ea337b2d6df813c5460f1a3db844ce2802b8ba09` 的 `lab/result.md`。

## ORIENTBENCH-03 操纵有效性失败时低效应不能触发机制 KILL

- 类型：协议/实现无效。
- 为何失败：COI r004/r005 的八个 `DeltaY` 都不大，但真实 clean-high 操纵门八格失败，且 noise scale、bootstrap 分母有缺陷；结果只能是 `INCONCLUSIVE_PROTOCOL_VALIDITY`。
- 避坑：按“操纵有效→非坍塌→主效应”顺序裁决；前置操纵失败时不把低效应写成方法或信息论否定。
- 边界：也不得通过重选剂量、删除对象或换模型挽救同一轮。
- 证据：`ziyu24/orientbench@ea337b2d6df813c5460f1a3db844ce2802b8ba09` 的 `lab/failed_methods.md`、`lab/result.md`。
## ORIENTBENCH-04 融合选择恒等于 raw 时没有方法增量

- 类型：科学证伪。
- 为何失败：GR-EQS 在三个数据集的非劣门失败，18 组均选 `lambda=0`，fusion 与 raw 恒等；正式接受总体还发生 cohort 漂移。
- 避坑：先验证非恒等选择率和固定总体；最优解总是 identity 时停止融合主张，不缩 cohort 或改 gate。
- 边界：不外推所有风险控制无效。
- 证据：`ziyu24/orientbench@ea337b2d6df813c5460f1a3db844ce2802b8ba09` 的 `lab/failed_methods.md`、`lab/result.md`。

## ORIENTBENCH-05 已消费路线不能靠换名、阈值或新 selector 复活

- 类型：科学证伪。
- 为何失败：Q-SetOD、OER、SAUR、AHC、P2C、CORA、PEF 及 PSC repair 已分别失败、漂移或无集合 witness；外部 RotatedFCOS-PSCD 上 PSC 候选为 0/24。
- 避坑：新候选必须改变可观测量、干预或推断对象，并超过同预算 VM-NLL/AQE 等强基线；不再枚举小 selector、角度 quality head 或标量 TTA 融合。
- 边界：各路线的局部诊断事实可保留，不能重命名成新贡献。
- 证据：`ziyu24/orientbench@ea337b2d6df813c5460f1a3db844ce2802b8ba09` 的 `lab/failed_methods.md`、`lab/result.md`。

## ORIENTBENCH-06 执行总体保留门失败不是 TAL 科学失败

- 类型：协议/实现无效。
- 为何失败：r006 的 ORCNN stride-8 若干 y shift 只保留约 `88.49--89.68%`，低于逐 shift 90% 门；parity 与复算通过也不能补足总体有效性。
- 避坑：标记 `INCONCLUSIVE_EXECUTION_VALIDITY`，不改 padding、margin 或阈值重开已查看的 official test。
- 边界：不能据此声称不存在 translation-to-angle leakage。
- 证据：`ziyu24/orientbench@ea337b2d6df813c5460f1a3db844ce2802b8ba09` 的 `lab/failed_methods.md`、`lab/result.md`。

## ORIENTBENCH-07 当前主机无资产不等于官方资产不存在

- 类型：资产不可用。
- 为何失败：r007/r009 的合格结论只说明冻结主机数据根没有候选资产；RarePlanes 官方资源仍存在。资产 token 不含方法效果，也不能外推互联网或其他主机。
- 避坑：可用性结论绑定主机、候选范围和时间；科学结论单独裁决。
- 边界：后续资产落地需新任务，不能把旧不可用 token 改写成方法失败。
- 证据：`ziyu24/orientbench@ea337b2d6df813c5460f1a3db844ce2802b8ba09` 的 `lab/result.md`。

## ORIENTBENCH-08 标识符科学计数法损坏可制造虚假 component 不足

- 类型：历史结论已推翻。
- 为何失败：RarePlanes metadata 的 26 行 `cat_id` 被科学计数法破坏，直接 union 后得到 83 components；用 image_id 后缀、GeoJSON CAT 和影像键唯一约束恢复后为 102，旧停止理由失效。
- 避坑：ID 始终按字符串读取；数值化前验证格式、唯一性和多源一致性，并用独立实现重建 component。
- 边界：102 只是 footprint 合并前数量，未闭合真实 COG overlap，不能直接升级 READY。
- 证据：`ziyu24/orientbench@ea337b2d6df813c5460f1a3db844ce2802b8ba09` 的 `lab/failed_methods.md`、`lab/result.md`。

## ORIENTBENCH-09 证据修复必须绑定实际执行和冻结 split

- 类型：协议/实现无效。
- 为何失败：r011 发布产物与登记源码、结束时间和位置矛盾；component key 从 lexical 改 numeric 后重新随机化 split，且 lineage、支持门、footprint 双实现和严格模型 load 均未闭合。
- 避坑：产物绑定执行提交、命令和时间；修复 identity 时恢复事前 split，不在多个 split 中择优；独立验证不得复用主实现候选表。
- 边界：r011 未读取 H1/H2 outcome，因此既不是资产最终失败也不是科学失败。
- 证据：`ziyu24/orientbench@ea337b2d6df813c5460f1a3db844ce2802b8ba09` 的 `lab/failed_methods.md`、`lab/result.md`。
