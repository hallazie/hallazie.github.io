### cudnn

用于training阶段的优化提速。

---

### Xavier

包含七种处理器：ISP（图像传感器处理单元），PVA（可编程立体视觉加速器），VPU（视频处理器），OFE（光流引擎），tensorCore（可编程张量处理器），CUDA（并行加速器），DLA（深度学习加速器），CPU。

---

### tensorRT

用于对inference阶段的优化提速。（high performance inference optimizer and runtime engine for product deployment）

会主动合并部分layers，提高吞吐，减小延迟，降低功耗，降低内存使用。

---

### tensorCore

用于加速大型矩阵运算，可进行混合精度矩阵运算。在一个GPU中可运行数百个tensorCore。

![Turing-Tensor-Core_30fps_FINAL_736x414](E:\Notes\GPU\img\Turing-Tensor-Core_30fps_FINAL_736x414.gif)

---

### deepstream

deepstream是Jetson平台用于处理视频流数据的SDK。

---

### DLA



---

### JetPack

// TODO

---

### L4T

// TODO

---

### Issac

仿真平台。

---

### rapids

数据挖掘库，pandas-like api and sklearn-like api。

---

### nvidia driver

nv的自动驾驶解决方案（包括硬件解决方案/NVIDIA drive AGX，软件解决方案，仿真方案），磊大佬的文档里说应该适合做startup项目。但是官网上看需要contact them提交申请才能用啊。