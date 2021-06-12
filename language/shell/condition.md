# Shell 条件语句

在本文中，我们将会介绍在 shell 中，如何实现条件控制。

## if else 语法

if 语句的语法格式如下:

```shell
if condition
then
    command1 
    command2
    ...
    commandN 
fi
```

写成一行其实也是可以的:

```shell
if [ `ps -ef | grep -c "ssh"` -gt 1 ]; then echo "true"; fi
```

Ps: 末尾的 fi 就是 if 倒过来拼写，后面还会遇到类似的写法。

if else 的语法格式如下:

```shell
if condition
then
    command1 
    command2
    ...
    commandN
else
    command
fi
```

if else-if else 语法格式如下:

```shell
if condition1
then
    command1
elif condition2 
then 
    command2
else
    commandN
fi
```

完整示例代码如下:

```shell
a=10
b=20
if [ $a == $b ]
then
   echo "a 等于 b"
elif [ $a -gt $b ]
then
   echo "a 大于 b"
elif [ $a -lt $b ]
then
   echo "a 小于 b"
else
   echo "没有符合的条件"
fi
```

输出结果如下:

```shell
a 小于 b
```

if else 语句经常与 test 命令结合使用，如下所示：

```shell
num1=$[2*3]
num2=$[1+5]
if test $[num1] -eq $[num2]
then
    echo '两个数字相等!'
else
    echo '两个数字不相等!'
fi
```

关于 `test` 命令的更多介绍，可以参考 [文档](https://www.runoob.com/linux/linux-shell-test.html) 。

Ps: test 其实可以简单为 [] 方括号~
