# Python目录相关操作总结

## 前言

在 Python 程序中，我们常常会涉及到一些目录相关的操作，例如，在当前目录下创建一个文件等。

那么，怎么找出当前文件所在目录、当前程序运行目录等等呢？下面，我们来依次看一下。

## 当前文件所在目录

在 python 文件中，查询当前文件所在目录时，需要涉及到以下相关知识。

1. `__file__` 内置变量
2. `os.path.abspath()` 函数
3. `os.path.dirname()` 函数


`__file__` 内置变量可以用于查询当前文件的地址。
若显示执行Python，会得到绝对路径;
若按相对路径来直接执行脚本./pyws/path_demo.py，会得到相对路径。

`os.path.abspath()` 函数接收一个文件地址作为输入参数，返回文件的绝对路径。

`os.path.dirname()` 函数接收一个文件地址作为输入参数，返回文件所属的目录。

完整示例如下:

```python
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
```

## 当前程序运行目录

在 python 文件中，查询当前程序的运行目录相对简单，可以直接调用如下函数即可。

```python
import os
workdir = os.getcwd()
print(workdir)
```

Ps: 该函数会返回当前程序的工作目录。
