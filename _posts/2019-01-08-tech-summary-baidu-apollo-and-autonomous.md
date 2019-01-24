---
layout:     post
title:      技术总结 - Apollo & 自动驾驶
date:       2019-01-08 20:00:00
author:     作壹條苟
tags:
 - 技术总结
 - 自动驾驶
---

> Udacity上看了Apollo的course，正好又在GTC看了一些自动驾驶肌肉秀。既然是要做AGV，自动驾驶当然是要学习的。

### Apollo的架构

* 定位：
	1. RTK(real time kinematic)：GPS+IMU
	2. 多传感器融合：GPS+IMU+激光雷达

* 感知：  
	* input：雷达数据，图像数据，雷达传感器校准外部参数，前摄像机标定的外部和内在参数，车辆的速度、角速度。  
	* output：  
		1. 具有航向、速度、分类信息的三维障碍轨迹
		2. 车道标志信息具有拟合参数、空间信息以及语义信息

* 预测：  
	针对障碍物的运动预测，输入障碍物与定位信息，输出具有预测轨迹的障碍物

* 路由：  
	输入地图数据，路由请求（始终点），输出路由导航信息

* 规划：  
	* input：定位、车辆状态、地图、路由、感知、预测   
	* output：安全舒适的轨迹，交由控制器执行   

* 控制：  
	* input：规划轨迹、车辆状态、定位、DW自动模式更改request  
	* output：底盘控制命令（转向、节流、刹车）  

### 其他

#### LineNet，车道线检测

先进行segmentation，将图像分割为车道和背景，再通过embedding把分割后的的车道分离为车道实例。

![image](https://github.com/hallazie/hallazie.github.io/blob/master/img/in-post/lanenet.jpg)
