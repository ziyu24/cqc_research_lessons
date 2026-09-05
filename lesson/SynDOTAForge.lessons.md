# SynDOTAForge 科学问题与失败教训

> 使用边界：教训须结合适用条件与原始证据使用，同条件下的有效反证不能忽略，也不能跨条件自动否决新研究；来源不可访问时须注明“未独立核实”，不得将摘要当作已核实的原始证据。

审计基线：`ziyu24/SynDOTAForge@79976ce1773fbdf9ae1c909d4f7e48347e9c1703`

快速阅读路径：先读“项目研究什么”→“教训一、二、三、四”→“方法族停止索引”。

## 项目研究什么

项目研究能否生成具有可控旋转框、俯视几何和真实遥感外观的合成 DOTA 数据，用于低数据检测训练与机制分析。

## 领域位置与当前结论

- **事实**：旧内部资产上的 synthetic pretrain→real finetune 在低数据条件有正信号，并呈真实数据量×检测器能力交互；直接 mix 常更差。
- **事实**：程序化 v3/v4/v5 和 R4 多次未过人工真实感门；B-v2 inpainting 虽改善背景保护与尺度控制，直升机仍为斜视，飞机/储罐仍有语义伪影。
- **事实**：mask-PCA、OBB canonicalization 和 32/32 测试只闭合几何/导出链；当前不得声称新资产高质量、训练有效或可发布。
- **推断**：旧训练协议的正结果与新资产质量是两条独立证据链，不能用前者给后者背书。
- **未知**：任何通过人工门的新资产是否能复现旧训练收益尚未测试；项目已停止维护，不自动重开。

## 实际采用过的方法

项目先用程序化三维资产、材质和 PCA mask 生成标注，再用 prompt 与 mask 的生成式 inpainting 改善飞机、船、储罐和直升机外观，并用自动 QA 与少量训练实验评估数据价值。

## 教训一：改材质不能补救几何与场景瓶颈

- 失败命题：连续调整纹理和材质即可把玩具式程序化物体变成可信遥感目标。
- 失败原因：多版材质变化在俯视图中几乎不可见，主要失真来自轮廓、姿态、比例、阴影和场景上下文；优化错了主导误差源。
- 后续做法：先由人类视觉审计分解几何、视角、材质和上下文误差，再优先修复贡献最大的层级。
- 边界：几何已可信且传感器分辨率足够时，材质仍可能重要。
- 证据：`ziyu24/SynDOTAForge@79976ce1773fbdf9ae1c909d4f7e48347e9c1703` 的 `lab/failed_methods.md`、`lab/result.md`。

## 教训二：标注几何正确不等于图像分布真实

- 失败命题：PCA mask 与旋转框对齐良好、格式测试通过，就说明合成图可用于训练。
- 失败原因：这些检查只证明 mask、框和导出算术一致，不能衡量目标外观、背景共现、传感器噪声和域差。
- 后续做法：将几何/格式 QA 与视觉真实性、分布距离和下游训练效用分开验收，并保留人工盲评。
- 边界：几何正确是必要条件，仍适合单元测试和受控形状实验。
- 证据：`ziyu24/SynDOTAForge@79976ce1773fbdf9ae1c909d4f7e48347e9c1703` 的 `lab/failed_methods.md`、`lab/result.md`。

## 教训三：prompt 与 mask 不能强制物理视角成立

- 失败命题：提示词要求“nadir view”并给定 mask，就能稳定生成俯视、类别正确的遥感对象。
- 失败原因：直升机仍呈斜视，飞机出现停机坪填充，储罐退化为圆盘；生成模型满足纹理语义时并未保持三维姿态和物体结构。
- 后续做法：逐类验证显式形状/视角条件是否真正约束生成结果；可控三维几何、相机模型或多视图一致性是候选手段，不是未经比较就规定的唯一解法。
- 边界：对结构简单、视角不敏感的类别，inpainting 仍可改善外观。
- 证据：`ziyu24/SynDOTAForge@79976ce1773fbdf9ae1c909d4f7e48347e9c1703` 的 `lab/failed_methods.md`、`doc/server26-stage/experiments/manual_obb_annotation_handoff.md`。

## 教训四：合成数据收益依赖真实数据量与检测器强度

- 失败命题：合成预训练或混合训练会对不同检测器和真实数据规模普遍有益。
- 失败原因：增益随真实数据量增加而收窄，但“检测器越强收益必越小”也不成立：DOTA real100 的 RetinaNet 增量约 `0.201`，Oriented R-CNN 约 `0.278`；real3000 才分别约 `0.019/0.010`。两种检测器同时改变架构与训练动态，不能单独归因为容量；旧资产结果也不能给新资产质量背书。
- 后续做法：预设真实数据量乘检测器强度的二维消融，分别比较预训练、混合与纯真实训练，并先通过人工视觉资格审查。
- 边界：这不否定低数据域的价值。人工真实感是当前资产目标和项目验收条件，不是所有合成数据改善检测的必要定理；标签预算收益也不自动等于同总算力收益。
- 证据：`ziyu24/SynDOTAForge@79976ce1773fbdf9ae1c909d4f7e48347e9c1703` 的 `lab/failed_methods.md`、`lab/discussion.md`、`lab/result.md`。

## 方法族停止索引

| 方法族 | 最强负证据或限制 | 停止范围 | 当前 main 证据路径 |
| --- | --- | --- | --- |
| material-only procedural | 同 seed 图像变化极小或仍显玩具感，多轮人工门失败 | 停止作为真实感主线；仅保留几何诊断 | `doc/server26-stage/reports/syndotaforge_stage_report_041_cn.md`；`lab/failed_methods.md` |
| mask-PCA / OBB chain | 主轴与框边修正、测试通过，但不评价图像真实性 | 只支持标注几何，不支持数据集质量 | `lab/result.md`；`doc/server26-stage/PROJECT_EXECUTION_REPORT.md` |
| prompt+mask inpainting | 直升机非 nadir，飞机/tank 仍有结构语义错误 | 停止无显式视角/形状控制的扩量 | `doc/server26-stage/reports/syndotaforge_stage_report_041_cn.md` |
| synthetic mix | 充足真实数据下常不如 pretrain→finetune | 停止把直接混训作为默认协议 | `doc/server26-stage/PROJECT_EXECUTION_REPORT.md` |
| low-data pretraining | 旧资产下正信号随数据量和检测器能力变化 | 保留条件性历史结论；不得外推到未过门新资产 | `doc/server26-stage/PROJECT_EXECUTION_REPORT.md`；`lab/result.md` |
