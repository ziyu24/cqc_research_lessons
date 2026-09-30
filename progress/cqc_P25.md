# P25 项目进展

## 最初科学问题

没有完整OBB标注源域，仅有部分HBox或Point图像与完全无标签图像，如何学习对训练不可见目标域泛化的旋转检测器。

## 核心进展

r019已完成P19现成H/O教师的零训练四域配对诊断。源域DOTA四类宏平均O−H VOC07 AP50/AP75为+4.693/+14.905点；目标域HRSC为+3.687/+2.349点，SODA为+1.351/+4.854点，FAIR为+1.170/+5.734点。大车和小车的AP50监督差距在SODA/FAIR明显收缩，因此“弱监督差距跨域统一扩大”不成立；O在所有目标类AP75仍为正，强几何价值和类别异质性保留。

诊断路线成功，但P25方法目标尚未达成，原一般命题未被证伪，也没有形成顶刊方法贡献。P19是282张L图、九类头及不同初态，不替代P25 195-L四类精确强弱对照；后者仍后置且不自动启动。

## 服务器当前内容

SERVER于2026-09-30 05:42:28--06:41:55 UTC在26完成r019，RUN `COMPLETE`/exit 0。P19 H/O两模型各在HRSC、DOTA val、SODA和FAIR冻结评测，共8份报告、16份分片；每个模型域均由物理GPU 0/1两个rank执行，训练和优化器更新为0。按用户要求将后续独立SODA/FAIR分片在同一GPU 0/1上并发；一次重复O-DOTA启动在产生输出前终止，唯一有效原任务分片正常完成。当前无P25计算进程。

大型结果位于26的`/dev/shm/cqc/study/P25/runs/r019/artifacts`；无新增checkpoint，P19源权重保护不变。恢复配置为P25的`configs/r019.recovery.json`。

## 核验说明

8份报告、16份互斥分片和16条GPU证明全部通过，前向图像总数62026恰为两模型固定输入总数。原图ID、原图数、切片数、空图、类别映射和逐类GT分母与r012冻结报告一致。DOTA、SODA、FAIR共享报告为UNCHANGED；复用既有DOTA切片审计，没有重复切片、完整解码或全量像素哈希。总摘要SHA256为`1aa3ebce0489cae54c10139da545ec42625deb9c894db6dad6be1ed331daf6d1`。

## 执行阶段

服务器执行结束，结果已由来源项目提交并推送。当前无活动rNNN任务；r018精确强参照和r017缩放训练均未执行，不从本页自动恢复。

记录者：SERVER；更新日期：2026-09-30。

## 下一步与维护

后续若继续立题，应优先针对强弱模型共享、且按域/类别不同的迁移瓶颈设计可证伪机制；不得仅由源域强弱差距预设弱几何是目标域主因。若用户明确要求精确P25强参照，再沿保留方案启动，不追加阈值、种子或模型追阳性。

动作执行者按[主动更新约定](README.md)在真实事件发生时更新本页并发布总览。

## 证据

[r019完整结果](https://github.com/ziyu24/cqc_P25/blob/948b9a0d657b4170fab4fd059a90043e9266aa29/lab/result.md)；[小型核验证据](https://github.com/ziyu24/cqc_P25/blob/948b9a0d657b4170fab4fd059a90043e9266aa29/doc/r019_review.json)；[恢复入口](https://github.com/ziyu24/cqc_P25/blob/948b9a0d657b4170fab4fd059a90043e9266aa29/configs/r019.recovery.json)；[当前讨论](https://github.com/ziyu24/cqc_P25/blob/948b9a0d657b4170fab4fd059a90043e9266aa29/lab/discussion.md)；[已登记教训](../lesson/cqc_P25.lessons.md)。
