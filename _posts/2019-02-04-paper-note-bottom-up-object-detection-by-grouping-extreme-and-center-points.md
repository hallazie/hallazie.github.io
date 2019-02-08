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

> [文章](https://arxiv.org/abs/1901.08043)提出一种利用极值点回归以极值点连接的菱形/八边形而非bounding box represented的object detection，以更好的表达被识别物体。该方法是完全基于外观信息的底层方法，通过学习不同类别物体的极值点，避免了region proposal及对区域进行classification的计算消耗。但同时将极值点组合为有意义的物体分组也引入了很大的额外消耗。  
> 对于h×w的输入，previous one stage approaches需要从O(h<sup>2</sup>w<sup>2</sup>)的anchors空间进行搜索，而该工作只需要从O(hw)的空间进行搜索。  
> 通过这篇文章，同时也对keypoint detection，pose recognition进行学习。

<!-- 单就回归出粗粒度极值而言其实感觉比较鸡肋。物体识别回归出bounding box只完成了一个low level的任务，在之上会有如instance segmentation，multi-object classification等任务，所以既然实际任务不会以得到bounding box为终结，extremenet将bounding box-segmentation的二段任务分段向后推了一点实际意义还有待思考。   -->


<!-- * 要得到instance segmentation，需要data -> ExtremeNet(extreme bounding box) -> DeepExtremeCut(segmentation mask)
* multi peak heatmap -->

<!-- * 共C×5个heatmap，C为类别数，5为4个端点+1个中心点。五个heatmap是相对独立的，故需要把不同的heatmap点组合成一个物体，这采用了[Deformable Part Model](http://cs.brown.edu/people/pfelzens/papers/lsvm-pami.pdf)。 -->

### 模型结构

![extremenet step 1](/img/in-post/extremenet.jpg)

* label：模型训练采用对上下左右四个极值点及中心点做回归。使用extreme click标注四个极值点，并计算左右、上下极值点的均值作为中心点 x<sub>c</sub>=(x<sub>l</sub>+x<sub>r</sub>)/2, y<sub>c</sub>=(y<sub>t</sub>+y<sub>b</sub>)/2。

* 使用keypoint estimation net提取图像中物体的上、下、左、右极值点。文章假设所有的物体都服从一种基于上下左右极值点的通用表达，通过对CornerNet进行finetune，使模型学习输入中所有物体的极值点。极值点通过heatmap表达，由每一个类型的特定极值点（如汽车的下侧极值点）形成一个heatmap。keypoint提取模型训练方式可以包括：
	1. 将label keypoint使用高斯核模糊之后，直接以L2 loss进行训练；
	2. 以逐点logistic regression训练。

![extremenet step 2](/img/in-post/extremenet-2.jpg)

* peak extraction，将heatmap的高斯模糊峰值转换为极值点物理坐标。

* 使用[Deformable Part Model](http://cs.brown.edu/people/pfelzens/papers/lsvm-pami.pdf)的思想对极值点进行grouping。其中中心点相当于DPM的root filter，四个极值点相当于对于所有类别通用的四个分解部分，四个极值点与中心点构成一种固定的几何形态。

#### Keypoint detection

TODO

#### CornerNet

* [Cornernet: Detecting objects as paired keypoints](https://arxiv.org/abs/1808.01244)
* [Stacked Hourglass Networks for Human Pose Estimation](https://arxiv.org/abs/1603.06937)

#### Deep Extreme Cut

TODO

### 适用任务

