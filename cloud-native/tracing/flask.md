# 基于Python Flask框架的http headers透传

在本文中，我们将会介绍在 Flask HTTP 框架中，如何能够简单快速的实现 headers 的透传方案。


## 原理分析

对于任何一个微服务而言，想要实现 headers 的透传的话，也是主要分三步：

 - 接收 HTTP 请求时，从请求中读取中 headers 信息。
 - 将 headers 在程序内部进行保存和传播。
 - 发送 HTTP 请求时，将内部传播的 headers 在客户端请求加入并发送出去。

此外，为了避免在各个请求接收和请求发送中，都需要进行相关的改动，我们在程序实现中应该按照 AOP 的思想，一次改动全场生效。

### 请求读取

首先，在 flask 框架中，可以通过如下方式获取请求的 headers 信息：

```python
from flask import request

request_headers = request.headers
```

### 请求内部传播

在 Flask 框架中，HTTP Server 都是一个 Request 只由一个线程处理。

所以，我们可以将 HTTP 请求 headers 信息存储在一个 Thread Local 中，然后在该线程中，需要使用时可以从中提取。

幸运的是，flask 框架中的 `request.headers` 本身已经帮助我们完成了对应的工作。
因此，我们不再需要自己重复在内部进行传播了，而是可以在使用时直接在 `request.headers` 中使用了。

### 请求发送

对于 Python 而言，对外的 HTTP 请求发送主要是通过 `requests` 库来实现的。

因此，我们可以直接从全局来修改 `requests` 库的逻辑，优先从 `request.headers` 中读取 headers 信息，然后追加至请求的 header 中。

## 实战

具体代码可以参考如下 [repo](https://github.com/qa-tools-famliy/header-tracing/tree/main/flask) 。

具体来说，使用起来也非常简单，只需要引入一个 `instrument` 函数，并调用该函数即可实现 AOP 的注入。

```python
from request_wrapper import instrument

instrument()
```

此外，另外一种相关的实现也可以参考 [Flask+requests headers 透传](https://github.com/AminoApps/context-propagation-python) 。
