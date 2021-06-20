# RabbitMQ的Fanout类型的Exchange（发布订阅模式）

在之前的内容中，我们学习了RabbitMQ的介绍、安装和以工作队列的形式发布和接收消息。

在本文中，我们将会讲解另一种RabbitMQ消息传递模式。

即将同一条消息传递给多个接收者。这种模式也称之为发布、订阅模式。

## 场景描述

在本文中，我们将会实现一个日志处理系统。

该系统包含两个部分：

1. 第一部分是产生日志。 
2. 第二部分是接收日志并打印日志。

在运行的过程中，我们会启动多个接收日志并打印日志的服务。

我们希望可以看到每个服务都接收到全部的日志信息。也就是说，服务1产生的日志最终会广播至所有的接收者。

## Exchanges

在之前的文章中，我们讲解了一个RabbitMQ模型由以下几个部分组成：

 - 消息生产者：产生消息的来源。
 - 队列：存储尚未处理的消息。
 - 消息处理者：接收消息并处理。

实际上，这个模型仅仅是一个简化版的RabbitMQ模型。

对于真实的RabbitMQ模型而言，消息生产者是不会直接将消息传入队列中的。相反，消息生产者会把消息发送给Exchanges（中转所），而Exchanges（中转所）在接收到消息后，才会把消息插入到队列中。

在Exchanges（中转所）中，实现的功能包括：

 - 该消息是否需要插入某个队列中。
 - 该消息仅需要发送至一个队列还是需要发送至多个队列。
 - 该消息是否根据某些Exchanges（中转所）的类型需要被忽略等等。


Exchanges包含如下几个类型：`direct`, `topic`, `headers`以及`fanout`。

在本文中，我们首先来学习fanout类型。

fanout的含义是将每条消息都广播发送给所有的消息接收者。

例如，可以实现如下：

```shell
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')
```

即声明exchange的类型为fanout，且名称为logs。

在声明了exchange后，我们可以继续发布消息：

```python
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
```

## 临时队列

在之前的文章中，我们需要指定一个特定的队列名称，因为我们需要将一组Worker用于接收某个指定的队列名称中的消息。

但是，对于发布、订阅模式场景而言，我们需要的是：

 - 接收全部的消息，而不是其中的一部分消息。
 - 只接收最新产生的消息，而忽略之前传入的消息。

因此，我们需要完成以下两个部分的工作：

Step1: 每次在连接到RabbitMQ时，创建一个空的队列。实现该功能的方式是我们可以创建一个随机名称的队列。

```python
result = channel.queue_declare()
```

Ps: 在不指定参数时，默认将会产生一个随机字符串组成的队列。

Step2: 此外，我们需要在创建队列时添加一个额外的参数：

```python
result = channel.queue_declare(exclusive=True)
```

Ps: `exclusive=True`表示当消息接收者断开连接时，自动删除该队列。

## 将 Exchange 与 Queue 进行关联

目前，我们已经创建了一个fanout类型的exchange。同时，在消息接收者中也创建了队列。

现在，我们需要做的是将exchange和消息队列关联起来。

```python
channel.queue_bind(exchange='logs',
                   queue=result.method.queue)
```

## 完整实现

最后，我们来给出消息生产者和消息接收者的完整实现：

消息生产者：`emit_log.py`

```python
#!/usr/bin/env python
import pika
import sys
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')
message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
print(" [x] Sent %r" % message)
connection.close()
```

消息接收者：`receive_logs.py`

```python
#!/usr/bin/env python
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='logs',
                   queue=queue_name)
print(' [*] Waiting for logs. To exit press CTRL+C')
def callback(ch, method, properties, body):
    print(" [x] %r" % body)
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
channel.start_consuming()
```

实际来看一下效果吧：

我们可以先启动两个消息接收者：

receiver1:

```shell
python receive_logs.py
```

receiver2:

```shell
python receive_logs.py
```

然后，我们来发送几条消息：

```shell
python emit_log.py
python emit_log.py
```

怎么样？是不是每条消息都被两个消息接收者同时接收到了？~
