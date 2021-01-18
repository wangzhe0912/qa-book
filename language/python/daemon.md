# Python多线程中daemon属性的作用

## 基本概念

在详细讲解Python多线程中deamon属性之前，我们首先需要了解一些基本概念。

### 什么是线程、什么是进程？

进程（Process）是计算机中的程序关于某数据集合上的一次运行活动，是系统进行资源分配和调度的基本单位，是操作系统结构的基础。

线程（Thread）是操作系统能够进行运算调度的最小单位。它被包含在进程之中，是进程中的实际运作单位。一条线程指的是进程中一个单一顺序的控制流，一个进程中可以并发多个线程，每条线程并行执行不同的任务。

每个进程至少包含一个线程，并最为程序的入口，这个线程我们称之为该进程的主线程，其他线程称之为工作线程。

### 什么是子线程？

了解了"进程"和"线程"的基本概念后，下面我们需要了解另一个概念"子线程"。

如果线程A启动了另一个线程，即线程B。那么，线程A就是线程B的父线程，而线程B就是线程A的子线程。

## daemon的作用

daemon又称为"守护程序"，对于daemon线程而言，也就是我们说的守护线程。

那么守护线程有什么作用呢？它又是在守护什么呢？

简单来说，我们有时希望一个线程能够伴随主线程常驻执行，比如周期性进行一些相关任务检查等。这时，我们可能就会需要一个`while True`循环来实现这一功能。
但是这个线程最终还是给退出呢~
退出的时机应该就是主线程退出的时间。
这时，我们就需要用到守护线程了。

总结来说，daemon线程适用于一些随父线程常驻的线程，本身线程无需自动退出。 只有当父线程退出后，会跟随父线程一起退出的场景。

## 示例说明

下面，我们来通过一些python示例代码来演示相关daemon属性相关的作用。

首先，我们来看一下Thread类的初始化函数：

```python
class Thread:
    """A class that represents a thread of control.
    """
    _initialized = False
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        # ...
        if daemon is not None:
            self._daemonic = daemon
        else:
            self._daemonic = current_thread().daemon
        # ...
```

上面的代码中，仅仅保留了`__init__`函数中与daemon参数相关的部分。

可以看到，当daemon值为None的时候，实际上相关的与继承了父线程的daemon属性。

除了None之类，dameon参数接收的取值为**True和False**。

下面，我们来分别看下daemon取值为true或false时，本身线程的行为是什么样的。

### daemon为False时

当daemon为False时，父线程在运行完毕后，会等待所有子线程退出才结束程序。

```python
import threading
import time
 
 
def foo():
    for i in range(3):
        print('i={},foo thread daemon is {}'.format(i,threading.current_thread().isDaemon()))
        time.sleep(1)


t = threading.Thread(target=foo,daemon=False)
t.start()
 
print("Main thread daemon is {}".format(threading.current_thread().isDaemon()))
print("Main Thread Exit.")

"""
运行结果：
i=0,foo thread daemon is False
Main thread daemon is False
Main Thread Exit.
i=1,foo thread daemon is False
i=2,foo thread daemon is False
"""
```

根据运行结果的顺序可以得知，主程序在线程完线程对象后就立即启动了，然后子线程返回了结果中第一行内容，然后sleep 1秒模拟 IO，这时CPU发现子线程阻塞了，就立即切到主线程继续执行。
主线程先后打印第二行和第三行，此时主线程的代码已经执行到结尾。
然后，因为主线程为子线程设置了daemon=False属性，这时就又发生了线程切换到子线程，子线程先后执行完第四行和第五行，然后子线程就完全执行完毕。
主线程看到子线程退出以后，也立即退出，整个程序结束。

换句话说，如果此时的子线程是一个无限循环的话，该程序将会永远无法退出。

### daemon为True时

```python
import threading
import time
 

def foo():
    for i in range(3):
        print('i={},foo thread daemon is {}'.format(i,threading.current_thread().isDaemon()))
        time.sleep(1)


t = threading.Thread(target=foo,daemon=True)
t.start()


print("Main thread daemon is {}".format(threading.current_thread().isDaemon()))
print("Main Thread Exit.")

"""
运行结果 ：
i=0,foo thread daemon is True
Main thread daemon is False
Main Thread Exit.
"""
```

从运行结果来看，当子线程设置daemon属性为True时，即主线程不关心子线程运行状态，主线程退出，子线程也必须跟着退出。

所以运行结果中子线程只执行了一句语句，就轮到主线程，主线程执行完最后两句，就立即退出，整个程序结束。

### 嵌套子线程的daemon为False时的情况

下面，我们来看一种相对复杂的情况，主线程首先Fork出daemon为True的线程，然后该线程继续Fork出多个daemon为False的线程。

```python
import threading
import time
 
 
def bar():
    while True: # 无限循环的子子线程
        print('【bar】 daemon is {}'.format(threading.current_thread().isDaemon()))
        time.sleep(1)
 
def foo():
    for i in range(3): #启动3个子线程
        print('i={},【foo】 thread daemon is {}'.format(i,threading.current_thread().isDaemon()))
        t1 = threading.Thread(target=bar,daemon=False)
        t1.start()
 
t = threading.Thread(target=foo,daemon=True)
t.start()
 
print("Main thread daemon is {}".format(threading.current_thread().isDaemon()))
time.sleep(2)
print("Main Thread Exit.")

"""
运行结果：
i=0,【foo】 thread daemon is True
Main thread daemon is False
【bar】 daemon is False
i=1,【foo】 thread daemon is True
【bar】 daemon is False
i=2,【foo】 thread daemon is True
【bar】 daemon is False
【bar】 daemon is False
【bar】 daemon is False
【bar】 daemon is False
Main Thread Exit.
【bar】 daemon is False
【bar】 daemon is False
【bar】 daemon is False
【bar】 daemon is False
【bar】 daemon is False
【bar】 daemon is False
【bar】 daemon is False
【bar】 daemon is False
【bar】 daemon is False
【bar】 daemon is False
【bar】 daemon is False
.......无限循环....
"""
```

主线程本来是不等子线程执行完毕的，但子线程要等待子子线程执行完毕，子子线程又是无限循环。
所以最终主线程也拦不住子子线程一直疯狂的输出，这就好比爷爷管得了儿子，但管不了孙子呀。

## 总结

通过上面的讲解，相信你已经了解了什么是daemon线程，以及如何选择是否创建daemon线程。

希望上面的内容对你有一些帮助。
