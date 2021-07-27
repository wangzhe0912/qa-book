# RabbitMQ的配置详解

在上一节的内容中，我们讲解了如何快速安装一个 RabbitMQ 的服务。
因为仅仅是一个示例，我们没有对它的配置进行任何的修改就直接启动了服务。

然而，在生产环境中，我们常常需要对 rabbitmq 的配置进行一些修改，然后再启动服务，而在本文中，我们将会重点讲解 RabbitMQ 如何进行相关的配置。

## 概述

RabbitMQ 提供了三种方式来定制服务相关的配置:

 - 环境变量: RabbitMQ 的部分服务端参数可以直接通过环境变量进行配置，例如节点名称、RabbitMQ配置文件地址、端口等。
 - 配置文件: RabbitMQ 可以通过配置文件定义 RabbitMQ 的服务配置和相关的插件设置等，例如 TCP监听端口、内存磁盘限制等。
 - 运行时参数和策略: RabbitMQ 的集群层面相关的配置可以在运行时通过参数和策略进行配置。


## 环境变量

RabbitMQ 的环境变量都是以 `RABBITMQ_` 开头的，可以直接在 shell 中进行配置，
也可以在 `rabbitmq-env.conf` 这个 RabbitMQ 环境变量文件中统一设置（推荐）。

Ps: shell 配置的环境变量优先级高于 `rabbitmq-env.conf` 配置文件。

例如一个简单的 `rabbitmq-env.conf` 文件内容如下:

```sh
# 定义节点名称
NODENAME=rabbit@node1
# 定义RabbitMQ对外通信端口号
NODE_PORT=5672
# 定义RabbitMQ配置文件地址，其中，如果配置文件的后缀是 .config ，则可以直接省略后缀
CONFIG_FILE=/opt/rabbitmq/etc/rabbitmq/rabbitmq
```

其中，`rabbitmq-env.conf` 文件默认位于 `$RABBITMQ_HOME/etc/rabbitmq/` 目录下。

下面，我们来罗列一些常用的环境变量:

|变量名称|描述|
|------|----|
|RABBITMQ_NODE_IP_ADDRESS|绑定某个特性的网络接口，默认为空，表示绑定到所有网络接口上。|
|RABBITMQ_NODE_PORT|监听客户端连接的端口，默认为5672|
|RABBITMQ_DIST_PORT|分布式通信的端口号，默认为 RABBITMQ_NODE_PORT + 20000|
|RABBITMQ_NODENAME|节点名称，默认为rabbit@$HOSTNAME，每个erlang和机器的组合中，节点名称必须唯一|
|RABBITMQ_CONFIG_FILE|配置文件地址，不需要.config文件后缀|
|RABBITMQ_CONF_ENV_FILE|环境变量配置文件地址，默认为$RABBITMQ_HOME/etc/rabbitmq/rabbitmq-env.conf|
|RABBITMQ_USE_LONGNAME|当机器名称包含.时，默认取.前面的部分，设置为true时，会取完整名称|
|RABBITMQ_MNESIA_DIR|存储服务节点的数据库、数据存储、集群状态相关的目录，默认为$RABBITMQ_MNESIA_BASE/$RABBITMQ_NODENAME|
|RABBITMQ_MNESIA_BASE|RABBITMQ_MNESIA_DIR的父目录，默认为$RABBITMQ_HOME/var/lib/rabbitmq/mnesia|
|RABBITMQ_LOGS|日志目录，默认为$RABBITMQ_LOG_BASE/$RABBITMQ_NODENAME.log|
|RABBITMQ_LOG_BASE|日志父目录，默认为$RABBITMQ_HOME/var/log/rabbitmq|
|RABBITMQ_SASL_LOGS|RabbitMQ服务于erlang的SASL日志，默认为$RABBITMQ_LOG_BASE/$RABBITMQ_NODENAME-sasl.log|
|RABBITMQ_PLUGINS_DIR|插件所在的路径，默认为$RABBITMQ_HOME/plugins|

## 配置文件

RabbitMQ 的配置文件指的是上述环境变量`RABBITMQ_CONFIG_FILE`对应的文件，可以用于设置 RabbitMQ 的详细配置。

一个极简单的 `rabbitmq.config` 文件的内容如下（不能遗漏最后的 .）:

```
[
    {
        rabbit, [
            {tcp_listeners, [5673]}
        ]
    }
].
```

上述配置的含义是将 RabbitMQ 的端口由默认的 5672 修改为了 5673。

关于 RabbitMQ 的详细配置文件可以参考[官方文档](https://www.rabbitmq.com/configure.html#config-file) ，此处不再一一罗列了。

## 运行时参数和策略配置

对于 RabbitMQ 的绝大部分参数，其实都可以通过修改 RabbitMQ 的配置文件来完成。

但是也有一些参数，我们希望能够在服务运行的过程中进行动态的修改，这种参数我们就称之为"运行时参数"。

RabbitMQ 的运行时参数可以通过 `rabbitmqctl` 工具或者 RabbitMQ Management 插件提供的 HTTP API 来实现。

此处就不展开介绍了。
