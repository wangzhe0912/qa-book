# Nginx HTTP模块详解

在本文中，我们将会以 Nginx 请求处理流程的方式，将 HTTP 模块相关的使用方法进行分析和讲解。

## Nginx 请求事件处理流程

在介绍 Nginx 的 各个 HTTP 模块功能之前，我们需要先来了解一下 Nginx 对于一个请求事件而言，其通用的处理流程是怎么样的。

![http1](./picture/http1.png)

首先，如果有访问Nginx的服务，首先是会与Linux内核进行一次TCP的三次握手。

当三次握手成功之后，会转给 nginx 的事件管理模块去建立一个连接，此时 nginx 需要对齐分配对应的连接内存池，同时，此时 Nginx 的 HTTP 模块会
对齐设置一个 header 读取的超时时间。

接下来，就是等待客户端继续发送请求的 header 信息了，当客户端发送 header 信息后，nginx 的HTTP模块会继续申请读缓冲区内存，用于接收
客户端发送的 header 信息。

![http2](./picture/http2.png)

后续的 header 接收与处理逻辑如上图所示。

其中，开启 11 个阶段的 http 请求处理之前的所有逻辑，都是 nginx 服务本身内置的 http 相关的逻辑，而用户可以开发插入的逻辑都集中在
11个阶段中。

那么，nginx HTTP 处理请求的 11 个阶段又是什么样的呢？

我们先来看一个大致的示意图：

![http3](./picture/http3.png)

 - 首先，对于一个请求而言，我们首先会读取请求的 header 信息，如上述流程所示。
 - 接下来，会根据 header 信息来判断它属于哪一个配置块，找出对应的配置信息。
 - 然后判断是否属于限速、限并发等流量控制策略限定域中。
 - 接下来，会有鉴权相关的访问控制处理。
 - 当确认该请求可以正常进行后，需要生成对应的响应体，其中，对于反向代理场景而言，需要访问上游服务获取对应的响应体。
 - 在返回具体的响应体之前呢，还可以对响应信息再次进行处理，如gzip压缩等。
 - 最后，当上述步骤都处理完成后，先记录access log，并将结果返回给请求客户端。


下面，我们来具体看一下，对于Nginx HTTP请求处理而言，具体包含哪些阶段:

|阶段序号|阶段名称|示例模块|
|------|------|-------|
|1|POST READ|realip|
|2|SERVER_REWRITE|rewrite|
|3|FIND_CONFIG|
|4|REWRITE|rewrite|
|5|POST_REWRITE|
|6|PREACCESS|limit_conn, limit_req|
|7|ACCESS|auth_basic,access,auth_request|
|8|POST_ACCESS|
|9|PRECONTENT|try_files|
|10|CONTENT|index,auto_index,concat|
|11|LOG|access_log|


转换成一张图的话，基本如下图所示：

![http4](./picture/http4.png)

## 指令与配置块

在正式进入 http 各个模块与指令讲解之前，我们还需要先来了解一下 nginx 中关于配置块和指令的一些基本概念。

对于一个 nginx 指令而言，都有有其对应的上下文的约束，具体来说，就是限制该指令可以出现在什么位置上，例如可以出现在哪些配置块中。
这个上下文约束，我们称之为对应的 context 。

当然，对于一些指令而言，其本身可以在多个不同的配置块中出现，即其 context 可以是多种不同的配置块。

那么，对于一个指令而言，如果它同时出现在了多个不同的配置块中，且指定设置的结果不一致时，这时最终哪个指令配置的结果会生效呢？

这时，基本可以主要分为两种类型：

 - 对于设置配置项值的指令，例如 root, access_log 等，它们可以对配置项进行合并，合并的规则是子配置存在时，直接覆盖父配置，子配置不存在时，继承父配置。
 - 对于设置动作行为类的指令，例如 rewrite, proxy_pass 等，通过无法对其合并，而是在生效结果直接执行。通常，对于动作类指令，主要在 server_rewrite, rewrite, content阶段生效。


## 正则表达式

正则表达式在 nginx 中可以说是得到了相关广泛的应用，因此在正式进入 nginx http 模块学习之前，我们还需要先来了解一下Nginx 中的正则表达式。

Nginx 中的正则表达式中支持的元字符如下表所示：

|代码|说明|
|---|----|
|.|匹配除换行符之外的任意字符|
|\w|匹配字母/数字/下划线/汉字|
|\s|匹配任意空白符|
|\d|匹配数字|
|\b|匹配单词的开始和结束|
|^|匹配行开头|
|$|匹配行结尾|


此外，除了单个字符的匹配之外，还有用于重复的正则字符串的表达方式:

|代码|说明|
|---|----|
|*|重复零次或更多次|
|+|重复一次或更多次|
|?|重复零次或一次|
|{n}|重复n次
|{n,}|重复n次或更多次|
|{n,m}|重复n到m次|


通过正则表达式，我们可以在 location, server_name, rewrite 中取得极大的便利。

## listen 指令

前面聊了这么多的基础知识，下面，我们就可以开始正式了解一些 nginx http 模块中的指令了。

`listen` 指令可以说是 server 块中最最基础的指令了，用于设置在本地监听哪些端口用于接收请求。

`listen` 指令仅允许出现在 `server` 块这个 context 中。


常用的基本语法如下:

```shell
listen address[:port];
listen port;
listen unix:path;
```

例如:

```shell
listen 8000;   # 监听所有网卡的8000端口
listen 127.0.0.1:8001;   # 监听localhost的8001端口
listen unix:/var/run/nginx.sock;  # 监听指定socket文件，仅限于本机通讯
```

## server_name 指令

在 Nginx 配置中，`server_name` 也是一个非常重要的指令，通过 server_name 可以帮助我们找到指定请求对应生效的配置块。

说到这儿你可能就会有一些奇怪了，我们刚才已经讲到了 listen 指令，通过 listen 指令指定的端口不是已经就可以帮助我们找到对应的配置块了嘛？
为什么还需要 server_name 这么一个东西呢？

说起来也简单，由于 Nginx 往往是会作为我们整个网关的一个流量入口，该流量入口上常常可能会绑定多个域名，这时，我们希望多个域名对应的
服务都能够以80，或443这种常用端口来对外提供服务，而nginx可以跟进客户端请求的域名不同，来自动识别到不同的配置块上。

简单的来说，server_name 本身上就是可以根据客户端HTTP请求中header中的HOST信息与server_name进行匹配，找到对应的配置块。

server_name 可以出现的 context 为 http, server 以及 location 中。

其基本的语法格式为:

```shell
server_name www.missshi.cn;  # 精准匹配
server_name *.missshi.cn;    # 泛域名，* 仅支持在最前或最后
server_nane ~^www\d+\.missshi\.cn$;  # ~开头，正则表达式
```

此外，在 server_name 的正则表达式中，我们还可以用小括号来创建变量，并在其余位置使用：

```shell
server {
  server_name ~^(www\.)?(.+)$;
  location / {
    root/sites/$2;
  }
}
```

其中，我们在 location 中就使用了 $2 来表示 server_name 中匹配的域名。

或者是:

```shell
server {
  server_name ~^(www\.)?(?<domain>.+)$;
  location / {
    root/sites/$domain;
  }
}
```

那么，在多个 Server 块都监听了相同的端口，且 server_name 设置不一致但都可能匹配的情况下，会如何进行优先匹配呢？

1. 精准匹配。
2. *在前的泛域名
3. *在后的泛域名
4. 按照文件中顺序匹配正则表达式域名
5. 全部不匹配时，如果有server块被设置为default，则匹配default块。
6. 全部不匹配时，且没有default块时，默认匹配第一个。


## realip 模块






## rewrite 模块下的 return 指令




## rewrite 模块下的 rewrite 指令



## rewrite 模块下的 if 指令



## find_config 阶段找到对应 location 块 - location 指令



## preaccess 阶段下的 limit_conn 模块



## preaccess 阶段下的 limit_req 模块



## access 阶段下的 access 模块



## access 阶段下的 auth_basic 模块 








