# MQTT的安装（Mosquitto）

首先，需要声明一点的是MQTT本身是一个通用的协议。

具体实现了MQTT协议的Broker软件非常多，例如我们经常听到的RabbitMQ，ActiveMQ等，其实都是可以通过插件等实现支持MQTT协议的。

而在本文中，我们主要介绍的是一块在MQTT协议中非常流行的开源MQTT Broker软件: mosquitto 。

## mosquitto 简介

Mosquitto是一款开源软件（经EPL / EDL许可），它实现了MQTT协议版本5.0、3.1.1和3.1的消息代理。

Mosquitto非常轻巧，适合在从低功耗的嵌入式计算板到服务器的不同的设备上使用。

Mosquitto项目还提供了一个C库，用于实现MQTT客户端。同时，它还提供了非常流行的`mosquitto_pub`和`mosquitto_sub`命令行MQTT客户端。


## 下载与安装

Mosquitto提供了不同平台的安装方式：

Mac:

```shell
brew install mosquitto
brew services start mosquitto
```

其中，配置文件位于`/usr/local/etc/mosquitto/mosquitto.conf`。

Ubuntu:

```shell
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
sudo apt-get install mosquitto           # 安装broker
sudo apt-get install mosquitto-clients   # 安装相关的二进制命令行客户端
```

Raspberry Pi:

```shell
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl status mosquitto
```


## demo实战

Step1: 首先，我们需要先打开一个终端，创建一个消息订阅者接收消息：

```shell
mosquitto_sub -h localhost -t "test/message"
```

此时，该命令将会同步阻塞在此处，等待test/message Topic中接收到的消息。

Step2：下面，我们需要新打开一个终端，并像该Topic中发送一条hello world的消息。

```shell
mosquitto_pub -h localhost -t "test/message" -m "Hello, world"
```

输入完成后，你回到mosquitto_sub的命令行终端，是不是已经收到的对应的消息了呢。

通过上述验证，我们可以看到我们的mosquitto broker已经能够正常的工作了。
