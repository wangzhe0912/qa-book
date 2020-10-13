# Ubuntu系统下搭建与使用FTP服务器

## 环境准备

在本文中，我们将会以 Ubuntu 20.04 版本的操作系统为例，演示如何快速搭建一个FTP服务器。

## Step By Step

**Step1: 安装FTP服务器**

```bash
sudo apt-get install vsftpd
```

简单一条命令，其实我们就已经完成了FTP服务的安装，接下来我们需要创建对应的用户并修改相关配置文件使其生效。

**Step2：创建FTP用户**

```bash
# 创建用户
sudo useradd -m ftpuser

# 设置用户密码
sudo passwd ftpuser
```

至此，FTP用户已经成功创建好了，下面，我们来修改FTP服务的相关配置文件

**Step3：修改FTP配置文件**

```bash
sudo vim /etc/vsftpd.conf
```

此时，为了能够让我们的FTP服务器能够正常运行，我们仅仅只需要修改开启write_enable即可：

```bash
# Uncomment this to enable any form of FTP write command.
write_enable=YES
```

其他配置可以保持不变。

**Step4：重启FTP服务使配置生效**

```bash
service vsftpd restart
```

此时，FTP服务已经正常启动了，接下来我们就可以正常使用FTP服务了。

## 其他配置说明

关于 `vsftpd` 服务的相关配置都位于 `/etc/vsftpd.conf` 配置文件中。
下面，我们来依次讲解一些常用的配置。

### 自定义端口

对于FTP服务器，其默认端口为21。
有时，我们希望能够修改FTP服务监听的端口，此时，则使用到了如下配置：

```bash
listen_port=8021
```

除了修改 `/etc/vsftpd.conf` 配置文件外，我们还需要修改 `/etc/services` 文件，其中有系统Service相关的端口设置：

```bash
ftp             8021/tcp
ftp             8021/udp          fsp fspd
```

### pasv_promiscuous参数

```bash
pasv_promiscuous=YES
```

该参数可以是YES / NO。默认值为NO。
当该参数设置为NO时，会进行被动模式安全检查，这一检查可以保证数据连接源于同一个IP地址。
当该参数设置为YES时，则会忽略该检查。

## FTP服务文件上传下载

### 客户端工具

我们以Mac为例，可以选择使用 ForkLift 客户端软件来与FTP服务器进行交互。

![ftp1](./picture/ftp1.png)

### 命令行工具

除了客户端外，我们最常用的命令行工具就是 *wget* 工具了。

```bash
wget ftp://${username}:${password}@{hostname}:${port}/{filepath}
```

其中，FTP协议的默认端口是21，如果没有修改端口的话，可以不用传入端口信息。

除了 *wget* 命令行工具外，一个更加强大的命令行工具就是telnet了。

telnet是一个基于TCP协议的强大的命令行工具。使用telnet可以与FTP Server进行正常交互。
下面，我们以一个示例来演示如何使用telnet命令行工具与FTP Server进行交互。

Ps: 假设FTP Server的IP为192.168.1.22，端口为21。用户名和密码都是ftpuser。

Step1: 连接FTP服务器：

```bash
telnet 192.168.1.22 21
# 220 (vsFTPd 3.0.3)
```

Step2：输入用户名和密码：

```bash
USER ftpuser
# 331 Please specify the password.
PASS ftpuser
# 230 Login successful.
```

Step3：切换目录 与 查询当前目录

```bash
# cd /
CDUP
# cd ./test
CWD test
# pwd
PWD
```

Step4：删除文件

```bash
DELE hello.txt
```

Step5：上传文件

上传文件时，相对过程比较复杂，我们需要开启两个终端来进行操作。

首先，使用终端1 连接FTP服务器的21端口，并进行用户名和密码登录。

```bash
telnet 192.168.1.22 21
# Trying 192.168.1.22...
# Connected to 192.168.1.22.
# Escape character is '^]'.
# 220 (vsFTPd 3.0.3)
USER ftpuser
# 331 Please specify the password.
PASS ftpuser
# 230 Login successful
```

接下来，需要在终端1中 通过 *PASV* 命令请求FTP 服务器开启另外一个端口等待数据传输。

```bash
PASV
# 227 Entering Passive Mode (192,168,1,22,165,92).
```

可以看到，PASV命令执行后会返回一个包含6个元素的元组。其中前四位表示FTP服务器的IP，后两位组成的时临时端口。

临时端口的计算方式如下：

```bash
165 * 256 + 92 = 42332
```

然后，我们需要使用终端2中使用 `telnet` 命令连接FTP服务器临时申请的端口用于数据传输。

```bash
telnet 192.168.1.22 42332
# Trying 192.168.1.22...
# Connected to 192.168.1.22.
# Escape character is '^]'.
```

在终端1中启动文件写入命令：

```bash
STOR test.txt
# 150 Ok to send data.
```

此时，就可以在终端2中输入响应需要写入的数据了。

```bash
this is test data
missshi
```

当数据写入完成后，在终端1中退出即可。


附录：FTP常用命令

|命令|描述|
|---|----|
| USER \<username\> | 系统登录的用户名 |
| PASS \<password\> | 系统登录密码 | 
| CDUP \<dir path\> | 改变服务器上的父目录 | 
| CWD \<dir path\> | 改变服务器上的工作目录 | 
| PWD | 显示当前工作目录 | 
| HELP \<command\> | 返回指定命令信息 |
| QUIT | 从 FTP 服务器上退出登录 |  
| LIST \<name\> | 如果是文件名列出文件信息，如果是目录则列出文件列表 | 
| DELE \<filename\> | 删除服务器上的指定文件 |
| RMD \<directory\> | 在服务器上删除指定目录 |  
| MKD \<directory\> | 在服务器上建立指定目录 | 
| STOR \<filename\> | 储存（复制）文件到服务器上 | 
| STOU \<filename\> | 储存文件到服务器名称上 | 
| SYST | 返回服务器使用的操作系统 | 
| PASV | 请求服务器等待数据连接 | 
| ABOR | 中断数据连接程序 | 
| ACCT \<account\> | 系统特权帐号 | 
| ALLO \<bytes\> | 为服务器上的文件存储器分配字节 | 
| APPE \<filename\> | 添加文件到服务器同名文件 | 
| MODE \<mode\> | 传输模式（S=流模式，B=块模式，C=压缩模式） | 
| NLST \<directory\> | 列出指定目录内容 | 
| NOOP | 无动作，除了来自服务器上的承认 | 
| REIN | 重新初始化登录状态连接 | 
| REST \<offset\> | 由特定偏移量重启文件传递 | 
| RETR \<filename\> | 从服务器上找回（复制）文件 | 
| RNFR \<old path\> | 对旧路径重命名 | 
| RNTO \<new path\> | 对新路径重命名 | 
| SITE \<params\> | 由服务器提供的站点特殊参数 | 
| SMNT \<pathname\> | 挂载指定文件结构 | 
| STAT \<directory\> | 在当前程序或目录上返回信息 | 
| STRU \<type\> | 数据结构（F=文件，R=记录，P=页面） | 
| TYPE \<data type\> | 数据类型（A=ASCII，E=EBCDIC，I=binary） | 
