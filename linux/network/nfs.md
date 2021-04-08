# NFS网络文件系统搭建

## 概述

NFS或网络文件系统是一种分布式文件系统协议，最初是由Sun Microsystems构建的。

通过NFS，您可以允许系统通过网络与其他人共享目录和文件。
在NFS文件共享中，用户甚至程序可以访问远程系统上的信息，就像它们驻留在本地计算机上一样。

NFS 以客户端 - 服务器方式运行，其中服务器负责管理客户端的身份验证，授权和管理，以及特定文件系统内共享的所有数据。

授权后，任意数量的客户端都可以访问共享数据，就好像它们存在于其内部存储中一样。

在 Ubuntu 系统上设置 NFS 服务器非常简单。

在本文中，我们将逐步说明如何设置NFS服务器和客户端，使您能够将文件从一个Ubuntu系统共享到另一个Ubuntu系统。

## 服务端搭建

Step1: 安装 NFS 服务器

```shell
sudo apt-get update
sudo apt install nfs-kernel-server
```

Step2: 创建共享目录

```shell
sudo mkdir -p /home/wangzhe/Desktop/sync_data_executor_dir
sudo chown nobody:nogroup /home/wangzhe/Desktop/sync_data_executor_dir
sudo chmod 777 /home/wangzhe/Desktop/sync_data_executor_dir
```

Step3: 设置目录访问权限

修改 `/etc/exports` 文件，增加如下内容:

```shell
/home/wangzhe/Desktop/sync_data_executor_dir 192.168.1.0/24(rw,sync,no_subtree_check)
```

上述内容的含义表示: 允许 192.168.1.0/24 网段的机器读写 /home/wangzhe/Desktop/sync_data_executor_dir 共享目录。

Step4: 重启NFS服务端使得配置生效

```shell
sudo exportfs -a
sudo service nfs-kernel-server restart
```

此时，NFS 服务端就已经搭建完成了。

## 客户端搭建

Step1: 安装 NFS Common （包含 NFS 客户端）

```shell
sudo apt-get update
sudo apt-get install nfs-common
```

Step2: 在客户端机器上创建一个目录用于挂载共享目录

```shell
sudo mkdir -p /home/wangzhe/Desktop/sync_data_executor_dir
sudo mount 192.168.1.102:/home/wangzhe/Desktop/sync_data_executor_dir /home/wangzhe/Desktop/sync_data_executor_dir
```

Step3: 测试一下吧

此时，其实我们的 NFS 服务端和客户端就都已经搭建完成了，下面我们可以来验证一下。

在客户端机器的目录上创建一个文件，然后在服务端对应的共享目录上看一下，是不是已经可以看到该文件了呢。
