---
layout:     post
title:      论文笔记 - FCOS: Fully Convolutional One-Stage Object Detection
date:       2019-04-07 13:18:00
author:     作壹條苟
tags:
 - deep learning
 - neural networks
 - 论文笔记
---

> 文章提出一种不依赖于预定义锚点的逐像素预测的OD方法。



基于锚点的OD方法具有如下缺陷：

* 与锚点相关的超参必须被小心选择，否则会较明显的影响最终预测效果（如average precision）。
* 预置的锚点大小、比例在检测差异较大物体时不够灵活，且在迁移数据集后需要重新设计。
* 为提高召回率，多个锚点box被紧密排列，而绝大部分锚点都被标定为negative，这样会导致训练时negative与positive的比例失衡。
* 大量的锚点会导致运算量增大，特别是计算IOU时。



### 模型结构

用于训练的groundtruth bbox结构如下：
$$
B_i = (x^{(i)}_0, y^{(i)}_0, x^{(i)}_1, y^{(i)}_1, c^{(i)})\in R^4\times{1,2...C}
$$
