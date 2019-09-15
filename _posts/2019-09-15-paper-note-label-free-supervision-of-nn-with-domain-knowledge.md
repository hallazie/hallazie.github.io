---
layout:     post
title:      论文笔记 - Label-free Supervision of NNs with Physics and Domain Knowledge
date:       2019-04-07 13:18:00
author:     作壹條苟
tags:
 - deep learning
 - neural networks
 - 论文笔记
---

> 针对标注数据稀缺问题，[文章](https://www.aaai.org/Conferences/AAAI/2017/PreliminaryPapers/12-Stewart-14967.pdf)提出一种以定律/特定领域知识代替标注数据的监督学习方法。


使用特定领域知识代替标注数据进行监督学习的关键是将损失函数中基于output-groundtruth pair distance的最优化，改变为将input-output pair约束到最符合先验知识域的映射。即从

$$
f^* = \mathop{argmin}_{f\in F}\sum^n_{l=1}l(f(x_i), y_i) 
$$

变为

$$
f^* = \mathop{argmin}_{f\in F}\sum^n_{l=1}g(x_i, f(x_i)) + R(f)
$$