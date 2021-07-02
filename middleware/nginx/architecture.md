# 浅谈nginx架构

接下来，在本文中，我们将会和大家浅谈 nginx 的架构和设计。

只有了解了 Nginx 的架构和设计方案，我们才能更好的发挥出 nginx 的优势。

## Nginx 的请求处理流程

首先，我们来了解一下一个请求进入 Nginx 后，整体的处理流程是什么样的。

![architecture1](./picture/architecture1.png)

1. 首先nginx接收到输入流量主要是WEB、EMAIL和TCP流量。
2. 由于 Nginx 本身的机制是非阻塞式的 epoll 进行事件驱动处理，因此，为了能够正常实现异步处理，其内部维护了传输层状态机、HTTP状态机、以及MAIL状态机。
3. 对于一个静态资源下载的请求而言，Nginx会直接访问本地的静态资源并通过sendfile的方式进行返回，再涉及到磁盘IO相关的操作时，Nginx维护了一个线程池用于实现磁盘阻塞调用。
4. 对于一个反向代理请求时，Nginx可以将请求转发给对应的代理服务中。
5. 当请求处理完成后，nginx会打印access访问日志和错误日志。


## Nginx 的进程结构

了解了 Nginx 请求处理的主体流程之后，我们再从进程层面了解一下 nginx 的进程结构。

Nginx 本身支持两种不同的进程结构，分别是单进程结构和多进程结构，其中，单进程结构并不适合生产结构，我们此处不再进行说明。

![architecture2](./picture/architecture2.png)

首先，nginx 有一个统一的父进程: master process，主要用于整体的管理。

其中，该父进程又会包含很多子进程，这些子进程大致可以分为2个大类：

1. worker进程，负责真正的请求处理。
2. cache相关进程，包括 cache manager 和 cache loader，负责缓存的管理和载入。

首先，我们先来了解一下nginx为什么选择多进程而非多线程呢？

我们都知道，对于多线程而言，它们会复用内存空间。而一旦出现内存处理异常时，多线程的服务会全部异常，而多进程则影响会小很多。因此，从可用性的
角度来看，Nginx选择了多进程这样的模式。

此外，为了更好的发挥出 nginx 的能力，我们通过会设置 worker 数量与机器的 CPU 数量一致，同时进行绑核，减少缓存失效等问题。

下面，我们通过一些具体的命令操作来观察一下Nginx中各个进程的关系。

首先，我们启动一个包含2个worker进程的nginx服务。Ps: 修改nginx配置文件中worker_processes为2。

```shell
# (base) root@wangzhe-swarm-dev:/home/wangzhe/nginx# ps -ef|grep nginx
root     23382     1  0 09:15 ?        00:00:00 nginx: master process ./sbin/nginx
nobody   23383 23382  0 09:15 ?        00:00:00 nginx: worker process
nobody   23384 23382  0 09:15 ?        00:00:00 nginx: worker process
nobody   23385 23382  0 09:15 ?        00:00:00 nginx: cache manager process
nobody   23386 23382  0 09:15 ?        00:00:00 nginx: cache loader process
root     23390 24374  0 09:15 pts/1    00:00:00 grep --color=auto nginx
```

可以看到，和我们预期的是一样的，查询到的nginx进程包括:

1. 一个master进程。
2. 两个worker进程。
3. 一个cache manager进程。
4. 一个cache loader进程。
5. 其中，master进程是其他所有进程的父进程。

下面，我们可以执行一个 reload 的操作，然后再观察一下进程的变化情况：

```shell
./sbin/nginx -s reload
ps -ef|grep nginx
```

得到的结果如下:

```shell
# (base) root@wangzhe-swarm-dev:/home/wangzhe/nginx# ps -ef|grep nginx
root     23382     1  0 09:15 ?        00:00:00 nginx: master process ./sbin/nginx
nobody   23832 23382  0 09:18 ?        00:00:00 nginx: worker process
nobody   23833 23382  0 09:18 ?        00:00:00 nginx: worker process
nobody   23834 23382  0 09:18 ?        00:00:00 nginx: cache manager process
root     23985 24374  0 09:19 pts/1    00:00:00 grep --color=auto nginx
```

可以看到，master进程的PID没有发生变化，而其他几个子进程的的PID发生了变化，也就是说明了 worker 和 cache进程等在reload操作时，会被master优雅退出原有进程并重新启动新的进程。

下面，我们可以试试当某个worker进程异常退出时会发生什么呢？

```shell
kill 23833
ps -ef|grep nginx
```

观察结果如下:

```shell
# (base) root@wangzhe-swarm-dev:/home/wangzhe/nginx# ps -ef|grep nginx
root     23382     1  0 09:15 ?        00:00:00 nginx: master process ./sbin/nginx
nobody   23832 23382  0 09:18 ?        00:00:00 nginx: worker process
nobody   23834 23382  0 09:18 ?        00:00:00 nginx: cache manager process
nobody   26401 23382  0 09:23 ?        00:00:00 nginx: worker process
root     26403 24374  0 09:23 pts/1    00:00:00 grep --color=auto nginx
```

虽然，原有的`23833`号进程退出了，但是nginx master很快就有创建出来了一个新的子进程，保证nginx worker的存活数量始终满足配置文件的要求。
