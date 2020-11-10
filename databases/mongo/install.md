# MongoDB的安装

本文中，我们将会讲解MongoDB在各种平台下的安装方式。

## Ubuntu下安装MongoDB

在Ubuntu系统下，MongoDB的安装非常简单，可以直接使用 `apt-get` 命令安装即可。

```bash
sudo apt-get install mongodb
```

安装完成后，我们可以检查服务状态已经端口是否正常启动：

```bash
# 检查服务状态
service mongodb status

# 检查端口是否正常启动
sudo lsof -i:27017
```

![mongodb status](./picture/install1.png)

默认情况下，mongoDB服务仅允许在127.0.0.1进行本地访问。
因此，我们需要修改配置文件使得它运行外网访问。

mongodb的配置文件位于: `/etc/mongodb.conf`。

```
bind_ip = 0.0.0.0
```

Ps：修改配置文件中bind_ip的值为0.0.0.0即可。

配置文件修改完成后，需要重新启动mongodb服务使之生效：

```bash
service mongodb restart
```

## Linux下MongoDB集群环境搭建

搭建一个多节点的副本集MongoDB时，至少需要3个节点（机器）。

分别在每个机器上执行如下命令：

Step1：下载指定版本的MongoDB并解压到/home/zhiyun/mongodb-4.2.2目录中。
Step2：创建服务创建相关目录和配置文件：

```bash
cd /home/zhiyun/mongodb-4.2.2
mkdir logs
mkdir -p ./data/db
mkdir conf
vim ./conf/config.yaml
```

其中config.yaml文件如下：

```bash
systemLog:
    destination: file
    path: /home/zhiyun/mongodb-4.2.2/logs/mongod.log
    logAppend: true
storage:
    dbPath: /home/zhiyun/mongodb-4.2.2/data/db
net:
    bindIp: 0.0.0.0
    port: 8017
replication:
    replSetName: zhiyunrs
processManagement:
    fork: true
```

Step3：依次启动每台机器的MongoDB服务：

```bash
cd /home/zhiyun/mongodb-4.2.2
./bin/mongod -f ./conf/config.yaml
```

Step4：当所有节点的mongodb服务均启动成功后，在任一节点中执行如下命令，将其设置为副本集模式：

```bash
./bin/mongo --port 8017
```

然后在mongo交互式命令行中输入如下内容：

```
rs.initiate({
    _id: "zhiyunrs",
    members: [
        {
            _id: 0,
            host: "${IP1}:8017"
        }, {
            _id: 1,
            host: "${IP2}:8017"
        }, {
            _id: 2,
            host: "${IP3}:8017"
        }
    ]
})
```

至此为止，一个三副本的MongoDB服务就搭建完成了。
