# Python正则表达式详解

## 什么是正则表达式

正则表达式就是描述字符串排列的一套规则。

主要目的是用于字符串匹配。

Python中，使用`re`模块来使用正则表达式。

本文主要从以下几个方面进行介绍：原子、元字符、模式修正符、贪婪模式和懒惰模式、Python中re模块的使用来介绍。

## 原子

原子是正则表达式中最基本的组成单位，每个正则表达式中最少要包含一个原子。

常见的原子包含以下几类：

1.普通字符
2.非打印字符
3.通用字符
4.原子表

### 普通字符

```python
import re
pattern = "shi"
string = "http://www.missshi.cn"
result = re.search(pattern, string)
print(result.span())
# (15, 18)
```

其中，"shi"就是一组普通字符，普通字符就是指的是没有特殊含义的字符串。

### 非打印字符

```python
import re
pattern = "\n"
string = """http://www.missshi.cn
nianshi
"""
result = re.search(pattern, string)
print(result.span())
# (21, 22)
```

其中，"\n"就是一个非打印字符，或者也叫做转义字符或不可见字符。

常用的非打印字符见下表：

| 符号 | 含义 |
| --- | --- |
|\n|换行符 |
|\t|Tab制表符 |


### 通用字符

```python
import re
pattern = "\w\wshi\D"
string = "www.missshi.cn"
result = re.search(pattern, string)
print(result.span())
#(6, 12)
```

其中，`\w`、`\D`等字符就是通用字符，通用字符只是可以通过一个字符来匹配一类普通字符的字符。

常用的通用字符如下表：

| 符号 | 含义 |
| --- | --- |
|.|匹配除换行符外的全部符号 |
|\w|匹配任意一个字母、数字或下划线 |
|\W|匹配任意一个除字母、数字或下划线以外的字符 |
|\d|匹配任意一个十进制数 |
|\D|匹配任意一个除十进制数以外的字符 |
|\s|匹配任意一个空白字符 |
|\S|匹配任意一个除空白字符以外的字符 |


### 原子表

```python
import re
pattern = "[abcs]shi"
string = "www.missshi.cn"
result = re.search(pattern, string)
print(result.span())
# (7, 11)
```

其中，"[abcs]"表示的就是一个原子表。
原子表可以定义一组地位平等的原子，在匹配时，取任意一个原子进行匹配。

具体来说，原子表由`[]`表示，`[]`内的原子地位相同。
此外，`[^]`时，表示的是除了括号内里面的原子外其余均可以匹配。

## 元字符

元字符是指在正则表达式中具有一些特殊含义的字符。

常见元字符见如下列表：

| 符号 | 含义 |
| --- | --- |
|^|匹配字符串开始位置 |
|$|匹配字符串结束为止 |
|*|匹配0次、1次或多次前面的原子 |
|?|匹配0次或1次前面的原子 |
|+|匹配1次或多次前面的原子 |
|{n}|匹配前面的原子出现n次|
|{n,}|匹配前面的原子出现n次或以上|
|{n,m}|匹配前面的原子出现n次到m次|
|&#124;|模式选择符（从多个模式中选择一个）|
|()|模式单元符（将多个原子合并为一个原子块）|

## 模式修正

模式修正符是指在不改变正则表达式的情况下，通过模式修正符改变正则表达式的含义，从而实现一些匹配结果的调整等功能。

```python
import re
pattern = "Sshi"
string = "www.missshi.cn"
result = re.search(pattern, string)
print(result)
# None
 
import re
pattern = "Sshi"
string = "www.missshi.cn"
result = re.search(pattern, string, re.I)
print(result.span())
# (7, 11)
```

可以看到，其中第一部分并没有匹配到内容，但是在第二部分中确匹配到了对应的字符串。

这就是`re.I`模式修正的功能，其中`re.I`表示了忽略大小写的匹配。

一些常见的模式修正符的含义如下：

| 符号 | 含义 |
| --- | --- |
|I|匹配字符串开始位置 |
|M|匹配字符串结束为止 |
|L|匹配0次、1次或多次前面的原子 |
|U|匹配0次或1次前面的原子 |
|S|匹配1次或多次前面的原子 |

## 贪婪模式与懒惰模式

贪婪模式是指匹配尽可能长的长度。设置方法：p.*y。

懒惰模式是指采用就近匹配原则，找到即终止。设置方法：p.*?y。

```python
import re
pattern = "w.*s"
string = "www.missshiw.cn"
result = re.search(pattern, string)
print(result.span())
# (0, 9)
 
import re
pattern = "w.*?s"
string = "www.missshiw.cn"
result = re.search(pattern, string)
print(result.span())
# (0, 7)
```

## re模块详解

Python中常用的正则表达式函数有：re.match()，re.search()，findall()，re.sub()等。

### re.match()

re.match是从源字符串的第一个字符开始匹配，相当于在正则表达式的开头自动添加^。

示例：

```python
import re
pattern = "shi"
string = "www.missshi.cn"
result = re.match(pattern, string)
print(result)
# None
 
import re
pattern = "w.*shi"
string = "www.missshi.cn"
result = re.match(pattern, string)
print(result.span())
# (0, 11)
```

### re.search()

re.search是全局正则匹配，在之前的示例中都已经演示了。

### findall方式

之前的匹配方法都仅仅查找到第一个匹配对象，而如果有多个匹配对象，无法全部找出。

全部匹配的方式如下:

1. 使用re.compile()对正则表达式进行预编译。
2. 用编译生成的对象的findall()方法找出所有符合模式的结果。

示例代码如下：

```python
import re
pattern = "shi"
patt = re.compile(pattern)
result = patt.findall("nianshinianshinianshi")
print(result)
# ['shi', 'shi', 'shi']
```

## re.sub()

如果希望对正则表达式匹配到的部分进行替换，则需要利用到re.sub()函数。

函数原型：re.sub(pattern, rep, string,  max)

参数说明：

1. pattern: 要匹配的模式
2. rep: 要替换成的字符串
3. string: 被替换的原始字符串
4. max: 最大替换次数，默认全部替换

示例如下：

```python
import re
pattern = "shi"
result = re.sub(pattern, "nan", "nianshinianshinianshi", 2)
print(result)
# niannanniannannianshi
```
