# 使用Python操作Neo4j数据库 - py2neo

## 概述

和官方提供了 neo4j 库一样，py2neo 也是一个 Python 用于操作 Neo4j 数据库的客户端库。

该库可以直接 bolt 和 HTTP 协议通信方式，还提供了 High Level API 、OGM、管理工具、交互式控制台等功能，整体来说，它的功能会比 neo4j 官方库更加强大和易用。

## 安装

和大部分的 Python 第三方库一样， py2neo 的安装也非常简单，直接使用 pip 包管理工具安装即可:

```sh
pip install py2neo
```

## 快速示例

下面，我们就以一个最简单的示例开始，来演示一下 py2neo 的使用吧。

```python
from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
graph.run("UNWIND range(1, 3) AS n RETURN n, n * n as n_sq")
#    n | n_sq
# -----|------
#    1 |    1
#    2 |    4
#    3 |    9
```

这个例子实在是太简单了，简单到它本质上其实并没有真正与数据库进行增删改查操作。

不过，我们通过这个例子，至少可以知道:

 - py2neo 提供了一个 Graph 类用于连接 neo4j 数据库。
 - Graph 类实例化的对象可以直接用 run 方法来执行 Cypher 语句。

## 常用操作






