### 资料

大牛讲堂｜SLAM第一篇：基础知识： https://zhuanlan.zhihu.com/p/23247395

大牛讲堂｜SLAM最终话：视觉里程计： https://zhuanlan.zhihu.com/p/23382110	



### Stuff

典型的VSLAM包含四个部分：

1. Visual Odometry：估计两个时刻间机器人的相对运动量。激光SLAM中因为可以直接得到有距离信息的全局地图所以只需要把当前位置在地图中匹配。

   对于VO特别是mono VO，主流采用基于特征的方法：提取特征（如角点），根据特征Map的匹配求解相机姿态。特征点通过描述子（descriptor）进行描述，描述子为特征点与周围领域的信息。

   实际中，一般先用代数方法求粗略解，再用bundle adjustment进行优化。

   ![img](https://pic2.zhimg.com/80/v2-d40794f8488ce5495b870805179dfeb5_hd.jpg)

2. 后端：为了估计累积误差，较早的方法将SLAM构建成卡尔曼滤波，最小化运动方程与观测序列之间的噪声，迭代求解。现在采用 **Bundle Adjustment** 方法，把误差平均到每一次观测。

3. 建图：TODO

4. 回环检测：机器人识别曾经到过的场景的能力。普遍采用词袋模型进行回环检测（将视觉特征聚类，建立词典，）

---

纯视觉实现的车道线检测：

【博客】https://zhuanlan.zhihu.com/p/29113411