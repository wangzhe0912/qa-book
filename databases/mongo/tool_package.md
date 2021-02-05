# MongoDB工具包剖析

在上一篇文章中，我们了解了MongoDB的安装包的内容。

接下来，我们来讲述MongoDB工具包中提供的MongoDB相关的配套工具。

## 工具包概述

MongoDB数据库工具是用于处理MongoDB实例的命令行实用程序的集合。

数据库工具包括以下二进制文件：

### 二进制导入导出类

1. mongodump: 将mongod数据库实例中的数据导出到一个二进制文件中。
2. mongorestore: 将mongodump导出得到的文件恢复到mongod或mongos实例中。
3. bsondump: 把BSON文件转化为JSON。

### 数据导入导出类

1. mongoimport: 将Extended JSON, CSV或TSV中的数据导入到MongoDB中。
2. mongoexport: 将mongod实例中的数据存储到JSON或CSV文件中。

### 问题分析工具

1. mongostat: 一个用于查询运行状态的mongod或mongods实例的概览指标的工具。
2. mongotop: 一个用于查询mongod实例读写耗时指标的工具。

### 网格文件系统相关工具

1. mongofiles: 支持在GridFS中处理文件。

## 下载与安装

MongoDB Tools的下载地址如下: https://www.mongodb.com/try/download/database-tools?tck=docs_databasetools

选择对应的平台版本下载即可。

MongoDB Tools的安装方式非常简单，只需要将工具包解压，并将其中的二进制工具文件放到环境变量PATH包含的目录中即可，例如`/usr/local/bin/`下。

## 工具使用方式详解

### mongodump

mongodump工具的作用是将运行中的mongodb实例中的数据导出到一组.bson文件中。

其中，可以使用-d指定database，-c指定collection。

mongodb连接地址字符串应该是一个以`mongodb://`或`mongodb+srv://`开头的。

完整的参数列表如下：

```
通用参数：
    --help                                              打印帮助信息
    --version                                           打印版本信息

日志级别参数：
    -v, --verbose=<level>                               打印更详细的日志信息
    --quiet                                             忽略所有日志打印

连接连接参数：
    -h, --host=<hostname>                               mongodb实例主机（对于副本集而言，应该是setname/host1,host2）
    --port=<port>                                       mongodb服务端口，也可以统一在--host hostname:port中设置
    
uri参数：    
    --uri=<mongodb-uri>                                 mongodb uri连接字符串

ssl参数：
    --ssl                                               连接mongo或mongos实例时，开启ssl
    --sslCAFile=<filename>                              包含证书颁发机构的根证书链的.pem文件
    --sslPEMKeyFile=<filename>                          包含证书和密钥的.pem文件
    --sslPEMKeyPassword=<password>                      解密sslPEMKeyFile的密码（如果加密了的话）
    --sslCRLFile=<filename>                             包含证书吊销列表的.pem文件
    --sslFIPSMode                                       使用已安装的openssl库的FIPS模式
    --tlsInsecure                                       跳过服务器证书链和主机名的验证

鉴权参数：
    -u, --username=<username>                           数据库用户名
    -p, --password=<password>                           数据库密码
    --authenticationDatabase=<database-name>            存放用户登录凭证的数据库
    --authenticationMechanism=<mechanism>               使用的认证机制
    --awsSessionToken=<aws-session-token>               AWS IAM的授权Token

kerberos参数:
    --gssapiServiceName=<service-name>                  使用GSSAPI / Kerberos进行身份验证时要使用的服务名称（默认：mongodb）
    --gssapiHostName=<host-name>                        使用GSSAPI / Kerberos进行身份验证时使用的主机名（默认值：<远程服务器的地址>）

生效空间参数：
    -d, --db=<database-name>                            指定数据库
    -c, --collection=<collection-name>                  指定database

查询参数：
    -q, --query=                                        查询过滤器，扩展JSON字符串，例如'{"x"：{"$gt"：1}}'
    --queryFile=                                        包含查询过滤器JSON字符串的文件
    --readPreference=<string>|<json>                    指定首选项模式（例如'nearest'）或首选项json对象（例如'{mode："nearest"，tagSets：[{a："b"}]，maxStalenessSeconds：123}'）

输出参数：
    -o, --out=<directory-path>                          导出目录，用'-'可以表示导出至标准输出，默认为'dump'
    --gzip                                              导出目录使用gzip压缩
    --oplog                                             使用oplog用于快照
    --archive=<file-path>                               作为存档转储到指定路径。如果指定的标志没有值，则将存档写入stdout。
    --dumpDbUsersAndRoles                               导出指定数据库的用户和角色信息
    --excludeCollection=<collection-name>               过滤指定collection排除出导出内容
    --excludeCollectionsWithPrefix=<collection-prefix>  过滤指定开头的collections，排除出导出内容
    -j, --numParallelCollections=                       指定多个collections并行导出
    --viewsAsCollections                                将视图与生成的数据一起作为普通集合转储，而忽略标准集合
```


### mongorestore

mongorestore工具的作用是将mongodump生成的备份数据恢复到一个运行的数据库实例中。

其中，可以使用-d指定database，-c指定collection。

mongodb连接地址字符串应该是一个以`mongodb://`或`mongodb+srv://`开头的。

完整的参数列表如下：

```
通用参数（同mongodump）
日志级别参数（同mongodump）
连接连接参数（同mongodump）
uri参数（同mongodump）
ssl参数（同mongodump）
鉴权参数（同mongodump）
kerberos参数（同mongodump）

生效空间参数：
    -d, --db=<database-name>                            指定数据库
    -c, --collection=<collection-name>                  指定database
    --nsExclude=<namespace-pattern>
    --nsInclude=<namespace-pattern>
    --nsFrom=<namespace-pattern>
    --nsTo=<namespace-pattern>

输入参数：
    --objcheck
    --oplogReplay
    --oplogLimit=<seconds>[:ordinal]
    --oplogFile=<filename>
    --archive=<filename>
    --restoreDbUsersAndRoles
    --dir=<directory-name>
    --gzip

恢复参数：
    --drop
    --dryRun
    --writeConcern=<write-concern>
    --noIndexRestore
    --convertLegacyIndexes
    --noOptionsRestore
    --keepIndexVersion
    --maintainInsertionOrder
    -j, --numParallelCollections=
    --numInsertionWorkersPerCollection=
    --stopOnError
    --bypassDocumentValidation
    --preserveUUID
    --fixDottedHashIndex
```

### bsondump


### mongoimport


### mongoexport


### mongostat


### mongotop


### mongofiles



