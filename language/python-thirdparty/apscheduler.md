# APScheduler实现Python定时任务管理

## 简介

Advanced Python Scheduler (APScheduler) 是一个 Python 库，可以管理 Python 的定时任务。
利用 APScheduler ，我们可以轻松的添加或移除相关的定时任务。

我们还可以把 Job 信息存储在数据库中，这样它就能维护其自身的信息和状态。
即使当服务发生了重启，它也能正常恢复相关需要执行的任务。

除此之外，APScheduler 可以用作跨平台、特定于应用程序的平台特定调度程序。

但是请注意，APScheduler 本身不是守护程序或服务，也不附带任何命令行工具。

APScheduler 默认支持三种内置的任务调度方式：

 - Cron 式调度（具有可选的开始/结束时间）
 - 基于间隔的执行（以均匀间隔运行job，具有可选的开始/结束时间）
 - 一次性延迟执行（在设定的日期/时间运行一次job）

此外，APScheduler 的后端存储对接了各种各样的存储服务，例如内存、SQL、MongoDB、Redis、ZK 等。

## 快速上手

在使用之前，我们首先需要安装 `apscheduler`，安装方式非常简单:

```sh
pip install apscheduler
```

一个最简单的示例代码如下:

```python
from datetime import datetime
import os

from apscheduler.schedulers.blocking import BlockingScheduler


def tick():
    print('Tick! The time is: %s' % datetime.now())


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
```

运行上述代码，你就可以看到效果了！

```sh
Press Ctrl+C to exit
Tick! The time is: 2021-07-27 16:32:52.281270
Tick! The time is: 2021-07-27 16:32:55.282624
Tick! The time is: 2021-07-27 16:32:58.281650
Tick! The time is: 2021-07-27 16:33:01.281851
Tick! The time is: 2021-07-27 16:33:04.282868
Tick! The time is: 2021-07-27 16:33:07.281247
```

## 核心概念

了解了 apscheduler 最简单的使用方式之后，我们就来展开对 apscheduler 的学习。

首先，我们来了解一下 apscheduler 中的一些核心概念。

apscheduler 包含如下几个核心概念：

 - triggers: 包含调度相关逻辑，每个Job都有自己的触发器，用于确定下一次运行job的时间，除了初识配置之外，触发器是无状态的。
 - job stores: 包含了已调度的Job信息。默认情况下，这些Job信息仅仅保存在内存中，但是我们可以通过配置将其持久化到数据库中。
 - executors: 负责执行对应的Job，它们负责将Job中指定的任务交给对应的线程池或进程池来完成对应的操作。Job完成后，executor 会通知 schedulers 相关任务已完成。
 - schedulers: 调度器用于负责上述相关实体信息的绑定操作。通过，整个程序中只有一个调度器在运行。用户只需要管理Job信息即可，调度器负责触发Job的执行等操作。

## scheduler、job stores、executor 和 trigger 的选择

对 scheduler 的选择主要取决于 APScheduler 的使用场景和目的。

以下是选择 scheduler 的快速指南：

 - BlockingScheduler: APScheduler 是一个独立的应用。
 - BackgroundScheduler: APScheduler是集成在其他应用中，且期望 APScheduler 可以后台执行。
 - AsyncIOScheduler: 使用了 asyncio 模块。
 - GeventScheduler: 使用了 gevent 的应用。
 - TornadoScheduler: Tornado 应用。
 - TwistedScheduler: Twisted 应用。
 - QtScheduler: QT 应用。

是不是足够简单呢？

Job 信息的存储方案可选的方案比较多，大致选择思路如下：

 - 是否在意服务重启后数据丢失？如果不在意，直接用默认的内存存储即可。
 - 如果在意，就需要持久化数据，持久化的方案可以根据业务需要选择，SQL 是一种比较推荐的存储方式。

关于 executor 的配置，通常使用默认的 ThreadPoolExecutor 即可。
如果要执行的是 CPU 密集型的任务，也可以切换为 ProcessPoolExecutor 来发挥多个 CPU 的多核处理能力。

在添加 job 时，需要为 job 设置对应的 trigger。
trigger 的设置完全依赖的业务的需求，根据业务需求设置即可。

## 配置 Scheduler

APScheduler 提供了许多不同的方式来配置 Scheduler 。
您可以使用配置字典，也可以将选项作为关键字参数传入。
您还可以先实例化 Scheduler 程序，然后添加 job 并配置 Scheduler 。
通过这种方式，您可以在任何环境中获得最大的灵活性。

一个默认的 APSscheduler 程序的配置方式如下:

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
```

默认情况下，将会得到一个 BackgroundScheduler ，它的 Job 信息存储在内存中，名称是 default。
同时使用了 ThreadPool 的方式的 executor，最大的线程是为 10。

下面，我们来看一个定制后的 Scheduler 对象：

```python
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

jobstores = {
    'default': MongoDBJobStore(client=get_mongodb())   # get_mongodb 返回一个 MongoClient() 对象
}
executors = {
    'default': ThreadPoolExecutor(20)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BlockingScheduler(
    jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone="Asia/Shanghai"
)
```

可以看到，在上述的 Scheduler 配置中，我们实现了:

 - 使用了 MongoDB 进行数据持久化
 - executor 的并发数设置为了 20
 - 默认情况下为新job关闭合并
 - 新job的默认最大实例限制为 3
 - 时区设置为上海时间。


## 启动 Scheduler

启动 Scheduler 的方式非常简单:

```python
scheduler.start()
```

即可。
其中，对于 BlockingScheduler ，调用 start 函数后就会阻塞等待，而其他的类型的 Scheduler 将会后台执行。

## 添加 Job

向 Scheduler 中添加 Job 有两种方式：

 - 调用 add_job() 函数
 - 通过 scheduled_job 装饰器函数

其中，add_job() 函数是最常用的方式，该函数会返回一个 `apscheduler.job.Job` 对象，可以对它进行进一步的修改或删除。

您可以随时在调度程序上调度job。如果添加job时调度程序尚未运行，则job将被暂定调度，并且仅在调度程序启动时计算其第一次运行时间。

需要注意的是，如果您使用序列化job的执行程序或job存储，它将对您的job增加一些要求：

 - 目标可调用对象必须可全局访问。
 - 可调用对象的任何参数都必须是可序列化的。


在内置job存储中，只有 MemoryJobStore 不序列化job。
在内置执行器中，只有 ProcessPoolExecutor 会序列化job。

Ps: 如果您在应用程序初始化期间在持久job存储中安排job，则必须为job定义显式 ID 并使用 `replace_existing=True`，
否则每次应用程序重新启动时您都会获得job的新副本！

示例如下:

```python
scheduler.add_job(
    func1, trigger="cron", hour="14",
    id="func1",
    replace_existing=True
)
```

## 限制同一个 Job 最大的并发实例执行数

默认情况下，每个job只允许同时运行一个实例。

这意味着，如果job即将运行，但前一次运行尚未完成，则将最新运行任务会当做 misfired 。

通过在添加job时使用 max_instances 关键字参数，可以设置调度程序允许并发运行的特定job的最大实例数。

## 任务合并

有时，调度程序可能无法在计划运行时执行计划作业。

最常见的一个场景就是当我们希望执行该任务时，当前程序处于退出的状态等。
发生这种情况时，该作业被视为 misfired 。
然后调度程序将根据作业的 misfire_grace_time 选项检查每个错过的执行时间，以查看是否仍应触发执行。

在这种情况下，这可能导致作业连续执行多次。

如果您的特定用例不希望这种行为，则可以使用合并将所有这些错过的执行合并为一个。
换句话说，如果为作业启用了合并并且调度程序看到该作业的一个或多个排队执行，它只会触发它一次。

## 调度实践管理

我们可以将事件侦听器附加到调度程序。
调度程序事件在某些情况下被触发，并且可能在其中包含有关该特定事件详细信息的附加信息。

通过为 add_listener() 提供适当的掩码参数，或者将不同的常量组合在一起，可以只侦听特定类型的事件。

可调用侦听器使用一个参数调用，即事件对象。

示例代码如下:

```python
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')

scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
```
