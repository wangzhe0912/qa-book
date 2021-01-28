# Python时间日期详解

在Python开发中，我们常常会用到各种时间日期相关的工具。我们将在本节中对时间、日期相关的常用操作进行一系列的总结。

其中，本文主要涉及的Python库包括：`time`、`datetime`等。

## 获取当前的时间戳

```python
import time
print(time.time())
```

## 获取当前时间的字符串格式

```python
import time
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
```

## 获取当前日期的字符串格式

```python
import time
print(time.strftime("%Y-%m-%d", time.localtime()))
```
