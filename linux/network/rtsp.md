# rtsp协议概述与实战

## 协议概述

RTSP（Real Time Streaming Protocol），RFC2326，中文名称为实时流传输协议，是TCP/IP协议体系中的一个应用层协议。
它由哥伦比亚大学、网景和RealNetworks公司提交的IETF RFC标准。
该协议定义了一对多应用程序如何有效地通过IP网络传送多媒体数据。

RTSP在体系结构上位于RTP和RTCP之上，它使用TCP或UDP完成数据传输。
HTTP与RTSP相比，HTTP请求由客户机发出，服务器作出响应；使用RTSP时，客户机和服务器都可以发出请求，即RTSP可以是双向的。

RTSP是用来控制声音或影像的多媒体串流协议，并允许同时多个串流需求控制，传输时所用的网络通讯协定并不在其定义的范围内，服务器端可以自行选择使用TCP或UDP来传送串流内容，它的语法和运作跟HTTP 1.1类似，但并不特别强调时间同步，所以比较能容忍网络延迟。

而前面提到的允许同时多个串流需求控制（Multicast），除了可以降低服务器端的网络用量，更进而支持多方视讯会议（Video Conference）。
因为与HTTP1.1的运作方式相似，所以代理服务器〈Proxy〉的快取功能〈Cache〉也同样适用于RTSP，并因RTSP具有重新导向功能，可视实际负载情况来转换提供服务的服务器，以避免过大的负载集中于同一服务器而造成延迟。


## Python rtsp协议实战

在下面的实战中，我们使用Python及Python的第三方库rtsp来拉取RTSP的视频流以及相关操作。

Ps：在本实验中，我们使用的Python的版本是Python 3.8。

首先，需要安装Python的第三方库rtsp。

```bash
pip install rtsp==1.1.8
```

接下来，我们来了解几种rtsp最常用的方式：

一、抓取RTSP瞬时截图

```python
import rtsp
client = rtsp.Client(rtsp_server_uri = 'rtsp://192.168.1.202/1')
client.read().show()
client.close()
```

二、抓取RTSP视频流

```python
import rtsp
with rtsp.Client(rtsp_server_uri = 'rtsp://192.168.1.202/1') as client:
    client.preview()
```

三、持续抓取视频帧并处理

```python
import rtsp


def process_image(image):
    """
    # 处理每一帧图像的逻辑
    """
    pass

with rtsp.Client(rtsp_server_uri = 'rtsp://192.168.1.202/1') as client:
    _image = client.read()

    while True:
        process_image(_image)
        _image = client.read(raw=True)
```
