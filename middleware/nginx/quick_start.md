# nginx的快速上手

在之前的文章中，我们已经讲解了一些 nginx 的基本概念并且安装了 nginx 的基础环境。

接下来，我们本文中，我们将会带着大家使用nginx完成一些基础的功能，简单的把nginx使用起来。

## 使用nginx搭建一个静态资源WEB服务器

### 基本服务启动

假设，我们在本机的 `/home/wangzhe/nginx/books/` 目录下存在了一系列的静态资源，如index.html文件，jpg文件等。

下面，我们来看一下如何配置nginx，使得可以创建一个静态资源的WEB服务器。

首先，WEB服务器首先是属于http块内部的。

下面，我们来看一下http下的server块内容应该如何编写：

![quick_start1](./picture/quick_start1.png)

我们来解读一下上述配置文件：

 - 首先，我们监听的端口设置为8080.
 - 接下来，我们定义了一个 location 块，直接监听了所有访问 / 根目录的请求，同时，对于所有访问 / 根目录的请求，会将根目录转化为本地 books/ 目录下的文件，并对后缀进行匹配。

下面，我们来启动nginx看一下。

![quick_start2](./picture/quick_start2.png)

赞~现在我们的页面已经可以正常打开了。

### gzip 压缩

打开network选项卡后，你可以发现我们发送请求查询静态资源时，得到的文件大小与真实的文件大小是一致的。

那么，我们有没有什么办法可以对传输的文件进行压缩呢？从而可以有效的节省我们的网络带宽。

对，是有的，就是 gzip 压缩。

下面，我们来继续修改 nginx 配置文件：

![quick_start3](./picture/quick_start3.png)

可以看到，我们在 http 块中加入了一些 gzip 相关的指令：

 - 开启gzip压缩。
 - 设置启用gzip压缩的最小文件大小为1字节。
 - gzip的压缩级别为2。
 - 同时也指定了哪些数据传输类型需要进行gzip压缩。


完成上述配置后，我们重新加载一下nginx的配置来看一下效果，可以看到，我们对于同一个文件，从之前的80多k降低到了13k。

![quick_start4](./picture/quick_start4.png)

### autoindex

下面，我们来看一下如果我们希望将本地的目录结构对外暴露到WEB服务中，使得用的可以根据需要自主选择文件进行进行查询和下载。

在 nginx 中提供了一个 `autoindex` 的模块，参见[文档](https://nginx.org/en/docs/http/ngx_http_autoindex_module.html) 。

`autoindex` 的模块可以在我们访问 `/` 结尾的url时，可以显示该目录的结构信息。

使用方式也非常简单，只需要在 location 块中增加 `autoindex on;` 指令即可。

接下来，我们再次访问一个 books/ 目录下包含的一个目录，例如service/。

![quick_start5](./picture/quick_start5.png)

此时，我们就可以看到该目录下对应的目录结构了。用户也可以自己根据目录进行嵌套查询相关的内容。

### 请求限速

有时，当我们的nginx WEB服务器会被很多用户访问时，为了避免个别请求打满整个带宽，导致其他用户无法正常访问的情况出现，我们可能会需要对单个请求的访问速率进行限制。

此时，需要用到 set 命令配置一些特殊变量来实现相关的功能。

![quick_start6](./picture/quick_start6.png)

在上述命令中，我们设置了 `limit_rate` 变量的值为 5k，表示单个请求的最大下载速率为 5k/s。

关于 `limit_rate` 的文档，可以参考[文档](https://nginx.org/en/docs/http/ngx_http_core_module.html#limit_rate) 。

### 规范日志打印格式

下面，我们来看一下如何设置nginx的日志打印格式。

![quick_start7](./picture/quick_start7.png)

我们在 http 块中通过 log_format 指令来定义了一个 main 名称的 access log 的日志打印格式。

可以看到，我们在日志格式中，引用了大量的nginx内置的特殊变量，例如remote_addr等。

接下来，我们在server块中通过access_log指定设置了对于该server块的access_log存储的位置以及使用的日志打印格式。

![quick_start8](./picture/quick_start8.png)


## 使用nginx搭建一个具备缓存的反向代理服务


## 用GoAccess实现可视化并实时监控access日志

