# 使用Python操作Neo4j数据库

## 概述

在上一节中，我们已经了解了如何在 neo4j 浏览器中进行 Neo4j 数据的相关操作了。

现在，我们会继续看一下如何使用 Python 编程语言来调用 Neo4j 数据库，这样，你就可以在自己的项目中使用它了。

其中：

 - [Neo4j](https://neo4j.com/docs/developer-manual/current/drivers/#driver-get-the-driver) 官方提供了 JS, Java, .Net 
   和 Python 的驱动程序。
 - 此外， [社区](https://neo4j.com/developer/language-guides/) 还提供了一些 PHP, Ruby, Go, Haskell 等编程语言的驱动。

下面，我们就以 Python 为例，还演示如何使用 Python 调用 Neo4j 数据库。

## Python 驱动安装

Neo4j 的 Python 驱动安装非常简单，可以直接使用 Python 的包管理工具直接安装即可：

```sh
pip install neo4j-driver
# Successfully installed neo4j-driver-4.3.3 pytz-2021.1
```

## HelloWorld 

下面，我们来编写第一个用 Python 调用 Neo4j 数据的示例代码：

```python
from neo4j import GraphDatabase


class HelloWorldExample(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]


if __name__ == "__main__":
    example = HelloWorldExample("neo4j://localhost:7687", "neo4j", "password")
    example.print_greeting("Hello World!")
    example.close()
```

运行一下看看结果吧:

```sh
python3 ./hello_world.py
# Hello World!, from node 0
python3 ./hello_world.py
# Hello World!, from node 1
python3 ./hello_world.py
# Hello World!, from node 2
```

可以看出，这种使用方法其实非常简单，仅仅就是直接用 Python 组装一个 Cypher 语句，然后调用 run 函数来执行即可。

## 通用示例

下面，我们再来看一个更加通用的示例:

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))

def add_friend(tx, name, friend_name):
    tx.run("MERGE (a:Person {name: $name}) "
           "MERGE (a)-[:KNOWS]->(friend:Person {name: $friend_name})",
           name=name, friend_name=friend_name)

def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
        print(record["friend.name"])

with driver.session() as session:
    session.write_transaction(add_friend, "Arthur", "Guinevere")
    session.write_transaction(add_friend, "Arthur", "Lancelot")
    session.write_transaction(add_friend, "Arthur", "Merlin")
    session.read_transaction(print_friends, "Arthur")

driver.close()
```

虽然我们还没有详细学习 Cypher 的语法，但是我们其实也已经可以了解到，上述命令其实就是先向数据库中写入了几条数据，然后进行了依次进行了查询。

关于 Neo4j Driver 更多的介绍可以参考 [官方文档](https://neo4j.com/docs/driver-manual/1.7/#driver-get-the-driver) 。

至此，我们基本就可以了解到 Neo4j 的 Python Driver 的使用也非常简单，其核心是需要我们了解 Cypher 的相关的语法。

接下来的文章中，我们将会详细介绍 Cypher 的相关语法。
