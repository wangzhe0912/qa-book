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
