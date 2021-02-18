# Kotlin循环语句

## for 循环

for 循环可以对任何提供迭代器（iterator）的对象进行遍历，语法如下:

```kotlin
for (item in collection) {
    print(item)
}
```

如上所述，for 可以循环遍历任何提供了迭代器的对象。

如果你想要通过索引遍历一个数组或者一个 list，你可以这么做：

```kotlin
for (i in array.indices) {
    print(array[i])
}
```

注意这种"在区间上遍历"会编译成优化的实现而不会创建额外对象。

或者你可以用库函数 withIndex：

```kotlin
for ((index, value) in array.withIndex()) {
    println("the element at $index is $value")
}
```

Ps: Kotlin中的for循环与Python中的for循环非常的类似。


## while 与 do ... while 循环

while是最基本的循环，它的结构为：

```kotlin
while( 布尔表达式 ) {
  //循环内容
}
```

do ... while 循环 对于 while 语句而言，如果不满足条件，则不能进入循环。
但有时候我们需要即使不满足条件，也至少执行一次。
也就是说， do ... while 循环和 while 循环相似，不同的是，do .. while 循环至少会执行一次。

```kotlin
do {
       //代码语句
} while(布尔表达式);
```

## 返回和跳转
































