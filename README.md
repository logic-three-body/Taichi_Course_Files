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

代码原版是3000颗小行星之间万有引力作用，在此基础上加入一颗常量行星（不受其他行星万有引力作用但对其他行星有作用力）

常量行星的质量相比小行星大很多倍，这样会吸引周围的行星涌向自己，常量行星半径也很大（为了醒目，后续会有鼠标控制）

```python
m = 1#小行星质量
M = 5000#常量行星质量
planet_radius = 2#小行星半径
Const_planet_radius = 30#常量行星半径
```

给常量行星一个初始位置，后面鼠标也会控制这个位置

```python
Const_Pos=ti.Vector.field(2,ti.f32,())
Const_Pos[None]=[.5,.5]
```

在计算作用力的函数中，添加常量行星和其他行星作用力逻辑（和小行星逻辑一样，核心是万有引力公式），这里会给每个小行星做一个标记，当常量星和小行星到达一定距离会被标记，在开启吸入模式后（点击鼠标右键），这些小行星会被吸入，这里吸入的逻辑就是将他们的position置为负（就不在屏幕空间[0,1]X[0,1]内了），velocity置为0

compute_force函数：

```python
# Const planet
for i in range(N):
    diff = pos[i] - Const_Pos[None]#距离
    if diff.norm() < 1e-2:#吸入标记
    	IsHale[0, i] = 1
    else:
    	IsHale[0, i] = 0

	r = diff.norm(1e-2)  # clamp to 1e-1 if diff<0
	f = -G * m * M * (1.0 / r) ** 3 * diff #万有引力公式
	force[i] += f
```

update函数：

```python
if Start[None] and IsHale[0, i]:
	pos[i] = [-10000, -10000]
	vel[i] = [0, 0]
else:
	vel[i] += dt * force[i] / m
	pos[i] += dt * vel[i]
```

## 成功效果展示
### HW1

#### JuliaSet RGB

![JuliaSet](./data/JuliaSet.gif)

#### NoBody Galaxy

鼠标左键控制常量巨星的位置，点击右键常量巨星会开始吸收周围行星（其他按键：点击键盘‘r’重新开始，空格暂停）

![fractal demo](./data/Galaxy.gif)
## 整体结构（Optional）
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

