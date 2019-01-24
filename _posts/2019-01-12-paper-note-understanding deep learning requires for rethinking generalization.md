---
layout:     post
title:      论文笔记 - Understanding deep learning requires for rethinking generalization
date:       2019-01-12 12:00:00
author:     作壹條苟
tags:
 - deep learning
 - neural networks
 - 论文笔记
 - TODO
---

> 一般认为大型神经网络的高泛化性一定程度上来自于正则项约束。[这篇文章](https://arxiv.org/abs/1611.03530)通过随机label训练得出结论，多种正则均无法保证大型神经网络的泛化性，但可以优化训练过程，得到更快的收敛结果。  
> 同时文章得出结论，大型神经网络一定可以“记忆”住定量的数据集的（注意非学习，因为学习需要具有可泛化性）。并给出计算公式：DNNs的学习能力为N+2D，其中N为样本数，D为输入维度。  
> 文章读下来，感觉重新泛化与正则之间的insight是很有意义的，但直觉上总觉得文章里实验到结论之间不是很说得通。还有待思考。同时后面又有一篇文章 <[Rethinking generalization requires revisiting old ideas: statistical mechanics approaches and complex learning behavior](https://arxiv.org/abs/1710.09553)>，需要找时间仔细读一下。

Ian Goodfellow将regularization定义为：
> "any modification we make to a learning algorithm that is intended to reduce its generalization error, but not its training error."