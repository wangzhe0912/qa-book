# RabbitMQ的Demo示例

本文中，我们将会实现一个入门级的Demo程序来了解一下 RabbitMQ 的使用。

## Producing Demo 实现

首先，我们需要实现一个Producing，来向RabbitMQ发送消息。

完整的示例代码`send.py`如下：

```python
#!/usr/bin/env python
import pika  # pika是Python连接RabbitMQ的工具
# 第一步是用于连接RabbitMQ
# Demo程序中，send.py运行机器与RabbitMQ位于同一台机器中，因此使用localhost表示本机，如果部署在不同机器中，可以指定IP地址。
# Demo程序中，RabbitMQ默认启动占用的是5672端口，因此无需指定，如果RabbitMQ使用其他端口，需要使用port=****来指定端口信息。
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
# 第二步，在发送消息之前，我们需要确保收件人队列存在。
# 如果我们发送消息到不存在的位置，RabbitMQ将只删除该消息。
# 下面，我们来创建一个将传递消息的hello队列
channel.queue_declare(queue='hello')
# 创建完成收件人队列后，我们就可以发送消息了。
# 第一条消息此处是一个字符串Hello World
# 在RabbitMQ中，消息永远不会直接发送到队列，它总是需要经过交换来实现的。
# 交换的功能细节我们会在后续进行讲解，现在只需要知道的使用由空字符串标识的默认交换。
# 我们可以使用routing_key参数中指定消息发送至哪个收件人队列。
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
# 在退出程序之前，我们需要确保网络缓冲区被刷新，并且我们的消息被实际传送到RabbitMQ。 
# 因此，我们需要执行断开连接功能。
connection.close()
```

## Consuming Demo 实现

Producing代码完成后，我们来继续学习Consuming部分的代码`receiver.py`。

在这个Demo中Consuming实现的功能就是接收到消息后将其打印出来（标准输出）。

```python
#!/usr/bin/env python
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
# 同样进行验证指定队列存在（如果不存在则创建该队列，如果已经存在则忽略）
channel.queue_declare(queue='hello')
# 下面，我们定义一个回调函数。
# 每当我们收到一条消息，这个回调函数就在收到消息后调用。 
# 在我们的例子中，这个函数会在屏幕上打印消息的内容。
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
# 接下来，我们需要告诉RabbitMQ这个特定的回调函数应该从我们的hello队列接收消息
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
# 最后，我们进入一个永无止境的循环，等待数据在必要时运行回调。
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
```

## 运行实验

下面，我们来运行一下看看吧~

首先，我们需要启动consumer来等待消息发送：

```shell
python receiver.py
```

接下来，我们可以用 `sender.py` 来发送消息，每次执行后会发送一条消息：

```shell
python sender.py
```

现在，我们可以看到每次发送消息后，在`receiver.py`运行的终端中，会打印出`sender.py`中发送的消息HelloWorld。
