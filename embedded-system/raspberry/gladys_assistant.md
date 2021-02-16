# 树莓派Gladys Assistant环境搭建

## Gladys Assistant概述

Gladys Assistant是一个开源的智能家居平台。

它是一个刚刚重新设计和开发的智能家居平台。
原生支持 Z-Wave、MQTT 和小米等设备接口，并且在平台中嵌入了自己的 NLP（自然语言处理）对话引擎。
你可以在平台上定义复杂的场景模式。

Gladys Assistant 的主要交互界面是 Web 页面。
不过这些 Web 界面在手机上的体验也非常好，因为它是基于 PWA（Progressive Web App）实现的。
PWA 技术使 Web 应用在手机的体验基本和原生 App 一致。

Gladys Assistant 使用 JavaScript 语言实现的。
它对于树莓派的支持非常不错，提供了基于 Raspbian 的系统镜像。
另外，通过 Docker 的方式对 MacOS 和 Windows 系统也提供了支持。

Gladys Assistant 代码采用的是 Apache License 2.0开源协议。

## Gladys Assistant环境搭建

现在，我们就开始动手，在树莓派上安装Gladys Assistant，
体验一下通过智能家居系统监测设备数值的过程。

### 准备器材

首先我介绍一下需要准备的器材有哪些：

1. 树莓派 Raspberry Pi 4B，要求内存 2GB 以上，但是 8GB 内存版本要谨慎选择，因为有些开源平台软件对 Arm 64bit 芯片支持不够好。
2. 供电电源，要求支持 3A 以上电流。
3. Micro SD 卡，也叫 TF 卡，存储容量最好在 16GB 以上。在选择的时候，你要关注读写速度等级，比如 U3 表示最低写入速度是 30MB/s。同时你也要关注应用性能等级，它定义了 Micro SD 卡进行随机读写的性能，最好是选择 Application Performance Class 2（卡面上标识 A2 图标）。在卡上存储应用程序和应用程序数据时，这个性能指标非常重要。
4. Micro SD 卡读卡器。有些电脑自带这个接口，如果没有的话，你可以买一个便宜的使用。
5. 普通网线。如果你希望以有线的方式使用树莓派，需要准备一根。同时，我也会介绍树莓派接入 Wi-Fi 的方式。

### 烧录系统镜像

树莓派板子在启动的时候，会从 SD 卡读取操作系统镜像文件，完成操作系统的引导启动工作。
所以我们接下来要在 SD 卡上烧录系统镜像。

具体怎么烧录呢？我们可以使用一个免费的烧录工具，Etcher。
它支持 MacOS、Windows 和 Linux 三种主流的电脑系统，
你可以从[官方网站](https://www.balena.io/etcher/) 上下载和安装。
也可以点击这个[链接](https://github.com/balena-io/etcher/releases) 下载最新版。

下载完成后，正常安装Etcher烧录软件即可。

然后，我们需要下载树莓派的系统镜像文件。

树莓派有官方的操作系统镜像 Raspbian 可以选择，但是为了避免手动在 Raspbian 系统中安装 Gladys Assistant 软件的麻烦，我们直接选择官方提供的已经配置好 Gladys Assistant 的 Raspbian 镜像文件。
从这个[链接](https://cdn.elephantcdn.com/gh/gladysassistant/gladys/releases/download/v4.0.0/gladys-4.0.0-rev3.img.zip) 中下载好镜像文件，并且解压缩得到"img"扩展名的文件。

然后把 Micro SD 卡插入读卡器，或者直接插入你的电脑接口中，运行 Etcher 软件，按照步骤把镜像文件烧录到存储卡中。

![etcher](./pictures/Etcher.png)

树莓派支持网线接口，不过，如果你希望树莓派接入家里的 Wi-Fi 热点，而不是使用网线访问网络，那么就需要在 Micro SD 卡中增加一个配置文件。

这个配置文件的文件名必须是 `wpa_supplicant.conf`。

你可以在电脑上使用自己熟悉的文本编辑器创建这个文件，并且在文件中输入下面的内容：

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=CN


network={
 ssid="你的Wi-Fi热点SSID名称"
 psk="你的Wi-Fi热点密码"
 key_mgmt=WPA-PSK
}
```

Ps: 注意，将 Wi-Fi 热点的 SSID 和密码替换为你家里的 Wi-Fi 路由器的真实情况。

然后将这个文件拷贝到 Micro SD 卡的根目录。
这时，你就可以把 Micro SD 卡插入树莓派开发板了。

### 启动系统

烧录好镜像文件，准备好 Micro SD 卡后，你可以把 Micro SD 卡从读卡器取出，插入树莓派的对应接口中。

接着，接上电源线（如果你使用网线方式，记得也将网线接入树莓派板的网口上）。
这时树莓派将自动启动运行，需要等待一段时间。

过一会儿之后，在你的电脑上，打开浏览器，输入 [http://gladys.local](http://gladys.local) 来访问树莓派上的 Gladys Assistant 系统，如下图所示。

![assistant](./pictures/assistant.png)


### 在 Gladys Assistant 上添加设备

因为我们是第一次配置 Gladys Assistant，所以要在上面的页面中选择“Create local account with your Email”，来创建一个本地账号。

创建完账号后，其他的步骤不是必填项，你根据喜好填写就行了。
房屋配置部分，你可以创建一个名称为 bedroom 的房间，后面会用到。

最后，你应该可以看到这个 Dashboard 页面。

![Dashboard](./pictures/dashboard.png)

接下来，我们来添加一个设备，来体验一下 Gladys Assistant 的功能。

首先，我们在 Gladys Assistant 上准备 MQTT Broker。

选择 Dashboard 上部的标签页“Integrations”，点击 MQTT 标签。

![Integrations](./pictures/intergrations.png)

进入 MQTT 设置界面后，你现在需要点击左边的 Setup，开始安装 MQTT Broker。
我们通过默认选项，即使用 Docker 的方式来完成。

![install_mqtt](./pictures/install_mtqq.png)

这个过程需要几分钟时间。

完成后，你就可以看到 MQTT Broker 的用户名和密码。
你也可以修改为你自己需要的密码，这个密码需要记下来，后面模拟MQTT中需要用到。

![set password](./pictures/set_mqtt_pwd.png)

接着，我们点击左边的 Device，切换到 MQTT 设备页面。
点击右上角的 New 打开创建页面。

设备名称我们可以选择 Temperature Sensor，External ID 填写 mqtt:bedroom:temperature-sensor。
字符串中 bedroom 是和下一项房间填写的信息一致的。

![device](./pictures/device.png)

然后，我们为设备添加特性（Features）。这里，我们选择 Temperature 类型。

![feature](./pictures/feature.png)

选择完类型后，我们点击 Add feature，开始设置具体的特性参数。
你可以按照下图的内容来设置自己的参数。
其中，external ID 填写 mqtt:bedroom:temperature-sensor:temperature 字符串。

![add_feature](./pictures/add_feature.png)

最下面的 MQTT Topic，你需要记录下来，后面发送消息时需要用到。

点击下部的保存（Save）和返回（Back），然后我们可以看到创建完成的 MQTT 设备。

![manage](./pictures/manage.png)

在模拟发送 MQTT 消息之前，我们还需要编辑一下 Dashboard 界面。
你需要点击左上角切换回 Home 标签页，然后点击右上角的 Edit 按键。
在编辑界面的 Column 1 选择 Devices in room 类别。
然后依次选择 bedroom 和我们刚创建的设备 Temperature Sensor 传感器。

![dashboard_edit](./pictures/dashboard_edit.png)

点击页面右下角的 Save，保存 Dashboard 的编辑界面。

![dashboard2](./pictures/dashboard2.png)


### 模拟 MQTT 设备

由于，我们在树莓派上通过Docker部署的MQTT仅限于localhost访问，远程其他设备无法正常访问到MQTT。

因此，我们为了能够模拟MQTT设备远程连接到树莓派上面的MQTT服务，我们需要搭建一个nginx来代理MTQQ的端口，并允许远程访问。

Nginx的安装方式参考[如下](../../middleware/nginx/install.md)

Nginx的配置文件如下：

```
worker_processes  1;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       8002;
        server_name  localhost;
        location / {
            root   html;
            index  index.html index.htm;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }

}

stream {
    server {
        listen 1884;
        proxy_pass    mqtt;
    }

    upstream mqtt {
        server 127.0.0.1:1883;
    }
}
```

其核心是最下面的stream块，它表示监听本地1884端口，并将请求转发至本地的1883端口。

最后，我们在本地打开一个终端窗口，输入下面的命令：

```shell
hbmqtt_pub -d --url mqtt://wangzhe:wangzhe@gladys.local:1884 -t gladys/master/device/mqtt:bedroom:temperature-sensor/feature/mqtt:bedroom:temperature-sensor:temperature/state -m 25.2
```

其中:

1. wangzhe:wangzhe 是用户名和密码，它们以分号相连。
2. gladys.local 是树莓派的域名。
3. -t 后面的消息主题就是你刚才记录的 MQTT Topic 字符串。
4. -m 后面是温度数值。

执行这个命令后，你再打开 Gladys Assistant 的 Dashboard 界面，这时你就可以看到设备卡片显示出来了刚才发送的温度数值。

![dashboard3](./pictures/dashboard3.png)
