# cypher概述及基本语法

## Cypher 概述

Cypher 是一种声明式的图数据库查询语言，具有丰富的表现力，能够高效的查询和更新图数据。

Cypher 借鉴了 SQL 语言的结构，可以组合各种语句来实现相关的功能。

最常用的语句包括：

 - MATCH: 匹配图模式，Cypher 中最核心的语句。
 - WHERE: 添加额外的约束条件。
 - RETURN: 定义返回的结果。


一个简单的示例如下:

```
MATCH (john {name: 'John'})-[:friend]->()-[:friend]->(fof)
RETURN john.name, fof.name
```

上述语句的含义是找出 John 的朋友的朋友列表。

此外，我们还可以引入 WHERE 语句进行一些过滤:

```
MATCH (user)-[:friend]->(follower)
WHERE user.name IN ['Joe', 'John'] AND follower.name =~ 'S.*'
RETURN user.name, follower.name
```

Cypher 语句的含义非常直观，甚至对于一个完全没有接触过 Cypher 的同学，基本都可以直接了解到该数据的功能。

上述介绍的几个语句主要是用于数据查询相关，而对于数据修改而言，常用的语句包括:

 - CREATE/DELETE: 创建/删除节点和关系。
 - SET/REMOVE: 使用SET设置属性值和标签，使用REMOVE移除属性值和标签。
 - MERGE: 匹配已经存在的或者创建新的节点和模式，这对于有唯一性约束的时候非常有效。

关于这些语句的具体使用，我们将会在 [下一篇文章](./cypher_language.md) 中进行深入的讲解。

## Cypher 模式

Cypyer 查询语句非常依赖于模式。
模式可以非常简单，例如某个人 LIVE_IN 某个城市；也可以非常复杂，例如多个模式可以组装在一起。

而 Cypyer 最大的魅力就在于其模式的语言表达能力。

在图数据库中包括两种对象，分别是 "节点" 和 "关系" 。

其中，在 Cypher 语法中，节点使用一对圆括号来表示:

```
()   # 匿名节点
(matrix)  # 命名节点，matrix 变量可在后续语句中引用
(:Movie)  # 指定节点标签为Movie的匿名节点
(matrix:Movie)   # 指定节点标签为Movie的命名节点
(matrix:Movie {title: "The Matrix"})   # 指定节点标签和属性的命名节点
(matrix:Movie {title: "The Matrix", released: 1997})   # # 指定节点标签和多个属性的命名节点
```

从上述示例中可以看出，除了用一对圆括号来表示一个节点之外，我们还可以知道:

 - 使用 `:XXX` 来指定节点类型。
 - 使用 `{key: value}` 来指定节点属性。

此外，在 Cypher 语法中，关系使用一对短横线（--）来表示，有向关系使用（-->或<--）来表示，示例如下：

```
-->   # 匿名关系
-[role]->   # 命名关系
-[:ACTED_IN]-> # 指定类型的匿名关系
-[role:ACTED_IN {roles: ["Neo"]}]-> # 指定类型、属性的命名关系
```

Ps: 需要注意的是，关系的属性值可以是数组。

当我们了解了如何表示节点和关系后，我们就可以组合它们来实现一些模式了，例如:

```
(tom:Person:Actor {name:"Tom"})-[role:ACTED_IN {roles:["Neo"]}]->(matrix:Movie {title: "The Matrix"})
```

此外，我们还可以将一个模式赋值给一个变量，例如:

```
acted_in = (:Person)-[:ACTED_IN]->(:Moive)
```

## Cypher 查询和更新数据

了解了 Cypher 的模式之后，我们再来看一下如何使用 Cypher 来查询和更新数据。

### 查询数据

Cypher 查询数据非常简单，只需要使用 MATCH 语句结合上述的模式表达式即可，例如:

```
MATCH (person:Person)-[:ACTED_IN]->(:Moive)
RETURN person
```

另外，我们还可以用 WITH 语句将多个查询语句连接在一起:

```
MATCH (person:Person)-[:ACTED_IN]->(moive:Moive)
WITH person, count(movie) AS movieCount
WHERE movieCount > 3
RETURN person, movieCount
```

### 更新数据

使用 Cypher 更新数据时，常常用到 SET 等语句。

```
MATCH (person:Person)-[:ACTED_IN]->(moive:Moive)
WITH person, count(movie) AS movieCount
SET person.movieCount = movieCount
RETURN person, movieCount
```

上述命令中，我们将 Person 参演的电影数量作为属性值设置给了 Person 节点。

## Cypher 事务

Cypher 支持事务的功能，可以保证一个事务内的操作要么全部成功、要么全部失败。

当一个 Cypher 语句本身没有在一个事务的上下文中时，则该 Cypher 语句会作为一个独立的事务执行。

而当一个 Cypher 语句已经在某个上下文中时，整个过程就会基于已有的上下文进行操作，直到整个事务成功提交之后，才会持久化至磁盘中。

## Cypher 的唯一性

Cypher 在进行模式匹配时，会保证单个模式中不会多次匹配到同一个图对象。

以一个示例为例:

```
MATCH (a:Person)-[:friend]-()-[:Friend]-(b:Person)
RETURN a, b
```

上述是一个无方向的模式，也就是说，a 的朋友的朋友理论上应该有可能是自己。

但是在 Cypher 的唯一性约束下，同一个模式中，不会多次匹配到同一个对象，因此，此时不会将a和b匹配到同一个人上。

那如果我们的确有这种需求时，应该怎么办呢？也非常简单，直接把它们拆分到多个模式中即可，例如:

```
MATCH (a:Person)-[:friend]-(friend)
MATCH (friend)-[:Friend]-(b:Person)
RETURN a, b
```

此时，由于a和b已经不在同一个模式中，因此，二者可能会表示同一个节点。

## Cypher 基本语法

### Cypher 类型

Cypher 中所有处理的值都属于一个特定的类型，Cypher 支持的类型包括:

 - 数值型
 - 字符串型
 - 布尔型
 - 节点
 - 关系
 - 路径
 - MAP
 - LIST

### Cypher 表达式

在 Cypher 中，包含的表达式有:

 - 十进制数字: 13，3.14
 - 十六进制数字: 0x12
 - 八进制数字: 013
 - 字符串: "Hi", 'Hello'
 - 布尔值: true, false, TRUE, FALSE
 - 变量: x, name
 - 属性: x.name
 - 动态属性: x["name"]
 - 参数: $param, $0
 - 列表: ['a', 'b']
 - 函数调用: length(p)
 - 聚合函数: avg(x.prop), count(*)
 - 模式: (a)-->(b)
 - 计算式: 1 + 2 and 3 < 4
 - 断言表达式: a.prop = "hello" 或 exists(a.name)
 - 正则表达式: a.name =~ 'Tob.*'
 - 字符串匹配: a.username STARTS WITH 'wang'
 - CASE 表达式

其中，我们来简单聊一下 CASE 表达式，CASE 表达式给 Cypher 提供了一种逻辑判断的能力，使用效果和通常编程语言中的 if-else 类似。

例如:

```
CASE a.name
WHEN "wangzhe" THEN "admin"
WHEN "rongsong" THEN "user"
ELSE "invalid"
END
```

也可以扩展为如下格式:

```
WHEN a.name = "wangzhe" THEN "admin"
WHEN a.name = "rongsong" THEN "user"
ELSE "invalid"
END
```

该方式显得更加灵活，也与 if 语法更加类似。

一个完整是示例如下:

```
MATCH (n)
RETURN
    WHEN n.eyes = "blue" THEN 1
    WHEN n.eyes = "brown" THEN 2
    ELSE 3
    END
AS result
```

### Cypher 变量

在 Cypher 中的变量是区分大小写的，可以包含字母、数字、下划线，但必须是字母开头。

### Cypher 参数

Cypher 支持带参数的查询，也就意味着开发任务无需拼接字符串来查询，也可以使后续讲的执行计划更容易缓存。

需要注意的是，参数不能用于属性名，关系类型和标签。

参数名称是字母和数字的组合。

参数:

```json
{
  "name": "John"
}
```

查询语句:

```
MATCH (n {name: $name})
RETURN n
```

创建带有属性的节点:

参数:

```json
{
  "props": {
    "name": "Wangzhe",
    "age": 30
  }
}
```

语句：

```
CREATE (n:Person)
SET n = $props
RETURN n
```

### Cypher 运算符

Cypher 支持的运算符包括:

 - 数学运算符: +, -, *, /, %, ^
 - 比较运算符: =, <>, >, <, <=, >=, IS NULL, IS NOT NULL
 - 布尔运算符: AND, OR, XOR, NOT
 - 字符串运算符: +, =~
 - 列表运算符: +, IN

### Cypher 注释

在 Cypher 中，使用 // 进行『行』注释。

### 模式

在上面的内容中，我们已经提到了，在 Cypher 中，节点用 () 来表示，关系有 -- 来表示。

此处，关于关系的描述，我们再进行一些补充:

```
(a)-[r:TYPE1|TYPE2]->(b)
```

当我们想要支持多种关系类型任意查询时，可以使用 | 来分隔关系类型。

```
(a)-[*3..5]->(b)
```

当我们想要查询不定长关系时，可以在[]中添加 *min..max 来表示，其中，min和max后可以省略，例如:

```
(a)-[:upstream*]->(b)
```

表示 b 是 a 的任意关联的上游。

### Cypher List 与 Map 说明





### Cypher NULL 说明



