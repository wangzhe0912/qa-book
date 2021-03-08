# Kubernetes架构

## 节点

Kubernetes 通过将容器放入在节点（Node）上运行的 Pod 中来执行你的工作负载。 

节点可以是一个虚拟机或者物理机器，取决于所在的集群配置。每个节点包含运行 Pods 所需的服务， 这些 Pods 由控制面负责管理。

通常集群中会有若干个节点；而在一个学习用或者资源受限的环境中，你的集群中也可能 只有一个节点。

节点上的组件包括 kubelet、 容器运行时以及 kube-proxy。

### 管理

向 API 服务器添加节点的方式主要有两种：

1. 节点上的 kubelet 向控制面执行自注册；
2. 你，或者别的什么人，手动添加一个 Node 对象。


在你创建了 Node 对象或者节点上的 kubelet 执行了自注册操作之后， 控制面会检查新的 Node 对象是否合法。

例如，如果你使用下面的 JSON 对象来创建 Node 对象：

```json
{
  "kind": "Node",
  "apiVersion": "v1",
  "metadata": {
    "name": "10.240.79.157",
    "labels": {
      "name": "my-first-k8s-node"
    }
  }
}
```

Kubernetes 会在内部创建一个 Node 对象作为节点的表示。

Kubernetes 检查 kubelet 向 API 服务器注册节点时使用的 metadata.name 字段是否匹配。
如果节点是健康的（即所有必要的服务都在运行中），则该节点可以用来运行 Pod。 否则，直到该节点变为健康之前，所有的集群活动都会忽略该节点。

Ps: Kubernetes 会一直保存着非法节点对应的对象，并持续检查该节点是否已经变得健康。
你，或者某个控制器必需显式地 删除该 Node 对象以停止健康检查操作。

Node 对象的名称必须是合法的 DNS 子域名。


#### 节点自注册

当 kubelet 标志 --register-node 为 true（默认）时，它会尝试向 API 服务注册自己。 这是首选模式，被绝大多数发行版选用。

对于自注册模式，kubelet 使用下列参数启动：

 - --kubeconfig - 用于向 API 服务器表明身份的凭据路径。
 - --cloud-provider - 与某云驱动 进行通信以读取与自身相关的元数据的方式。
 - --register-node - 自动向 API 服务注册。
 - --register-with-taints - 使用所给的污点列表（逗号分隔的 <key>=<value>:<effect>）注册节点。 当 register-node 为 false 时无效。
 - --node-ip - 节点 IP 地址。
 - --node-labels - 在集群中注册节点时要添加的标签。 （参见 
   [NodeRestriction 准入控制插件](https://kubernetes.io/zh/docs/reference/access-authn-authz/admission-controllers/#noderestriction) 
   所实施的标签限制）。
 - --node-status-update-frequency - 指定 kubelet 向控制面发送状态的频率。


启用
[节点授权模式](https://kubernetes.io/zh/docs/reference/access-authn-authz/node/)
和
[NodeRestriction准入插件](https://kubernetes.io/zh/docs/reference/access-authn-authz/admission-controllers/#noderestriction) 
时，仅授权 kubelet 创建或修改其自己的节点资源。


#### 手动节点管理

你可以使用 kubectl 来创建和修改 Node 对象。

如果你希望手动创建节点对象时，请设置 kubelet 标志 --register-node=false。

你可以修改 Node 对象（忽略 --register-node 设置）。 例如，修改节点上的标签或标记其为不可调度。

你可以结合使用节点上的标签和 Pod 上的选择算符来控制调度。 例如，你可以限制某 Pod 只能在符合要求的节点子集上运行。

如果标记节点为不可调度（unschedulable），将阻止新 Pod 调度到该节点之上，但不会影响任何已经在其上的 Pod。 
这是重启节点或者执行其他维护操作之前的一个有用的准备步骤。

要标记一个节点为不可调度，执行以下命令：

```shell
kubectl cordon $NODENAME
```

Ps: 被 DaemonSet 控制器创建的 Pod 能够容忍节点的不可调度属性。
DaemonSet 通常提供节点本地的服务，即使节点上的负载应用已经被腾空，这些服务也仍需运行在节点之上。


### 节点状态

一个节点的状态包含以下信息:

 - 地址
 - 状态
 - 容量与可分配
 - 信息


你可以使用 kubectl 来查看节点状态和其他细节信息：

```shell
kubectl describe node <节点名称>
```

下面对每个部分进行详细描述。


#### 地址

这些字段的用法取决于你的云服务商或者物理机配置:

 - HostName：由节点的内核设置。可以通过 kubelet 的 --hostname-override 参数覆盖。
 - ExternalIP：通常是节点的可外部路由（从集群外可访问）的 IP 地址。
 - InternalIP：通常是节点的仅可在集群内部路由的 IP 地址。


#### 状态

conditions 字段描述了所有 Running 节点的状态。状态的示例包括：

节点状态|描述
-----|------
Ready|如节点是健康的并已经准备好接收 Pod 则为 True；False 表示节点不健康而且不能接收 Pod；Unknown 表示节点控制器在最近 node-monitor-grace-period 期间（默认 40 秒）没有收到节点的消息
DiskPressure|True 表示节点的空闲空间不足以用于添加新 Pod, 否则为 False
MemoryPressure|True 表示节点存在内存压力，即节点内存可用量低，否则为 False
PIDPressure|True 表示节点存在进程压力，即节点上进程过多；否则为 False
NetworkUnavailable|True 表示节点网络配置不正确；否则为 False


Ps: 如果使用命令行工具来查询已保护（Cordoned）节点的细节，其中的 Condition 字段可能 包括 `SchedulingDisabled`。
`SchedulingDisabled` 不是 Kubernetes API 中定义的 Condition，被保护起来的节点在其规约中被标记为不可调度（Unschedulable）。

节点条件使用 JSON 对象表示。例如，下面的响应描述了一个健康的节点。

```
"conditions": [
  {
    "type": "Ready",
    "status": "True",
    "reason": "KubeletReady",
    "message": "kubelet is posting ready status",
    "lastHeartbeatTime": "2019-06-05T18:38:35Z",
    "lastTransitionTime": "2019-06-05T11:41:27Z"
  }
]
```

如果 Ready 条件处于 Unknown 或者 False 状态的时间超过了 pod-eviction-timeout 值，
（一个传递给 kube-controller-manager 的参数）， 节点上的所有 Pod 都会被节点控制器计划删除。
默认的逐出超时时长为 5 分钟。

某些情况下，当节点不可达时，API 服务器不能和其上的 kubelet 通信，
此时，删除 Pod 的决定不能传达给 kubelet，直到它重新建立和 API 服务器的连接为止。
与此同时，被计划删除的 Pod 可能会继续在游离的节点上运行。

节点控制器在确认 Pod 在集群中已经停止运行前，不会强制删除它们。
你可以看到这些可能在无法访问的节点上运行的 Pod 处于 Terminating 或者 Unknown 状态。
如果 kubernetes 不能基于下层基础设施推断出某节点是否已经永久离开了集群， 集群管理员可能需要手动删除该节点对象。 
从 Kubernetes 删除节点对象将导致 API 服务器删除节点上所有运行的 Pod 对象并释放它们的名字。

节点生命周期控制器会自动创建代表状况的
[污点](https://kubernetes.io/zh/docs/concepts/scheduling-eviction/taint-and-toleration/) 。
当调度器将 Pod 指派给某节点时，会考虑节点上的污点。 Pod 则可以通过容忍度（Toleration）表达所能容忍的污点。

#### 容量与可分配

描述节点上的可用资源：CPU、内存和可以调度到节点上的 Pod 的个数上限。

 - capacity 块中的字段标示节点拥有的资源总量。 
 - allocatable 块指示节点上可供普通 Pod 消耗的资源量。


可以在学习如何在节点上
[预留计算资源](https://kubernetes.io/zh/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable) 
的时候了解有关容量和可分配资源的更多信息。

#### 信息

关于节点的一般性信息，例如内核版本、Kubernetes 版本（kubelet 和 kube-proxy 版本）、 
Docker 版本（如果使用了）和操作系统名称。这些信息由 kubelet 从节点上搜集而来。

#### 节点控制器


#### 节点容量


### 节点拓扑



### 节点优雅退出




## 控制面到节点通信




## 控制器




## 云控制器管理器的基础概念




