---
layout:     post
title:      论文笔记 - Understanding deep learning requires for rethinking generalization
date:       2019-01-12 12:00:00
author:     作壹條苟
tags:
 - deep learning
 - CNNs
---

> regularization不一定是保证large scale DNNs泛化性的原因。对于N样本，D维度的数据集，DNNs的参数大于N+2D时，一定可以“记忆”住该数据集（注意非学习，因为学习需要具有可泛化性）

[文章地址](https://arxiv.org/abs/1611.03530)

### Abstract

successful DNNs 能将训练集与测试集