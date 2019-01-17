---
layout:     post
title:      论文笔记 - Understanding deep learning requires for rethinking generalization
date:       2019-01-12 12:00:00
author:     作壹條苟
tags:
 - deep learning
 - CNNs
---


### 结论：
* regularization 不一定 是保证 large scale DNNs 泛化性的原因。
* 对于 N 样本，D 维度的数据集，DNNs的参数大于 N + 2D时，一定可以“记忆”住该数据集（注意非学习，因为学习需要具有可泛化性）

