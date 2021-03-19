# Keras实战之手写数字识别

在之前的实战章节中，我们学会了如何使用 tensorflow 自身提供的 API 去实现一个房价预测的模型。

但是，这个模型是一个非常简单的线性回归，并不能算作深度学习。

而在本节中，我们将以一个类似于深度学习的 `hello world` 示例来演示如何使用 Tensorflow 的 High Level API **Keras** 来实现一个
用于自动识别手写数字的模型。

## MNIST 数据集简介

MNIST 是一套手写体数字的图像数据集，包含 60000 个训练样本和 10000 个测试样本，由纽约大学的 Yann LeCun 等人维护。

![mnist](./pictures/mnist.jpg)

MNIST 图像数据集使用形如［28，28］的二阶数组来表示每个手写体数字，数组中的每个元素对应一个像素点，
即每张图像大小固定为 28x28 像素。

MNIST 数据集中的图像都是256阶灰度图，即灰度值 0 表示白色（背景），255 表示 黑色（前景），
使用取值为［0，255］的uint8数据类型表示图像。

### 下载 mnist 数据集

Keras 提供了一个 datasets 的模块，其中包括了各个常用的开放数据集。因此，我们可以直接使用 `keras.datasets` 来下载 mnist 数据集。

```python
from keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data('mnist/mnist.npz')

print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)

# (60000, 28, 28) (60000,)
# (10000, 28, 28) (10000,)
```

其中， `load_data` 函数接收一个参数 `path` 表示数据集下载后存放的地址。
需要注意的是，该地址是一个相对目录，实际存放数据集的绝对目录为: `~/.keras/datasets/$path` 。

我们可以将下载的部分数据进行可视化显示:

```python
import matplotlib.pyplot as plt

fig = plt.figure()
for i in range(15):
    plt.subplot(3,5,i+1) # 绘制前15个手写体数字，以3行5列子图形式展示
    plt.tight_layout() # 自动适配子图尺寸
    plt.imshow(x_train[i], cmap='Greys') # 使用灰色显示像素灰度值
    plt.title("Label: {}".format(y_train[i])) # 设置标签为子图标题
    plt.xticks([]) # 删除x轴标记
    plt.yticks([]) # 删除y轴标记
```

![mnist_demo](./pictures/mnist_demo.png)


## Softmax 网络介绍



## 利用 Softmax 实现手写数字识别的模型



## CNN 网络介绍



## 利用 CNN 实现手写数字识别的模型


