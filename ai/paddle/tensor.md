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

Tensor的name是其唯一的标识符，为python 字符串类型，查看一个Tensor的name可以通过Tensor.name属性。

默认地，在每个Tensor创建时，Paddle会自定义一个独一无二的name。

**五. stop_gradient**



### Tensor 的操作

**一. resize**


**二. cast**


**三. 索引和切片**


**四. 数据运算符**


**五. 逻辑运算符**


**六. 线性代数运算**







