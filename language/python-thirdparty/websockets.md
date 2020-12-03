# Python实战websocket协议

## websocket概述

WebSocket是一种在单个TCP连接上进行全双工通信的协议。WebSocket通信协议于2011年被IETF定为标准RFC 6455，并由RFC7936补充规范。WebSocket API也被W3C定为标准。

WebSocket使得客户端和服务器之间的数据交换变得更加简单，允许服务端主动向客户端推送数据。在WebSocket API中，浏览器和服务器只需要完成一次握手，两者之间就直接可以创建持久性的连接，并进行双向数据传输。

## Python第三方库websocket

websocket是一个Python实现的基于websocket协议的操作lib库。

通过websocket库可以实现websocket的客户端与服务端。

安装方式如下：

```bash
pip3 install websocket
```


## Python Websocket服务端

下面，我们来参考一个基于Python的Websocket服务端实例Demo:

将下列内容保存为`server.py`：

```python
# -*- coding: UTF-8 -*-
"""
# www.missshi.cn
"""
import time
import asyncio
import websockets


async def hello(websocket, path):
    """
    # 定义异步函数
    :param websocket:
    :param path:
    :return:
    """
    print("requests url: %s" % path)
    name = await websocket.recv()
    print("receive message: %s" % name)
    greeting = "Hello %s!" % name

    await websocket.send(greeting)
    while True:
        await websocket.send("what happened")
        print("send message: %s" % greeting)
        time.sleep(1)


# 启动服务
start_server = websockets.serve(hello, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

```

## Python Websocket客户端

将下列内容保存为`client.py`：

```python
# -*- coding: UTF-8 -*-
"""
# www.missshi.cn
"""
import asyncio
import websockets


async def hello():
    """
    # 发送ws消息
    :return:
    """
    uri = "ws://localhost:8765/123"
    async with websockets.connect(uri) as websocket:
        name = "missshi!"
        await websocket.send(name)
        print("send message: %s" % name)

        while True:
            greeting = await websocket.recv()
            print("receive message: %s" % greeting)


asyncio.get_event_loop().run_until_complete(hello())
```

## demo运行

下面，我们第一步首先要启动服务端：

```bash
python3 ./server.py
```

然后，打开另外一个终端，启动客户端：

```bash
python3 ./client.py
```
