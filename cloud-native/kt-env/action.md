# KT-env实战

在之前的内容中，我们已经完成了 KT-env 的环境搭建。
同时，也了解了请求路由的基本原理。

下面，我们就来具体使用 KT-env 来实现对应的虚拟环境。

## QuickStart

Step1: 创建虚拟环境。

创建一个`virtual-environment-cr.yaml` 文件：

```yaml
apiVersion: env.alibaba.com/v1alpha2
kind: VirtualEnvironment
metadata:
  name: demo-virtualenv
spec:
  envHeader:
    name: ali-env-mark
    autoInject: true
  envLabel:
    name: virtual-env
    splitter: "."
    defaultSubset: dev
```

实例创建后，会自动监听所在Namespace中的所有Service、Deployment和StatefulSet对象并自动生成路由隔离规则，形成虚拟环境。

```shell
kubectl apply -n default -f virtual-environment-cr.yaml
```

Step2: 拉取Git仓库，进入示例代码目录。

```shell
git clone https://github.com/alibaba/virtual-environment.git
cd virtual-environment/examples
```

Step3: 设置 default namespace 自动注入 sidecar 并使得 webhook 能够为 Envoy 自动注入环境变量。

```shell
kubectl label namespace default environment-tag-injection=enabled
kubectl label namespace default istio-injection=enabled
```

Step4: 在集群随意创建一个临时的Pod作为发送测试请求的客户端。

```shell
kubectl create deployment sleep --image=virtualenvironment/sleep --dry-run -o yaml | kubectl apply -n default -f - 
```

Step5: 部署相关应用

KtEnv支持Deployment和StatefulSet对象的路由隔离，
在这个例子中将部署3种不同语言实现的示例应用，
其中app-js和app-java被部署为Deployment，而app-go被部署为StatefulSet。

修改 `app.sh` 脚本中 apply_pods 函数如下：

```shell
apply_pods() {
    type=${1}
    ee=`echo ${e} | sed -e "s/\./-/g"`
    echo $s
    cat ${basepath}/${type}.yaml | sed -e "s/service-name-env-placeholder/${s}-${ee}/g" \
                        -e "s/service-name-placeholder/${s}/g" \
                        -e "s/app-env-placeholder/${e}/g" \
                        -e "s/app-image-placeholder/`hget images ${s}`/g" \
                        -e "s#app-url-placeholder#`hget urls ${s}`#g" \
                  | kubectl ${action} --validate=false -n ${namespace} -f -
}
```

使用`app.sh`脚本快速创建示例所需的VirtualEnvironment、Deployment、StatefulSet和Service资源：

```shell
# default namespace 下启动演示的服务实例
deploy/app.sh apply default
```

依次使用`kubectl get virtualenvironment`、`kubectl get deployment`、`kubectl get statefulset`、`kubectl get service`
命令查看各资源的创建情况，等待所有资源部署完成。

Step6: 进入同Namespace的任意一个Pod，例如前面步骤创建的sleep容器。

```shell
# 进入集群中的容器
kubectl exec -n default -it $(kubectl get -n default pod -l app=sleep -o jsonpath='{.items[0].metadata.name}') -- /bin/sh
```

Step7: 实验一下

分别在请求头加上不同的虚拟环境名称，使用curl工具调用app-js服务。

3个服务的关系是: `app-js -> app-go -> app-java` 。 

注意该示例创建的VirtualEnvironment实例配置使用`.`作为环境层级分隔符，同时配置了传递标签Header的键名为`ali-env-mark`。

已知各服务输出文本结构为`[项目名 @ 响应的Pod所属虚拟环境]` <- 请求标签上的虚拟环境名称。

观察实际响应的服务实例情况:

```shell
# 使用dev.proj1标签
> curl -H 'ali-env-mark: dev.proj1' app-js:8080/demo
  [springboot @ dev.proj1] <-dev.proj1
  [go @ dev] <-dev.proj1
  [node @ dev.proj1] <-dev.proj1

# 使用dev.proj1.feature1标签
> curl -H 'ali-env-mark: dev.proj1.feature1' app-js:8080/demo
  [springboot @ dev.proj1.feature1] <-dev.proj1.feature1
  [go @ dev] <-dev.proj1.feature1
  [node @ dev.proj1] <-dev.proj1.feature1

# 使用dev.proj2标签
> curl -H 'ali-env-mark: dev.proj2' app-js:8080/demo
  [springboot @ dev] <-dev.proj2
  [go @ dev.proj2] <-dev.proj2
  [node @ dev] <-dev.proj2

# 不带任何标签访问
# 由于启用了AutoInject配置，经过node服务后，请求自动加上了Pod所在虚拟环境的标签
> curl app-js:8080/demo
  [springboot @ dev] <-dev
  [go @ dev] <-dev
  [node @ dev] <-empty
```


## VirtualEnvironment 配置文件解读

虚拟环境实例通过VirtualEnvironment类型的Kubernetes资源定义。其内容结构示例如下：

```yaml
apiVersion: env.alibaba.com/v1alpha2
kind: VirtualEnvironment
metadata:
  name: demo-virtualenv
spec:
  envHeader:
    name: ali-env-mark
    autoInject: true
  envLabel:
    name: virtual-env
    splitter: "."
    defaultSubset: dev
```

参数作用如下表所示：

|配置参数|	默认值|	说明|
|------|---------|-----|
|envHeader.name|	X-Virtual-Env|	用于透传虚拟环境名的HTTP头名称（虽然有默认值，建议显性设置）|
|envHeader.autoInject|	false	|是否为没有虚拟环境HTTP头记录的请求自动注入HTTP头（建议开启）|
|envLabel.name	|virtual-env	|Pod上标记虚拟环境名用的标签名称（除非确实必要，建议保留默认值）|
|envLabel.splitter|	.|	虚拟环境名中用于划分环境默认路由层级的字符（只能是单个字符）|
|envLabel.defaultSubset	|无	|请求未匹配到任何存在的虚拟环境时，进行兜底虚拟环境名（默认为随机路由）|


注意：VirtualEnvironment实例只对其所在的Namespace有效。如有需要，可以通过在多个Namespace分别创建相同配置的实例。
