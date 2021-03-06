---
layout:     post
title:      论文笔记 - Label-free Supervision of NNs with Physics and Domain Knowledge
date:       2019-09-15 13:00:00
author:     作壹條苟
mathjax:    true
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

实际上f作为高维数据x到低维数据y的映射，y的信息是隐藏在x的子空间流形中的。即，$l(f(x_i), y_i)$ 中，通过找到最小化loss的f，可将f约束得到正确的映射关系。这是在没有y在x子空间中分布的先验知识的前提下。若有先验知识，则可使用约束让映射得到符合先验知识的分布，即公式2。