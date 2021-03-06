---
layout:     post
title:      论文笔记 - Bottom-up Object Detection by Grouping Extreme and Center Points
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

* extreme point extraction

![extremenet step 2](/img/in-post/extremenet-2.jpg)

* peak extraction

* center grouping

#### Keypoint detection

使用Hourglass Network作为backbone对每个物体类别进行极值点及中心点回归。They follow the training setup, loss and offset prediction of Corner Net。其中offset是类别无关，但极值点相关的。

* [Cornernet: Detecting objects as paired keypoints](https://arxiv.org/abs/1808.01244)
* [Stacked Hourglass Networks for Human Pose Estimation](https://arxiv.org/abs/1603.06937)

使用keypoint estimation net提取图像中物体的上、下、左、右极值点。文章假设所有的物体都服从一种基于上下左右极值点的通用表达，通过对CornerNet进行finetune，使模型学习输入中所有物体的极值点。极值点通过heatmap表达，由每一个类型的特定极值点（如汽车的下侧极值点）形成一个heatmap。keypoint提取模型训练方式可以包括：
	1. 将label keypoint使用高斯核模糊之后，直接以L2 loss进行训练；
	2. 直接对label keypoint以逐点logistic regression训练。
heatmap的学习以[0,1]区间的根据极值点、中心点渲染的Gaussian map为label。其中极值、中心点为Gaussian kernel的均值，方差可以设为固定值，也可以与物体大小等比例。

#### Center(peak) grouping

对于每个heatmap，使用extractpeak procedure将连续的Gaussian kernel转换为离散（单一值）keypoint coordinate。将heatmap的高斯模糊峰值转换为极值点物理坐标。设置阈值τ，任意大于τ且在3×3窗口内为极值点的像素则取为peak点。（文章没有说具体实现，比较好奇对与整体很亮的一个Gaussian kernel如何提取）。

使用[Deformable Part Model](http://cs.brown.edu/people/pfelzens/papers/lsvm-pami.pdf)的思想对极值点进行grouping。其中中心点相当于DPM的root filter，四个极值点相当于对于所有类别通用的四个分解部分，四个极值点与中心点构成一种固定的几何形态。  
具体为使用穷举法进行grouping。对于任意一个peak四元组(l, r, t, b)，如果x<sub>c</sub>=(x<sub>l</sub>+x<sub>r</sub>)/2, y<sub>c</sub>=(y<sub>t</sub>+y<sub>b</sub>)/2点上有高的center heatmap响应，就认定为一组。其时间复杂度为O(n<sup>4</sup>)

对于空间上线性对称分布的物体，grouping时可能将不同物体的l, r, t, b聚为一组。对此采用soft NMS进行抑制。

> If the sum of scores of all boxes contained in a certain bounding box exceeds
3 times of the score of itself, we divide its score by
2. This non-maxima suppression is similar to the standard
overlap-based non-maxima suppression, but penalizes potential
ghost boxes instead of multiple overlapping boxes.

#### Deep Extreme Cut

简单实现为形成一个八边形的bbox。对四个极值点，在其对应方向上两侧延申1/4的h/w值，遇到corner则截断。

refine的segmentation为：DEC读入四个极值点，并进行与类别无关的前景分割。

![extremenet result](/img/in-post/extremenet-result.jpg)

### 适用任务

TODO

### TODO LIST

* Focal loss

* 在segment时，先用keypoints estimation构造一个大的Gaussian kernel represent的mask，以此为基础进行segment，效果是否更好。如给定一个显著性物体，在显著性高的地方不应该出现seg。（有遮掩的情况下似乎行不通）
