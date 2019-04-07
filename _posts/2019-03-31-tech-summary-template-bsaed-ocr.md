---
layout:     post
title:      技术总结 - 基于模板的票据OCR
date:       2019-03-31 13:38:00
author:     作壹條苟
tags:
 - deep learning
 - 技术总结
---

> 对之前票据OCR项目的总结和梳理，以免遗忘。 

票据OCR与通用OCR不同在于，其识别目标往往限定为某类具有特定格式，特定文本内容的票据。如增值税发票数据内固定数量、固定属性的文本。借此我们可以将OCR任务分解为两部分：基于instance detection的line proposal，以及对line进行文本识别。

实际业务场景下，为了提高准确率，可以每种票据单独训练一个模型。而由于每种票据往往具有相同/相似格式，可以通过票据模板随机生成数据以极大扩充训练样本。生成数据时，记录插入坐标及文本行高度、宽度，作为文本行检测时的标签。

故基于模板的票据OCR任务实际由三部分组成：
* 基于模板的数据扩充，实现为pygame做文本渲染 + skimage做空间变换 + Pillow做图像融合。
* instance detection based line proposal，实现为仿YoloV3的目标识别网络。
* 单个line的文本识别，实现本来是VGG+LSTM，现在感觉不如直接用不定宽输入的ResNet。

### 1. 基于模板的数据扩充

基于模板的数据扩充即根据某类票据数据，按照其基本格式将对应文本替换，加入文本行坐标及角度的jitter，形成新的基本数据，再通过图像方法加入后期效果，模拟实际票据照片的拍摄角度、曝光、纸质等。后期效果的加入主要是启发式的规则，可进一步扩充。

#### 1.1 获取模板

这一步的目标是得到空白的票据模板。之前的方法为将增值税发票PDF文件导出为高分辨率图像，再通过Photoshop将文字涂抹，只留下空白网格、印章等信息。同时为每个文本行分配ID，并记录每个文本行所在的大致坐标位置。

#### 1.2 生成数据

为自动扩充数据，需要在每个文本行位置插入对应其ID的随机文本。为增加可信度，我们针对增值税发票爬取了如公司名、地址、银行分行名称等文本，保存在数据池中。生成时，地址、名称等使用爬取到的数据，而数量大写、电话号码、增值税编码等则采用按规则生成的方式。

在生成票据数据时，首先随机选择文本生成模板数据json文件。json中每个数据项格式如下：key为文本行ID，例子中为销售方地址及电话号码。rdshift为文本是否加入随机偏置值。space是啥忘了，chars为实际文本值，pos为像素坐标，fontsize为文本大小，font为采用的字体文件的相对路径。

```json
	"sell_addr_phone": {

		"rdshift": true,

		"space": 0,

		"chars": "和平南大街福地洞天小区12栋4号门市 56825099161",

		"pos": [265, 729],

		"fontsize": 18,

		"font": "font/simsun.ttc"
		
	}
```

之后图像生成模块在```gen_config.gen_single()```读入json配置，通过`pygame`模块进行文本行渲染。渲染后依次加入纸张效果、形变、背景图像、噪声、对比度变化，对数据进行拟真。

```python
config = gen_config.gen_single()
self.pannel = Image.open('sample/fp000.png').convert('RGB')
self.pannel_width, self.pannel_height = self.pannel.size
self.pannel = np.array(self.pannel).transpose()
self.position = {}
shift_lvl = (int(random.randint(-shift_range,shift_range)), int(random.randint(-shift_range,shift_range)))
for kv in config:
	self.render_line(kv, config[kv], shift_lvl)
self.add_paper_effect()
self.deform()
self.background()
self.noise()
self.enhance_contrast()
```

生成后保存的图像如图所示）。其中用于第二步line proposal及第三步文本识别的标签保存在文件名对应的json中。

![extremenet step 1](/img/in-post/ocr_yolo_output.png)

其中模型实现细节：

1. Anchor选择：如果是3个scale，每个scale3个Anchor共9个，则perform clustering on traning set boxes and output the average w and h for each class. Assign the anchors in descending order, e.g. 最大的三个分配给最前面（粗粒度）的output。

2. 由BoxInfo生成label时，生成shape=[(15,30,3,85),(30,40,3,85),(60,80,3,85)]的array（以80类VOC为例，3个scale的输出，每个scale三个anchor，每个anchor的(x,y,w,h,objectiveness_score,80类的score)）。生成时先生成np.zero(shape=shape)， 再将每个ground truth对应到对应的scale和像素中心。 即最终得到一个稀疏矩阵。
	a. 对每个gt_bbox，计算中心，找到每个scale对应的x,y
	b. 对每个scale的x,y计算与gt_bbox的intersection最大的一个scale的anchor（IOU），并以此scale作为添加gt_bbox的scale
		* IOU = intersect_area / (box_area + anchor_area - intersect_area)，对bbox expand到全部anchor向量化的size，再向量计算。
	c. 如：中间scale的中间anchor，第5,5像素，类=10，x,y偏置=(0.2,0.4)，w，h偏置为(1.2,3.3), label[1,4,4,1]=[0.2, 0.4, 1.2, 3.3, 1, 0, 0, ... 1, 0, 0, ... 0], shape=(1,85)

3. 由于票据中每项object面积较小，在downsample之后两个靠近的项可能会在三个尺度上都重叠在一起，从而造成丢失。

4. 输出x0,y0,w0,h0计算loss。输出转bbox，x=sigmoid(x0)+cx，y=sigmoid(y0)+cy，w=e^w0，h=e^h0。

5. loss: sum of squared error. y0:gt, y1:output, then: gradient=y0-y1

6. in our case, the scale can set to 1

7. at output, all the bbox-vec with objectness-confidence lower than the threshold is set to 0-vec.

8. total loss = xy_loss(ce) + wh_loss(se) + confidence_loss(ce) + classification_loss(ce)  # (ce=binary crossentropy)

9. 不加confidence mask(或类似置零-过滤机制)，label中占绝大部分的0-vec会让学习收敛到全0。

10. loss function: 论文原版 xy, wh, oc, cs 对应的分别是 binary-ce, squared, binary-ce, binary-ce。实验后发现 mae, mae, binary-ce, binary-ce效果更好。

### 2. 文本行检测

文本行检测采用简化的YoloV3网络结构。针对票据中每个文本实例分为一个类，进行文本行目标检测。网络结构如下。

在设置anchor时，anchor的宽度由对生成数据中文本行的宽度、高度聚类得到。

在构造整体损失函数时，对坐标、宽高、conf、分类使用了不同的损失函数，并直接进行拼接，还有调优空间。

```python
def conv_block(data, num_filter, kernel=(3,3), stride=(1,1), pad=(1,1), act_type='leaky', dilate=(0,0)):
	if dilate == (0,0):
		conv = mx.symbol.Convolution(data=data, num_filter=num_filter, kernel=kernel, stride=stride, pad=pad)
	else:
		conv = mx.symbol.Convolution(data=data, num_filter=num_filter, kernel=(3,3), stride=stride, pad=(2,2), dilate=(1,1))
	bn = mx.symbol.BatchNorm(data=conv)
	if act_type == 'leaky':
		act = mx.symbol.LeakyReLU(data=bn)
	elif act_type == 'none':
		act = bn
	else:
		act = mx.symbol.Activation(data=bn, act_type=act_type)
	return act

def pool_block(data, stride=(2,2), kernel=(2,2), pool_type='max'):
	return mx.symbol.Pooling(data=data, stride=stride, kernel=kernel, pool_type=pool_type)

def confidence_mask_thresh(data, threshold, train):
	bsize = BATCH_SIZE if train else 1
	obj_vec = mx.symbol.slice(data, begin=(None,4,None,None), end=(None,5,None,None))
	ths_vec = mx.init.Constant((np.ones((bsize,1,WIDTH//DOWNSAMPLE,HEIGHT//DOWNSAMPLE))*threshold).tolist())
	tht_vec = mx.sym.Variable('mask', shape=(bsize,1,WIDTH//DOWNSAMPLE,HEIGHT//DOWNSAMPLE), init=ths_vec)
	rsp_vec = mx.symbol.broadcast_greater(lhs=obj_vec, rhs=tht_vec)
	blk_vec = mx.symbol.BlockGrad(rsp_vec)
	return mx.symbol.broadcast_mul(lhs=data, rhs=blk_vec), obj_vec

def diverse_act(data):
	xy_part = mx.symbol.slice(data, begin=(None,0,None,None), end=(None,2,None,None))
	wh_part = mx.symbol.slice(data, begin=(None,2,None,None), end=(None,4,None,None))
	rs_part = mx.symbol.slice(data, begin=(None,4,None,None), end=(None,None,None,None))
	xy_act = mx.symbol.Activation(xy_part, act_type='sigmoid')
	rs_act = mx.symbol.Activation(rs_part, act_type='sigmoid')
	return mx.symbol.concat(xy_act, wh_part, rs_act)

def net(train):
	data = mx.symbol.Variable('data')
	label = mx.symbol.Variable('softmax_label')
	c1 = conv_block(data, 32)
	p1 = pool_block(c1)
	c2 = conv_block(p1, 64)
	p2 = pool_block(c2)
	c3 = conv_block(p2, 128)
	c4 = conv_block(c3, 128)
	p4 = pool_block(c4+c3)
	c5 = conv_block(p4, 256)
	c6 = conv_block(c5, 256)
	c7 = conv_block(c6, 256)
	p7 = pool_block(c7+c5)
	c8 = conv_block(p7, 384)
	c9 = conv_block(c8, 384)

	c12 = conv_block(c9, num_filter=33, kernel=(1,1), stride=(1,1), pad=(0,0), act_type='none')
	c13 = diverse_act(c12)
	msk, rsp_vec = confidence_mask_thresh(c13, THRESHOLD, train)
	if not train:
		return mx.symbol.Group([msk, rsp_vec])

	out_xy = mx.symbol.slice(data=msk, begin=(None,0,None,None), end=(None,2,None,None))
	out_wh = mx.symbol.slice(data=msk, begin=(None,2,None,None), end=(None,4,None,None))
	out_oc = mx.symbol.slice(data=msk, begin=(None,4,None,None), end=(None,5,None,None))
	out_cs = mx.symbol.slice(data=msk, begin=(None,5,None,None), end=(None,None,None,None))
	lbl_xy = mx.symbol.slice(data=label, begin=(None,0,None,None), end=(None,2,None,None))
	lbl_wh = mx.symbol.slice(data=label, begin=(None,2,None,None), end=(None,4,None,None))
	lbl_oc = mx.symbol.slice(data=label, begin=(None,4,None,None), end=(None,5,None,None))
	lbl_cs = mx.symbol.slice(data=label, begin=(None,5,None,None), end=(None,None,None,None))
	xy_loss = mx.symbol.MAERegressionOutput(data=out_xy, label=lbl_xy)
	wh_loss = mx.symbol.LinearRegressionOutput(data=out_wh, label=lbl_wh)
	oc_loss = mx.symbol.LogisticRegressionOutput(data=out_oc, label=lbl_oc)
	cs_loss = mx.symbol.SoftmaxOutput(data=out_cs, label=lbl_cs)
	loss = mx.symbol.concat(xy_loss, wh_loss, oc_loss, cs_loss)
	return loss
```

### 3. 文本识别

文本识别部分原本由VGG + LSTM + Warp-CTC实现，但是代码找不到了。现在感觉可以直接用不定宽输入（predict时）的ResNet + Warp-CTC实现。

训练时，由于渲染文本中单字宽度可控，故可以直接截取为固定高度、宽度的文本行作为训练数据。

预测时，由于文字大多数程正方形，故固定高度的文本行通过ResNet得到 1×m 的向量时，每个激活正好接近一个字符的感受野大小。但相比LSTM的劣势在于无法引入语言模型得到上下文效果，每个字符的识别相互条件独立。