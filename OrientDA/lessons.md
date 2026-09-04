# OrientDA 避坑点

审计基线：`ziyu24/OrientDA@793d2fce0d7d4a7f70998b06a5569bdd9a768b92`

## ORIENTDA-01 最近失败轮次不能抹掉成熟项目资产

- 类型：历史结论已推翻。
- 为何失败：只看 r008--r019 曾把 OrientDA 判断为“没有成熟实验包”；项目级重评确认已有统一 P-lite、双方向三 seed、强基线、消融、逐类、边界、图表和稿件，现实定位是 Remote Sensing，补强后可讨论 JSTARS。
- 避坑：接手先读全项目结果和当前权威方法身份，再看最近轮次；任务失败只更新对应路线边界。
- 边界：成熟资产不代表当前证据达到 TGRS/JPRS。
- 证据：`ziyu24/OrientDA@793d2fce0d7d4a7f70998b06a5569bdd9a768b92` 的 `lab/result.md`。

## ORIENTDA-02 分类头行号错误会让整个 teacher 身份失效

- 类型：协议/实现无效。
- 为何失败：r009 把 DOTA row 1 当 ship，实际 ship 是 row 6；Unified P-lite 从 baseball-diamond teacher 初始化，低 HRSC AP 不能归为机制失败。
- 避坑：重映射前核对公开类别序、前景/背景行，并做零步同图输出一致性；训练步数和分支非零不能补救错误身份。
- 边界：r009 准入停止有效，但“现代强基线淘汰 P-lite”解释已撤回。
- 证据：`ziyu24/OrientDA@793d2fce0d7d4a7f70998b06a5569bdd9a768b92` 的 `lab/failed_methods.md`、`lab/result.md`。

## ORIENTDA-03 全部臂连 source-only 都崩溃时不能比较机制等价

- 类型：协议/实现无效。
- 为何失败：r008 两方向十个臂 AP 几乎为零，source-only 也崩溃；臂间近零差只说明绝对有效性失败，不能写成 TSR 与强基线等价。
- 避坑：先设 source-only 有效性地板；基线崩溃时只排查数据/训练协议，不解释臂间差。
- 边界：高风险原因是按类别拆图后把其他对象变背景，但未独立隔离，不能写成已证因果。
- 证据：`ziyu24/OrientDA@793d2fce0d7d4a7f70998b06a5569bdd9a768b92` 的 `lab/failed_methods.md`、`lab/result.md`。

## ORIENTDA-04 修改作者数据协议后不能称 native reproduction

- 类型：协议/实现无效。
- 为何失败：r010 把作者 `HRSCDataset/trainval/XML` 改成 CocoDataset、自建 train split 和 HBox JSON，训练样本与标注转换均改变；参考指标失配不能否定官方方法。
- 避坑：作者复现先用原数据类、split、转换、checkpoint 和 evaluator 闭环；同构实验另命名，不冒充 native。
- 边界：只否定该参考协议；作者 checkpoint 的独立闭环仍有效。
- 证据：`ziyu24/OrientDA@793d2fce0d7d4a7f70998b06a5569bdd9a768b92` 的 `lab/failed_methods.md`。

## ORIENTDA-05 官方 checkpoint 复现与从头训练复现是两项证据

- 类型：范围限制。
- 为何失败：r011 能在 0.01 内复现作者 checkpoint，但同配置 seed1 最终训练 AP75 `0.657` 低于准入 `0.7049`；不能因训练失败否定发布 checkpoint，也不能因 checkpoint 通过证明本机训练可复现。
- 避坑：严格分开 checkpoint evaluation、training reproduction 和候选增量，各自设门。
- 边界：r011 只停止该主机/seed/配置的训练准入，不含 FSPT 性能结论。
- 证据：`ziyu24/OrientDA@793d2fce0d7d4a7f70998b06a5569bdd9a768b92` 的 `lab/failed_methods.md`。

## ORIENTDA-06 方法身份未隔离时不得启动性能实验

- 类型：协议/实现无效。
- 为何失败：r012 的 target HBox 同时受到旧 `loss_symmetry_ss` 和新增 FSPT 后验优化，source 几何监督也未完整成立；候选不是预注册方法本身。
- 避坑：在真实 source-target batch 上逐损失验证读取边界、目标模块梯度和权重；身份门失败先修方程，不用 500-step/AP 代替。
- 边界：不否定 feasible-set posterior 思想，r012 没有性能结果。
- 证据：`ziyu24/OrientDA@793d2fce0d7d4a7f70998b06a5569bdd9a768b92` 的 `lab/failed_methods.md`。

## ORIENTDA-07 可行集与积分定义必须先通过数学覆盖门

- 类型：协议/实现无效。
- 为何失败：r013 的 180-bin feasible set 对真实 OBB 的 IoU@0.95 recall 仅 `0.720<0.990`；r014 到最小步仍未过 polygon-IoU 门，端点权重又与严格正要求矛盾、奇异分支缺失。
- 避坑：训练前用真实标注检查集合覆盖、奇异分支和 N/2N 或参考解收敛；失败不靠加 bins、放宽 IoU 或插入真角度。
- 边界：否定冻结离散化/积分实现，不是 FSPT 性能负结果。
- 证据：`ziyu24/OrientDA@793d2fce0d7d4a7f70998b06a5569bdd9a768b92` 的 `lab/failed_methods.md`。

## ORIENTDA-08 验证器连续修补不能无限替代可训练候选

- 类型：协议/实现无效。
- 为何失败：LSET r015--r017 连续围绕 permutation gradient/prediction identity 修判据；最终巨大逐行差又被发现主要来自错误的字典序集合比较。三轮没有产生 500-step 或性能结果。
- 避坑：集合比较用类别内一对一匹配，先分开代数恒等、同序数值噪声和更新后预测；验证合同反复失效且触发最终止损时退役路线，不继续加门。
- 边界：LSET 退役原因是未形成合法可训练候选，不是集合代数已被科学反证。
- 证据：`ziyu24/OrientDA@793d2fce0d7d4a7f70998b06a5569bdd9a768b92` 的 `lab/failed_methods.md`。

## ORIENTDA-09 用趋零的同分布距离作分母会制造 gate 下溢

- 类型：协议/实现无效。
- 为何失败：OCST 用 source split-half energy distance 作跨域距离分母；该量随样本增加趋零，导致指数 gate 下溢为 `0.0`，任何 equivariance 分数都无法恢复。
- 避坑：校准公式先做渐近和量纲审计；不得靠 epsilon 或人工 floor 修复结构性退化。
- 边界：不否定 source geometry 或安全投影，只否定 r018 gate 定义。
- 证据：`ziyu24/OrientDA@793d2fce0d7d4a7f70998b06a5569bdd9a768b92` 的 `lab/failed_methods.md`。

## ORIENTDA-10 弱监督去噪机制不能外推成全监督通用原则

- 类型：科学证伪。
- 为何失败：全监督 DOTA 上 observability mask 的 mAP75 比 base 低约 `0.021--0.022`，且比同 mask 比例随机控制更差；它集中删除低 AR 类的有效角监督，使 weak/near-square 角误差恶化。
- 避坑：从弱监督环境获得的去噪收益必须用干净全监督和随机 mask 对照验证通用性；失败后收窄为条件性组件。
- 边界：不抹除其在特定弱监督跨域设置中的已有收益。
- 证据：`ziyu24/OrientDA@793d2fce0d7d4a7f70998b06a5569bdd9a768b92` 的 `doc/legacy/c5/top_journal_upgrade_v1/c5_tj_v1_negative_result_freeze.md`、`doc/legacy/c5/final_decision/final_claim_boundary.md`。

## ORIENTDA-11 用 target AP 选最终变体后不能再声称完全无 target 选型

- 类型：历史结论已推翻。
- 为何失败：旧 simplified final 是看过双域 target AP75 的 2×2 比较后冻结，因而不满足“完全不使用 target OBB/AP 做方法选择”的强声明。
- 避坑：开发、选择和独立确认 split 明确分离；若已看 target 指标，就如实称开发性结果并另设独立确认。
- 边界：这不否定既有数值可复现，只限制确认性和论文措辞。
- 证据：`ziyu24/OrientDA@793d2fce0d7d4a7f70998b06a5569bdd9a768b92` 的 `doc/legacy/c5/final_freeze/091_final_go_no_go.md`、`lab/result.md`。
