# Paddle 核心概念 Tensor 详解

作为 Paddle 学习的第一课，我们将首先从 Paddle 中最核心的的 Tensor 对象来进行讲解。

Paddle 和其他深度学习框架一样，使用 Tensor 来表示数据，在神经网络中传递的数据均为 Tensor 对象。

Tensor可以将其理解为多维数组，其可以具有任意多的维度，不同Tensor可以有不同的数据类型 (dtype) 和形状 (shape)。

同一Tensor的中所有元素的dtype均相同。如果你对 Numpy 熟悉，Tensor是类似于 Numpy Array 的概念。

## Tensor 的基本操作

### 创建 Tensor

创建 Tensor 有多种方式。

最常用的方式之一就是使用 `paddle.to_tensor()` 函数来将 list, np.array 等对象转化为 Tensor 对象。

```python3
# 一维 Tensor
ndim_1_tensor = paddle.to_tensor([2.0, 3.0, 4.0], dtype='float64', stop_gradient=False)
# 二维 Tensor
ndim_2_tensor = paddle.to_tensor(numpy.random.rand(3, 2))
# 三维 Tensor
ndim_3_tensor = paddle.to_tensor([[[1, 2, 3, 4, 5],
                                   [6, 7, 8, 9, 10]],
                                  [[11, 12, 13, 14, 15],
                                   [16, 17, 18, 19, 20]]])
```

Ps: 

1. Tensor 对象可以非常方便的转化为 numpy.array 对象，只需要调用 `Tensor.numpy()` 方法即可。
2. Tensor 对象中要求所有元素的 dtype 类型必须是一致的。


除了根据 list, np.array 转化为 Tensor 对象外，还可以使用一些 Paddle 的 API 来快速生成 Paddle 对象：

```python
paddle.zeros([m, n])                     # 创建数据全为0，shape为[m, n]的Tensor
paddle.ones([m, n])                      # 创建数据全为1，shape为[m, n]的Tensor
paddle.full([m, n], 10)                  # 创建数据全为10，shape为[m, n]的Tensor
paddle.arange(start, end, step)          # 创建从start到end，步长为step的Tensor
paddle.linspace(start, end, num)         # 创建从start到end，元素个数固定为num的Tensor
```


### Tensor 的属性

**一. shape**

查看一个Tensor的形状可以通过 `Tensor.shape` 属性查询，shape 属性可以显示 tensor 对象在每个维度上的元素数量。

与 shape 强关联的属性还有：

1. ndim: 显示 tensor 的维度数量，等价于 len(shape)
2. size: 显示 tensor 中的元素数量，等价于 shape 各个维度元素数量的乘积。


**二. dtype**

dtype 属性表示了 Tensor 元素中的数据类型，可以通过 Tensor.dtype 来查看。
dtype支持：'bool'，'float16'，'float32'，'float64'，'uint8'，'int8'，'int16'，'int32'，'int64'。

1. 通过Python元素创建的Tensor，可以通过dtype来进行指定，如果未指定：
    1. 对于python整型数据，则会创建int64型Tensor
    2. 对于python浮点型数据，默认会创建float32型Tensor，并且可以通过set_default_type来调整浮点型数据的默认类型。
2. 通过Numpy array创建的Tensor，则与其原来的dtype保持相同。


**三. place**

初始化 Tensor 时可以通过 place 参数来指定其分配的设备位置，可支持的设备位置有三种：

1. CPU
2. GPU
3. 固定内存


其中固定内存也称为不可分页内存或锁页内存，其与GPU之间具有更高的读写效率，并且支持异步传输，这对网络整体性能会有进一步提升，
但其缺点是分配空间过多时可能会降低主机系统的性能，因为其减少了用于存储虚拟内存数据的可分页内存。

示例如下：

```python
# CPU
cpu_tensor = paddle.to_tensor(1, place=paddle.CPUPlace())
# GPU
gpu_tensor = paddle.to_tensor(1, place=paddle.CUDAPlace(0))
# 固定内存
pin_memory_tensor = paddle.to_tensor(1, place=paddle.CUDAPinnedPlace())
```


**四. name**

Tensor 的 name 是其唯一的标识符，为 python 字符串类型，查看一个Tensor的name可以通过Tensor.name属性。

默认地，在每个Tensor创建时，Paddle会自定义一个独一无二的name。

**五. stop_gradient**

stop_gradient 用于表示对于一个 Tensor 对象而言，是否需要累积计算对应的梯度信息。
默认为 True ，即不保留梯度信息。

对于模型中需要训练的参数而言，stop_gradient 为 false，即会保留梯度信息并用于迭代。


### Tensor 的操作

**一. resize**

在 Paddle 中，我们可能会经常需要重新定义 tensor 的 shape。

为此，Paddle 提供了 reshape 接口来改变 Tensor 的 shape :

```python
ndim_3_tensor = paddle.to_tensor(numpy.random.rand(3, 2, 5))
new_ndim_3_tensor = paddle.reshape(ndim_3_tensor, [2, 5, 3])
print("After reshape:", new_ndim_3_tensor.shape)
```

其中，在 resize 操作中，是有一些特殊的使用技巧的：

1. 指定维度设置为 -1 时，表示这个维度的值是从Tensor的元素总数和剩余维度推断出来的。因此，有且只有一个维度可以被设置为-1。
2. 指定维度设置为 0 时，表示实际的维数是从 原Tensor对象的对应维数中复制出来的，与原 Tesnor 对象保持一致。
3. `paddle.reshape(ndim_3_tensor, [-1])` 可以将任意 Tensor 平铺展开为 1-D Tensor。 


**二. cast**

在 Paddle 中，使用 cast 函数可以修改指定的 Tensor 对象的 dtype：

```python
float32_tensor = paddle.to_tensor(1.0)

float64_tensor = paddle.cast(float32_tensor, dtype='float64')
print("Tensor after cast to float64:", float64_tensor.dtype)

int64_tensor = paddle.cast(float32_tensor, dtype='int64')
print("Tensor after cast to int64:", int64_tensor.dtype)
```

**三. 索引和切片**

我们可以通过索引或切片方便地访问或修改 Tensor。

Paddle 使用标准的 Python 索引规则，即与 Numpy 索引规则类似。

具体来说：

1. 基于 0-n 的下标进行索引，如果下标为负数，则从尾部开始计算。
2. 通过冒号 : 分隔切片参数 start:stop:step 来进行切片操作，其中 start、stop、step 均可缺省。


二维数据检索示例：

```python
ndim_2_tensor = paddle.to_tensor([[0, 1, 2, 3],
                                  [4, 5, 6, 7],
                                  [8, 9, 10, 11]])
print("Origin Tensor:", ndim_2_tensor.numpy())
print("First row:", ndim_2_tensor[0].numpy())
print("First row:", ndim_2_tensor[0, :].numpy())
print("First column:", ndim_2_tensor[:, 0].numpy())
print("Last column:", ndim_2_tensor[:, -1].numpy())
print("All element:", ndim_2_tensor[:].numpy())
print("First row and second column:", ndim_2_tensor[0, 1].numpy())
```


**四. 数学运算符**

在 Paddle 中，可以对多个 Tesnor 对象进行数学运算。

同时，在对 Paddle 进行数学运算的时候，还支持多种方式: Paddle API 方式与 Tensor 类成员方法，下面我们以具体的示例进行说明：

```python
x = paddle.to_tensor([[1.1, 2.2], [3.3, 4.4]], dtype="float64")
y = paddle.to_tensor([[5.5, 6.6], [7.7, 8.8]], dtype="float64")

# Paddle API 函数
print(paddle.add(x, y), "\n")

# Tensor 类成员方法
print(x.add(y), "\n")
```

两种方法的功能是相同的，因此，我们后续将仅以类成员方法为例进行说明。

目前，Paddle 支持的数学运算符包括如下：

```python
x.abs()                       #逐元素取绝对值
x.ceil()                      #逐元素向上取整
x.floor()                     #逐元素向下取整
x.round()                     #逐元素四舍五入
x.exp()                       #逐元素计算自然常数为底的指数
x.log()                       #逐元素计算x的自然对数
x.reciprocal()                #逐元素求倒数
x.square()                    #逐元素计算平方
x.sqrt()                      #逐元素计算平方根
x.sin()                       #逐元素计算正弦
x.cos()                       #逐元素计算余弦
x.add(y)                      #逐元素相加
x.subtract(y)                 #逐元素相减
x.multiply(y)                 #逐元素相乘
x.divide(y)                   #逐元素相除
x.mod(y)                      #逐元素相除并取余
x.pow(y)                      #逐元素幂运算
x.max()                       #指定维度上元素最大值，默认为全部维度
x.min()                       #指定维度上元素最小值，默认为全部维度
x.prod()                      #指定维度上元素累乘，默认为全部维度
x.sum()                       #指定维度上元素的和，默认为全部维度
```

Paddle对python数学运算相关的魔法函数进行了重写，以下操作与上述结果相同:

```shell
x + y  -> x.add(y)            #逐元素相加
x - y  -> x.subtract(y)       #逐元素相减
x * y  -> x.multiply(y)       #逐元素相乘
x / y  -> x.divide(y)         #逐元素相除
x % y  -> x.mod(y)            #逐元素相除并取余
x ** y -> x.pow(y)            #逐元素幂运算
```

**五. 逻辑运算符**

目前，Paddle 支持的逻辑运算符包括如下：

```python
x.isfinite()                  #判断tensor中元素是否是有限的数字，即不包括inf与nan
x.equal_all(y)                #判断两个tensor的全部元素是否相等，并返回shape为[1]的bool Tensor
x.equal(y)                    #判断两个tensor的每个元素是否相等，并返回shape相同的bool Tensor
x.not_equal(y)                #判断两个tensor的每个元素是否不相等
x.less_than(y)                #判断tensor x的元素是否小于tensor y的对应元素
x.less_equal(y)               #判断tensor x的元素是否小于或等于tensor y的对应元素
x.greater_than(y)             #判断tensor x的元素是否大于tensor y的对应元素
x.greater_equal(y)            #判断tensor x的元素是否大于或等于tensor y的对应元素
x.allclose(y)                 #判断tensor x的全部元素是否与tensor y的全部元素接近，并返回shape为[1]的bool Tensor
```

以下操作仅针对bool型Tensor:

```python
x.logical_and(y)              #对两个bool型tensor逐元素进行逻辑与操作
x.logical_or(y)               #对两个bool型tensor逐元素进行逻辑或操作
x.logical_xor(y)              #对两个bool型tensor逐元素进行逻辑亦或操作
x.logical_not(y)              #对两个bool型tensor逐元素进行逻辑非操作
```

同样地，Paddle对python逻辑比较相关的魔法函数进行了重写，以下操作与上述结果相同:

```shell
x == y  -> x.equal(y)         #判断两个tensor的每个元素是否相等
x != y  -> x.not_equal(y)     #判断两个tensor的每个元素是否不相等
x < y   -> x.less_than(y)     #判断tensor x的元素是否小于tensor y的对应元素
x <= y  -> x.less_equal(y)    #判断tensor x的元素是否小于或等于tensor y的对应元素
x > y   -> x.greater_than(y)  #判断tensor x的元素是否大于tensor y的对应元素
x >= y  -> x.greater_equal(y) #判断tensor x的元素是否大于或等于tensor y的对应元素
```

**六. 线性代数运算**

目前，Paddle 支持的线性代数操作如下：

```python
x.cholesky()                  #矩阵的cholesky分解
x.t()                         #矩阵转置
x.transpose([1, 0])           #交换axis 0 与axis 1的顺序
x.norm('fro')                 #矩阵的 Frobenius 范数
x.dist(y, p=2)                #矩阵（x-y）的2范数
x.matmul(y)                   #矩阵乘法
```

需要注意，Paddle中Tensor的操作符均为非inplace操作，即 x.add(y) 不会在tensor x上直接进行操作，而会返回一个新的Tensor来表示运算结果。

## Tensor 的广播机制

飞桨（PaddlePaddle，以下简称Paddle）和其他框架一样，提供的一些API支持广播(broadcasting)机制，允许在一些运算时使用不同形状的张量。

通常来讲，如果有一个形状较小和一个形状较大的张量，会希望多次使用较小的张量来对较大的张量执行一些操作，
看起来像是较小形状的张量的形状首先被扩展到和较大形状的张量一致，然后做运算。
值得注意的是，这期间并没有对较小形状张量的数据拷贝操作。

飞桨的广播机制主要遵循如下规则:

1. 每个张量至少为一维张量。
2. 从后往前依次比较张量的形状，当前维度的大小要么相等，要么其中一个等于一，要么其中一个不存在。


示例如下：

```python
import paddle

x = paddle.ones((2, 3, 4))
y = paddle.ones((2, 3, 4))
# 两个张量 形状一致，可以广播
z = x + y
print(z.shape)
# [2, 3, 4]

x = paddle.ones((2, 3, 1, 5))
y = paddle.ones(   (3, 4, 1))
# 从后向前依次比较：
# 第一次：y的维度大小是1
# 第二次：x的维度大小是1
# 第三次：x和y的维度大小相等
# 第四次：y的维度不存在
# 所以 x和y是可以广播的
z = x + y
print(z.shape)
# [2, 3, 4, 5]

# 相反
x = paddle.ones((2, 3, 4))
y = paddle.ones((2, 3, 6))
# 此时x和y是不可广播的，因为第一次比较 4不等于6
# z = x + y
# InvalidArgumentError: Broadcast dimension mismatch.
```


## Tensor 的自动微分机制






