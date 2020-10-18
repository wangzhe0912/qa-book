# 在Python中使用ETCD

在本文中，我们将会学习如何在Python中快速的使用ETCD进行数据读写等相关操作。

## 安装

在Python中使用etcd时，我们首先需要安装`etcd`第三方库。

```bash
pip install python-etcd==0.4.5
```

## 快速入门

在下面的内容中，我们将会讲述Python的ETCD库的一些标准使用方式，了解这些方式可以帮助你快速入门在Python中使用ETCD。

### 创建一个Client对象

```python
import etcd

# 几种初始化客户端的方式
# 单实例连接
client = etcd.Client(host='127.0.0.1', port=4003)
# 多实例连接
client = etcd.Client(host=(('127.0.0.1', 4001), ('127.0.0.1', 4002), ('127.0.0.1', 4003)))
# https://example.com
client = etcd.Client(srv_domain='example.com', protocol="https")
# https://api.example.com:443/etcd
client = etcd.Client(host='api.example.com', protocol='https', port=443, version_prefix='/etcd')
```

### 写入一个key

```python
client.write('/nodes/n1', 1)
# with ttl
client.write('/nodes/n2', 2, ttl=4)  # 4s后过期
```

### 读取一个key

```python
client.read('/nodes/n2').value
client.read('/nodes', recursive = True).children # 递归获取该目录下的所有key-value数据

# 读取一个不存在的key时会抛出异常
try:
    client.read('/invalid/path')
except etcd.EtcdKeyNotFound:
    print "error"
```

### 删除一个Key

```python
client.delete('/nodes/n1')
```

### 监听一个key

```python
client.read('/nodes/n1', wait=True) # wait直到该key变化，返回变化信息
client.read('/nodes/n1', wait=True, timeout=30) # wait直到该key变化或超时，返回变化信息或抛出超时异常
client.read('/nodes/n1', wait=True, recursive=True) # wait直到该key或子key变化，返回变化信息
```

### 刷新ttl过期时间

```python
client.write('/nodes/n1', 'value', ttl=30)  # 设置过期时间为30s
client.refresh('/nodes/n1', ttl=600)        # 修改过期时间为600s
```

### etcd用户分布式锁

```python
client = etcd.Client()
# Or you can custom lock prefix, default is '/_locks/' if you are using HEAD
client = etcd.Client(lock_prefix='/my_etcd_root/_locks')
lock = etcd.Lock(client, 'my_lock_name')

# Use the lock object:
lock.acquire(blocking=True, # will block until the lock is acquired
      lock_ttl=None) # lock will live until we release it
lock.is_acquired  # True
lock.acquire(lock_ttl=60) # renew a lock
lock.release() # release an existing lock
lock.is_acquired  # False

# The lock object may also be used as a context manager:
client = etcd.Client()
with etcd.Lock(client, 'customer1') as my_lock:
    do_stuff()
    my_lock.is_acquired  # True
    my_lock.acquire(lock_ttl=60)
my_lock.is_acquired  # False
```

### 获取集群中的机器列表

```python
client.machines
```

### 获取集群中的leader节点

```python
client.leader
```
