---
layout:     post
title:      论文笔记 - ExtremeNet
date:       2019-02-04 00:16:00
author:     作壹條苟
tags:
 - deep learning
 - neural networks
 - 论文笔记
---

> [文章](https://arxiv.org/abs/1901.08043)提出一种利用边界点回归非bounding polygon represented的object detection，以更好的表达被识别物体。对于h×w的输入，previous one stage approaches需要从O(h<sup>2</sup>w<sup>2</sup>)的空间进行搜索，而该工作只需要从O(hw)的空间进行搜索。  
> 通过这篇文章，同时也对keypoint detection，pose recognition进行学习。

<!-- 单就回归出粗粒度边界而言其实感觉比较鸡肋。物体识别回归出bounding box只完成了一个low level的任务，在之上会有如instance segmentation，multi-object classification等任务，所以既然实际任务不会以得到bounding box为终结，extremenet将bounding box-segmentation的二段任务分段向后推了一点实际意义还有待思考。   -->


* 要得到instance segmentation，需要data -> ExtremeNet(extreme bounding box) -> DeepExtremeCut(segmentation mask)
* multi peak heatmap
* grouping center and extreme points：共C×5个heatmap，C为channel数，5为4个端点+1个中心点。五个heatmap是相对独立的，故需要把不同的heatmap点组合成一个物体，这采用了Deformable Part Model[(pami)](http://cs.brown.edu/people/pfelzens/papers/lsvm-pami.pdf)

### 模型结构

![extremenet](/img/in-post/extremenet.jpg)


#### Keypoint detection

TODO

#### CornerNet

* [Cornernet: Detecting objects as paired keypoints](https://arxiv.org/abs/1808.01244)
* [Stacked Hourglass Networks for Human Pose Estimation](https://arxiv.org/abs/1603.06937)

#### Deep Extreme Cut

TODO

### 适用任务

