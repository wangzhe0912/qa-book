# Linux文本搜索

在 Linux 系统中，我们最常用的文本操作之一就是去进行指定文本操作了。

例如，我们经常需要从日志中查询某些关键词等等。

Linux 文本搜索支持完整匹配和正则匹配多种方式。

完整匹配相对比较简单，此处不做过多的赘述，我们主要来讨论一下 Linux 下的正则匹配。

## 元字符

在正则匹配中，首先需要了解的就是 **元字符** 。

元字符指的是具备一定特殊含义的特殊字符，例如包括：

 - . 匹配除换行符外的任意单个字符。
 - \* 匹配任意一个跟在它前面的字符，常用 .* 组合匹配任意字符串。
 - [] 匹配方括号中字符类中的任意一个。
 - ^ 匹配开头。
 - $ 匹配结尾。
 - \ 用于转义后面的特殊字符。
 - \+ 匹配前面的正则表达式且至少出现一次。
 - ? 匹配前面的正则表达式出现零次或一次。
 - | 匹配它前面或后面的正则表达式。


接下来，我们可以用 `grep` 命令与元字符组合来实现相关的文本搜索。

```shell
# 完整匹配
grep password /root/anaconda-ks.cfg

# . 匹配
grep pass.... /root/anaconda-ks.cfg

# 元字符组合使用
grep pass....$ /root/anaconda-ks.cfg
grep pass.* /root/anaconda-ks.cfg
grep pa[a-Z]* /root/anaconda-ks.cfg

# 转义字符的使用
grep "\*" /root/anaconda-ks.cfg
```

## find 文件查找命令

find 命令是一个用于文件查找的常用命令。

其基本的语法格式如下:

```shell
find 路径 查找条件 [补充条件]
```

示例：

```shell
# 在/etc目录下找出文件名为passwd的文件
find /etc -name passwd

# 使用通配符查询
find /etc -name pass*

# 使用正则表达式查询
find /etc -regex pass.*

# 使用正则表达式查询指定的文件夹/文件
find /etc -type d -regex pass.*
find /etc -type f -regex pass.*

# 8小时以内更新的文件
find /etc -type f -mtime 8 -regex pass.* 

# 查询 root 用户的文件
find /etc -type f -user root -regex pass.*

# 找到需要的文件并删除
find /etc -type f -user root -regex pass.* -exec rm -v {} \;
# 找到需要的文件并删除(需要交互式确认)
find /etc -type f -user root -regex pass.* -ok rm -v {} \;
```

## grep 命令的高级使用

使用 grep 加管道命令，我们可以将找到的内容进行切分并提取出我们想要的内容。

例如:

```shell
grep pass /root/anaconda-ks.cfg | cut -d " " -f 1
```

上述命令表示将找到的行用空格进行切分，并取出其中第一段。

此外，我们还可以使用 `uniq -c` 对提取到的信息进行统计，例如:

```shell
cut -d ":" -f 7 /etc/passwd | sort | uniq -c
```

Ps: 可以看到，我们中间加入了 sort 命令，原因是在用 `uniq` 进行统计时，只会对连续的内容进行重复统计，因此如果不提前排序，则会导致统计错误。
