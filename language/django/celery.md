# Django Celery快速入门

## 什么是Celery

Celery是一个分布式任务的框架，具备如下特点：

1. 简单：几行代码就可以创建一个简单的Celery任务。
2. 高可用：任务可以自动重试。
3. 快速：可以在一分钟内执行上百万个任务。
4. 灵活：每一部分都可以轻松进行扩展。


## Celery使用场景

Celery非常适合用于去做需要异步执行的任务，例如：

1. 发送电子邮件，发送IM消息通知
2. 爬取网页，数据分析
3. 图片和视频处理
4. 生成报告等

## Celery架构

Celery架构如下图所示：

![Celery架构](./pictures/celery架构.png)

1. 首先，任务的来源可以是WebServer下发，也是可以是定时任务器下发。
2. 接下来，下发的任务首先会存放到一个Broker的队列中等待处理。
3. 然后Worker会从Broker消息队列中读取消息并处理。
4. 最后将处理后得到的结果再次写入一个数据库进行存储。


## Celery环境搭建

下面，我们来看如何搭建Celery的环境。

第一步：安装Celery第三方库

```shell
pip3 install celery
```

第二步：安装Celery依赖库

```shell
pip3 install "celery[librabbitmq,redis,auth,msgpack]"
```

第三步：做为Broker示例，我们需要安装一个Redis，此处，我们用docker了部署一个Redis实例

```shell
docker run -d -p 6379:6379 redis
```

到此为止，Celery的基本环境我们就已经准备完成了，下面我们可以用一个Celery的demo来验证我们的环境是否OK。

## Celery Demo

创建`tasks.py`文件如下:

```python
from celery import Celery


app = Celery('tasks', broker='redis://127.0.0.1', backend='redis://127.0.0.1')


@app.task
def add(x, y):
    return x + y
```

启动celery worker:

```shell
celery -A tasks worker --loglevel=info
```

![CeleryWorker](./pictures/celery_worker.png)

接下来，我们创建一个运行任务的脚本`run_task.py`:

```python
from tasks import add

result = add.delay(4, 4)
print('Is Task ready: %s' % result.ready())

run_result = result.get(timeout=1)
print("task result: %s" % run_result)
```

运行脚本，观察输出如下：

```shell
python3 ./run_task.py
# Is Task ready: False
# task result: 8
```

可以看到，该任务的确是异步执行的，首先执行后，任务的状态并未完成，然后等待任务执行完成后，获取到了计算的结果。

## Celery任务的监控

因为任务异步化对于我们项目的运维和问题定位无疑是增加了一定的成本，为了能够让我们的系统更加容易监控和观察，Celery提供了一套监控方案：Flower。

下面，我们来体验一下Flower。

Step1: 安装flower

```shell
pip3 install flower==0.9.7
```

Step2: 启动flower

```shell
celery -A tasks flower --broker=redis://localhost:6379/0
```

![flower](./pictures/flower_start.png)

访问localhost:5555可以看到如下页面:

![flower](./pictures/flower_web.png)

在该页面中，我们可以查询Celery相关的节点，任务等一系列详细信息。

## Django集成Celery

在上面的例子中，我们主要在讲解Celery自身的功能和用法，接下来，我们将会结合Django来讲解如何在Django中使用Celery。






## 参考资源

1. [Celery官方文档](https://docs.celeryproject.org/en/stable/)
