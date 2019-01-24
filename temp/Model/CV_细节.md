* RGB颜色空间与HLS颜色空间可以对同一张图表现出不同的特性：

  ![FireShot Capture 1 - 高级车道线识别算法 - 知乎 - https___zhuanlan.zhihu.com_p_29113411](E:\Notes\Model\img\FireShot Capture 1 - 高级车道线识别算法 - 知乎 - https___zhuanlan.zhihu.com_p_29113411.png)

  ![v2-dc24e998b325f5b9643a45f27225d09c_hd](E:\Notes\Model\img\v2-dc24e998b325f5b9643a45f27225d09c_hd.jpg)

  ![v2-da14fa41669c2b1d3f947c2c355e687a_hd](E:\Notes\Model\img\v2-da14fa41669c2b1d3f947c2c355e687a_hd.jpg)

  从RGB空间转换到HLS空间后，黄色车道线可以从白色背景中被成功分离并由Sobel得到边缘信息。

* Hough变换

  识别图像中几何形状的基本方法。将几何形状通过曲线的表达形式映射到参数空间，将问题从全局的曲线检测转换为参数空间局部的峰值检测。