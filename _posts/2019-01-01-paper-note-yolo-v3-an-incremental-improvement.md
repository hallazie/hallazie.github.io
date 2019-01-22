---
layout:     post
title:      论文笔记 - YOLOv3 An Incremental Improvement
date:       2019-01-01 12:00:00
author:     作壹條苟
tags:
 - deep learning
 - neural networks
 - paper reading
---

> 对Yolo系列是直接从[v3](https://arxiv.org/abs/1804.02767)开始看的，这篇笔记是对整个Yolo系列方法的学习，同时也作为自己对object detection整体脉络理解的整理。
> Yolo 的一大优势在于对可以端到端的回归出bounding box的位置、宽高、分类及其conf。而取得这种优势的源头在于其颠覆性（自己确实没有在其他work中见过类似思路）的对传统CNNs中特征张量不同维度的使用，将以channel分离的2-d feature map作为计算单元改变为以width-height分离的1-d 空间特征向量作为计算单元。其外的如固定的anchor boxes，最后3层不同resolution的output等都是在其上锦上添花的tricks。
> 对数据的理解能力对炼丹师傅是非常essential的。这种理解不仅是对原数据，还有对中间数据的intuition。希望通过Yolo能对CNNs的中间激活图张量能有更深的理解。

### Yolo 的优势

与Yolo对比的object detection方法主要是RCNN系列及SSD。TODO:回头再看下RCNN和SSD的思想，现在忘了。

* Yolo是端到端的：通过改变特征张量的计算单元，同时以固定的anchor boxes固定输出数量，Yolo实现了对object的类别与空间信息的端到端回归。
* Yolo很快：整个网络通过全卷积实现。
* Yolo的准确率较高：还没总结。

针对这些优势，重新整理思路，对Yolo及object detection进行理解。

### 网络结构

TODO

### 输出层结构及数据转换

TODO

### 对比其他方法，理解object detection

TODO

### 一些应用上的思考

TODO