# Github mirror实现飞速上传/下载

我们在用git的向github拉取代码的时候，一定体会过10+kb下载的绝望吧~

辛苦等待几小时，结果又fail了。

本文主要是讲解一个小技巧，让你能够实现飞速的对github拉取/上传代码。

## 常用mirror推荐

1. https://github.com.cnpmjs.org/
2. https://hub.fastgit.org/
3. https://gitclone.com/github.com/

## Git Clone加速示例

```shell
#原地址
git clone https://github.com/kubernetes/kubernetes.git

#改为
git clone https://github.com.cnpmjs.org/kubernetes/kubernetes.git

#或者
git clone https://hub.fastgit.org/kubernetes/kubernetes.git

#或者
git clone https://gitclone.com/github.com/kubernetes/kubernetes.git
```

## release下载加速

```shell
#原地址
wget https://github.com/goharbor/harbor/releases/download/v2.0.2/harbor-offline-installer-v2.0.2.tgz

#改为
wget https://hub.fastgit.org/goharbor/harbor/releases/download/v2.0.2/harbor-offline-installer-v2.0.2.tgz
```

## 全局替换方法

```shell
git config --global url."https://github.com.cnpmjs.org".insteadOf https://github.com

# 测试
git clone https://github.com/kubernetes/kubernetes.git

# 查看git配置信息
git config --global --list

# 取消git配置
git config --global --unset url.https://github.com.cnpmjs.org.insteadof
```
