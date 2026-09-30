# P25 项目进展

## 最初科学问题

没有完整OBB标注源域，仅有部分HBox或Point图像与完全无标签图像，如何学习对训练不可见目标域泛化的旋转检测器。

## 核心进展

用户已接受先复用P19现成强弱模型，C已交付零训练的四域配对评测入口。两份120k教师已严格加载，四类输出映射和全部评测输入覆盖通过CPU核验，尚无新跨域分数。P19九类源域AP50为60.92%/66.04%，但其类别和标注图片与P25不同，不能据此报告精确P25强弱差距。原精确强参照训练后置。

## 服务器当前内容

C已交付r019：复用P19 H/O固定教师，顺序HRSC→DOTA val→SODA→FAIR，每域两臂都评完再转下一域；每模型实际两卡，0训练更新。SERVER于2026-09-30 05:42 UTC在26启动同号RUN，运行器选择物理GPU 0/1；H、O首批均完成两卡真实前向且优化器更新为0。随后HRSC H正式两rank已在GPU 0/1开始，两个活跃子PID的UUID回读均为MATCH。此前未执行的r018仍按用户取舍后置，不在本轮自动启动。

## 核验说明

上一轮52组完整PR、预测身份、终点和实际双卡核验继续有效，直接复用。此前外部公开模型核查发现30%标注、15类、180k强模型；本轮内部资源核查补充了更接近的P19配对，纠正只考虑外部模型的不足。P19为DOTA1.0、282个有标原图、九known类、120k，同初态及配对采样/增强摘要，但不是P25的195个有标原图和四类。不能拿P19强模型直接减P25弱模型归因。

C于04:33:50 UTC完成11项目资源核查；本轮进一步在26严格加载P19两份最终教师，每份371项状态，初态一致，九类头和原生推理不变。04:58:50 UTC的CPU检查确认[3,2,1,0]映射、HRSC原ship通道、低分和空图保留、错误类序/头宽/臂/步数/NaN拒绝、实际图像变换及差值方向；随后追加6项缓存反例和旧评测器默认行为检查通过。全部原图集合与453/5297/20751/4512个推理输入覆盖已核；共享报告UNCHANGED，只复用实际原文件身份，不改SODA自定义口径。HRSC无共享报告，定向核453原图字节；没有重切或重扫其他域像素。

上述核验足以交付冻结评测，不能当成真实GPU前向通过。入口将自动完成每模型两卡首批、记录实际前向次数与CUDA耗时，再连续评测。旧精确强参照的195个L原图、34380个实例和CPU梯度路由核验保留于来源历史，本轮不执行那条训练，也不使用其替代损失检查来证明当前GPU推理。

主看逐域/逐类AP50，AP75、完整PR、连续AP及召回用于解释；源与目标同类差距变化只作描述性判断。P19额外五类仍参与原生候选竞争，其九类头/L划分/初态、监督包同时改变多个目标及单种子边界保留。没有新模型成绩、没有新方法成功，原目标未完成。

## 执行阶段

服务器执行中；2026-09-30 05:42 UTC已确认r019在26使用物理GPU 0/1完成H/O真实首批并进入HRSC正式评测。r018未执行训练已后置；命令RUNNING及首批通过不等于四域科学输出完成。

记录者：SERVER；更新日期：2026-09-30。保留C于05:08:20 UTC的启动前观察和B于03:50 UTC的审查背景；本次实际启动事实来自26同号RUN及活跃GPU PID，不称B/C共同讨论或共识。

## 下一步与维护

SERVER拉取来源项目唯一r019入口，真实两卡首批通过后直接完成固定两模型四域评价。若强弱共同失败，研究共同跨域瓶颈；若源域接近而目标差距拉开，才增强弱监督额外域敏感性解释；若源域已经落后，先分辨基础学习差距。完整逐类差距表和取舍说明齐全即结束，不追加模型、oracle扫描、阈值或种子追阳性，不自动启动后置训练。

动作执行者按[主动更新约定](README.md)在真实事件发生时更新本页并发布总览。

## 证据

[当前唯一任务](https://github.com/ziyu24/cqc_P25/blob/2596f3de9a5c066baf6d6265d8d4606aa14354c9/lab/sug.md)；[可执行评测入口与恢复边界](https://github.com/ziyu24/cqc_P25/blob/2596f3de9a5c066baf6d6265d8d4606aa14354c9/doc/p19_reference.md)；[CPU及数据核验证据](https://github.com/ziyu24/cqc_P25/blob/2596f3de9a5c066baf6d6265d8d4606aa14354c9/doc/p19_reference_review.json)；[用户取舍及训练后置](https://github.com/ziyu24/cqc_P25/blob/2596f3de9a5c066baf6d6265d8d4606aa14354c9/lab/discussion.md)。

[SERVER恢复入口](https://github.com/ziyu24/cqc_P25/blob/a03fd9ce7182fb36546a3f2128765c2bdac95c6e/configs/r019.recovery.json)。实际RUN、PID和GPU回读留在26项目运行目录，不复制到本库。

[P18–P28资源核查与权重身份](https://github.com/ziyu24/cqc_P25/blob/f6a9284acae750c9cf435e101b470aff09246b28/doc/resource_audit.md)；[本轮资源判断及限制](https://github.com/ziyu24/cqc_P25/blob/f6a9284acae750c9cf435e101b470aff09246b28/lab/discussion.md)。

[范围与最初立题](https://github.com/ziyu24/cqc_P25/blob/1a5053823bf340800d5230ef5cb293729aef3ef6/README.md)；[用户取舍与当前讨论](https://github.com/ziyu24/cqc_P25/blob/1a5053823bf340800d5230ef5cb293729aef3ef6/lab/discussion.md)；[历史结果与旧计划撤回](https://github.com/ziyu24/cqc_P25/blob/1a5053823bf340800d5230ef5cb293729aef3ef6/lab/result.md)；[唯一任务](https://github.com/ziyu24/cqc_P25/blob/1a5053823bf340800d5230ef5cb293729aef3ef6/lab/sug.md)；[CPU和数据核验](https://github.com/ziyu24/cqc_P25/blob/1a5053823bf340800d5230ef5cb293729aef3ef6/doc/strong_reference_review.json)。[已登记教训](../lesson/cqc_P25.lessons.md)。
