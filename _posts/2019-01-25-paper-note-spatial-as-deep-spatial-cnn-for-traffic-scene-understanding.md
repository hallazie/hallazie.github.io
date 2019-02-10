---
layout:     post
title:      论文笔记 - Spatial CNN for Traffic Scene Understanding
date:       2019-01-25 10:50:00
author:     作壹條苟
tags:
 - deep learning
 - 自动驾驶
 - 论文笔记
 - TODO
---

> [文章](https://arxiv.org/abs/1712.06080)针对traffic scene understanding中，基于局部感受野进行特征识别的传统CNN对具有连续明显几何特征（pole、lane）物体识别效果不佳的问题，提出spatial CNN，使特征能够在同一个layer中进行传播，以更好的学习空间特征。SCNN将feature map的行或列作为layer，。SCNN不仅可以学习连续空间特征，还可以对遮掩的连续特征进行补全。

### 预备知识-概率图模型，CRF和语义分割

有向图模型（贝叶斯网络）通过条件概率计算目标边际概率（Marginal Probability，如满足某些给定随机变量的结果group出现的概率）或联合概率（Joint Probability，如满足全部给定随机变量的特定结果出现的概率）或条件概率。无向图模型如CRF，MRF，假设图的节点为变量，边表示两个变量之间存在相互依赖但不存在因果关系。无向图相邻随机变量节点间的联系通过**factor**表示，即给相邻随机变量节点的所有组合给定不同的权重。与条件概率不同，其权重和不一定为1。求无向图的联合概率即将factor连乘，再进行归一化。

基于FCN与CRF的语义分割follow通用的pipeline：FCN对输入进行特征提取，并通过多层上采样得到跟原图size相同的pixel-wised分类输出。之后通过CRF对输出图进行refine post-process，得到更精细的分割图。

### 模型

在SCNN中，**C×H×W**的张量将被split为H个slices，第一个slice被送入具有C个channel的kernel size为C×*w*的卷积层，其中*w*为卷积核宽度。