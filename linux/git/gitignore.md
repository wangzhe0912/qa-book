# Git忽略已加入版本控制系统中的文件

## 背景描述

众所周知，对于git项目，可以在.gitignore中添加一些文件/文件夹，以此来进行文件忽略。
然而，对于一些已经被track的文件，再添加至.gitignore中是没有效果的。

在本文中，我们将会主要讲解针对已经被track的文件如何通过.gitignore文件进行忽略。

## 实现方式

具体来说，为了实现通过.gitignore文件进行忽略已经被track的文件，需要通过如下两步：

1. 清除本地缓存。
2. 重新提交commit信息。

```bash
git rm -r --cached .
git add .
git commit -m 'update .gitignore'
```
