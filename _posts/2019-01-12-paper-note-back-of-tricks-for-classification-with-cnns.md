---
layout:     post
title:      论文笔记 - Bag of tricks for classification with convolutional neural networks
date:       2019-01-12 12:00:00
author:     作壹條苟
tags:
 - deep learning
 - CNNs
---

> 通过这篇文章，可以系统化的掌握一些调优方式，同时可以将整个模型训练的过程及其中涉及的一些细节进行系统化的总结。

### Abstract
当前 image classification 领域的进步很大程度来自于对**训练过程的优化**，如`data argumentation`和`optimization`方面的改进。这篇文章对这些方法进行了测试并通过 ablation 对他们对于模型最终表现的影响进行了 empirically evaluation。通过结合这些方法，ResNet-50的 top1 准确率得到了提高，而更高准确率的分类模型在迁移到其他 domain 后也有了更好的表现。

文章内容：
* baseline training procedure
* 在新的硬件上进行高效训练的几个tricks
* review了三种模型结构调优（tweaks）的方法，和四种训练过程优化方法。
* 讨论了更高准确率分类模型对迁移学习的影响。

