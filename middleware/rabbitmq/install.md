# RabbitMQ的安装

本文中，我们将会讲解RabbitMQ在各种平台下的安装方式。

## 什么是 RabbitMQ

RabbitMQ是一个消息代理：它的主要功能是接收和转发消息。 你可以把它想象成一个邮局：当你把你想要邮寄的邮件放在邮箱后，邮递员最终将邮件发送给你的收件人。在这个例子中，RabbitMQ充当的是邮政信箱，邮局和邮递员的角色。

RabbitMQ和邮局的主要区别在于它处理的不是实物邮件，而是接收，存储和转发二进制数据（我们称之为消息）。

在RabbitMQ中，我们有一些常用的术语：

 - Producing（消息生产者）：在RabbitMQ的使用场景中，Producing表示消息的生产者，它是用来发送消息的。
 - Queue（队列）：RabbitMQ接收到消息后，会将其存放在队列中。一个队列受到主机内存和磁盘限制的约束，它本质上是一个很大的消息缓冲区。 许多生产者可以发送消息至同一个队列，许多消费者可以从一个队列中接收数据。
 - Consuming（消息消费者）：消费者又称为接收者，实际就是消息的接收者，

Ps: 需要说明的是，在RabbitMQ的使用场景中，Producing、Queue和Consuming无需部署在同一机器上，仅仅需要互相之间网络联通即可。

## 什么场景会使用RabbitMQ？

了解了什么是RabbitMQ以后，我们来思考一下，什么场景需要使用RabbitMQ？

RabbitMQ其中一个常用场景是分布式异步任务处理功能。

想象一下，在一个分布式系统中，模块A通过HTTP请求调用模块B的接口，而传递给模块B处理的任务又相对复杂，有一定的耗时。

如果是同步请求，所有的请求都等到模块B完整处理完成后再返回模块A的话，一个直接导致的后果是会在模块A和模块B之间阻塞大量的任务。一方面可能会由于给模块B的压力过大导致调度失败，同时也可能由于模块B连接打满无法接收任务。

此时，一种较好的解决方案如下：
模块A将任务信息发送给RabbitMQ即可，然后RabbitMQ将消息发送给模块B进行处理。一方面，避免了长连接导致的模块B无法访问，另一方面，可以通过调度任务处理机制以及部署多个模块B来进行分布式处理从而缓解服务压力。

## Ubuntu下安装RabbitMQ

在Ubuntu系统下，RabbitMQ的安装非常简单，可以直接使用 `apt-get` 命令安装即可。

```bash
sudo apt-get install rabbitmq-server
```

安装完成后，我们可以检查服务状态已经端口是否正常启动：

```bash
# 检查服务状态
service rabbitmq-server status

# 检查端口是否正常启动
sudo lsof -i:5672
```

![rabbimtmq status](./picture/install1.png)

## Docker 安装方式

下面，我们来讲解一下如何使用Docker来安装RabbitMQ。

首先，我们需要安装Docker服务，安装的方式此处不再赘述。

安装完成Docker后，我们可以执行如下命令来拉取最新的rabbitmq镜像：

```shell
sudo docker pull rabbitmq
```

然后执行如下命令启动即可：

```shell
sudo docker run -d --name rabbitmq -p 5671:5671 -p 5672:5672 -p 4369:4369 -p 25672:25672 -p 15671:15671 -p 8439:15672 rabbitmq
```


## RabbitMQ配置与管理

RabbitMQ搭建完成后，我们需要添加一个管理员用户用于RabbitMQ的管理。

```bash
sudo rabbitmqctl add_user  admin  admin
```

赋予该用户管理员权限：

```bash
sudo rabbitmqctl set_user_tags admin administrator
```

赋予virtual host中所有资源的配置、写、读权限以便管理其中的资源:

```bash
sudo rabbitmqctl  set_permissions -p / admin '.*' '.*' '.*'
```

启用RabbitMQ管理页面:

```bash
sudo rabbitmq-plugins enable rabbitmq_management
```

之后在浏览器访问 [http://server-ip:15672](http://server-ip:15672) ，账号与密码都是刚才设置的 admin。
