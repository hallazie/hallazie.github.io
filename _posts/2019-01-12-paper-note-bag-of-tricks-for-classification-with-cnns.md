---
layout:     post
title:      论文笔记 - Bag of tricks for classification with convolutional neural networks
date:       2019-01-12 12:01:00
author:     作壹條苟
tags:
 - deep learning
 - CNNs
 - paper reading
---

> 通过[这篇文章](https://arxiv.org/abs/1812.01187)，可以系统化的掌握一些调优方式，同时可以将整个模型训练的过程及其中涉及的一些细节进行系统化的总结。

### Abstract
当前image classification领域的进步很大程度来自于对**训练过程的优化**，如`data argumentation`和`optimization`方面的改进。这篇文章对这些方法进行了测试并通过ablation对他们对于模型最终表现的影响进行了 empirically evaluation。通过结合这些方法，ResNet-50的top1准确率得到了提高，而更高准确率的分类模型在迁移到其他 domain 后也有了更好的表现。

文章内容：
* baseline training procedure
* 在新的硬件上进行高效训练的几个tricks
* review了三种模型结构微调（tweaks）的方法，和四种训练过程优化方法。
* 讨论了更高准确率分类模型对迁移学习的影响。

### Baseline Procedure

训练 ResNet-50：
1. 随机选择一张图像，编码为[0., 255.]的float32矩阵；
2. 随机crop出一个aspect ratio从[3/4, 4/3]中随机采样，面积从[8%, 100%]中随机采样的矩形，并缩放到224×224大小；
3. 以0.5的概率进行水平翻转；
4. 将HSL值（hue, saturation, lightness）以[0.6, 1,4]的均匀分布进行缩放；
5. 添加服从正态分布N(0, 0.1)的PCA噪声；
6. 将RGB通道进行归一化，分别减去123.68, 116.779, 103.939，并除以58.393, 57.12, 57.375。

而在验证中：
1. 将图像的短轴缩放到256，并从中心截取224×224；
2. 将RGB通道进行归一化，分别减去123.68, 116.779, 103.939，并除以58.393, 57.12, 57.375。

卷积层与全连接层的权重均通过 Xavier 进行初始化：[-a, a]，a=sqrt(6/(d<sub>in</sub>+d<sub>out</sub>))
其中d<sub>in</sub>是输入通道数，d<sub>out</sub>是输出通道数。偏置均为0，batch norm中，&gamma;=1, &beta;=0。
optimizer采用Nesterov Accelerated Gradient（NAG），训练120个 epochs，batchsize 为256，初始学习率为0.1，并在第30，60，90个epoch时处以10。

### GPU高效训练的几个tricks

GPU的发展使最近performance related trade-offs已经发生了变化，如大batch size的低精度表达。主要review了以下几种tricks：

#### large batch training

对凸优化问题，随着batch size的增大，收敛率会随之降低。神经网络也收到了类似的经验。换句话说，对于相同的epoch数量，使用大的batch size的模型在validation上的表现会比小batch size的模型差。以下四种启发式的trick尝试解决这个问题：

**linear scaling learning rate**：mini batch SGD的训练过程是随机过程，因为样本的选取是随机的。而增大batch的大小不会改变batch的期望（需要无偏的假设才行），但会改变方差。即：大的batch size降低了梯度的噪声，所以我们可以在梯度的反方向进行更大步长的下降。随batch size线性增长的learning rate在ResNet-50上取得了实验证明。如果对batch size=256，learning rate=0.1，则当我们将batch size增大为 *b* 时，我们可以将learning rate增大到 0.1 × *b* / 256

**learning rate warmup**：在训练的初期使用大的learnig rate可能会引起训练的不稳定（振荡，发散）。learning rate warmup提出，可以在训练的初期使用小的learning rate，在训练稳定后，再变为初始学习率。一种具体的策略是线性warmup，即训练开始时，学习率为0，而在warmup阶段的batch中，每t个batch将学习率线性增大，直到得到初始学习率（如0.1）。

**zero &gamma;**：假设残差块的输入为x，则输出为x+f(x)，而f(x)最后一层一般为一个batch norm层。batch norm首先将x归一化得到x<sub>n</sub>，在输出通过可学习参数&gamma;与&beta;进行线性变化后的值 &gamma;×x<sub>n</sub>+&beta;。通过在训练的初期将&gamma;置为0，可以使残差块输出=输入，使网络的层数隐式减少，从而降低初始阶段的训练难度。

**no bias decay**：decay通常会apply到网络的所有可学习参数中，实际等价于施加一个L2正则，以降低过拟合。而一些work提出，最好只对卷积weight和全连接层进行decay，而不对bias，以及batch norm层的&gamma;和&beta;进行decay。

#### low precision training

目前很多新式GPU对FP32与FP16的计算设计了不同的加速方法。如NvV100，`FP32为14TFLOPS`，同时`FP16为100TFLOPS`。需要注意的是，训练中低精度的数据可能会使计算结果out-of-range。有工作提出，使用FP16表示参数与激活，同时用FP16计算梯度，但同时在update时，将参数保存一份FP32的副本。

### 模型结构微调

ResNet模型的原始结构参见[文章](https://arxiv.org/abs/1512.03385)

**ResNet-B**：原始ResNet中，残差块3×3通道中卷积层顺序为 1×1(s=2)，3×3，1×1。这样的问题是在第一步，3/4的前层激活信息都被丢弃了。ResNet-B将通道改变为1×1，3×3(s=2)，1×1，使所有信息都被使用。同时，由于残差块的残差连接为1×1(s=2)，同样有3/4的信息被丢弃，故将残差连接改为2×2 average pooling，后接1×1(s=1)卷积。

**ResNet-C**：观察表示卷积的计算消耗与其卷积核宽高程二次关系。故将ResNet最下层的7×7卷积改为3层3×3卷积，减少计算消耗。

### training refinement

**cosine learning rate decay**：learning rate调整对于训练来说是非常关键的。step decay-每30个epoch乘以0.1，也有每2个epoch乘以0.94的线性decay。cosine decay则是：
$\eta_{t}=\frac{1}{2}(1+cos(\frac{t\pi}{T}))\eta$

**label smoothing**：对于分类，输出的概率q<sub>i</sub>为最后全连接层经过softmax变换之后的值。其loss通过与one-hot label的交叉熵计算。要使交叉熵最小，对于y<sub>i</sub>=1的q<sub>i</sub>要接近无限大，而过大的输出可能会导致过拟合。label smooth将q<sub>i</sub>转换为：q<sub>i</sub>=&sigma;，如果y<sub>i</sub>=1，否则q<sub>i</sub>=&sigma;/(K-1)。同时将交叉熵计算中对输出求指数的步骤舍去。
<!-- （感觉这种方法对于negative的学习不是很友好） -->

**知识蒸馏**：知识蒸馏是通过让低精度的小网络模拟一个高精度的大网络的输出，从而降低模型复杂度的。首先训练一个高精度的大网络（如ResNet-152），在其训练完成后，搭建一个小网络（如ResNet-50），并设置一个distillation loss，如对于具有相同输出类的两个网络，则设置交叉熵作为loss。通过最小化小网络与大网络输出的差值，使小网络间接学习。

**mixup training**：对于两个输入输出对（x<sub>i</sub>, y<sub>i</sub>, x<sub>j</sub>, y<sub>j</sub>），将输入输出对进行加权线性组合：
x<sup>t</sup>=&alpha;x<sub>i</sub>+(1-&alpha;)x<sub>j</sub>
y<sup>t</sup>=&alpha;y<sub>i</sub>+(1-&alpha;)y<sub>j</sub>
使用组合后的数据进行训练。（感觉有点扯）
