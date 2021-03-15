# -*- coding: UTF-8 -*-
import tensorflow as tf
# 定义一个hello 的常量
hello = tf.constant("Hello Tensorflow")

# 创建一个会话
session = tf.Session()

# 执行常量操作并打印到标准输出
print(session.run(hello))
