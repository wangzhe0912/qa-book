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

下面，我们来体验一下 tensorflow 的 hello world !

编写 `hello_tensorflow.py` 文件如下：

```python
# -*- coding: UTF-8 -*-
import tensorflow as tf
# 定义一个hello 的常量
hello = tf.constant("Hello Tensorflow")

# 创建一个会话
session = tf.Session()

# 执行常量操作并打印到标准输出
print(session.run(hello))
```

运行 `hello_tensorflow.py` 文件，你就可以看到命令行中打印的标准输出了。


## jupyter notebook 中使用 tensorflow

但是，通过编写一个完整的 Python 文件并执行在调试或者学习过程中，往往是非常低效的。

而 Python 虽然也提供了交互式命令行工具，但是对于画图等场景并不友好，因此，我们接下来，需要使用一个 Python 开发利器: `Jupyter Notebook`。

Jupyter Notebook 是一个 Python的交互式开发环境，也属于 Python 的第三方扩展工具，同样可以使用 `pip` 包管理工具进行安装。

同样是需要先进入之前创建的虚拟环境，然后执行如下命令可以安装 Jupyter Notebook :

```shell
pip3 install jupyter
```

安装完成后，只需要执行

```shell
jupyter-notebook
```

即可启动对应的 Jupyter Notebook 服务。

此时，`jupyter-notebook` 会自动打开浏览器，并访问对应 jupyter-notebook 页面，你可以在该页面中创建 notebook 文件并执行。


## 在 Docker 容器中使用 tensorflow

最后，我们来了解一下在云原生时代，我们是如何使用 tensorflow 的。

云原生时代最大的成果之一就是 Docker 了。

通过 Docker 镜像，我们可以将运行某个程序的所有依赖环境全部都打包的镜像中去，真正运行容器时，只需要拉取镜像并启动镜像即可。
不再需要因为环境搭建、依赖复杂等问题影响我们的工作效率了。

当然，想要使用 Docker 容器首先需要安装 Docker 软件，这一步骤
[官网](https://www.docker.com/get-started)
已经有了详细的说明，我们就不再赘述了。

安装完成后，我们可以直接拉取对应的 Docker 镜像：

```shell
docker pull tensorflow/tensorflow:nightly-jupyter
```

其中:

 - tensorflow/tensorflow 是对应的镜像名称。
 - nightly-jupyter 是我们要拉取的镜像tag，其中: nightly-jupyter 表示轻量级 tensorflow 且安装有 jupyter notebook


镜像拉取可能需要一段时间，当镜像拉取完成后，我们可以启动该 Docker 镜像:

```shell
docker run -it -p 8888:8888 -v ${local_path}:/tf/notebooks tensorflow/tensorflow:nightly-jupyter
```

其中:

 - -it 表示以交互式命令行的方式前台启动该镜像。
 - -p 表示需要镜像端口映射，即将容器内的8888端口映射到本地的8888端口，从而可以在本地浏览器进行访问。
 - -v 表示进行目录映射，即将本地的指定目录（需手动修改）挂载到容器内部的 `/tf/notebooks` 目录下，这样，我们就可以在容器内部看到并修改本地的文件了。


启动该容器后，我们就可以打开浏览器并访问 `http://127.0.0.1:8888/tree` 进行相关的操作了。
