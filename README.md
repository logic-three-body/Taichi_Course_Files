# 太极图形课S1-HTC Homework
## 背景简介

### About This repo

这里记录我在[太极图形课第一季](https://www.bilibili.com/video/BV1aL4y1a7pv?p=11)所学习taichi语言和计算机图形学的笔记（[note](https://github.com/logic-three-body/Taichi_Course_Files/tree/master/note/Lec1)）和相关代码（[code](https://github.com/logic-three-body/Taichi_Course_Files/tree/master/code)），实例图片会在[data](https://github.com/logic-three-body/Taichi_Course_Files/tree/master/data)文件夹

### HW1

#### JuliaSet RGB

Learn from:[【cflw】曼德勃罗集合和朱利亚集合](https://forum.taichi.graphics/t/topic/1742)

原版的Julia Set颜色输入的是灰度值

```python
pixels[i, j] = 1 - iterations * 0.02
```

如果希望是彩色输出则需要**RGB**值，可以用**ti.Vector**三维向量储存值

```python
pixels[i, j] = ti.Vector([r,g,b])
```

其中R可以为原来的**1 - iterations * 0.02**，G可以为R的反色**（1-R）**，B可以为R和G的**线性插值**

```python
color = iterations * 0.02
r=color
g=1-color
b=lerp(r,g,0.7)
```

```python
def lerp(a: float, b: float, t: float):
	return a + (b - a) * t
```

#### NoBody Galaxy

Learn from:[【zhiyingli】N-Body and 2 BlackHoles](https://forum.taichi.graphics/t/1-n-body-and-2-blackholes/1769)	[Galaxy案例详解](https://www.bilibili.com/video/BV1aL4y1a7pv?p=11)



## 成功效果展示
### HW1

#### JuliaSet RGB

![JuliaSet](./data/JuliaSet.gif)

#### NoBody Galaxy

![fractal demo](./data/Galaxy.gif)
## 整体结构（Optional）
脉络清晰的结构能完整展示你的设计思想，以及实现方式，方便读者快读代入，建议可以在repo的目录中包含如下内容：
这个部分希望大家可以大作业中加入，小作业中可以选择性加入（如果不加也是OK的）
```shell
.
├── LICENSE
├── README.md
├── code
│   └── HW1
│       ├── NoBody.py
│       └── JuliaSet.py
├── data
│   ├── Galaxy.gif
│   └── JuliaSet.gif
├── note
│   └── Lec1
│       ├── HelloTaichi.py
│       ├── TaichiData.py
│       └── ComputeCore.py
└── requirements.txt

```

## 运行方式
```shell
cd code/HW1
python XXX.py 
```

