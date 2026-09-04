# GeoStructDOTA 避坑点

审计基线：`ziyu24/GeoStructDOTA@7b9a5f846d99ca5a8cdd0c59d29315983b51526e`

## GEOSTRUCT-01 把 map posterior 直接变成 RBox 没有稳定增益

- 类型：科学证伪。
- 为何失败：pure、adaptive 和 Gaussian 三种直接映射没有形成稳定正收益，其中 Gaussian 为负；地理后验存在不等于能直接替代检测几何。
- 避坑：先用强 detection baseline 和恒等/随机 map 对照验证独立增量；不再换核或权重重复同一直接映射。
- 边界：不否定地图信息用于其他任务或更明确的关联机制。
- 证据：`ziyu24/GeoStructDOTA@7b9a5f846d99ca5a8cdd0c59d29315983b51526e` 的 `lab/failed_methods.md`、`lab/result.md`。

## GEOSTRUCT-02 dual-dustbin UOT 当前解耦会伤害 AP 与覆盖

- 类型：科学证伪。
- 为何失败：当前 existence/visual decoupling 与 dual dustbin 设计同时降低 AP 和 coverage，没有形成预期的拒配收益。
- 避坑：拒配机制必须同时比较匹配质量、覆盖和最终检测，不以更高 abstention 掩盖性能损失。
- 边界：只否定冻结 UOT 构造，不否定所有 unbalanced transport。
- 证据：`ziyu24/GeoStructDOTA@7b9a5f846d99ca5a8cdd0c59d29315983b51526e` 的 `lab/failed_methods.md`、`lab/result.md`。

## GEOSTRUCT-03 非标准 image-only 评价不能支持检测主张

- 类型：协议/实现无效。
- 为何失败：只有图像级或自定义评价、缺少标准实例匹配时，数值无法与 OBB 主任务或强基线等价比较。
- 避坑：先闭合官方 evaluator、类别映射和实例总体；非标准结果只能作诊断。
- 边界：image-only 测试可验证推理接口，不是科学性能证据。
- 证据：`ziyu24/GeoStructDOTA@7b9a5f846d99ca5a8cdd0c59d29315983b51526e` 的 `lab/failed_methods.md`、`doc/legacy/paper_notes/claims_audit_039.md`。

## GEOSTRUCT-04 缺少 identity/gold 时 headline 不可估

- 类型：协议/实现无效。
- 为何失败：panel headline 缺唯一对象身份与独立 gold，无法定义同一对象、独立单位和真实误差；汇总表完整不能补足可识别性。
- 避坑：在运行前建立 object/scene key、gold 来源和去重规则；缺失时明确 not estimable。
- 边界：可保留描述性覆盖统计。
- 证据：`ziyu24/GeoStructDOTA@7b9a5f846d99ca5a8cdd0c59d29315983b51526e` 的 `lab/failed_methods.md`、`doc/legacy/paper_notes/paper_assets_v6/10_claims_audit.md`。

## GEOSTRUCT-05 DSM/CLS 连通域不能伪造成实例屋顶真值

- 类型：资产不可用。
- 为何失败：DFC2019 的 DSM/CLS 没有实例 roof-footprint ID；connected components、VFLOW 或地图后处理生成的是派生实例，不是官方独立真值。
- 避坑：需要实例结论时先确认官方 identity/crosswalk；没有就收窄到语义/表面任务，不造伪 gold。
- 边界：派生组件可作候选或弱监督，不能作独立验证。
- 证据：`ziyu24/GeoStructDOTA@7b9a5f846d99ca5a8cdd0c59d29315983b51526e` 的 `lab/failed_methods.md`、`doc/legacy/paper_notes/class_scope_and_failure_taxonomy.md`。

## GEOSTRUCT-06 固定网页抓取不等于完整资产资格审计

- 类型：协议/实现无效。
- 为何失败：只检查少量固定 URL/目录会漏掉真实资源与版本，也不能闭合 Extended US3D 的 building ID、关联、crosswalk 和 manifest。
- 避坑：以内容签名、官方索引和有界候选发现审计资产；资产不可判定不升级为科学失败。
- 边界：禁止无限磁盘扫描；候选范围应事前限定。
- 证据：`ziyu24/GeoStructDOTA@7b9a5f846d99ca5a8cdd0c59d29315983b51526e` 的 `lab/failed_methods.md`、`doc/legacy/ops/project_status_034.md`。
