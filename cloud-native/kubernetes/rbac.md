# Kubernetes RBAC 杂谈

## RBAC 背景概述

了解 K8s 的同学都知道，Kubernetes 中所有的 API 对象都保存在 etcd 里。
而在 K8s 中，我们想要通过自己内插件来实现对 API 对象进行操作时，一定需要通过访问 kube-apiserver 来实现。

在 kube-apiserver  的调用中，首先需要来完成授权相关的工作。

而在 Kubernetes 项目中，负责完成授权（Authorization）工作的机制，就是 **RBAC**: 
基于角色的访问控制（Role-Based Access Control）。

## RBAC 基本概念

在 RBAC 中，有三个最核心的概念：

 - Role: 角色，它其实是一组规则，定义了一组对 Kubernetes API 对象的操作权限。
 - Subject: 被作用者，既可以是『人』，也可以是『机器』，也可以是你在 Kubernetes 里面定义的『用户』。
 - RoleBinding: 定义了『被作用者』和『角色』的绑定关系。

## Role

Role 本身就是一个 Kubernetes 的 API 对象，定义如下所示：

```yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: mynamespace
  name: example-role
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

首先，这个 Role 对象指定了它能产生作用的 Namespace: mynamespace 。

Ps: Namespace 是 Kubernetes 项目里的一个逻辑管理单位。不同 Namespace 的 API 对象，在通过 kubectl 命令进行操作的时候，是互相隔离开的。
当然，这仅限于逻辑上的“隔离”，Namespace 并不会提供任何实际的隔离或者多租户能力。

然后，这个 Role 对象的 rules 字段就是它所定义的权限规则。

以上面的示例为例，这条规则的含义就是：允许“被作用者”，对 mynamespace 下面的 Pod 对象，进行 GET、WATCH 和 LIST 操作。

在 Role 中，`verbs` 的全集包括: get, list, watch, create, update, patch, delete。

类似地，Role 对象的 rules 字段也可以进一步细化。比如，你可以只针对某一个具体的对象进行权限设置，如下所示：

```yaml
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  resourceNames: ["my-config"]
  verbs: ["get"]
```

这个例子就表示，这条规则的“被作用者”，只对名叫“my-config”的 ConfigMap 对象，有进行 GET 操作的权限。

## RoleBinding

那么，这个具体的“被作用者”又是如何指定的呢？这就需要通过 RoleBinding 来实现了。

RoleBinding 本身也是一个 Kubernetes 的 API 对象。它的定义如下所示：

```yaml
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: example-rolebinding
  namespace: mynamespace
roleRef:
  kind: Role
  name: example-role
  apiGroup: rbac.authorization.k8s.io  
subjects:
- kind: User
  name: example-user
  apiGroup: rbac.authorization.k8s.io
```

其中，包含了一个 roleRef 字段。

通过这个字段，RoleBinding 对象就可以直接通过名字，来引用我们前面定义的 Role 对象（example-role），
从而定义了“被作用者（Subject）”和“角色（Role）”之间的绑定关系。

需要注意的是：
Role 和 RoleBinding 对象都是 Namespaced 对象（Namespaced Object），
它们对权限的限制规则仅在它们自己的 Namespace 内有效，
roleRef 也只能引用当前 Namespace 里的 Role 对象。

那么，对于非 Namespaced（Non-namespaced）对象（比如：Node），
或者，某一个 Role 想要作用于所有的 Namespace 的时候，我们又该如何去做授权呢？

我们就必须要使用 ClusterRole 和 ClusterRoleBinding 这两个组合了。

这两个 API 对象的用法跟 Role 和 RoleBinding 完全一样。
只不过，它们的定义里，没有了 Namespace 字段。

示例如下：

```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: example-clusterrole
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: example-clusterrolebinding
subjects:
- kind: User
  name: example-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: example-clusterrole
  apiGroup: rbac.authorization.k8s.io
```

可以看到，这个 RoleBinding 对象里还包含了一个 subjects 字段，即“被作用者”。
它的类型是 User，即 Kubernetes 里的用户。这个用户的名字是 example-user。

## ServiceAccount

可是，在 Kubernetes 中，其实并没有一个叫作“User”的 API 对象。

而且，我们在前面和部署使用 Kubernetes 的流程里，既不需要 User，也没有创建过 User。

这个 User 到底是从哪里来的呢？

实际上，Kubernetes 里的“User”，也就是“用户”，只是一个授权系统里的逻辑概念。
它需要通过外部认证服务，比如 Keystone 来提供。
或者，你也可以直接给 APIServer 指定一个用户名、密码文件。
那么 Kubernetes 的授权系统，就能够从这个文件里找到对应的“用户”了。
当然，在大多数私有的使用环境中，我们只要使用 Kubernetes 提供的“内置用户”，就足够了。

而这个**内置用户**，其实就是: **ServiceAccount** 。

首先，我们要定义一个 ServiceAccount。它的 API 对象非常简单，如下所示：

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  namespace: mynamespace
  name: example-sa
```

可以看到，一个最简单的 ServiceAccount 对象只需要 Name 和 Namespace 这两个最基本的字段。

我们可以应用一下上述的 yaml 文件:

```shell
kubectl create -f svc-account.yaml
```

然后，我们来查看一下这个 ServiceAccount 的详细信息：

```yaml
- apiVersion: v1
  kind: ServiceAccount
  metadata:
    creationTimestamp: 2018-09-08T12:59:17Z
    name: example-sa
    namespace: mynamespace
    resourceVersion: "409327"
    ...
  secrets:
  - name: example-sa-token-vmfg6
```

可以看到，Kubernetes 会为一个 ServiceAccount 自动创建并分配一个 Secret 对象，
即：上述 ServiceAcount 定义里最下面的 secrets 字段。

这个 Secret，就是这个 ServiceAccount 对应的，用来跟 APIServer 进行交互的授权文件，我们一般称它为：`Token`。

Token 文件的内容一般是证书或者密码，它以一个 Secret 对象的方式保存在 Etcd 当中。

这时候，用户的 Pod，就可以声明使用这个 ServiceAccount 了，比如下面这个例子：

```yaml

apiVersion: v1
kind: Pod
metadata:
  namespace: mynamespace
  name: sa-token-test
spec:
  containers:
  - name: nginx
    image: nginx:1.7.9
  serviceAccountName: example-sa
```

可以看到，在 Pod 的 Spec 中，可以增加一个 serviceAccountName 字段来指定对应的 serviceAccount 名称。

等这个 Pod 运行起来之后，我们就可以看到，该 ServiceAccount 的 token，
也就是一个 Secret 对象被 Kubernetes 自动挂载到了容器的 `/var/run/secrets/kubernetes.io/serviceaccount` 目录下，如下所示:

```sh
kubectl describe pod sa-token-test -n mynamespace
```

输出如下:

```yaml
Name:               sa-token-test
Namespace:          mynamespace
...
Containers:
  nginx:
    ...
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from example-sa-token-vmfg6 (ro)
```

这时候，我们可以通过 kubectl exec 查看到这个目录里的文件：

```sh
kubectl exec -it sa-token-test -n mynamespace -- /bin/bash
# root@sa-token-test:/# ls /var/run/secrets/kubernetes.io/serviceaccount
# ca.crt namespace token
```

如上所示，容器里的应用，就可以使用这个 `ca.crt` 来访问 APIServer 了。

更重要的是，此时它只能够做 GET、WATCH 和 LIST 操作。
因为 example-sa 这个 ServiceAccount 的权限，已经被我们绑定了 Role 做了限制。

如果一个 Pod 没有声明 serviceAccountName，
Kubernetes 会自动在它的 Namespace 下创建一个名叫 default 的默认 ServiceAccount，然后分配给这个 Pod。
但是这个 default 的 ServiceAccount 实际没有关联任何的 Role，具体的权限是有 Kubernetes 默认的。

所以，**在生产环境中，我强烈建议你为所有 Namespace 下的默认 ServiceAccount，绑定一个只读权限的 Role**。

而上述的 RoleBinding 的 yaml 文件可以转化为如下格式:

```yaml
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: example-rolebinding
  namespace: mynamespace
subjects:
- kind: ServiceAccount
  name: example-sa
  namespace: mynamespace
roleRef:
  kind: Role
  name: example-role
  apiGroup: rbac.authorization.k8s.io
```

可以看到，在这个 RoleBinding 对象里，subjects 字段的类型（kind），不再是一个 User，而是一个名叫 example-sa 的 ServiceAccount。

Kubernetes 还拥有“用户组”（Group）的概念，也就是一组“用户”的意思。
如果你为 Kubernetes 配置了外部认证服务的话，这个“用户组”的概念就会由外部认证服务提供。
而对于 Kubernetes 的内置“用户”ServiceAccount 来说，上述“用户组”的概念也同样适用。

实际上，一个 ServiceAccount，在 Kubernetes 里对应的“用户”的名字是：

```
system:serviceaccount:<Namespace名字>:<ServiceAccount名字>
```

而它对应的内置“用户组”的名字，就是：

```
system:serviceaccounts:<Namespace名字>
```

比如，现在我们可以在 RoleBinding 里定义如下的 subjects：

```yaml
subjects:
- kind: Group
  name: system:serviceaccounts:mynamespace
  apiGroup: rbac.authorization.k8s.io
```

这就意味着这个 Role 的权限规则，作用于 mynamespace 里的所有 ServiceAccount。这就用到了“用户组”的概念。

而下面这个例子：

```yaml
subjects:
- kind: Group
  name: system:serviceaccounts
  apiGroup: rbac.authorization.k8s.io
```

就意味着这个 Role 的权限规则，作用于整个系统里的所有 ServiceAccount。

**在 Kubernetes 中已经内置了很多个为系统保留的 ClusterRole，它们的名字都以 system: 开头。**

你可以通过 `kubectl get clusterroles` 查看到它们。

一般来说，这些系统 ClusterRole，是绑定给 Kubernetes 系统组件对应的 ServiceAccount 使用的。

比如，其中一个名叫 system:kube-scheduler 的 ClusterRole，
定义的权限规则是 kube-scheduler（Kubernetes 的调度器组件）运行所需要的必要权限。

你可以通过如下指令查看这些权限的列表：

```sh
kubectl describe clusterrole system:kube-scheduler
```

```yaml
Name:         system:kube-scheduler
...
PolicyRule:
  Resources                    Non-Resource URLs Resource Names    Verbs
  ---------                    -----------------  --------------    -----
...
  services                     []                 []                [get list watch]
  replicasets.apps             []                 []                [get list watch]
  statefulsets.apps            []                 []                [get list watch]
  replicasets.extensions       []                 []                [get list watch]
  poddisruptionbudgets.policy  []                 []                [get list watch]
  pods/status                  []                 []                [patch update]
```

这个 system:kube-scheduler 的 ClusterRole，就会被绑定给 kube-system Namesapce 下名叫 kube-scheduler 的 ServiceAccount，
它正是 Kube-Scheduler 的 Pod 声明使用的 ServiceAccount。

除此之外，Kubernetes 还提供了四个预先定义好的 ClusterRole 来供用户直接使用：

 - cluster-admin
 - admin
 - edit
 - view

通过它们的名字，你应该能大致猜出它们都定义了哪些权限。比如，这个名叫 view 的 ClusterRole，就规定了被作用者只有 Kubernetes API 的只读权限。

上面这个 cluster-admin 角色，对应的是整个 Kubernetes 项目中的最高权限（verbs=*），因此，cluster-admin 的使用要非常慎用。
