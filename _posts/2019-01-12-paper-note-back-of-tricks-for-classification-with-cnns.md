---
layout:     post
title:      论文笔记 - Bag of tricks for classification with convolutional neural networks
date:       2019-01-12 12:01:00
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

### Baseline Procedure
训练：
1. 随机选择一张图像，编码为[0., 255.]的 float32 矩阵；
2. 随机 crop 出一个 aspect ratio 从[3/4, 4/3]中随机采样，面积从[8%, 100%]中随机采样的矩形，并缩放到224×224大小；
3. 以0.5的概率进行水平翻转；
4. 将HSL值（hue, saturation, lightness）以[0.6, 1,4]的均匀分布进行缩放；
5. 添加服从正态分布N(0, 0.1)的PCA噪声；
6. 将RGB通道进行归一化，分别减去123.68, 116.779, 103.939，并除以58.393, 57.12, 57.375。
而在验证中：
1. 将图像的短轴缩放到256，并从中心截取224×224；
2. 将RGB通道进行归一化，分别减去123.68, 116.779, 103.939，并除以58.393, 57.12, 57.375。

卷积层与全连接层的权重均通过 Xavier 进行初始化：[-a, a]
```mathjax
a = \sqrt{{6/(d_{in}+d_{out})}}
```
其中d<sub>in</sub>是输入通道数，d<sub>out</sub>是输出通道数。