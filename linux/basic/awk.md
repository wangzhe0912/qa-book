# Linux文本处理之awk

## awk 和 sed 的区别

awk 更像是脚本语言。适用于比较规范的文本处理，常用于统计数量并输出指定字段。

与之对比，sed 则常用于将不规范的文本转换为比较规范的文件。

因此，在 Linux 中，我们常常将 awk 和 sed 搭建使用。

## awk 脚本的流程控制

awk 脚本的控制流程包含如下:

 - 输入数据前例程 BEGIN{}
 - 主输入循环{}
 - 所有文件读取完成例程 END{}


## awk 的字段引用和分离

在 awk 中每一行称之为 awk 的一条记录。

使用空格、制表符分隔的单词在 awk 中称之为一个字段。当然，也可以自己指定分隔字段的符号。

在 awk 中，我们可以使用 $1, $2 等表示第一个字段、第二个字段等。

Ps: $0 表示整行。

一个简单的 awk 命令如下：

```shell
awk '{ print $1,$2,$3 }' filename
```

上式表示打印每一行的第一、第二、第三的三个字段。

如果字段分隔符不是空格和换行符时，也可以使用 `-F` 来改变字段分隔符。例如：

```shell
awk -F ',' '{ print $1,$2,$3 }' filename
```

Ps: 在 awk 中，字符分隔符还可以是正则表达式。

此外，在 awk 中，我们还可以在 awk 命令中增加正则表达式过滤，只有正则匹配的行才进行处理。

格式如下：

```shell
awk '/正则表达式/{ print $1,$2,$3 }' filename
```

如果，我们在 awk 打印中，增加打印的序号时，可以增加内容如下:

```shell
awk '/正则表达式/{ print x++,$1,$2,$3 }' filename
```

其中，x++ 表示我们要显示的序号，每打印一行则序号自增1。

## awk 表达式

从本质上来看，awk 其实非常类似于一门编程语言，它有着自己的表达式，分支和循环语句，数组，甚至是函数。

下面，我们先来看一下 awk 的表达式是什么样的吧~

### 赋值操作符

= 是 awk 中最常用的赋值操作符。

例如：

```
var1 = "name"
var2 = "hello" "world"  # 会自动拼接
var3 = $1
```

其他的赋值操作符还有++，--，+=，-=，*=，/=，%=，^=等。

### 算术运算符

算术运算符比较简单，包括+,-,*,/,%,^等。

### 系统变量

awk 内部包含一些特殊的系统变量，包括：

 - FS 和 OFS 字段分隔符，其中，OFS 表示输出的字段分隔符。
 - RS 记录分隔符
 - NR 和 FNR 表示行数，其中NR不区分文件，数字持续累加，FNR序号针对每个文件进行重新排序。
 - NF 表示字段数量，最后一个字段的内容可以使用 $NF 来获取。

之前，我们用 -F 指定分隔符时，本质上就是在设置 FS 系统变量。

下面，我们来换一种编写方式:

```shell
head -5 /etc/passwd | awk 'BEGIN{FS=":"}{print NR,$1,$NF}'
```

### 关系操作符

关系操作符包括: <, >, <=, >=, ==, !=, ~, !~ 等。

### 布尔操作符

逻辑操作符包括: &&, ||, !

关系操作符和布尔操作符主要用于 awk 判断等场景中，我们后面会重点说明，此处不多做赘述。

## awk 条件和循环语句

### 条件语句

awk 的条件语句使用 if 开头，根据表达式的结果来判断执行哪条语句。

基本格式如下：

```shell
if (表达式)
  awk 语句1
[else if(表达式)
  awk 语句2
]
[else
  awk 语句2
]
```

Ps: 条件语句内部，如果有多个语句需要执行，可以使用 {} 来将多个语句包围起来。

示例代码如下:

```shell
awk '{if($2>=80) print $1}' kpi.txt
```

### 循环语句

在 awk 中，支持 while、 do-while 循环和 for 循环。

while 循环的基本格式如下：

```shell
while(表达式)
  awk语句
```

do-while 循环的基本格式如下：

```shell
do {
  awk语句
}while(表达式)
```

for 循环的基本格式如下：

```shell
for (初始值; 循环判断条件; 累加)
  awk语句
```

此外，在循环语句中，和其他编程语言一样，也支持 break 和 continue 语句。

一个简单的示例代码如下:

```shell
head -1 kpi.txt|awk '{sum=0;for(c=2;c<=NF;c++)sum+=$c;print sum}'
```

## awk 数组

awk 数据和其他编程语言中的数据类似，是一组有某种关联的数组，可以通过下标来访问。

赋值方法：`数组名称[下标] = 值`

需要注意的是：下标可以使用数字，也可以使用字符串。Ps: 本质上类似于 Python 的 dict 。

数组的遍历也非常简单，可以使用如下形式的 for 循环:

```shell
for (变量 in  数组名)
  print 数组名[变量]
```

删除数组：`delete 数组名`。

删除数组中指定元素: `delete 数组名[下标]`。

示例代码如下:

```shell
head -1 kpi.txt|awk '{sum=0;for(c=2;c<=NF;c++)sum+=$c;average[$1]=sum/(NF-1)}END{for(user in average) total+=average[user]; print(total/NR)}'
```

### 命令行参数数组

在使用 awk 时，有时我们会从命令行中传入一些参数，而在 awk 命令中可以对这些参数进行解析。

其中，涉及到了两个内部变量，分别是:

 - ARGC: 传入的参数的格式。
 - ARGV: 传入的参数数组。

一个常用的示例如下：

```shell
BEGIN{
  for(x=0;x<ARGC;x++) {
    print ARGV[x]
  }
  print ARGC
}
```


## awk 函数

### 算术函数

awk 支持的算术函数比较多，一些常用的算术函数包括:

 - sin() cos()
 - int()
 - rand()

示例代码如下：

```shell
BEGIN{
  pi=3.14
  print int(pi)
  srand()  # 重新获取随机种子
  print rand()
}
```

### 字符串函数

awk 中常用的字符串函数包括:

 - gsub(r, s, t): 字符串切分
 - index(s, t): 找出字符串子串
 - length(s): 计算字符串长度
 - match(s, r): 字符串匹配
 - split(s, a, sep): 字符串分隔
 - sub(r, s, t): 字符串切分
 - substr(s, p, n): 字符串切分


### 自定义函数

awk 中也支持自定义函数，自定义函数的格式如下:

```shell
function 函数名 (参数) {
  awk语句
  return awk变量
}
```

Ps: awk 自定义函数需要编写在 BEGIN，主循环和END 的外侧。

示例如下：

```shell
awk 'function a() {return 0} BEGIN{ print a() }'
```
