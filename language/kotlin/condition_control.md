# Kotlin条件控制

## if 表达式

一个 if 语句包含一个布尔表达式和一条或多条语句。

```kotlin
// 传统用法
var max = a 
if (a < b) {
    max = b
}

// 缩略写法

var max = a
if (a < b) max = b

// 使用 else 
var max: Int
if (a > b) {
    max = a
} else {
    max = b
}
```

我们也可以把 if 表达式的结果赋值给一个变量。

```kotlin
val max = if (a > b) {
    print("Choose a")
    a
} else {
    print("Choose b")
    b
}
```

即在 if 语句块中最后一行的表达式可以作为结果对变量赋值。

最终，我们可以用如下的表示方式来代替三元操作符:

```kotlin
val max = if (a > b) a else b
```

### 遍历区间

使用 in 运算符来检测某个数字是否在指定区间内，区间格式为 x..y ，对于 .. 操作符表示的区间，需要注意的是它的左右区间都是闭区间。

```kotlin
fun main(args: Array<String>) {
    val x = 5
    val y = 9
    if (x in 1..8) {
        println("x 在区间内")
    }
}
```

## when表达式

when 将它的参数和所有的分支条件顺序比较，直到某个分支满足条件，对标于其他语言的 switch 语句。

when 既可以被当做表达式使用也可以被当做语句使用。如果它被当做表达式，符合条件的分支的值就是整个表达式的值，如果当做语句使用， 则忽略个别分支的值。

一个最简单的 when 的使用示例如下：

```kotlin
when (x) {
    1 -> print("x == 1")
    2 -> print("x == 2")
    else -> { // 注意这个块
        print("x 不是 1 ，也不是 2")
    }
}
```

在 when 中，else 同 switch 的 default。
如果其他分支都不满足条件将会求值 else 分支。

如果很多分支需要用相同的方式处理，则可以把多个分支条件放在一起，用逗号分隔：

```kotlin
when (x) {
    0, 1 -> print("x == 0 or x == 1")
    else -> print("otherwise")
}
```

我们也可以检测一个值在（in）或者不在（!in）一个区间或者集合中：

```kotlin
when (x) {
    in 1..10 -> print("x is in the range")
    in validNumbers -> print("x is valid")
    !in 10..20 -> print("x is outside the range")
    else -> print("none of the above")
}
```

另一种可能性是检测一个值是（is）或者不是（!is）一个特定类型的值。
注意： 由于智能转换，你可以访问该类型的方法和属性而无需 任何额外的检测。

```kotlin
fun hasPrefix(x: Any) = when(x) {
    is String -> x.startsWith("prefix")
    else -> false
}
```

when 也可以用来取代 if-else if链。

如果不提供参数，所有的分支条件都是简单的布尔表达式，而当一个分支的条件为真时则执行该分支：

```kotlin
when {
    x.isOdd() -> print("x is odd")
    x.isEven() -> print("x is even")
    else -> print("x is funny")
}
```
