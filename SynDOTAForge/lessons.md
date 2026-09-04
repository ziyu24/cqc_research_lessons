# SynDOTAForge 避坑点

审计基线：`ziyu24/SynDOTAForge@79976ce1773fbdf9ae1c909d4f7e48347e9c1703`

## SYNDOTA-01 几何与格式正确不能替代视觉真实感

- 类型：科学证伪。
- 为何失败：material-only 和 procedural 生成多次通过 mask/OBB/格式检查，却反复未通过人工视觉门；它们只能证明管线有效，不能证明合成图像可用于真实遥感检测。
- 避坑：自动 QA 与人工 realism gate 分开；视觉门失败时只保留几何、标注和格式诊断价值。
- 边界：不否定程序化数据用于单元测试或几何预训练。
- 证据：`ziyu24/SynDOTAForge@79976ce1773fbdf9ae1c909d4f7e48347e9c1703` 的 `lab/failed_methods.md`、`lab/result.md`。

## SYNDOTA-02 prompt+mask 不能强制视角语义成立

- 类型：科学证伪。
- 为何失败：即使明确要求 nadir helicopter 并提供 mask，生成结果仍出现斜视和 3/4 视角；空间约束没有控制相机/物体姿态语义。
- 避坑：视角是独立验收项，需要人工或可靠姿态估计；mask 对齐不能作为 nadir 证明。
- 边界：该结论限于当前生成流程和提示策略。
- 证据：`ziyu24/SynDOTAForge@79976ce1773fbdf9ae1c909d4f7e48347e9c1703` 的 `lab/failed_methods.md`、`doc/server26-stage/experiments/manual_obb_annotation_handoff.md`。

## SYNDOTA-03 自动 QA 通过只说明管线，不说明训练价值

- 类型：范围限制。
- 为何失败：文件可读、框合法、类别完整和渲染成功都不测 domain realism 或下游增益；把它们合并成“数据质量 PASS”会遮蔽真正失败。
- 避坑：分别报告工程完整性、视觉真实性和真实数据下游效果；三者不得互相替代。
- 边界：自动 QA 仍是生成数据交付的必要条件。
- 证据：`ziyu24/SynDOTAForge@79976ce1773fbdf9ae1c909d4f7e48347e9c1703` 的 `lab/failed_methods.md`、`lab/discussion.md`。
