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

### 创建一个节点

```python
from py2neo import Graph, Node
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
node = Node("Book", name="Neo4j权威指南", version="1.1")
graph.create(node)
```

### 根据属性查询一个节点

```python
from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
node = graph.nodes.match("Book", name="Neo4j权威指南").first()
```

### 根据节点ID查询节点信息

```python
from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
node = graph.nodes.get(38)
print(dict(node))  # 将节点属性转为dict格式
```

### 查询属性全部匹配的节点

```python
from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
node = graph.nodes.match("Book", name="Neo4j权威指南").all()
```

### 根据关系查询关系

```python
from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
node = graph.nodes.get(38)
current_subtopo_relations = graph.match((node,), r_type="write").all()
for relation in current_subtopo_relations:
    print(relation, relation.end_node)
```

### 创建两个节点并添加对应的关系

```python
from py2neo import Graph, Node, Relationship
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
node1 = Node("Book", name="Neo4j权威指南", version="1.1")
node2 = Node("Person", name="张帜", gender="man")
relation = Relationship(node1, "write", node2)
graph.create(relation)
```

### 修改一个节点的属性

```python
from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
node = graph.nodes.get(38)
node["age"] = 53
graph.push(node)
```

### 删除节点

```python
from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
node = graph.nodes.get(38)
graph.delete(node)
```

### 删除关系

```python
from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
node = graph.nodes.get(38)
current_subtopo_relations = graph.match((node,), r_type="write").all()
for relation in current_subtopo_relations:
    graph.separate(relation)   # 仅删除关系
```

### 执行 Cypher 语句

```python
from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
cypher = 'MATCH (resource:Book {name: "Neo4j权威指南"})<-[write]-(:Person) RETURN resource'
data = graph.run(cypher).data()
for item in data:
    print(item["resource"])
```

### 事务性操作

```python
from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
tx = graph.begin()
try:
    node = graph.nodes.get(38)
    graph.delete(node)
    tx.commit()
except Exception as e:
    tx.rollback()
    raise Exception(e)
```
