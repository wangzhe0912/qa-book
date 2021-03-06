# 程序实体概述

在本节中，我们将会初步学习Go语言中的实体的通用逻辑，包括变量、常量、函数、结构体、接口等。

Go 语言是静态类型的编程语言，所以我们在声明变量或常量的时候，都需要指定它们的类型，或者给予足够的信息，这样才可以让 Go 语言能够推导出它们的类型。

PS：在 Go 语言中，变量的类型可以是其预定义的那些类型，也可以是程序自定义的函数、结构体或接口。常量的合法类型不多，只能是那些 Go 语言预定义的基本类型。它的声明方式也更简单一些。

## 变量的声明

一种常用方式如下：

```go
var name string
name = "hello world"
```

另外一种更加简单的方式如下：

```go
name := "hello world"
```

看起来在上面的方法好像并没有明确指名name的变量类型，但实际上，这里利用了Go语言自身的类型推断，可以从赋值的信息中自动推断出新的变量一定是string类型。

Ps：需要说明的是，第二种方式仅限于在函数内部使用。

这样使用的一个好处是可以大大增加程序的灵活性：

```go
package main

import (
  "flag"
  "fmt"
)

func main() {
  name := getTheFlag()
  flag.Parse()
  fmt.Printf("Hello, %v!\n", *name)
}

func getTheFlag() *string {
  return flag.String("name", "everyone", "The greeting object.")
}
```

以上述程序为例，name其实可以是任意类型变量，我们可以对getTheFlag函数进行任意修改，甚至修改其返回类型，外部程序都能很多的做到兼容。


## 变量的重声明

重声明就是指对已经声明过的变量再次声明。变量重声明的前提条件如下:

1. 由于变量的类型在其初始化时就已经确定了，所以对它再次声明时赋予的类型必须与其原本的类型相同，否则会产生编译错误。
2. 变量的重声明只可能发生在某一个代码块中。如果与当前的变量重名的是外层代码块中的变量，那么就是另外一种含义了，后续我们会提及。
3. 变量的重声明只有在使用短变量声明时才会发生，否则也无法通过编译。如果要在此处声明全新的变量，那么就应该使用包含关键字var的声明语句，但是这时就不能与同一个代码块中的任何变量有重名了。
4. 被“声明并赋值”的变量必须是多个，并且其中至少有一个是新的变量。这时我们才可以说对其中的旧变量进行了重声明。

示例如下：

```go
var err error
n, err := io.WriteString(os.Stdout, "Hello, everyone!\n")
```

## 程序实体的作用域

在 Go 语言中，代码块一般就是一个由花括号括起来的区域，里面可以包含表达式和语句。

Go 语言本身以及我们编写的代码共同形成了一个非常大的代码块，也叫全域代码块。

这主要体现在，只要是公开的全局变量，都可以被任何代码所使用。

相对小一些的代码块是代码包，一个代码包可以包含许多子代码包，所以这样的代码块也可以很大。

接下来，每个源码文件也都是一个代码块，每个函数也是一个代码块，每个if语句、for语句、switch语句和select语句都是一个代码块。

甚至，switch或select语句中的case子句也都是独立的代码块。

走个极端，我就在main函数中写一对紧挨着的花括号算不算一个代码块？当然也算，这甚至还有个名词，叫“空代码块”。

也就是说：一个代码块可以有若干个子代码块；但对于每个代码块，最多只会有一个直接包含它的代码块（后者可以简称为前者的外层代码块）。

这种代码块的划分，也间接地决定了程序实体的**作用域**。下面，我们来进行详细说明。

大家都知道，一个程序实体被创造出来，是为了让别的代码引用的。那么，哪里的代码可以引用它呢，这就涉及了它的作用域。

程序实体的访问权限有三种：**包级私有的**、**模块级私有的**和**公开的**。

包级私有和模块级私有访问权限对应的都是代码包代码块，公开的访问权限对应的是全域代码块。
然而，这个粒度是比较粗的，我们往往需要利用代码块再细化程序实体的作用域。

比如，我在一个函数中声明了一个变量，那么在通常情况下，这个变量是无法被这个函数以外的代码引用的。这里的函数就是一个代码块，而变量的作用域被限制在了该代码块中。

简单的说：一个程序实体的作用域总是会被限制在某个代码块中，而这个作用域最大的用处，就是对程序实体的访问权限的控制。

思考一个问题：如果一个变量与其外层代码块中的变量重名会出现什么状况？我们通过一段代码来验证一下：

```go
package main

import "fmt"

var block = "package"

func main() {
  block := "function"
  {
    block := "inner"
    fmt.Printf("The block is %s.\n", block)
  }
  fmt.Printf("The block is %s.\n", block)
}
```

这个命令源码文件中有四个代码块，它们是：全域代码块、main包代表的代码块、main函数代表的代码块，以及在main函数中的一个用花括号包起来的代码块。

我在后三个代码块中分别声明了一个名为block的变量，并分别把字符串值"package"、"function"和"inner"赋给了它们。
此外，我在后两个代码块的最后分别尝试用fmt.Printf函数打印出“The block is %s.”。

那么，上述代码可以通过编译吗？如果能，会打印的结果是什么呢？

实际上，上述代码是可以通过编译的，打印的结果如下：

```go
The block is inner.
The block is function.
```

如果不了解作用域的概念的话，你可能会觉得这段代码在三处都声明了相同名称的变量，可能会导致编译失败。

但是实际上，对于不同的代码块中的代码，变量重名是没什么影响的。
那么，在不同代码块中的包含相同的变量声明时，真正引用的变量是哪一个呢？

1. 首先，代码引用变量的时候总会最优先查找当前代码块中的那个变量。
2. 其次，如果当前代码块中没有声明以此为名的变量，那么程序会沿着代码块的嵌套关系，从直接包含当前代码块的那个代码块开始，一层一层地向上查找。
3. 一般情况下，程序会一直查到当前代码包代表的代码块。如果仍然找不到，那么 Go 语言的编译器就会报错了。


PS：如果我们在当前源码文件中导入了其他代码包，那么引用其中的程序实体时，是需要以限定符为前缀的。
所以程序在找代表变量未加限定符的名字（即标识符）的时候，是不会去被导入的代码包中查找。
但有个特殊情况，如果我们把代码包导入语句写成`import . "XXX"`的形式（注意中间的那个“.”），那么就会让这个“XXX”包中公开的程序实体，被当前源码文件中的代码，视为当前代码包中的程序实体。

现在，再看一下刚才的代码，是否已经非常清晰了呢？

## 变量类型检查

在Go语言中，除了Go语言自带的编译器变量类型检查外，往往还需要主动进行相关的变量类型检查。

以如下代码为例：

```go
package main

import "fmt"

var container = []string{"zero", "one", "two"}

func main() {
  container := map[int]string{0: "zero", 1: "one", 2: "two"}
  fmt.Printf("The element is %q.\n", container[1])
}
```

在上述代码段中，有两个都叫做container的变量，分别位于main包代码块和main函数代码块。

main包代码块中的变量是切片（slice）类型的，另一个是字典（map）类型的。在main函数的最后，我们试图打印出container变量的值中索引为1的那个元素。

很显然，无论是切片类型还是字典类型，都是支持索引进行数据查询的。

但是，如果我们想要确切的查询变量类型的时候，索引表达式就不再够用了，此时需要使用**类型断言**表达式。

```go
value, ok := interface{}(container).([]string)
```

上述是一条赋值语句。在赋值符号的右边，是一个类型断言表达式。

它包括了用来把container变量的值转换为空接口值的`interface{}(container)` 以及 一个用于判断前者的类型是否为切片类型 []string 的 `.([]string)`。

这个表达式的结果可以被赋给两个变量，在这里由value和ok代表。
变量ok是布尔（bool）类型的，它将代表类型判断的结果，true或false。 如果是true，那么被判断的值将会被自动转换为[]string类型的值，并赋给变量value，否则value将被赋予nil（即“空”）。

顺便提一下，这里的ok也可以没有。也就是说，类型断言表达式的结果，可以只被赋给一个变量，在这里是value。但是这样的话，当判断为否时就会引发异常。

这种异常在 Go 语言中被叫做panic，我把它翻译为运行时恐慌。
除非显式地“恢复”这种“恐慌”，否则它会使 Go 程序崩溃并停止。所以，在一般情况下，我们还是应该使用带ok变量的写法。

