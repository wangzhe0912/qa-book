# tensorflow初体验之房价预测

了解了 tensorflow 的基本概念后，接下来，我们将以一个 房价预测 的案例为例，演示 tensorflow 的基本功能使用。

## 背景知识说明

开始正式进入 Tensorflow 实战之前，我们还需要了解一些机器学习相关的背景知识。

### 监督学习（supervised learning）

监督学习是机器学习的方法之一，它是指从训练数据（输入和预期输出）中学到的一个模型（函数），并且可以根据模型推断出新实例的方法。

其中，函数的输出既可以是一个连续值（如回归分析）或一个离散值/类别标签（如分类问题）。

![supervised_learning](./pictures/supervised_learning.png)

上图表示了一个监督学习的基本流程。

典型的监督学习算法非常多，例如：

 - 线性回归（Linear Regression）
 - 逻辑回归（Logistic Regression）
 - 决策树（Decision Tree）
 - 随机森林（Random Forest）
 - 最近邻算法（k-NN）
 - 朴素贝叶斯（Naive Bayes）
 - 支持向量机（SVM）
 - 感知器（Perceptron）
 - 深度神经网络（DNN）


### 线性回归与梯度下降法

线性回归可以说是监督学习中最简单的算法了，下面我们来对线性回归进行分析。

在统计学中，线性回归是指 **利用线性回归方程的最小二乘函数对一个或多个自变量和因变量之间的关系进行建模的一种回归分析** 。

这种函数是一个或多个称为回归系数的模型参数的线性组合。

以 单变量线性回归 为例，如果一个模型是线性关系的，那么它可以表示如下：

$$
y = wx + b
$$

那么，我们也就可以假设函数如下：

$$
h_\theta(x) = \theta(x)_0 + \theta(x)_{1}x_1 = \theta(x)_{0}x_0 + \theta(x)_{1}x_1 = \theta(x)^Tx  (x_0=1)
$$

其中，$$\theta$$ 就是我们假设的函数参数。

而假设函数和理想模型的损失值（误差）就是：

$$
loss = y - h_{\theta}(x)
$$

因此，我们想要做的就是从一组样本 $$(x_i, y_i)$$ 中找出误差最小的 $$\theta$$ 值。
此时，我们可以使用最小二乘法，即它的优化目标为最小化残差平方和：

$$
J(\theta) = \frac{1}{n} \sum_{i=1}^{n} (h_{\theta}(x_i) - y_i)^2
$$

而梯度迭代法就是指在优化目标函数的每一轮迭代中，都按照模型参数 $$\theta$$ 的梯度方向进行变更，即表达式如下：

$$
\theta_j := \theta_j - \alpha \frac{\partial}{\partial\theta_j} J(\theta)
$$

代入 $$J(\theta)$$ 进行求导，得到的结果如下：

$$
\theta_j := \theta_j - 2\alpha \frac{1}{n} \sum_{i=1}^{n} (h_{\theta}(x_i) - y_i) (x_i)
$$

下面，我们来看一下 **多变量** 线性回归的场景：

多变量线性回归可以表示如下：

$$
y = w_{0} + w_{1}x_{1} + w_{2}x_{2} = W^{T}X
$$

那么，我们也就可以假设函数如下：

$$
h_\theta(X) = \theta_{0}x_0 + \theta_{1}x_1 + \theta_{2}x_2 = \theta(x)^{T}X      (x_0=1)
$$

其中，$$\theta$$ 就是我们假设的函数参数。

而假设函数和理想模型的损失值（误差）就是：

$$
loss = y - h_{\theta}(X)
$$

同样可以使用最小二乘法，即它的优化目标为最小化残差平方和：

$$
J(\theta) = (h_\theta(X) - y)^T(h_\theta(X) - y)
$$


## 问题描述

下面，我们来以单变量房价预测问题为例，即根据房屋面试 $$x$$ 来预测销售价格 $$y$$ 。

示例的训练数据如下：

|面积（平方英尺）|价格（美元）|
|-------------|----------|
|2104|399900|
|1600|329900|
|2400|369000|
|1416|232000|
|3000|539900|
|1985|299900|
|1534|314900|
|1427|198999|
|1380|212000|
|1494|242500|
|1940|239999|
|2000|347000|
|1890|329999|
|4478|699900|
|1268|259900|
|....|......|

此外，我们来考虑一下当房价预测问题为多变量预测问题时，输入的数据会是什么样？
假设给定的输入数据中包含房屋面积 $$x_1$$ 和 卧室数量 $$x_2$$，来预测其房屋价格：

示例的训练数据如下：

|面积（平方英尺）|卧室数量（个）|价格（美元）|
|-------------|----------|-----------|
|2104|3|399900|
|1600|3|329900|
|2400|3|369000|
|1416|2|232000|
|3000|4|539900|
|1985|4|299900|
|1534|3|314900|
|1427|3|198999|
|1380|3|212000|
|1494|3|242500|
|1940|4|239999|
|2000|3|347000|
|1890|3|329999|
|4478|5|699900|
|1268|3|259900|
|....|......|


了解了想要解决的问题之后，我们就要看如何一步步的解决问题了。

使用 Tensorflow 训练模型的整体工作流如下图所示：

1. 数据读入
2. 数据分析
3. 数据预处理（数据规范化）
4. 创建模型（数据流图）
5. 创建会话（运行环境）
6. 训练模型


下面，我们来依次学习如下步骤。

## 数据读入

首先是数据读入，对于机器学习中的数据，常常是使用 csv 文件的方式进行存储，而我们想要做的其实就是从 csv 中读取文件。

在 Python 的大量第三方库中，其实有很多库都可以操作 csv 文件，而在此处，我们将会使用的是一个 `pandas` 的库。

熟悉机器学习的同学应该对 `pandas` 库并不会太陌生。它是一个基于 BSD 开源协议许可的软件库，
面向 Python 用户的高性能和易于上手的数据结构化和数据分析的工具。

在 pandas 中， DataFrame 是其最核心的数据存储对象。
具体来说，DataFrame 是一个二维带标记的数据结构，每一列的数据类型可以不同，我们常常可以用它来当做电子表格或数据库表。

![data_frame](./pictures/dataframe.png)

而使用 `pandas` 来读取 csv 文件的内容非常简单，简单到只需要一行代码就能将 excel 数据转换为 dataframe 对象：

```python
import pandas as pd
# 读取指定 csv 文件，并为每一列设置列名
df0 = pd.read_csv('data0.csv', names=['square', 'price'])
# 打印 dataframe 的前五行
df0.head()
```


## 数据预处理与可视化

当我们将 csv 数据读入后，常常会简单的对数据进行一定的分析，如数据分布情况等。而数据分析的最佳方式之一就是数据可视化了。

接下来，我们来看一下如何进行数据的可视化。

Python 中关于数据可视化提供了如下相关的第三方库：

1. matplotlib: 它是一个 Python 的 2D 绘图库，可以生成高质量的图片并支持各种存储格式，同时能够广泛支持多个运行平台，
   如 Python 脚本、 IPython Shell 和 Jupyter Notebook.
2. seaborn: 它是一个基于 matplotlib 的 High Level 的 Python 数据可视化库，提供了更加易用的高级接口，用于绘制
   精美且信息丰富的统计图形。
3. mpl_toolkits.mplot3d: 它是一个基础的 3D 绘图工具集，也是 matplotlib 的一部分。


下面，我们分别来将刚才的读入的数据进行数据可视化。

对于单变量数据而言，其数据可视化数据如下，横轴表示房屋面积，纵轴表示房屋价格：

```python
import pandas as pd
import seaborn as sns

# 设置 seaborn 的基本配置
sns.set(context="notebook", style="whitegrid", palette="dark")

# 读取指定 csv 文件，并为每一列设置列名
df0 = pd.read_csv('data0.csv', names=['square', 'price'])

# 数据可视化图
sns.lmplot('square', 'price', df0, height=4, fit_reg=False)  # fit_reg 设置为 True 时，可以自动生成拟合线
```

![dimension_1](./pictures/dimension_1.png)


对于多变量数据而言，其数据可视化数据如下，x轴表示房屋面积，y轴表示房间数量，z轴表示房屋价格：

```python
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# 读取多变量数据
df1 = pd.read_csv('data1.csv', names=['square', 'bedrooms', 'price'])

# 创建一个 Axes3D object
fig = plt.figure()
ax = plt.axes(projection='3d')
# 设置 3 个坐标轴的名称
ax.set_xlabel('square')
ax.set_ylabel('bedrooms')
ax.set_zlabel('price')
# 绘制 3D 散点图, c表示散点深度的取决对象，cmap表示散点的颜色
ax.scatter3D(df1['square'], df1['bedrooms'], df1['price'], c=df1['price'], cmap='Greens')
```

![dimension_2](./pictures/dimension_2.png)

观察上述三维散点图，你会发现它的 x 轴、 y 轴 和 z 轴的分布太不均匀了。

例如：

 - x 轴的区间是 1-5
 - y 轴的区间是 0- 5000
 - z 轴的区间甚至是 0 - 7000000


如此不均匀的分布对于模型训练等场景都会带来一定的弊端，因此，在模型训练还是之前，我们通常需要将其进行数据归一化。

常用的数据归一化的方式如下：

$$
x' = \frac{x - \bar{x}}{\sigma}
$$

那么，我们再来看看如何用代码实现呢？这是就要体现出 pandas 强大的功能了。

```python
def normalize_feature(df):
    """
    归一化函数
    """
    return df.apply(lambda column: (column - column.mean()) / column.std())

df1 = pd.read_csv('data1.csv', names=['square', 'bedrooms', 'price'])
df = normalize_feature(df1)
```

我们定义了一个归一化函数 `normalize_feature` ，在该函数内，我们针对每一列，计算的列内元素的均值和方差，并从而进行了数据的归一化。

```python
# 创建一个 Axes3D object
fig = plt.figure()
ax = plt.axes(projection='3d')
# 设置 3 个坐标轴的名称
ax.set_xlabel('square')
ax.set_ylabel('bedrooms')
ax.set_zlabel('price')
# 绘制 3D 散点图, c表示散点深度的取决对象，cmap表示散点的颜色
ax.scatter3D(df['square'], df['bedrooms'], df['price'], c=df['price'], cmap='Reds')
```

归一化后的数据可视化图如下所示：

![normalized_image](./pictures/normalized_image.png)

## 设计数据流图

下面，我们就要正式进入到数据流图的设计中了。 而设计数据流图的第一步就是要确定输入、输出数据了。

我们以 **多变量预测问题** 为例，我们其实就是想要估计下式中的 `\theta` :

$$
h_\theta(X) = \theta_{0}x_0 + \theta_{1}x_1 + \theta_{2}x_2 = \theta(x)^{T}X      (x_0=1)
$$

为了能够方便的进行矩阵乘法，我们需要对输入参数中进行 $$x_0 = 1$$ 的填充，即增加一列全为1的列。

此时，我们就需要用到另外一个 Python 的第三方库 numpy 了。

numpy 可以说是 Python 机器学习中的基础了，几乎所有的深度学习框架底层的数据结构存储都是基于 numpy 的。
同时 numpy 也是一个基础科学计算库，在多维数组上实现了线性袋鼠、傅立叶变换和其他丰富的函数计算。

下面，我们就来看看如何将读取的数据进行转换，得到模型的输入和输出数据吧：

```python
import numpy as np
ones = pd.DataFrame({'ones': np.ones(len(df))})  # 生成一列全为1的列
df = pd.concat([ones, df], axis=1) # 将全为1的列插入到原有的 dataframe 中

X_data = np.array(df[df.columns[0:3]])  # 前三列为模型的输入数据
y_data = np.array(df[df.columns[-1]]).reshape(len(df), 1)   # 最后一列为标记结果，用于与模型的输出结果计算偏差
```

完成了输入和输出数据，接下来，就是要完整的定义模型的数据流图了：

```python
import tensorflow as tf

alpha = 0.01 # 学习率 alpha
epoch = 500 # 训练全量数据集的轮数

# 输入 X，形状[47, 3]
X = tf.placeholder(tf.float32, X_data.shape)
# 输出 y，形状[47, 1]
y = tf.placeholder(tf.float32, y_data.shape)

# 权重变量 W，形状[3,1]
W = tf.get_variable("weights", (X_data.shape[1], 1), initializer=tf.constant_initializer())

# 假设函数 h(x) = w0*x0+w1*x1+w2*x2, 其中x0恒为1
# 推理值 y_pred  形状[47,1]
y_pred = tf.matmul(X, W)

# 损失函数采用最小二乘法，y_pred - y 是形如[47, 1]的向量。
# tf.matmul(a,b,transpose_a=True) 表示：矩阵a的转置乘矩阵b，即 [1,47] X [47,1]
# 损失函数操作 loss
loss_op = 1 / (2 * len(X_data)) * tf.matmul((y_pred - y), (y_pred - y), transpose_a=True)
# 随机梯度下降优化器 opt
opt = tf.train.GradientDescentOptimizer(learning_rate=alpha)
# 单轮训练操作 train_op
train_op = opt.minimize(loss_op)
```

在上述的代码中，我们完整的定义了整个模型的结构（即数据流图），其中包含了节点关系、损失函数以及优化器等。


## 模型训练

当数据流图定义完成，此时我们就可以直接建立一个会话进行模型的训练了：

```python
with tf.Session() as sess:
    # 初始化全局变量
    sess.run(tf.global_variables_initializer())
    # 开始训练模型，
    # 因为训练集较小，所以每轮都使用全量数据训练
    for e in range(1, epoch + 1):
        sess.run(train_op, feed_dict={X: X_data, y: y_data})
        if e % 10 == 0:
            loss, w = sess.run([loss_op, W], feed_dict={X: X_data, y: y_data})
            log_str = "Epoch %d \t Loss=%.4g \t Model: y = %.4gx1 + %.4gx2 + %.4g"
            print(log_str % (e, loss, w[1], w[2], w[0]))
```

此时，模型才会正式进入计算的过程中，并在不断迭代的过程中打印相关的loss值及训练过程中的模型参数值等信息。
