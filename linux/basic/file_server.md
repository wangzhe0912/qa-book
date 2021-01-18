# 使用Python搭建简单的文件服务器

## 依赖准备

本文主要依赖Python2.7，提前安装Python2.7即可。

## 文件下载服务器

Python2内置了一个SimpleHTTPServer的模块，通过命令行工具，我们就可以快速启动一个HTTP服务器用于文件下载。

```bash
python2 -m SimpleHTTPServer 8000
```

其中，上述命令中的8000表示启动HTTP服务的端口，可以根据你的需要进行修改。

Ps：对于Python3而言，启动命令变为如下：

```bash
python3 -m http.server 8000
```

## 文件上传服务器

对于文件上传，我们推荐一个[Droopy](http://stackp.online.fr/?spm=a2c6h.12873639.0.0.32284b63maAGSs&p=28)的第三方工具。

Droopy是一个简单的用于文件上传的Web服务器。

![droopy](./picture/droopy.png)

droopy本身是一个命令行脚本，下载地址如下：[droopy](http://stackp.online.fr/wp-content/uploads/droopy)

你可以将它下载下来后保存至~/bin/目录下，从而可以直接使用。

启动方式如下：

```bash
mkdir ~/uploads
cd ~/uploads
python ~/bin/droopy -m "Hi, it's me Bob. You can send me a file." -p ~/avatar.png
```

上述命令会启动droopy服务器并占用8000端口。

其中，droopy命令行的使用方式如下：

```bash
Usage: droopy [options] [PORT]

Options:
  -h, --help                            帮助信息
  -d DIRECTORY, --directory DIRECTORY   上传文件的保存目录
  -m MESSAGE, --message MESSAGE         提示消息
  -p PICTURE, --picture PICTURE         提示图片
  --dl                                  提供下载链接
  --save-config                         将参数保存到配置文件
  --delete-config                       删除配置文件并退出
```
