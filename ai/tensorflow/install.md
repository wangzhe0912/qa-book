# tensorflow 环境搭建

了解了 tensorflow 的各种优点、应用场景后，接下来，我们就需要去快速体验一下 tensorflow 的功能了。

那么，实战 tensorflow 的第一步永远都是环境搭建，下面，我们来分别用几种不同的方式来进行 tensorflow 的环境搭建。

## 基础环境说明

首先，Tensorflow 支持各种各样的硬件平台，例如：

 - CPU
 - GPU
 - Cloud TPU
 - Android
 - IOS
 - 嵌入式系统
 - 浏览器等


而支持 Tensorflow 的操作系统也多种多样，例如: Ubuntu, Windows, macOS, Raspbian 等等。

下面，我们将以 macOS 为例来演示如何通过多种方式搭建 tensorflow 基础环境。

Ps: 在本文中，我们将会搭建 tensorflow 1.15.5 （tensorflow 1.0版本中的最新版本）环境，在后续的文章中，我们以后搭建 tensorflow 2.0+ 的
版本。


## 物理机 / 虚拟机上搭建 tensorflow

我们在本系列文章中，主要会以 Python 代码为例，来演示 tensorflow 相关的功能使用，因此，我们搭建的 tensorflow 也是基于 Python 语言的。

而搭建 Python 的 Tensorflow 环境首先就需要安装 Python 和 Python 的包管理工作 `pip` 。

而 `Anaconda` 是一个集成了 Python + Python 部分依赖的一个软件包，我们可以直接使用
[Anaconda](https://www.anaconda.com/products/individual)
进行相关环境搭建。

安装完成 Anaconda 后，我们可以使用 `conda` 来创建一个 Python 的虚拟环境。

```shell
conda create -n tensorflow115 python=3.6
```

其中：

 - -n 表示创建新创建的虚拟环境的名称
 - python=3.6 表示当前创建的虚拟环境使用的Python版本是3.6


Ps: Python虚拟环境可以在同一台机器上管理多个不同版本的 Python 解释器，同时，可以给每个 Python 解析器安装不同的版本的第三方库依赖。
这样，我们就可以在同一台机器上同时体会 Python 2.7 和 Python 3.6，也可以同时使用 Tensorflow 1.X 和 Tensorflow 2.X。


接下来，我们可以切换到新创建的虚拟环境中: 

```shell
conda activate tensorflow115
```

此时，我们使用 `pip` 进行安装的依赖都会安装到该虚拟环境下，同时使用的 python 以及其他第三方库二进制可执行文件都会使用该虚拟环境下的文件。

切换到对应的虚拟环境后，我们就可以安装 Python 的 tensorflow 依赖库了:

```shell
pip3 install tensorflow==1.15.5
```

我们使用了 1.15.5 版本的tensorflow进行安装，如果依赖包下载速率太慢的话，也可以指定国内的一些 `pip` 源:

```shell
pip3 install tensorflow==1.15.5 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

安装完成后，我们就可以使用 python 解析器来验证一下 tensorflow 是否已经正常安装了:

```shell
python3 -c "import tensorflow as tf"
```

如果没有看到什么报错的话，那么恭喜你，你的 tensorflow 环境已经基本搭建好了。

## jupyter notebook 中使用 tensorflow







## 在 Docker 容器中使用 tensorflow











