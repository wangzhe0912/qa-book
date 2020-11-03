# 解决Nginx中文乱码问题

解决nginx的中文乱码问题非常简单，只需要在Server块的配置中增加如下一行即可：

```bash
charset utf-8;
```

示例如下：

```
upstream you.domainName.com {
    server 127.0.0.1:8081;
}

server {
    listen      80;
    server_name  you.domainName.com;
    charset utf-8;

    location /examples {
        return 403;
    }
}
```

然后，重启nginx服务即可。
