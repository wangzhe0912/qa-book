# 使用ijson解析超大JSON文件

在使用Python解析一个超大的JSON文件时，如果JSON文件过大，直接将其内容全部加载至内存中进行JSON解析往往会因为内存不足而失败。

而ijson是具有标准Python迭代器接口的迭代JSON解析器，非常适用于解析超大的JSON文件。

## 安装

ijson作为一个Python的第三方库可以用Python标准的包管理工具进行安装：

```bash
pip3 install ijson
```

## QuickStart

我们将以如下json字符串为例来演示ijson相关的功能使用。

```
{
  "earth": {
    "europe": [
      {"name": "Paris", "type": "city", "info": { ... }},
      {"name": "Thames", "type": "river", "info": { ... }},
      // ...
    ],
    "america": [
      {"name": "Texas", "type": "state", "info": { ... }},
      // ...
    ]
  }
}
```

ijson最常用的方法是将数据流转为一个可迭代对象：

```python
import ijson

f = urlopen('http://.../')
objects = ijson.items(f, 'earth.europe.item')
cities = (o for o in objects if o['type'] == 'city')
for city in cities:
    do_something_with(city)
```

上述的例子是直接从一个url中读取数据进行解析的方式，如果想要从文件中解析JSON数字，使用方式如下：

```python
import ijson


with open(mark_file, "r") as f:
    objects = ijson.items(f, 'earth.europe.item')


cities = (o for o in objects if o['type'] == 'city')
for city in cities:
    do_something_with(city)
```
