# dgobb-synthprobe 避坑点

审计基线：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed`

## SYNTHPROBE-01 单图伪标签适配不能靠同类筛选参数续命

- 类型：科学证伪。
- 为何失败：r003 的单图伪标签梯度适配在 matched HRSC 协议下各变体均远低于 four-view TTA，quotient-ST 相对 TTA 的置信区间完全小于零。
- 避坑：强 TTA 对照稳定占优后停止同类 confidence、rotated-IoU 或 quotient-loss 扫描。
- 边界：不否定所有 test-time adaptation，只否定该单图伪标签家族。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `lab/failed_methods.md`。

## SYNTHPROBE-02 没有新增物理观测的 orbit fusion 只是 TTA 组合

- 类型：科学证伪。
- 为何失败：rotation TTA、pullback、OBB 距离和 WBF/一致性集成没有引入新的可识别信息，重新命名为 orbit-consensus 不能形成新方法。
- 避坑：明确新可观测量或新推断对象；仅组合既有视图与融合算子时归入强基线。
- 边界：工程融合仍可提升系统，不构成独立原创。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `lab/failed_methods.md`。

## SYNTHPROBE-03 物理采集路线必须先有可审计 carrier

- 类型：资产不可用。
- 为何失败：CODrone 虽有高度/角度 strata 和许可，但缺原始 flight/scene ID、内参、GSD、MTF/PSF、地理链、配对采集或验证 simulator；高度类别只能支持 conditioning，不能识别 acquisition kernel。
- 避坑：零 GPU 先审核配对单位、传感器几何和 forward operator；缺失时停止 carrier，不从图像统计反推物理链。
- 边界：这是数据载体不足，不是 DAG-OBB 理论或算法的性能失败。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `doc/legacy/audits/dg_obb_2_h000005_final_scientific_decision.md`。

## SYNTHPROBE-04 标准物理/统计组件的直接组合不产生新颖性

- 类型：科学证伪。
- 为何失败：RayLift 只是 orthorectification、RPC/pose、world-BEV、height-footprint 和 KD 的组合；Spin2 的 frame transport/tensor product 仍留下 90° 歧义；RIVE 也只是重包装。
- 避坑：在实验前做严格归约；若核心可由现成算子逐项表达，停止改名路线。
- 边界：这些组件可作为实现模块或基线。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `lab/failed_methods.md`。

## SYNTHPROBE-05 数字 probe 未经过真实传感器链不能证明真实行动风险

- 类型：协议/实现无效。
- 为何失败：DPIRT 的成像后 positive/null probe 只在数字域变化，probe-to-real action-risk 排序需要目标侧不可识别的 bridge bound；否则只是 synthetic validation 或 model selection。
- 避坑：物理风险主张必须绑定真实传感器或经验证 simulator，并报告 operator error；无桥接界时只称数字敏感性。
- 边界：数字 probe 仍可作软件测试和候选筛查。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `lab/failed_methods.md`。

## SYNTHPROBE-06 多视图预测联合分布不能识别共同漏检风险

- 类型：科学证伪。
- 为何失败：相同预测联合分布可对应风险排序相反的真值世界，common miss 根本不进入 proposal universe；多光谱载体也没有现成可校准 emission 闭环。
- 避坑：先给两世界不可识别反例；无独立真值、物理 emission 或额外假设时，不把一致性当准确率或安全性。
- 边界：不否定多视图作为下界、拒判或带额外锚点的用途。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `lab/failed_methods.md`。

## SYNTHPROBE-07 可靠性越严越不动、越松越有害是结构性困境

- 类型：科学证伪。
- 为何失败：FSQA 在 reliability 0.8 大量 metric-vector 恒等、确认门失败；放宽到 0.6 后全部发生变化却出现负 stress 或 clean-safety 排除。当前 scalar gate 未找到既活跃又有益的区域。
- 避坑：同时测 application rate、预测级变化和收益；不能把“不动”称保守成功，也不能把“有变化”称适配有效。
- 边界：跟踪证据缺 prediction payload/receipt，精确原因仍不可识别；只否定当前 scalar-gated FSQA。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `doc/legacy/audits/collab_round042/FAILURE_MECHANISM_AUDIT.md`。

## SYNTHPROBE-08 同尺度轴观察不等于同一方向机制

- 类型：范围限制。
- 为何失败：Paper A directed-down 与 DG-OBB A2 的输入空间语义/历史 baseline 预处理不匹配，现有资产无法把两者正结果归到同一机制，合并 gate 保持 HOLD。
- 避坑：跨项目合并前要求 matched-policy common baseline 和方向语义一致；共享相关轴只算线索。
- 边界：两个项目各自结果可保留，但不能合并成统一论文机制。
- 证据：`ziyu24/dgobb-synthprobe@5deedb7da5665fde50cbc5a7c2a55fc8b3ee52ed` 的 `doc/legacy/audits/merge_gate_final_decision_104.md`。
