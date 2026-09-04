# pcp-obb-beyond 避坑点

审计基线：`ziyu24/pcp-obb-beyond@439e415ce3ded5fd1336bc2703160f7fa40c09c9`

## PCPB-01 已被数据否定的 A2 不得在后续稿件复活

- 类型：科学证伪。
- 为何失败：早期 A2 没有获得数据支持，后续结论由 path X 取代；把 A2 混回 v5/TPAMI 叙事会重新引入错误因果链。
- 避坑：论文和交接只引用现行 path X，并把 A2 保留为失败边界。
- 边界：不影响后续 path X 与 NMS 稳定性结果。
- 证据：`ziyu24/pcp-obb-beyond@439e415ce3ded5fd1336bc2703160f7fa40c09c9` 的 `lab/failed_methods.md`、`lab/result.md`。

## PCPB-02 预测数组不能按文件名字典序猜测 image_id

- 类型：工程失败。
- 为何失败：LSKNet 原始输出按 dataset `data_infos` 顺序，而转换器按目录字典序生成 ID，导致同 ID 关联到另一张图，matched pairs 一度只有 21/93；改用真实 dataset 顺序后升至 17722/30380。
- 避坑：预测、标注和图像用稳定 ID 显式联接，并在运行前检查顺序 hash 与抽样逐项匹配。
- 边界：HRSC 恰好顺序一致不能证明多类数据也安全。
- 证据：`ziyu24/pcp-obb-beyond@439e415ce3ded5fd1336bc2703160f7fa40c09c9` 的 `doc/notes/decision_log.md`、`doc/notes/box_level_iou_audit_summary.json`。

## PCPB-03 重新执行 NMS 后的 self-consistent baseline 不能冒充旧 baseline

- 类型：范围限制。
- 为何失败：多类 OBB 的 tie ordering 使 raw+re-NMS 与 V7 原结果存在约 3pp 差异，5/6 配置无法四位对齐；横向阈值趋势可用，但绝对数不再是同一 baseline。
- 避坑：将 re-NMS 口径单独命名，报告偏差和 box-level 对齐；跨表比较必须使用同一 NMS 实现与 tie 规则。
- 边界：within-pipeline 阈值扫描仍可成立，不需要修改第三方 C++ 强求逐位复现。
- 证据：`ziyu24/pcp-obb-beyond@439e415ce3ded5fd1336bc2703160f7fa40c09c9` 的 `doc/notes/decision_log.md`、`doc/notes/bidirectional_sanity_dota_v10_r50_FAIL.json`。
