# Python程序中判断当前Python版本

## 前言

随时 Python2 的不再维护，越来越多的项目逐渐在向 Python3 迁移。

然而，很多时间我们项目已经存在了各种依赖，因此 Python2 -> Python3 的迁移过程往往要经历一段时间，
而这一段时间内，我们需要保证我们的程序对 Python2 和 Python3 均能够兼容。

那么，针对部分 Python2 和 Python3 不兼容的 API 而言，我们如何做到程序兼容呢？

一个简单的方法是在程序中获取当前 Python 的版本，并针对不同的版本编写不同的代码。


## 查询 Python 的版本

Python 程序中，查询 Python 的版本非常简单，查询示例如下：

```python
import sys
python_version = sys.version_info
print(python_version.major) # 2
print(python_version.minor) # 7
print(python_version.micro) # 18
```


## 程序适配

当我们能够查询到当前的 Python 版本后，则可以根据不同的 Python 版本进行适配，以命令执行为例:

```python
import sys
python_version = sys.version_info
if python_version.major == 2:
    import commands
    status, output = commands.getstatusoutput("pwd")
else:
    import subprocess
    status, output = subprocess.getstatusoutput("pwd")
```

在上面的例子中，我们针对 Python2 和 Python3 支持的不同命令执行 API 进行了相关的适配。
