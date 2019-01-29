---
layout:     post
title:      技术总结 - Instance Level Segmentation
date:       2019-01-09 10:50:00
author:     作壹條苟
tags:
 - deep learning
 - 技术总结
 - TODO
---

> Object detection可以看作是一种粗粒度的instance segmentation。在场景推理中，重叠物体的遮掩及其空间关系之间的判断与推理以object detection的bounding box representation实现起来比较困难。携带边缘和occlusion信息的instance segmentation在这种任务上更有优势。

[UToronto的instance segmentation ppt](http://www.cs.toronto.edu/~urtasun/courses/CSC2541/08_instance.pdf)

### 实现1. Mask RCNN

git: https://github.com/matterport/Mask_RCNN

Mask-RCNN以Fast-RCNN为backbone实现了instance segmentation。step 1与Fast-RCNN相同，首先进行region proposal。在RPN以sliding window得到region后，通过VGG/ResNet得到512×14×14的tensor。
![mask-rcnn net structure step 1](/img/in-post/maskrcnn.jpg)
![mask-rcnn net structure step 2-1](/img/in-post/maskrcnn2.jpg)
![mask-rcnn net structure step 2-2](/img/in-post/maskrcnn3.jpg)

### 实现2. Deep Mask

git: https://github.com/facebookresearch/deepmask