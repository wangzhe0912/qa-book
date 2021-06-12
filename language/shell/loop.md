# Shell 循环语句

在本文中，我们将会介绍在 shell 中，如何实现循环控制。

## for 循环

与其他编程语言类似，Shell支持for循环。

for循环一般格式为：

```shell
for var in item1 item2 ... itemN
do
    command1
    command2
    ...
    commandN
done
```

同时，上述代码也可以简化成一行:

```shell
for var in item1 item2 ... itemN; do command1; command2; done;
```

当变量值在列表里，for 循环即执行一次所有命令，使用变量名获取列表中的当前取值。

命令可为任何有效的 shell 命令和语句。

示例代码如下：

```shell
for str in This is a string
do
    echo $str
done
```

## while 循环

while 循环用于不断执行一系列命令，也用于从输入文件中读取数据。其语法格式为：

```shell
while condition
do
    command
done
```

以下是一个基本的 while 循环，测试条件是：如果 int 小于等于 5，那么条件返回真。int 从 1 开始，每次循环处理时，int 加 1。
运行上述脚本，返回数字 1 到 5，然后终止。

```shell
#!/bin/bash
int=1
while (( $int<=5 ))
do
    echo $int
    int=`expr $int + 1`
done
```

上述代码中，使用 ``(( ))`` 包围了一个数学表达式用于条件判断。

同时，在循环体中，使用了 `expr` 来实现了变量值加一。


### 无限循环

无限循环语法格式：

```shell
while :
do
    command
done
```

或

```shell
while true
do
    command
done
```

或

```shell
for (( ; ; ))
```

## until 循环

until 循环执行一系列命令直至条件为 true 时停止。

until 循环与 while 循环在处理方式上刚好相反。

一般 while 循环优于 until 循环，但在某些时候—也只是极少数情况下，until 循环更加有用。

until 语法格式:

```shell
until condition
do
    command
done
```

condition 一般为条件表达式，如果返回值为 false，则继续执行循环体内的语句，否则跳出循环。

以下实例我们使用 until 命令来输出 0 ~ 9 的数字：

```shell
a=0

until [ ! $a -lt 10 ]
do
   echo $a
   a=`expr $a + 1`
done
```


## case .. esac 语句

case ... esac 为多选择语句，与其他语言中的 switch ... case 语句类似，是一种多分枝选择结构。

每个 case 分支用右圆括号开始，用两个分号 ;; 表示 break，即执行结束，跳出整个 case ... esac 语句，esac（就是 case 反过来）作为结束标记。

可以用 case 语句匹配一个值与一个模式，如果匹配成功，执行相匹配的命令。

case ... esac 语法格式如下：

```shell
case 值 in
模式1)
    command1
    command2
    ...
    commandN
    ;;
模式2）
    command1
    command2
    ...
    commandN
    ;;
esac
```

case 工作方式如上所示，取值后面必须为单词 in，每一模式必须以右括号结束。

取值可以为变量或常数，匹配发现取值符合某一模式后，其间所有命令开始执行直至 ;;。

取值将检测匹配的每一个模式。
一旦模式匹配，则执行完匹配模式相应命令后不再继续其他模式。
如果无一匹配模式，使用星号 * 捕获该值，再执行后面的命令。

示例代码如下:

```shell
echo '输入 1 到 4 之间的数字:'
echo '你输入的数字为:'
read aNum
case $aNum in
    1)  echo '你选择了 1'
    ;;
    2)  echo '你选择了 2'
    ;;
    3)  echo '你选择了 3'
    ;;
    4)  echo '你选择了 4'
    ;;
    *)  echo '你没有输入 1 到 4 之间的数字'
    ;;
esac
```

## break 和 continue

在循环过程中，有时候需要在未达到循环结束条件时强制跳出循环，Shell使用两个命令来实现该功能：`break` 和 `continue`。

### break 命令

break命令允许跳出所有循环（终止执行后面的所有循环）。

下面的例子中，脚本进入死循环直至用户输入数字大于5。要跳出这个循环，返回到shell提示符下，需要使用break命令。

```shell
#!/bin/bash
while :
do
    echo -n "输入 1 到 5 之间的数字:"
    read aNum
    case $aNum in
        1|2|3|4|5) echo "你输入的数字为 $aNum!"
        ;;
        *) echo "你输入的数字不是 1 到 5 之间的! 游戏结束"
            break
        ;;
    esac
done
```

### continue 命令

continue命令与break命令类似，只有一点差别，它不会跳出所有循环，仅仅跳出当前循环。

对上面的例子进行修改：

```shell
#!/bin/bash
while :
do
    echo -n "输入 1 到 5 之间的数字: "
    read aNum
    case $aNum in
        1|2|3|4|5) echo "你输入的数字为 $aNum!"
        ;;
        *) echo "你输入的数字不是 1 到 5 之间的!"
            continue
            echo "游戏结束"
        ;;
    esac
done
```

Ps: 运行代码发现，当输入大于5的数字时，该例中的循环不会结束，语句 echo "游戏结束" 永远不会被执行。