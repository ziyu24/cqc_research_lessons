# GeoPDE-OBB 避坑点

审计基线：`ziyu24/GeoPDE-OBB@9566c7fa1b6184a5ffbe8b9924aadef82a4c6786`

## GEOPDE-01 主方案必须胜过去机制的简单归因对照

- 类型：科学证伪。
- 为何失败：oriented-anisotropic v20 只有 `+0.0047` 的单 seed 小幅差，GN-only 不低于它，isotropic Laplacian 反而高出约 `0.0121`；方向投影没有独立贡献。
- 避坑：为 normalization、普通平滑和 isotropic 版本设置硬归因对照；简单臂解释全部收益时停止主机制。
- 边界：不否定所有方向扩散，只否定 v20 冻结实现和该方向场。
- 证据：`ziyu24/GeoPDE-OBB@9566c7fa1b6184a5ffbe8b9924aadef82a4c6786` 的 `results/diagnostics/ablation_comprehensive_comparison.md`、`results/reports/geopde_obb_005_decision_memo.md`。

## GEOPDE-02 诊断场饱和或近随机时不能继续写物理语义

- 类型：科学证伪。
- 为何失败：结构张量方向中位轴误差约 `37.5°`，仅略好于随机 `45°`；coherence 中位和最大都为 1，无法门控，且不同 FPN level 出现轴/切向反转。
- 避坑：先验证观测场与目标方向的可辨识性和动态范围；失败后把它当普通特征变换，不继续作几何机制解释。
- 边界：该诊断不否定结构张量在其他图像或尺度上的用途。
- 证据：`ziyu24/GeoPDE-OBB@9566c7fa1b6184a5ffbe8b9924aadef82a4c6786` 的 `results/diagnostics/theta_semantics_summary.md`、`docs/HANDOFF.md`。

## GEOPDE-03 单 seed 的最佳简单臂也必须复现

- 类型：科学证伪。
- 为何失败：iso_laplace 在 seed30 看似最佳，但三 seed 复核的平均 baseline 增益约 `0.0064<0.008`、相对 GN 仅 `0.00184<0.005`，seed50 相对 GN 为负，最终 gate 为 fail。
- 避坑：把从消融中发现的新胜者视为新假设，以独立 seeds 和同条件 baseline 复核；不得把探索赢家直接写入论文。
- 边界：只否定当前 isotropic 单 Laplacian 的预注册门，不证明所有简单平滑无效。
- 证据：`ziyu24/GeoPDE-OBB@9566c7fa1b6184a5ffbe8b9924aadef82a4c6786` 的 `results/replications/iso-single-laplacian-replication-20260728-r1/final_gate.json`、`docs/HANDOFF.md`。
