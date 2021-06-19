# RabbitMQ的Direct类型的Exchange（选择性订阅）

在之前的文章中，我们实现了一个简单的日志系统。

该日志系统在接收到一条日志消息后，可以将其分发给所有的消息接收者。

在本文中，我们将对该功能进行拓展，从而实现仅订阅其中的一部分消息。

例如，我们只能将重要的错误消息引导到日志文件（以节省磁盘空间），同时仍然能够在控制台上打印所有日志消息。

## 关联

回想一下，在之前的文章中，我们将exchange与队列通过如下方式进行关联：

```python
channel.queue_bind(exchange=exchange_name,
                   queue=queue_name)
```

这种关联表示了该队列关注于这个exchange中的消息。

而在创建关联时，实际上我们还可以添加一个参数：routing_key。

例如：

```python
channel.queue_bind(exchange=exchange_name,
                   queue=queue_name,
                   routing_key='black')
```

routing_key 的功能与 exchange 的类型有关，在我们之前使用的fanout类型的exchange中，routing_key是一个无用的参数。

## Direct类型的exchange

之前我们仅仅学习了fanout类型的exchange。 接下来，我们将要学习的是direct类型的exchange。

direct类型的exchange的功能如下：根据routing_key进行完全匹配，将消息发送给所有routing_key匹配的通道中。

![direct_scene1](./picture/direct_scene1.png)

在上图所示的模型中，使用了direct类型的exchange，并包含了两个通道。

在通道1中，会接收所有routing_key='orange'的消息，而在通过2中，会接收所有routing_key='black'或者'green'的消息。而其他所有消息将会被忽略。

### 多绑定

当然，将某种类型的数据绑定给多个通过也是没问题的，例如下图所示：

![direct_scene2](./picture/direct_scene2.png)

当接收到routing_key='black'的消息时，将会同时传递给通道1和通道2。

## 具体实现

最后，我们来完成之前描述的功能，即实现一个日志管理系统，将重要的错误消息引导到日志文件（以节省磁盘空间），同时仍然能够在控制台上打印所有日志消息。

![direct_scene3](./picture/direct_scene3.png)

消息生产端 `emit_log_direct.py` 文件如下：

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')
# 命令行中第一个参数表示severity，默认为info
severity = sys.argv[1] if len(sys.argv) > 2 else 'info'
# 命令行中第二个即以后的参数拼接表示message，默认为'Hello World!'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
# 发送消息中添加routing_key
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()
```

消息处理端 `receive_logs_direct.py` 文件如下：

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
# 接收参数作为severities
severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)
for severity in severities:
    # 一个通道中接收多个routing_key
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)
print(' [*] Waiting for logs. To exit press CTRL+C')
def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
channel.start_consuming()
```

下面，我们来启动服务验证一下效果吧！

启动消息接收服务1：

```shell
# 接收info warning error级别的日志并打印在屏幕上
python receive_logs_direct.py info warning error
```

启动消息接收服务2: 

```shell
# 接收error级别的日志并写入logs_from_rabbit.log文件
python receive_logs_direct.py error > logs_from_rabbit.log
```

发送一些消息看看吧：

```shell
python emit_log_direct.py error "Run. Run. Or it will explode."
python emit_log_direct.py debug "Run. Run. Or it will explode."
python emit_log_direct.py info "Run. Run. Or it will explode."
python emit_log_direct.py warning "Run. Run. Or it will explode."
```

怎么样？结果是否符合预期呢？欢迎大家一起讨论。
