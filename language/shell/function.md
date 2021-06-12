# Shell 函数详解

在本节中，我们将会详细讲解 Shell 中函数的使用。

## 函数基本格式

linux shell 可以用户定义函数，然后在shell脚本中可以随便调用。

shell中函数的定义格式如下：

```shell
[ function ] function_name() {
    action;
    [return int;]
}
```

说明：

 - 在函数定义前，可以加 function 关键词，也可以省略。
 - 函数参数返回，可以加 return 进行显示指定返回值，如果不显示使用 return 语句，则将会以最后一条命令的返回码作为返回值返回。


示例程序如下：

```shell
demoFun(){
    echo "这是我的第一个 shell 函数!"
}
echo "-----函数开始执行-----"
demoFun
echo "-----函数执行完毕-----"
```

Ps: 需要注意的是函数调用的过程中，不能在函数名后追加 () 。

注意：所有函数在使用前必须定义。这意味着必须将函数放在脚本开始部分，直至shell解释器首次发现它时，才可以使用。调用函数仅使用其函数名即可。


## 带有 return 的函数

下面，我们来针对一个带有返回值的函数进行演示。

```shell
funWithReturn(){
    echo "这个函数会对输入的两个数字进行相加运算..."
    echo "输入第一个数字: "
    read aNum
    echo "输入第二个数字: "
    read anotherNum
    echo "两个数字分别为 $aNum 和 $anotherNum !"
    return $(($aNum+$anotherNum))
}
funWithReturn
echo "输入的两个数字之和为 $? !"
```

其中，通过 `$?` 可以读取上一条函数执行得到的返回值。

## 函数传参

下面，我们来看一下如果和参数调用的过程中进行参数传递。

在Shell中，调用函数时可以向其传递参数。

与其他语言的函数调用不一样，对于 shell 而言，在函数体内部，通过 `$n` 的形式来获取参数的值，例如，`$1` 表示第一个参数，`$2` 表示第二个参数。

一个示例如下：

```shell
funWithParam(){
    echo "第一个参数为 $1 !"
    echo "第二个参数为 $2 !"
    echo "第十个参数为 $10 !"
    echo "第十个参数为 ${10} !"
    echo "第十一个参数为 ${11} !"
    echo "参数总数有 $# 个!"
    echo "作为一个字符串输出所有参数 $* !"
}
funWithParam 1 2 3 4 5 6 7 8 9 34 73
```

其中，主要注意的是：

 - `$10` 不能获取第十个参数，获取第十个参数需要 `${10}`，即当 `n>=10` 时，需要使用 `${n}` 来获取参数。
 - `$#` 可以获取传递到脚本或函数的参数个数。
 - `$*` 或 `$#` 以一个字符串显示所有向脚本传递的参数。


## 函数的输入参数处理

针对多个参数传入而言，shell 中有多种推荐的处理方式。

方式一: for 循环处理

```shell
for para in $*
do 
  echo "receive param： ${para}"
done
```

方式二: while 循环处理

```shell
while [ $# -gt 0 ]; do
    echo "receive param： ${1}"
    shift
done
```

其中，`shift` 表示去除传入的第一个参数。
