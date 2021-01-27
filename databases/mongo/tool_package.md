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


### mongorestore


### bsondump


### mongoimport


### mongoexport


### mongostat


### mongotop


### mongofiles


