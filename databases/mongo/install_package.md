# MongoDB安装包剖析

在上一节中，我们已经以Ubuntu为例，讲解了如何快速安装MongoDB。

而在本节中，我们将通过安装包下载的方式来详细讲解MongoDB的安装包中包含了哪些内容，以及相关的工具的介绍。

## 安装包下载

我们可以从 [MongoDB官方网站](https://www.mongodb.com/try/download/community) 下载MongoDB的安装包。

我们以Mac系统为例，下载完成后，我们可以解压该压缩包：

```bash
tar -zxvf mongodb-macos-x86_64-4.4.3.tgz
```

进入该目录后，我们看到如下内容：

```
.
├── LICENSE-Community.txt
├── MPL-2
├── README
├── THIRD-PARTY-NOTICES
└── bin
    ├── install_compass
    ├── mongo
    ├── mongod
    └── mongos
```

其中：

1. `LICENSE-Community.txt`、`MPL-2`以及`THIRD-PARTY-NOTICES`文件都是开源协议以及第三方使用相关授权事项等信息，不在本文展开讨论。
2. `README`是MongoDB安装包相关的介绍文档，建议完整阅读，下文中也会给出相关的中文翻译版本。
3. `bin`目录下是可以直接运行的MongoDB二进制包以及一些配套的工具，都会在`README`中提及。

## README

下面，我们来看一下MongoDB安装包中的README文档。

欢迎使用MongoDB！

### MongoDB安装包中包含如下内容：

1. mongod: 数据库服务端程序。
2. mongos: 分片路由程序。
3. mongo: 数据库交互式shell工具。

### 其他工具：

1. install_compass: 可以快速安装MongoDB Compass的工具。

### 源码构建方式

参考docs/building.md文件

### 服务启动：

1. 查询命令行参数的方式: `./mongod --help`
2. 快速启动一个单实例的数据库：
```bash
sudo mkdir -p /data/db
./mongod  # 启动mongodb服务端

# mongo javascript 交互式Shell默认连接localhost的test数据库:
./mongo
# > help
```

### 安装Compass

你可以使用bin目录下的install_compass脚本来快速安装Compass：

```bash
./install_compass
```

上述脚本会下载适用于你的平台的Compass部署包并执行相关的安装操作。

### 驱动

大部分语言的客户端驱动可以在 https://docs.mongodb.com/manual/applications/drivers/ 找到。

此外，还可以使用`mongo`交互式shell工具来进行相关的管理任务。

### Bug反馈

详见: https://github.com/mongodb/mongo/wiki/Submit-Bug-Reports

### 打包

在buildscripts目录中，有一个`package.py`脚本可以自动的创建对应的RPM和Debian包。

### 文档

使用文档详见: https://docs.mongodb.com/manual/

### MongoDB云服务

见: https://www.mongodb.com/cloud/atlas

### 论坛

1. MongoDB使用问题相关论坛: https://community.mongodb.com
2. MongoDB构建和开发问题相关论坛: https://community.mongodb.com/c/server-dev

### 学习MongoDB

https://university.mongodb.com/

### 许可

MongoDB是免费和开源的。
2018年10月16日之前发布的版本适用于AGPL许可。
2018年10月16日之后发布的所有版本（包括先前版本的修补程序修复）均根据服务器端公共许可证（SSPL）v1发布。

## 二进制程序

### mongod

`mongod` 是mongodb服务端的二进制执行程序，通过`mongod`我们可以快速启动一个MongoDB服务。

### mongos

对于分片群集，`mongos`实例提供客户端应用程序和分片群集之间的接口。

通过`mongos`服务，可以实现MongoDB集群横向扩展。

### mongo

`mongo` 是一个交互示shell的MongoDB交互工具，通过`mongo`命令行工具，可以对MongoDB服务端进行相关管理操作，基本使用格式如下：

```
usage: ./mongo [options] [db address] [file names (ending in .js)]
```

### install_compass

`install_compass`是一个Python脚本。

它的功能是可以在除Windows之外的操作系统中，根据当前的操作系统下载适合版本的Compass工具并安装。

使用方式非常简单，直接执行如下命令即可：

```bash
./install_compass
```
