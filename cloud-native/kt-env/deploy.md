# KT-env部署

## 前置条件

KT-env 部署之前，首先需要有一个 Kubernetes 集群并且已经部署了 Istio 。
同时，本地还需要一个配置好的 kubectl 工具。

## 下载部署包

首先，我们需要从 [发布页面](https://github.com/alibaba/virtual-environment/releases) 下载最新的部署文件包，并解压。

```shell
wget https://github.com/alibaba/virtual-environment/releases/download/v0.5.4/kt-virtual-environment-v0.5.4.zip
unzip kt-virtual-environment-v0.5.4.zip
cd v0.5.4/
```

## 安装相关组件

### 创建 CRD

在 KT-env 中，定义了一种新的资源对象: VirtualEnvironment 。

下面，我们第一步就来创建对应的 CRD 资源对象：

```shell
kubectl apply -f global/ktenv_crd.yaml
```

CRD组件会在Kubernetes集群内新增一种名为VirtualEnvironment的资源类型，在下一步我们将会用到它。可通过以下命令验证其安装状态：

```shell
kubectl get crd virtualenvironments.env.alibaba.com
```

若输出类似以下信息，则表明KtEnv的CRD组件已经正确部署：

```shell
NAME                                  CREATED AT
virtualenvironments.env.alibaba.com   2020-04-21T13:20:35Z
```


### 部署 Webhook 组件

Webhook组件用于将Pod的虚拟环境标写入到其Sidecar容器的运行时环境变量内。

```shell
kubectl apply -f global/ktenv_webhook.yaml
```

Webhook组件默认被部署到名为kt-virtual-environment的Namespace中，包含一个Service和一个Deployment对象，以及它们创建的子资源对象，可用以下命令查看：

```shell
kubectl -n kt-virtual-environment get all
```

若输出类似以下信息，则表明KtEnv的Webhook组件已经部署且正常运行:

```shell
NAME                                  READY   STATUS    RESTARTS   AGE
pod/webhook-server-5dd55c79b5-rf6dl   1/1     Running   0          86s

NAME                     TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/webhook-server   ClusterIP   172.21.0.254   <none>        443/TCP   109s

NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webhook-server   1/1     1            1           109s

NAME                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/webhook-server-5dd55c79b5   1         1         1       86s
```

### 创建 Role 和 ServiceAccount

如果 K8s 集群中，已经开启了 RBAC 权限控制，那么，为了保证我们的 Operator 可以正常工作，还需要部署相应的Role和ServiceAccount。

```shell
kubectl apply -n default -f ktenv_service_account.yaml
```

### 部署 KT-env Operator

Operator是由CRD组件定义的虚拟环境管理器实例，需要在**每个使用虚拟环境的Namespace里单独部署**。

以使用default Namespace为例，通过以下命令完成部署:

```shell
kubectl apply -n default -f ktenv_operator.yaml
```


此外，为了让Webhook组件对目标Namespace起作用，还应该为其添加值为enabled的environment-tag-injection标签。

```shell
kubectl label namespace default environment-tag-injection=enabled
```

现在，Kubernetes集群就已经具备使用虚拟环境能力了。
