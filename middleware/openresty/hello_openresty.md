# Hello OpenResty

在上一节中，我们已经完成了 OpenResty 的环境搭建。

下面，我们来快速体验一下 OpenResty 的使用吧！

## OpenResty 目录结构说明

首先，我们进入 OpenResty 的目录来看一下：

```
-rw-rw-r--  1 work work  22924 Aug  2 13:53 COPYRIGHT
drwxrwxr-x  6 work work   4096 Aug  2 13:53 luajit
drwxrwxr-x  5 work work   4096 Aug  2 13:53 lualib
-rw-rw-r--  1 work work 226376 Aug  2 13:53 resty.index
drwxrwxr-x 47 work work   4096 Aug  2 13:53 pod
drwxrwxr-x  6 work work   4096 Aug  2 13:53 nginx
drwxrwxr-x  5 work work   4096 Aug  2 13:53 site
drwxrwxr-x  2 work work   4096 Aug  2 13:53 bin
```

其中，我们重点来一下如下几个目录：

 - bin: bin目录下包含 OpenResty 中核心的可执行文件和脚本工具等。
 - pod: pod 是 Perl 里面的一种标记语言，用于给 Perl 的模块编写文档。pod 目录中存放的就是 OpenResty、 NGINX、lua-resty-*、LuaJIT 的文档。
 - nginx: Nginx 相关的目录。
 - luajit: LuaJIT 相关的目录。
 - lualib: OpenResty 中使用到的一些 Lua 库。


## Hello OpenResty!

每当我们开始学习一个新的开发语言或者平台，都会从最简单的hello world开始，OpenResty 也不例外。

下面，我们就来使用 OpenResty 提供一个地址返回 Hello OpenResty!

Step1: 修改 Nginx 的配置文件 `/home/work/openresty/nginx/conf/nginx.conf`

```
events {
    worker_connections 1024;
}

http {
    server {
        listen 8000;
        location / {
            content_by_lua '
                ngx.say("hello, OpenResty!")
            ';
        }
    }
}
```

Step2: 启动 Nginx

然后，我们就可以启动 Nginx 服务了：

```sh
./bin/openresty -p `pwd`/nginx -c conf/nginx.conf
```

没有报错的话，OpenResty 的服务就已经成功启动了。你可以打开浏览器，或者使用 curl 命令，来查看结果的返回：

```sh
curl -i 127.0.0.1:8000
# HTTP/1.1 200 OK
# Server: openresty/1.15.8.1
# Date: Mon, 02 Aug 2021 06:28:31 GMT
# Content-Type: text/plain
# Transfer-Encoding: chunked
# Connection: keep-alive
# 
# hello, OpenResty!
```

Step3: 修改配置文件并重启 Nginx

修改配置文件是 OpenResty 的使用场景中的一个高频场景，下面，我们就来看一下如何修改配置文件，并使其生效吧！

修改 `/home/work/openresty/nginx/conf/nginx.conf` 文件如下:

```
events {
    worker_connections 1024;
}

http {
    server {
        listen 8000;
        location / {
            content_by_lua '
                ngx.say("hi, OpenResty!")
            ';
        }
    }
}
```

然后，我们可以执行如下来重启 Nginx:

```sh
./bin/openresty -p `pwd`/nginx -s reload -c conf/nginx.conf
```

重新调用一下接口，看看是否已经发生了变化了呢？

```sh
curl -i 127.0.0.1:8000
# HTTP/1.1 200 OK
# Server: openresty/1.15.8.1
# Date: Mon, 02 Aug 2021 06:33:18 GMT
# Content-Type: text/plain
# Transfer-Encoding: chunked
# Connection: keep-alive
# 
# hi, OpenResty!
```

Step4: 当我们 OpenResty 程序使用完成后，可以通过如下命令来停止 OpenResty 服务:

```sh
./bin/openresty -p `pwd`/nginx -s quit -c conf/nginx.conf
```
