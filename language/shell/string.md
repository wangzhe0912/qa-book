# Shell 文本处理

在之前的 [Shell 变量详解](./variable.md) 一文中，我们简单的讲解了 shell 中的一些字符串基本用法，
比如字符串的截断、计算字符串的长度等。

但实际上，shell 对于本文/字符串的操作的能力远比这个强大的多，下面，我们来以使用场景为例，来说明如果使用 shell 来完成相关功能。

## string.replace 功能

字符串处理中，一个最常用的方式就是将指定字符串中的某个字符串替换为其他字符串，下面，我们来看一下如何实现。

例如，对于一个字符串: `apple,pear,banana`，我们希望能够将',' 替换为 ' '。

### {str//,/ } 来处理

我们先来讲述一个最简单的方法，就是直接用 ' ' 来替换 ',' 字符串，并将用 ' ' 分割的字符串转化为数组。

基本语法如上表达式。

```shell
${string//字符串1/字符串2}
```

上述操作的函数表示将 string 中的所有 字符串1 替换为 字符串2 。

那么，我们来看一下如果想要将 , 转换成为 空格 需要怎么实现，没错，就是这样:

```shell
${string//,/ }
```

即此时字符串1对应','，而字符串2对应' '即可。

完整示例代码如下:

```shell
old_str="apple,pear,banana"
new_str=${old_str//,/ }
echo $new_str
```

### tr 命令

下面，我们来讲解第二种可以用于字符串替换的方法，`tr` 命令。

Linux tr 命令用于转换或删除文件中的字符。

具体来说: tr 指令从标准输入设备读取数据，经过字符串转译后，将结果输出到标准输出设备，常常可以用于管道命令中。

`tr` 命令的基本语法如下：

```shell
tr [第一字符集] [第二字符集]  
```

即可以将输入输出中包含的第一字符集中的字符全部转换为第二字符集中的对应的字符。

还是用一个完整的代码来看一下:

```shell
old_str="apple,pear,banana"
new_str=`echo $old_str | tr ',' ' '`
echo $new_str
```

不过从上面的功能描述中，我们就已经可以感受到tr命令的强大了，tr可以针对一组字符进行一一映射的替换到另外一组字符上。

### awk 命令

awk 是一个更加强大的文本处理语言，在文本分析的场景中非常重要。

此处，我们先不对 `awk` 命令进行展开介绍，使用示例如下:

```shell
old_str="apple,pear,banana"
new_str=`echo $old_str | awk 'BEGIN{FS=",";OFS" "} {print $1,$2,$3}'`
echo $new_str
```

## string.split 功能

在 shell 脚本中，我们经常会有一个需求，就是将一个字符串按照指定关键字符进行切分，从而得到一个数组。

例如，对于一个字符串: `apple,pear,banana`，我们希望能够按照 `,` 进行切分，从而得到一个 (apple pear banana) 的数组。

那么，我们首先需要了解在 shell 中怎么才能创建一个数组。

在 shell 中创建一个数组的方式非常简单，基本格式如下：

```shell
arr=(element1 element2 element3)
```

可以看到，在 shell 中创建一个数组的方式非常简单，只需要用 `()` 包围一个字符串，且字符串中各个元素用空白符进行间隔，那么就会自动创建出来一个数组。

而在上文的介绍中，我们已经介绍了多种方式可以用 ',' 替换为空白符，那么此时我们只需要用 `()` 将替换后的结果包围起来就可以完成 `split` 的功能了。

完整的代码如下所示（以`tr`命令为例）:

```shell
str="apple,pear,banana"
arr=(`echo $str | tr ',' ' '`)

echo "first element is ${arr[0]}"
echo "total number is ${#arr[*]}"

for element in ${arr[*]} ; do
    echo "element is ${element}"
done
```

Ps: 其他替换的方式原理是一致的。
