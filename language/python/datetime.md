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

## 将字符串转化为时间戳

```python
import time

time_str = "2019-5-10 23:40:00"
# 先转换为时间数组
timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
# 转换为时间戳
timeStamp = int(time.mktime(timeArray))
```

## 对时间日期做加减操作

```python
import datetime

current_datetime = datetime.datetime.now()
tomorrow_datetime = current_datetime + datetime.timedelta(days=1, hours=0, minutes=0, seconds=0)
```

## datetime 转化为字符串格式

```python
import datetime

current_datetime = datetime.datetime.now()
print(current_datetime.strftime("%Y-%m-%d %H:%S:%M"))
```
