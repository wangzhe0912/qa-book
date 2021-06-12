# shell 变量详解

## 定义变量

在 shell 中定义一个变量的示例如下：

```shell
your_name="wangzhe0912"
```

注意：

 - **变量名和等号之间不能有空格**。
 - 命名只能使用英文字母，数字和下划线，首个字符不能以数字开头。
 - 中间不能有空格，可以使用下划线（_）。
 - 不能使用bash里的关键字。


除了显示的给变量赋值，在 shell 中还可以通过语句给变量赋值，如：

```shell
for file in `ls /etc`
// 或
for file in $(ls /etc)
```

以上语句将 `/etc` 下目录的文件名循环出来。

## 使用变量

使用一个定义过的变量，只要在变量名前面加美元符号即可，如：

```shell
your_name="qinjx"
echo $your_name
echo ${your_name}
```

其中，变量名外面的花括号是可选的，加不加都行（推荐加上）。

加花括号是为了帮助解释器识别变量的边界，比如下面这种情况：

```shell
for skill in Ada Coffe Action Java; do
    echo "I am good at ${skill}Script"
done
```

对于已定义的变量，可以被重新定义，如: 

```shell
your_name="tom"
echo $your_name
your_name="alibaba"
echo $your_name
```

## 只读变量

有时，我们希望某个变量是只读的，即不能被修改。
此时，可以使用 readonly 命令可以将变量定义为只读变量，只读变量的值不能被改变。

示例如下：

```shell
myUrl="https://www.google.com"
readonly myUrl
myUrl="https://www.runoob.com"
```

运行脚本，结果如下：

```shell
/bin/sh: NAME: This variable is read only.
```

## 删除变量

使用 unset 命令可以删除变量。语法：

```shell
unset variable_name
```

Ps: 变量被删除后不能再次使用。unset 命令不能删除只读变量。

## 变量类型

在运行shell时，会同时存在三种变量：局部变量、全局变量、环境变量。

### 局部变量

Shell 也支持自定义函数，但是 Shell 函数和 C++、Java、C# 等其他编程语言函数的一个不同点就是：
在 Shell 函数中定义的**变量默认就是全局变量**，它和在函数外部定义变量拥有一样的效果。请看下面的代码：

```shell
#!/bin/bash
#定义函数
function func(){
    a=99
}
#调用函数
func
#输出函数内部的变量
echo $a
```

上述命令输出结果为 99 。

也就是说，虽然 a 是在 func 函数内部定义的，但是在函数外部也可以得到它的值，证明它的作用域是全局的，而不是仅仅局限于函数内部。

要想变量的作用域仅限于函数内部，可以在定义时加上local命令，此时该变量就成了局部变量。

```shell
#!/bin/bash
#定义函数
function func(){
    local a=99
}
#调用函数
func
#输出函数内部的变量
echo $a
```

此时，输出结果为空，表明变量 a 在函数外部无效，是一个局部变量。


### 全局变量

上面已经提到了，shell 中默认定义的变量就是一个全局变量，那么这个全局变量生效的范围是什么样的呢？

所谓全局变量，就是指变量在**当前的整个Shell进程中都有效**。每个Shell进程都有自己的作用域，彼此之间互不影响。

这里面有一个很重要的概念，当前的整个Shell进程。

那么，怎么来理解什么是一个shell进程呢？

一. 不同的 shell 终端窗口对应着不同的 shell 进程，这个比较好理解，我们此处不多解释。
二. 在一个 Shell 进程中可以使用 source 命令执行多个 Shell 脚本文件，此时全局变量在这些脚本文件中都有效。

例如，现在有两个 Shell 脚本文件，分别是 a.sh 和 b.sh。a.sh 的代码如下：

```shell
#!/bin/bash
echo $a
b=200
```

b.sh 的代码如下：

```shell
#!/bin/bash
echo $b
```

打开一个 Shell 窗口，输入以下命令：

```shell
a=99
source ./a.sh
# 99
source ./b.sh
# 200
```

这三条命令都是在一个进程中执行的，从输出结果可以发现，在 Shell 窗口中以命令行的形式定义的变量 a，在 a.sh 中有效；在 a.sh 中定义的变量 b，
在 b.sh 中也有效，变量 b 的作用范围已经超越了 a.sh。

三. 在一个 shell 进程中，sh 执行其他 shell 脚本时，会创建出不同的 shell 进行，导致全局变量无法在新的 shell 脚本中生效。

同样还是以上述 a.sh 和 b.sh 的代码为例，打开一个 shell 窗口，输入如下命令：

```shell
a=99
sh ./a.sh
# 
sh ./b.sh
# 
```

我们把 source 修改为 sh 后，可以看到行为已经发生了具体的变化，这正式因为 sh 命令执行时会新建一个 shell 进程，导致全局变量无法传递。

### 环境变量

那么，如果我们想要让一个变量可以在 fork 出的 shell 进程中同样生效时，应该怎么处理呢？这就要用到我们接下来介绍的环境变量了。

如果使用 `export` 命令将全局变量导出，那么它就在所有的子进程中也有效了，这称为“环境变量”。

环境变量被创建时所处的 Shell 进程称为父进程，如果在父进程中再创建一个新的进程来执行 Shell 命令，那么这个新的进程被称作 Shell 子进程。

当 Shell 子进程产生时，它会继承父进程的环境变量为自己所用，所以说环境变量可从父进程传给子进程。不难理解，环境变量还可以传递给孙进程。

注意，两个没有父子关系的 Shell 进程是不能传递环境变量的，并且环境变量只能向下传递而不能向上传递，即“传子不传父”。

修改 `a.sh` 文件如下：

```shell
#!/bin/bash
echo $a
export b=200
```

打开一个 shell 窗口，输入如下命令：

```shell
export a=99
sh ./a.sh
# 99
sh ./b.sh
# 200
```

此时，可以发现此时虽然是用 `sh` fork 出来了子进程，但是我们设置的相关变量依旧是有效的。

Ps: 通过 export 导出的环境变量只对当前 Shell 进程以及所有的子进程有效，如果最顶层的父进程被关闭了，
那么环境变量也就随之消失了，其它的进程也就无法使用了，所以说环境变量也是临时的。

## shell 字符串

字符串是 shell 编程中最常用最有用的数据类型（除了数字和字符串，也没啥其它类型好用了），字符串可以用单引号，也可以用双引号，也可以不用引号。

### 单引号

```shell
str='this is a string'
```

单引号字符串的限制：

 - 单引号里的任何字符都会原样输出，**单引号字符串中的变量是无效的**；
 - 单引号字串中不能出现单独一个的单引号（对单引号使用转义符后也不行），但可成对出现，作为字符串拼接使用。


### 双引号

```shell
your_name='runoob'
str="Hello, I know you are \"$your_name\"! \n"
echo -e $str
```

输出结果为：

```shell
Hello, I know you are "runoob"! 
```

双引号的优点：

 - 双引号里可以有变量。
 - 双引号里可以出现转义字符。


### 拼接字符串

```shell
your_name="runoob"
# 使用双引号拼接
greeting="hello, "$your_name" !"
greeting_1="hello, ${your_name} !"
echo $greeting  $greeting_1
# 使用单引号拼接
greeting_2='hello, '$your_name' !'
greeting_3='hello, ${your_name} !'
echo $greeting_2  $greeting_3
```

输出结果为：

```shell
hello, runoob ! hello, runoob !
hello, runoob ! hello, ${your_name} !
```

### 获取字符串的长度

```shell
string="abcd"
echo ${#string} #输出 4
```

即在变量名前增加 `#` 号，并使用 `${}` 包围时相关于计算该字符串的长度。

### 截断子字符串

以下示例从字符串第 2 个字符开始截取 4 个字符：

```shell
string="runoob is a great site"
echo ${string:1:4}    # 输出 unoo
```

Ps: 字符串的索引规则与 Python 的语言一致，索引都是从0开始。


### 查找子字符串

查找字符 i 或 o 的位置(哪个字母先出现就计算哪个)：

```shell
string="runoob is a great site"
echo `expr index "$string" io`  # 输出 4
```

Ps: 上述脚本中使用了 `\`` 进行了命令执行。

## shell 数组

bash支持一维数组（不支持多维数组），并且没有限定数组的大小。

类似于 C 语言，数组元素的下标由 0 开始编号。获取数组中的元素要利用下标，下标可以是整数或算术表达式，其值应大于或等于 0。

### 定义数组

在 Shell 中，用括号来表示数组，数组元素用"空格"符号分割开。定义数组的一般形式为：

```shell
数组名=(值1 值2 ... 值n)
```

例如:

```shell
array_name=(value0 value1 value2 value3)
```

或者:

```shell
array_name=(
value0
value1
value2
value3
)
```

还可以单独定义数组的各个分量:

```shell
array_name[0]=value0
array_name[1]=value1
array_name[n]=valuen
```

Ps: 可以不使用连续的下标，而且下标的范围没有限制。

### 读取数组

读取数组元素值的一般格式是：

```shell
${数组名[下标]}
```

例如:

```shell
valuen=${array_name[n]}
```

使用 `@` 符号可以获取数组中的所有元素，例如：

```shell
echo ${array_name[@]}
```

### 获取数组的长度

获取数组长度的方法与获取字符串长度的方法相同，例如：

```shell
# 取得数组元素的个数
length=${#array_name[@]}
# 或者
length=${#array_name[*]}
# 取得数组单个元素的长度
lengthn=${#array_name[n]}
```

### shell 注释

以 # 开头的行就是注释，会被解释器忽略。

通过每一行加一个 # 号设置多行注释，像这样：

```shell
#--------------------------------------------
# 这是一个注释
#--------------------------------------------
##### 用户配置区 开始 #####
#
#
# 这里可以添加脚本描述信息
# 
#
##### 用户配置区 结束  #####
```

上面针对的是单行注释，如果想要进行多行注释，方式如下：

```shell
:<<EOF
注释内容...
注释内容...
注释内容...
EOF
```

其中，EOF 也可以替换为其他符号，例如:

```shell
:<<''
注释内容...
注释内容...
注释内容...
''

:<<!
注释内容...
注释内容...
注释内容...
!
```

## 系统环境变量

在 Linux 中，有一些系统内置且具备一些特殊含义的环境变量，例如：

1. $USER: 当前用户
2. $UID: 当前用户ID
3. $PATH: 默认命令搜索路径，该目录下包含的二进制命令和脚本可以直接运行，无须输入完整路径。
4. $PS1: 当前终端提示样式


## 预定义变量

预定义变量是指 Linux Shell 中一些内置的有特殊含义的变量，例如:

1. $?: 返回上一条命令的返回码
2. $$: 返回当前进程PID
3. $0: 返回当前的进程名称
4. ${number}: 用于参数接收，表示接收第 number 个传入的参数。
5. ${number-default}: 用于参数接收，表示接收第 number 个传入的参数，如果没有传入参数，则将default值作为默认值。

