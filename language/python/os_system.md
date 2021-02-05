# Python判断当前操作系统

## 前言

我们都知道，Python是一门跨平台的语言，Python解释器本身几乎可以在所有的操作系统中运行。

然而，对于不同的操作系统而言，为了完成相同的任务可能需要执行命令可能并不一致，因此，我们往往需要在Python代码中判断出当前执行的平台，然后针对当前平台的不同编写适合于对应平台的逻辑。

在Python语言中，有多个内置库都能查询操作系统版本信息，下面我们来一一说明，你可以跟进需求选择合适的方式。

## sys模块

下面，我们先看用一个示例开始我们的说明：

```python
import sys
print(sys.platform)
```

在上面的代码中，我们引入了Python自带的库`sys`，并读取了sys.platform属性。

那么，sys.platform属性具体能由哪些值呢？常见的值如下: 

|System|sys.platform的值|
|---|-----|
|AIX|aix|
|Linux|linux|
|Windows|win32|
|Windows/Cygwin|cygwin|
|macOS|darwin|

Ps: 需要说明的是，sys.platform属性值是在Python安装时就已经生成的。

## os模块

除了`sys`模块外，`os`模块也提供了与系统有关的版本信息。

同样用一个示例开始说明：

```python
import os
print(os.uname())
```

其中，os模块的uname方法会返回一个对象来说明当前操作系统的信息。其中该对象中包含如下字段：

1. sysname: 操作系统名称，如Darwin，Linux等
2. nodename: 机器名称，同hostname
3. release: 操作系统版本号，如19.3.0
4. version: 操作系统版本信息，如Darwin Kernel Version 19.3.0: Thu Jan  9 20:58:23 PS
T 2020; root:xnu-6153.81.5~1/RELEASE_X86_64
5. machine: 硬件标识信息，如x86_64

Ps: uname方法返回的对象用索引查询对应信息，也可以用.操作符查询对应属性值，例如：

```python
import os
version_info = os.uname()
print(version_info.sysname)
print(version_info[1])
```


## platform模块

除了sys和os模块外，Python还提供了一个更加强大的库专门用于查询操作系统相关信息。

下面，我们来通过实例依次讲解相关的方法。

```python
import platform
print(platform.python_version())  # 查询Python版本，如3.8.5
print(platform.architecture())    # 查询可执行程序的结构，如('32bit', 'WindowsPE')
print(platform.node())            # 查询机器名称
print(platform.platform())        # 获取操作系统名称及版本号，macOS-10.15.3-x86_64-i386-64bit
print(platform.processor())       # 查询处理器信息，如i386
print(platform.system())          # 查询操作系统信息，如Darwin
print(platform.release())         # 查询操作系统版本号，如19.3.0
print(platform.version())         # 查询操作系统版本信息
```
