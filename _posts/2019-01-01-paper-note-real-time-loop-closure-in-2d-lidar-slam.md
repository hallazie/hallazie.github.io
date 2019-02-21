---
layout:     post
title:      论文笔记 - Real-Time Loop Closure in 2D Lidar SLAM
date:       2019-02-22 00:12:00
author:     作壹條苟
tags:
 - 自动驾驶
 - 论文笔记
---

> Scan matched to submap at a short period is assumed to be sufficiently accurate. By aligning scan to submap at each short time period the map is constructed at real-time. Scan matching only happens on recent submap (at the same position of different time will form different submap).  

> For Cartographer, in-door office-like environments are no challenge for all the namedalgorithms. Featureless environments such as long tunnelsor out-door environments are problematic.

![where cartographer failed](/img/in-post/where_cartographer_failed.png)

[cartographer standalone without ROS](https://github.com/googlecartographer/cartographer/issues/1229)

### Basic

* grid-map, 5cm each pixel for resolution. each pixel consist of all points close to the grid point, to represent the probability of obstacle.
* scan-pose, each scan is corresponding to a pose (x,y,theta of the transformation of scan frame into submap frame coordinates).
* loop closure, for a current scan-pose, do pose estimation to achieve loop closure (pose optimization). a scan matcher find poses for well matched submaps in a window and add the poses as loop closure constrain. this happends every few seconds.
* branch and bound approach, to accelerate loop closing scan matching.
* global and local approach both optimize the **pose**.
* scan-into-submap, the current scan pose \ksee is optimized before inserting scan into submap everytime. which optimize a non-linear least square problem of maximizing the probability for scan points in submap.
* scan matching, for each scan point, first transform it by \ksee (pose transformation) from scan frame to objective submap frame. then use **bicubic interpolation** to smooth the value to scalar. (guess: first calculate a bicubic interpolation for transformed scan point, then calculate the Euclidean distance between the interpolated point and transformed scan point)
* sparse pose adjustment, to optimeze the poses of **all** scans and submaps.
* relative pose, -
* scan matching argmin the \ksee of current scan. SPA argmin the \Ksee_m and \Ksee_s, all the submap and scan poses. relative poses for certain scan and submap \ksee_{ij} is used as constraints for SPA.
* branch and bound approach
	* [BBA-example](https://www.jianshu.com/p/c738c8262087)
	* [BBA-stanford material slide](https://see.stanford.edu/materials/lsocoee364b/17-bb_slides.pdf)
	* [BBA-stanford material lecture notes](https://web.stanford.edu/class/ee364b/lectures/bb_notes.pdf)

### TODOLIST

* scan-matching
* sparse pose adjustment
* iterative closest points
* branch and bound approach
* ceres-solver
* what is the mathematical form (representation) of the **constraints** for global pose-graph-optimization ??

> Constraints can intuitively be thought of as little ropes tying all nodes together. The sparse pose adjustement fastens those ropes altogether. The resulting net is called the “pose graph”.

### Component

![carto_flow](/img/in-post/cartographer_flow.png)

Two scan matching strategies are available:

* The CeresScanMatcher takes the initial guess as prior and finds the best spot where the scan match fits the submap. It does this by interpolating the submap and sub-pixel aligning the scan. This is fast, but cannot fix errors that are significantly larger than the resolution of the submaps. If your sensor setup and timing is reasonable, using only the CeresScanMatcher is usually the best choice to make.

* The RealTimeCorrelativeScanMatcher can be enabled if you do not have other sensors or you do not trust them. It uses an approach similar to how scans are matched against submaps in loop closure (described later), but instead it matches against the current submap. The best match is then used as prior for the CeresScanMatcher. This scan matcher is very expensive and will essentially override any signal from other sensors but the range finder, but it is robust in feature rich environments.


### Trival but Important Tricks

* Submaps must be small enough so that the drift inside them is below the resolution, so that they are locally correct. On the other hand, they should be large enough to be distinct for loop closure to work properly.
