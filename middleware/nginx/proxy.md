# Nginx 反向代理详解

在本文中，我们将会详细介绍一下在 Nginx 中，反向代理与负载均衡是如何实现和使用的。

## HTTP 反向代理流程主体

首先，我们来看一下在 Nginx 中，对于一个 HTTP 反向代理的场景而言，它的完整处理流程是什么样的。

![proxy1](./picture/proxy1.png)

可以看到:

 - HTTP 反向代理的工作是从 content 阶段开始的。
 - 首先会判断是否命中了之前的 cache, 如果命中则直接返回，否则继续。
 - 然后根据相关指令和接收到的 header 来生成发往上游的 http 头部。
 - 读取客户端发送的包体信息。
 - 根据负载均衡策略选择对应的上游服务器。
 - 根据参数连接上游服务器。
 - 向上游服务器发送请求。
 - 接收上游服务器响应的头部。
 - 处理上游服务器的响应头部。
 - 接收上游服务器的响应体。
 - 发送给客户端响应头部。
 - 发送给客户端响应体。
 - 如果开启了cache，则将响应信息写入cache。
 - 关闭或复用连接，结束本次反向代理请求任务。

了解了一次 HTTP 反向代理的主体流程之后，下面，我们将根据主体流程的步骤，来依次说明每个步骤中，Nginx 的相关指令与功能。

## HTTP 协议的反向代理 - proxy 模块

我们首先要来了解的第一个模块就是 proxy 模块了。

proxy 模块是 Nginx 中用于对上游服务进行 http/https 协议进行反向代理的核心模块。

### 指定上游服务地址

proxy 模块中，包含了一个 **proxy_pass** 指令，这个也是反向代理的入口指令，用于设置对应的上游服务的地址。

**proxy_pass**

 - 功能描述: 指定反向代理的上游服务地址。
 - 语法格式: `proxy_pass URL;`'
 - Context: location

可以看到，看起来 proxy_pass 模块仅仅接收一个 URL 参数，比较简单，但是其实 URL 参数本身有着一些规则，使用中需要非常注意，下面我们来了解一下：

 - URL 必须以 `http://` 或者 `https://` 开头，后面接域名、IP、unix socket地址或者upstream名称，最后是一个可选的 URI。
 - URL 中是否携带 URI 会导致对上游请求转发的行为完全不同，具体来说：
    - 当不携带 URI 时，客户端请求中的URL会直接转发给上游，里面location中使用了正则表达式，@名字时，一般采用该方式。
    - 当携带 URI 时，客户端请求中的URL会将location参数中匹配的部分替换为 proxy_paas 中携带的 URI 内容。
 - URL参数中，也可以携带?+变量。


了解完反向代理的入口指令后，我们接下来继续了解一下 Nginx 在 HTTP 反向代理中是如何生成向上游服务器发送的 http 头部和包体的。

Ps: 由于 cache 部分相对独立，我们后续统一进行说明。

HTTP 反向代理中生成发往上游的请求其实主要包含三个部分：

 - 请求行
 - 请求头部
 - 请求体

下面，我们来依次进行说明：

### 生成请求行

HTTP 反向代理中，生成发往上游服务请求行中，主要包含如下两个指令:

**proxy_method**

 - 功能描述: 设置/修改 HTTP 反向代理发往上游请求的请求方法。
 - 语法格式: `proxy_method method;`'
 - Context: http, server, location

在生成发往上游服务请求行时，默认会使用客户端发往 nginx 的请求方法，但是你也可以通过 `proxy_method` 指令进行修改。

**proxy_http_version**

 - 功能描述: 设置/修改 HTTP 反向代理发往上游请求的HTTP协议版本。
 - 语法格式: `proxy_http_version 1.0|1.1;`'
 - 默认值: 1.0 
 - Context: http, server, location

在生成发往上游服务请求行时，默认会使用HTTP 1.0协议与上游服务进行通信，可以手动调整为HTTP 1.1。


### 生成请求头部

下面，我们来看一下 HTTP 反向代理中如何生成向上游服务发送的 HTTP 请求头部。

**proxy_set_header**

 - 功能描述: 设置/修改 HTTP 反向代理发往上游请求头部的指定字段。
 - 语法格式: `proxy_set_header field value;`'
 - 默认值: 
    - Host: $proxy_host;
    - Connection close;
 - Context: http, server, location

Ps: 在上述 `proxy_set_header` 命令中，如果指令的 value 为空字符串，那么，对应的key-value其实都不会发送。

**proxy_pass_request_headers**

 - 功能描述: 设置 HTTP 反向代理发往上游请求头部时是否将客户端发送过来的头部全部带过去。
 - 语法格式: `proxy_pass_request_headers on|off;`'
 - 默认值: on
 - Context: http, server, location

默认情况下，客户端发送给 Nginx 的请求头部，Nginx 会全部直接转发给上游业务服务。

### 生成发往上游的包体

接下来，我们来看一下 HTTP 反向代理中如何生成向上游服务发送的 HTTP 请求体。

**proxy_pass_request_body**

 - 功能描述: 设置 HTTP 反向代理发往上游请求包体时是否将客户端发送过来的包体全部带过去。
 - 语法格式: `proxy_pass_request_body on|off;`'
 - 默认值: on
 - Context: http, server, location

默认情况下，客户端发送给 Nginx 的请求包体，Nginx 会全部直接转发给上游业务服务。

**proxy_set_body**

 - 功能描述: 手动设置 HTTP 反向代理发往上游的请求包体。
 - 语法格式: `proxy_set_body value;`'
 - Context: http, server, location

除了直接转发客户端发送过来的请求体之外，Nginx HTTP 反向代理中，也允许自定义请求包体发送给上游业务服务。

### 客户端的包体接收方法

从之前的 HTTP 反向代理逻辑图中，我们其实可以看到，在 Nginx 处理客户端发送过来的包体时，有两种不同的处理方式。

 - 方案一: 先将客户端发送过来的请求包体全部接收下来，然后在与上游服务器建立连接统一发送。
 - 方案二: 先与上游服务器建立连接，然后在一边接收客户端的请求，一边发送给上游服务器。

这两种方式在 Nginx 的反向代理服务器中，可以说是各有优劣，下面，我们来展开说明：

对于方案一而言，比较适合于客户端网速较慢，服务端网速很快且服务端并并发连接数比较敏感的场景，在该场景下，由于 Nginx 会完整接收到客户端
的包体后再将服务端发送请求，所以可以有效的避免服务端的连接浪费，降低服务端的压力。

而对于方案二而言，可以更加及时的将请求信息发送给服务端，无需等待Nginx完全接收完客户端的请求，同时对于Nginx自身而言，可以有效降低nginx读写
磁盘的消耗（因为在方式一中，如果包体较大的话，nginx会先讲包体写入一个临时文件，然后时再从临时文件中读取）。

具体选择哪个方案，这个其实是需要从业务的角度来进行考虑的。

那么，在 nginx 中，又是如何配置该方案呢？下面，我们来讲解 **proxy_request_buffering** 指令：

**proxy_request_buffering**

 - 功能描述: 设置 HTTP 反向代理时，接收客户端包体和发送服务端包体的先后依赖关系。
 - 语法格式: `proxy_request_buffering on|off;`'
 - 默认值: on
 - Context: http, server, location

也就是说，默认情况下，Nginx 会先将客户端发送过来的包体接收完成，然后再与上游服务端建立连接并发送包体。

那么，我们下面来看一下具体Nginx是怎么接收客户端包体信息的。

首先，Nginx 在接收客户端发送头部信息的时候，可能会当头部信息传输完成后，顺带传递部分包体信息进来，此时将会出现如下一些情况：

 - 接收头部时，顺带已经将包体全部接收了，此时，针对包体的接收，则无需再做任何操作，已经接收完成了，否则如下。
 - 根据头部中说明的包体的大小，计算待剩余接收的包体大小，此时，如果剩余包体并不算太大时（小于client_body_buffer_size），直接分配对应内存接收body。
 - 如果剩余的包体很大时，那么，我们会将body信息写入临时文件来进行保存，然后发送请求时，再从临时文件中读取。

通过上述的描述，我们知道在这一个过程中，有一个阈值对包体的接收非常重要，即 client_body_buffer_size 。

下面，我们来看一下如何配置 client_body_buffer_size：

**client_body_buffer_size**

 - 功能描述: 设置 HTTP 反向代理时，使用内存接收包体的大小限制。
 - 语法格式: `client_body_buffer_size size;`'
 - 默认值: 8k|16k
 - Context: http, server, location

此外，在接收包体的配置中，还有一个参数也比较重要，就是 **client_body_in_single_buffer** :

**client_body_in_single_buffer**

 - 功能描述: 设置 HTTP 反向代理时，接收客户端包体时，设置是否在单一buffer块中保存包体。
 - 语法格式: `client_body_in_single_buffer on|off;`'
 - 默认值: off
 - Context: http, server, location

如果我们在 nginx 的配置中，频繁使用了 `request_body` 变量的话，那么建议开启该配置，直接可以避免频繁的内存拷贝操作。

在接收客户端包体信息中，我们还可以设置客户端发送包体的最大长度：

**client_max_body_size**

 - 功能描述: 设置 HTTP 反向代理时，设置接收客户端包体的最大长度。
 - 语法格式: `client_max_body_size size;`'
 - 默认值: 1m
 - Context: http, server, location

Nginx 中，会对请求头部中的 Content-Length 进行判断，如果超出我们设置的最大长度时，会直接返回 413 错误。

除了最大长度之外，我们还可以设置接收包体的超时时间:

**client_body_timeout**

 - 功能描述: 设置 HTTP 反向代理时，设置接收客户端接收包体时包体发送的数据间隔超时时间。
 - 语法格式: `client_body_timeout time;`'
 - 默认值: 60s
 - Context: http, server, location

之前，我们已经提到了当客户端发送的包体大小超过我们设置的阈值时，nginx 会先讲包体的内容保存在一个临时文件中，那么，具体关于临时文件保存，
有如下两个配置：

**client_body_temp_path**

 - 功能描述: 设置 HTTP 反向代理时，接收客户端包体后，如果需要保存临时文件时，临时文件所在的路径。
 - 语法格式: `client_body_temp_path path;`'
 - 默认值: client_body_temp
 - Context: http, server, location

**client_body_in_file_only**

 - 功能描述: 设置 HTTP 反向代理时，接收客户端包体后，是否需要保存在临时文件中。
 - 语法格式: `client_body_in_file_only on||clean|off;`'
 - 默认值: off
 - Context: http, server, location

其中：

 - on: 表示针对每个请求，都创建一个临时文件保存包体，并且保留临时文件不删除，主要用于debug等场景。
 - clean: 表示针对每个请求，都创建一个临时文件保存包体，但请求完成后，删除对应临时文件。
 - off: 按需创建临时文件，临时文件用完后自动删除。

