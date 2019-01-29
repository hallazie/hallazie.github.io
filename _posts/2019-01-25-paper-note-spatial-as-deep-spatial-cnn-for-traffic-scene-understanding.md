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

> 有点意思，TODO一个周末看

### 预备知识-概率图模型，CRF和语义分割

有向图模型（贝叶斯网络）通过条件概率计算目标边际概率（Marginal Probability，如满足某些给定随机变量的结果group出现的概率）或联合概率（Joint Probability，如满足全部给定随机变量的特定结果出现的概率）或条件概率。无向图模型如CRF，MRF，假设图的节点为变量，边表示两个变量之间存在相互依赖但不存在因果关系。无向图相邻随机变量节点间的联系通过**factor**表示，即给相邻随机变量节点的所有组合给定不同的权重。与条件概率不同，其权重和不一定为1。求无向图的联合概率即将factor连乘，再除以