
# 在Ubuntu中搭建DHCP服务

## 什么是DHCP？

动态主机设置协议（Dynamic Host Configuration Protocol，缩写：DHCP），又称动态主机组态协定。
是一个用于IP网络的网络协议，位于OSI模型的应用层，使用DHCP协议工作，主要有两个用途：

1. 用于内部网或网络服务供应商**自动分配IP地址**给用户。
2. 用于内部网管理员对所有电脑作中央管理。

## 安装DHCP服务

下面，我们以 Ubuntu 20.04 系统为例，来讲解如何安装DHCP服务。

### 1. 安装DHCP服务器

```
sudo apt-get installdhcp3-server
```

接下来，我们需要设置DHCP相关的配置文件。
与DHCP服务器相关的配置文件共有2个，分别是 `/etc/dhcp/dhcpd.conf` 和 `/etc/default/isc-dhcp-server`。

### 2. 修改 `/etc/default/isc-dhcp-server` 配置

首先我们首先来修改 `/etc/default/isc-dhcp-server` 配置文件。

在该配置文件中，我们仅仅只需要设置监听DHCP服务的网卡即可，首先，我们需要使用 `ip addr` 命令查询机器上可用的网卡名称：

```
$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s31f6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 54:e1:ad:28:cb:aa brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.22/24 brd 192.168.1.255 scope global noprefixroute enp0s31f6
       valid_lft forever preferred_lft forever
    inet6 fe80::56e1:adff:fe28:cbaa/64 scope link 
       valid_lft forever preferred_lft forever
```

从上面输出中，我们可以看到机器上有一个名为 `enp0s31f6` 网卡。

接下来就是编辑 `/etc/default/isc-dhcp-server` 配置文件，找到下面这行进行修改即可：

```
INTERFACESv4="enp0s31f6"
```

Ps：根据不同的操作系统版本，由于名词也不太一样，例如，有时会叫做 `INTERFACES` 可以根据默认配置文件进行查看。

### 3. 修改 `/etc/dhcp/dhcpd.conf` 配置

该文件中，需要修改两部分。

首先是注释第一部分中的 `option domain-name-servers` 行，如下所示：

```
# option definitions common to all supported networks...
option domain-name "example.org";
# option domain-name-servers ns1.example.org, ns2.example.org; # 注释该行

default-lease-time 600;
max-lease-time 7200;
```

第二部分则是修改 subnet 块：

```
# A slightly different configuration for an internal subnet.
subnet 192.168.1.0 netmask 255.255.255.0 {
  range 192.168.1.150 192.168.1.253;
  option domain-name-servers 192.168.1.1;
  option subnet-mask 255.255.255.0;
  option routers 192.168.1.1;
  option broadcast-address 192.168.1.255;
  default-lease-time 600;
  max-lease-time 7200;
}
```

### 4. 重启DHCP服务

```
sudo service isc-dhcp-server restart
```

### 5. 验证DHCP服务是否正常启动

```
sudo netstat -uap
# ...
# udp        0      0 0.0.0.0:bootps          0.0.0.0:*                           1084/dhcpd
# ...
```

Ps: 如果能够看到上述输出中包含dhcp任务，那就说明DHCP服务器已经正常启动了。
