# tensorflow 核心概念

在进一步学习 tensorflow 的使用之前，我们非常有必要来了解一些 tensorflow 的一些核心概念。

## 张量（tensor）

在数学定义中， **张量** 是一种几何实体，从广义上来讲，张量可以表示任意形式的数据。

其中：

 - 标量可以认为是0阶张量。
 - 向量可以认为是1阶张量。
 - 矩阵可以认为是2阶张量。
 - 数据立方体可以认为是3阶向量。
 - 超过3维的数据可以认为是n阶张量。


可以看出，张量的 **阶数** 描述它表示数据的最大维度。

而具体到 Tensorflow 中， Tensor 表示的是某种相同数据类型的多维数组。

因此，对于张量而言，它有两个重要属性:

 - 数据的类型：如浮点型、整型、字符串型等等。
 - 数组的形状：如各个维度的大小。


那么，在 Tensorflow 中，张量是用来做什么的呢，又具备哪些特点呢？

1. 首先，张量是用来表示 Tensorflow 计算过程中的多维数据的。
2. 对于 Tensorflow 中的每次执行操作而言，它的输入和输出数据其实都是张量。
3. 而张量本身也是有 Tensorflow 的执行操作来创建和计算的。
4. 同时，张量的形状在编译时可能不会完全确定，而是在运行的过程中通过输入内容进行推断计算得到的。


而 Tensorflow 中有几个相对特别的张量，我们来此处进行简单说明：

 - tf.constant: Tensorflow 中定义的常量，一旦设置后不能进行修改。 
 - tf.placeholder: Tensorflow 中定义的占位符，往往用于接收输入数据。
 - tf.Variable: Tensorflow 中定义的变量，在数据流图的计算过程中进行计算和赋值等操作。


针对上述提及的 constant 而言，相对来说比较简单，我们在后续应用到时直接讲解就行。

而针对 Variable 和 placeholder ，我们需要多提几句。

## 变量（Variable）

Tensorflow 中的 Variable 的主要作用是维护特定节点的状态，如深度学习或机器学习的模型参数。

其中：

 - tf.Variable 方法是一个 Operation。
 - 而 tf.Variable 方法的返回值是一个变量（一种张量）。


通过 tf.Variable 方法创建的变量与张量一样，也可以作为 Operation 的输入和输出，但是需要注意的是：

 - 普通张量的生命周期通常随着依赖的计算完成而结束，内存也就随之能够正常释放。
 - 而 Variable 变量则是常驻内存，在每一步训练时不断更新其值，从而实现模型参数的不断迭代优化。


此外，考虑到 tensorflow 在大型模型的训练过程中往往不是一蹴而就的，可能需要分多个阶段进行训练，甚至训练的过程中还会出现人工介入
进行参数调优等现象，因此，我们需要能够将 tensorflow 训练的模型参数能够持久化保存和恢复。

为此，tensorflow 提供了一个能够将 Variable 持久化到文件中的方法: `tf.train.Saver` 。

![saver](./pictures/saver.png)

如上图所示，Variable 在持久化保存时，会保存至 checkpoint 文件，同时，我们也可以在任意阶段重新进行持久化或者从持久化文件中恢复参数。


## 占位符（placeholder）

Tensorflow 使用占位符操作表示图外输入的数据，如训练数据和测试数据。

Tensorflow 数据流图描述了算法模型的计算拓扑，其中的各个操作（节点）都是抽象的函数映射和数学表达式。

换句话说，数据流图本身是一个具有计算拓扑和内部结构的『壳』，在用户向数据流图填充数据之前，图中并没有执行任何的计算。

```python
# 定义placeholder
x = tf.placeholder(tf.int16, shape=(), name="x")
y = tf.placeholder(tf.int16, shape=(), name="y")

# 建立session
with tf.Session() as session:
    # 填充数据后真正执行操作
    print(session.run(add, feed_dict={x: 2, y: 3}))  # 其中add和mul都是提前定义好的数据流图的操作
    print(session.run(mul, feed_dict={x: 2, y: 3}))
```


## 操作（operation）

在 Tensorflow 中用 数据流图 来表示算法模型。而数据流图是由节点和有向边组成的，每一个节点都对应了一个具体的操作。

因此，数据流图中，本身上就是定义了如何通过一组操作来依次处理数据的过程。

现在，我们就来学习一些 tensorflow 中的 操作（operation）具体的含义。

tensorflow 中的节点按照功能可以分为 3 种：

 - 存储节点：有状态的变量操作，通常用来存储模型参数。
 - 计算节点：无状态的计算或者控制操作，主要负责算法的逻辑表达式或者流程控制。
 - 数据节点：数据的占位符操作，用于描述图外的输入数据的属性。


下面，我们来看一下 tensorflow 中支持了哪些典型的计算和控制操作：

|操作类型|典型操作|
|-------|------|
|基础算术|add / multiply / mod / sqrt / sin / trace / fft / argmin|
|数组运算|size / rank / split / reverse / cast / one_hot / quantize|
|梯度裁剪|clip_by_value / clip_by_norm / clip_by_global_norm|
|逻辑控制和调试|identity / logical_and / equal / less / is_finite / is_nan|
|数据流控制|enqueue / dequeue / size / take_grad / apply_grad|
|初始化操作|zeros_initializer / random_normal_initializer / orthogonal_initializer|
|神经网络运算|convolution / pool / bias_add / softmax / dropout / erosion2d|
|随机运算|random_normal / random_shuffle / multinomial / random_gamma|
|字符串运算|string_to_hash_bucket / reduce_join / substr / encode_base64|
|图像处理运算|encode_png / resize_images / rot90 / hsv_to_rgb / adjust_gamma|


## 会话（session）

会话提供了计算张量和执行操作的运行环境。

具体来说，它本质上是一个发送计算任务的客户端，通过客户端将所有的计算任务下发给它连接的执行引擎来完成计算。

一个典型的Session流程包含如下步骤：

```python
# 1. 创建会话
session = tf.Session(target=..., graph=..., config=...)

# 2. 执行操作计算张量
session.run(...)

# 3. 关闭会话
session.close()
```

其中，可以看到，在创建 Session 对象时，用到了三个参数，它们的含义如下：

|参数名称|功能说明|
|------|-------|
|target|会话连接时的执行引擎|
|graph|会话加载时的数据流图|
|config|会话启动时的配置项|


关于上述参数的具体使用方式和详细介绍，在后续的文章中我们都会一一进行讲解。

下面，我们来看一个完整的示例：

```python
import tensorflow as tf
# 定义数据流图： z = x * y
x = tf.placeholder(tf.int16, shape=(), name="x")
y = tf.placeholder(tf.int16, shape=(), name="y")
z = tf.multiply(x, y, name="z")
# 创建会话
session = tf.Session()

# 执行操作计算张量
print(session.run(z, feed_dict={x: 3.0, z: 2.0}))

# 关闭会话
session.close()
```

除了上述示例中获取张量值用到的 `session.run` 外，其他还有两种方法来计算张量值：

 - Tensor.eval()
 - Operation.run()


我们以下面的代码为例进行说明：

```python
import tensorflow as tf
# 创建数据流图: y = W * x + b, 其中，W 和 b 为存储节点， x 为数据节点
x = tf.placehold(tf.float32)
W = tf.Variable(1.0)
b = tf.Variable(1.0)
y = W * x + b

# 创建会话
with tf.Session() as session:
    tf.global_variables_initializer().run()  # 初始化全部变量
    fetch = y.eval(feed_dict={x: 3.0})   # 等价于 fetch = session.run(y, feed_dict={x: 3.0})
    print(fetch)
```

那么，Tensorflow 的会话究竟是怎么执行的呢？下面，我们来简单看一下其执行原理。

当我们调用 `session.run(train_op)` 语句执行训练操作时:

1. 首先，程序内部提取操作依赖的所有前置操作。这些操作的节点会共同构成一副子图。
2. 然后，程序会将子图中的计算节点、存储节点、数据节点按照鸽子的执行设备进行分类，相同设备上的节点组成了一副局部图。
3. 最后，每个设备上的局部图在实际执行时，根据节点间的依赖关系将各个节点有序的加载到设备上执行。


对于一个单机程序而言，相同机器上不同编号的 GPU 或者 CPU 其实就是不同的设备，我们在创建节点的的时候其实就可以指定执行该节点的设备：

```python
# 在0号CPU执行的存储节点
with tf.device("/cpu:0"):
    v = tf.Variable(...)

# 在0号GPU执行计算的计算
with tf.device("/gpu:0"):
    z = tf.matmul(x, y)
```

![client-server-worker](./pictures/client-server-worker.png)

以上图为例，整体的运行流程如下：

1. Client 端负责数据流图的结构设计，并将设计完成的数据流图发送Server端。
2. Server 端对数据流图中的任务进行拆分，并下发给对应执行的设备Worker。
3. Worker 负责对应的OP执行相关操作。


## 优化器（optimizer）

在学习优化器之前，我们首先需要学习一下什么是 **损失函数** 、 **经验风险** 、 **结构风险** 。

损失函数是指在评估特定模型参数和指定的输入下，表达模型输出的的推理值和真实值之前的不一致程度。

一个广义的损失函数 L 的形式化定义如下：

$$
loss = L(f(x_i; \theta), y_i)
$$

其中：

1. $$x_i$$ 表示指定的输入
2. $$\theta$$ 表示指定的模型参数
3. $$f(x_i; \theta)$$ 表示将将指定输入传给模型后得到的模型推理值输出。
4. $$y_i$$ 表示真实值


常见的损失函数有：

平方损失函数

$$
loss = (y_i - f(x_i; \theta))^2
$$

交叉熵损失函数

$$
loss = y_i * \log(f(x_i; \theta))
$$

指数损失函数

$$
loss = exp(-y_i * f(x_i; \theta))
$$

了解了什么是损失函数，下面我们需要再继续看一下什么是经验风险。

使用损失函数对所有的训练样本求损失值，再累加求平均就可以得到模型的经验风险。转换为数学表达式的定义如下：

$$
R_{emp}(f) = \frac{1}{N} \sum_{i=1}^{N} L(f(x_i; \theta), y_i)
$$

理想情况下，我们希望能找到一组参数使得模型的经验风险最小。

但实际上，由于我们的测试数据不能包含全部数据，因此，如果过度追求训练数据的低损失值，就会造成过拟合问题。
简单来说，过拟合是指模型参数过分适配当前的训练集，导致在面对一些新的样本集就会无所适从，这次模型的泛化能力就会变差。

造成过拟合最常见的原因往往是模型复杂度过高导致，因此，为了降低训练过度导致的过拟合问题，可以引入一个
用于衡量模型复杂度的正则化项(regularizer)/惩罚项(penalty term)，我们称为 $$J(f)$$。

常用的正则化项有: L0 范数、L1 范数、L2 范数。

因此，我们将模型最优化的目标可以优化为泛化能力更好的 结构风险最小化（structural risk minimization, SRM）。

如下式所示，它由经验风险项和正则项两部分组成：

$$
R_{srm}(f) = \min\frac{1}{N} \sum_{i=1}^{N} L(f(x_i; \theta), y_i) + \lambda J(\theta)
$$

在模型训练的过程中，结构风险不断的降低。当小于我们设置的阈值损失值时，我们就可以认为此时的模型已经满足需求。

因此，模型训练的本质就是在最小化结构风险的同时取得最优的模型参数。

最优模型参数的表达式定义如下：

$$
\theta^* = arg \min_\theta R_{srm}(f) = arg \min\frac{1}{N} \sum_{i=1}^{N} L(f(x_i; \theta), y_i) + \lambda J(\theta)
$$

了解了 **损失函数** 、 **经验风险** 、 **结构风险** 的相关概念之后，我们知道其实深度学习本质上就是求解一个最优化的问题。

求解最优化问题的方法我们称之为 **优化算法** ，通常采用迭代的方式来实现:
首先设置一个初试的可行解，然后基于特定函数反复重新计算可行解，直到找到一个最优解或者达到预设的收敛条件。

不同的优化算法采用的迭代策略各有不同，常见的迭代算法包括：

 - 使用目标函数的一阶导数，如梯度下降法。
 - 使用目标函数的二阶导数，如牛顿法。
 - 使用前几轮的迭代信息，如Adam。


基于梯度下降法的迭代策略相对最简单，它表示直接沿着梯度的负方向，即 **目标函数下降最快** 的方向进行直线迭代，其计算表达式如下：

$$
x_{k+1} = x_k - \alpha * grad(x_k)
$$

其中，$$\alpha$$ 表示每次迭代的步长。

因此，对于一个典型的深度学习问题而言，包含以下三部分：

1. 模型：$$y = f(x) = wx + b$$，其中 x 是输入数据， y 是模型输出的推理值，f 是模型的定义，其中可能包含若干个需要用户训练的模型参数。
2. 损失函数：$$loss = L(y, y')$$，其中，y' 对应x的真实值（标签），loss为损失函数输出的损失值。
3. 优化算法：$$w <- w + \alpha * grad(w)$$、$$b <- b + \alpha * grad(b)$$ 其中，
   grad(w) 和 grad(b) 分别表示当损失值为loss时，模型参数 w 和 b 各自的梯度值。


而具体到优化算法时，一次典型的迭代优化可以分为以下 3 个步骤：

1. 计算梯度: 调用 `compute_gradients` 方法。
2. 处理梯度: 用户按照自己的需求处理梯度值，例如梯度裁剪和梯度加权。
3. 应用梯度: 调用 `apply_gradients` 方法，将处理后的梯度值应用到模型参数的迭代中。


最后，我们来看一下 tensorflow 中已经内置了哪些优化器吧：

|优化器名称|文件路径|
|-----|---------|
|Adadelta|tensorflow/python/training/adadelta.py
|Adagrad|tensorflow/python/training/adagrad.py
|Adagrad Dual Averaging|tensorflow/python/training/adagrad_da.py
|Adam|tensorflow/python/training/adam.py
|Ftrl|tensorflow/python/training/ftrl.py
|Gradient Descent|tensorflow/python/training/gradent_descent.py
|Momentum|tensorflow/python/training/momentum.py
|Proximal Adagrad|tensorflow/python/training/proximal_adagrad.py
|Proximal Gradient Descent|tensorflow/python/training/proximal_gradent_descent.py
|Rmsprop|tensorflow/python/training/rmsprop.py
|Synchronize Replicas|tensorflow/python/training/sync_replicas_optimizer.py
