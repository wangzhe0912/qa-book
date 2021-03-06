# Redis的安装

本文中，我们将会讲解Redis在各种平台下的安装方式。

## Ubuntu下安装Redis

在Ubuntu系统下，Redis的安装非常简单，可以直接使用 `apt-get` 命令安装即可。

```bash
sudo apt-get install redis-server
```

安装完成后，我们可以检查服务状态已经端口是否正常启动：

```bash
# 检查服务状态
service redis-server status

# 检查端口是否正常启动
sudo lsof -i:6379
```

![redis status](./picture/install1.png)

默认情况下，Redis服务仅允许通过使用127.0.0.1进行本地访问。
因此，我们需要修改配置文件使得它运行外网访问。

redis的配置文件位于: `/etc/redis/redis.conf`。

```
bind 0.0.0.0
```

Ps：修改配置文件中bind_ip的值为0.0.0.0即可。

配置文件修改完成后，需要重新启动redis服务使之生效：

```bash
service redis-server restart
```
