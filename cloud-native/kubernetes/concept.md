# Kubernetes 基本概念

Kubernetes 是一个开源的容器编排引擎，用来对容器化应用进行自动化部署、扩缩容和管理。

接下来，在本文中，我们将会讲解 Kubernetes 的一些基本概念。

## Kubernetes 是什么？

Kubernetes 是一个可移植、可扩展的开源平台，用于管理容器化的工作负载和服务，可促进声明式配置和自动化。 Kubernetes 拥有一个庞大且快速增长的生态
系统。Kubernetes 的服务、支持和工具非常广泛，适用于各个领域。


### 历史追溯

让我们回顾一下历史，从而看看为什么 kubernetes 如此的有用。

![container_evolution](./pictures/container_evolution.svg)

#### 传统部署时代

早期，各个组织机构都是在物理服务器上运行应用程序。而在物理机直接部署服务时，用户无法为物理服务器中的应用程序定义资源边界，这会导致资源分配问题。

例如，如果在物理服务器上运行多个应用程序，则可能会出现一个应用程序占用大部分资源的情况，结果可能导致其他应用程序的性能下降。
一种解决方案是在不同的物理服务器上运行每个应用程序，但是由于资源利用不足而无法扩展， 并且维护许多物理服务器的成本很高。

#### 虚拟化时代

为了解决物理机部署时代的资源隔离问题，人们引入了虚拟化的解决方案。

虚拟化技术是指允许用户在单个物理服务器的CPU上运行多个虚拟机（ VM ）。虚拟化的作用能够使用应用程序在 VM 之间隔离，并且提供了一定的安全保证。
因为一个应用程序的信息不能被另一应用程序随意访问。

虚拟化技术能够更好地利用物理服务器上的资源，并且因为可轻松地添加或更新应用程序 而可以实现更好的可伸缩性，降低硬件成本等等。

每个 VM 都是一台完整的计算机，在虚拟化硬件之上运行所有组件，包括其自己的**操作系统**。

#### 容器部署时代

容器与虚拟机类似，但是相比虚拟机而言，容器的隔离性并没有虚拟机那么强，它们可以在应用程序之间共享操作系统。
因此，容器可以被认为是一种轻量级的隔离方式。

容器与 VM 类似，具有自己的文件系统、CPU、内存、进程空间等。由于它们与基础架构分离，因此可以跨云、 OS 版本进行移植。

容器因为具备如下的许多优势而变得非常流行，下面是一些容器的优点：

 - 敏捷应用程序的创建和部署: 与使用 VM 镜像相比，容器的镜像创建的便捷性和效率更高。
 - 持续开发、集成和部署: 通过快速简单的回滚 (由于镜像的不可变性) ，支持可靠且频繁的容器镜像构建和部署。
 - 开发与运维的分离: 在构建/发布时创建应用程序容器镜像 (而不是在部署时)，从而将应用程序与基础架构分离。
 - 可观察性: 不仅可以显示操作系统级别的信息和指标，还可以显示应用程序的运行状况和其他指标。
 - 跨开发、测试和生产的环境一致性: 在个人计算机上甚至与与在云中运行的行为相同。
 - 跨云和操作系统发行版本的可移植性：可在 Ubuntu、RHEL、CoreOS、本地、 Google Kubernetes Engine 和其他任何地方运行。
 - 以应用程序为中心的管理：提高抽象级别，从在虚拟硬件上运行 OS 到使用逻辑资源在 OS 上运行应用程序。
 - 松耦合、分布式、弹性、解放的微服务：应用程序可以被分解成较小的独立部分，并且可以动态部署和管理，而不是在一台大型单机上整体运行。
 - 资源隔离：通过有效的资源隔离可以预测和保证容器内部署的应用程序的性能。
 - 资源利用：通过充分利用资源达到高效率和高密度。


### 为什么需要 Kubernetes，它能做什么?

容器是打包和运行应用程序的绝佳方式。

在生产环境中，你需要管理运行应用程序的容器，并确保不会停机。例如，如果一个容器发生故障，则需要启动另一个容器。那么，如果系统可以自动处理此行为，
你的工作量是不是会大大的减少？

Kubernetes 就是解决这些问题的方法！

Kubernetes 为你提供了一个可弹性运行分布式系统的框架。Kubernetes 会满足你的扩展要求、故障转移、部署模式等。例如，
Kubernetes 可以轻松管理系统的 Canary 部署。

详细来说， Kubernetes 为你提供了如下功能：

 - 服务发现和负载均衡: Kubernetes 可以使用 DNS 名称或自己的 IP 地址公开容器，如果进入容器的流量很大， Kubernetes
   可以负载均衡并分配网络流量，从而使部署稳定。
 - 存储编排: Kubernetes 允许你自动挂载你选择的存储系统，例如本地存储、公共云提供商等。
 - 自动部署和回滚: 你可以使用 Kubernetes 描述已部署容器的所需状态，它可以以受控的速率将实际状态 更改为期望状态。
   例如，你可以自动化 Kubernetes 来为你的部署创建新容器， 删除现有容器并将它们的所有资源用于新容器。
 - 自动完成装箱计算: Kubernetes 允许你指定每个容器所需 CPU 和内存（RAM）。
   当容器指定了资源请求时，Kubernetes 可以做出更好的决策来管理容器的资源。
 - 容器保活: Kubernetes 能够重新启动失败的容器、替换容器、杀死不响应用户定义的运行状况检查的容器，并且在准备好服务之前不将其通告给客户端。
 - 密钥与配置管理: Kubernetes 允许你存储和管理敏感信息，例如密码、OAuth 令牌和 ssh 密钥。
   你可以在不重建容器镜像的情况下部署和更新密钥和应用程序配置，也无需在堆栈配置中暴露密钥。


### Kubernetes 不是什么?

Kubernetes 不是传统的、包罗万象的 PaaS（平台即服务）系统。

由于 Kubernetes 在容器级别而不是在硬件级别运行，它提供了 PaaS 产品共有的一些普遍适用的功能， 例如部署、扩展、负载均衡、日志记录和监视。
但是，Kubernetes 不是单体系统，默认解决方案都是可选和可插拔的。 
Kubernetes 提供了构建开发人员平台的基础，但是在重要的地方保留了用户的选择和灵活性。

具体来说， Kubernetes：

 - 不限制支持的应用程序类型。 Kubernetes 旨在支持极其多种多样的工作负载，包括无状态、有状态和数据处理工作负载。
   如果应用程序可以在容器中运行，那么它应该可以在 Kubernetes 上很好地运行。
 - 不部署源代码，也不构建你的应用程序。持续集成(CI)、交付和部署（CI/CD）工作流取决于组织的文化和偏好以及技术要求。
 - 不提供应用程序级别的服务作为内置服务，例如中间件（例如，消息中间件）、 数据处理框架（例如，Spark）、
   数据库（例如，mysql）、缓存、集群存储系统 （例如，Ceph）。
   这样的组件可以在 Kubernetes 上运行，并且/或者可以由运行在 Kubernetes 上的应用程序通过可移植机制（例如， 开放服务代理）来访问。
 - 不要求日志记录、监视或警报解决方案。 它提供了一些集成作为概念证明，并提供了收集和导出指标的机制。
 - 不提供或不要求配置语言/系统（例如 jsonnet），它提供了声明性 API， 该声明性 API 可以由任意形式的声明性规范所构成。
 - 不提供也不采用任何全面的机器配置、维护、管理或自我修复系统。
 - 此外，Kubernetes 不仅仅是一个编排系统，实际上它消除了编排的需要。
   编排的技术定义是执行已定义的工作流程：首先执行 A，然后执行 B，再执行 C。
   相比之下，Kubernetes 包含一组独立的、可组合的控制过程， 这些过程连续地将当前状态驱动到所提供的所需状态。
   如何从 A 到 C 的方式无关紧要，也不需要集中控制，这使得系统更易于使用 且功能更强大、系统更健壮、更为弹性和可扩展。


## Kubernetes 组件

一个 Kubernetes 集群由一组被称作节点的机器组成。这些节点上运行 Kubernetes 所管理的容器化应用。每个集群具有至少一个工作节点。

**工作节点**托管作为应用负载的组件的 Pod 。 **控制平面**管理集群中的工作节点和 Pod 。 
为集群提供故障转移和高可用性，这些**控制平面**一般跨多主机运行，集群跨多个节点运行。

接下来，我们来讲解正常运行的 Kubernetes 集群所需的各种组件。

下图展示了包含所有相互关联组件的 Kubernetes 集群。

![components](./pictures/components-of-kubernetes.svg)


### 控制平面组件 （Control Plane Components）

控制平面的组件对集群做出全局决策(比如调度) 以及检测和响应集群事件（例如，当不满足部署的 replicas 字段时，启动新的 pod）。

控制平面组件可以在集群中的任何节点上运行。 
然而，为了简单起见，设置脚本通常会在同一个计算机上启动所有控制平面组件，并且不会在此计算机上运行用户容器。

#### kube-apiserver

API 服务器是 Kubernetes 控制面的组件， 该组件公开了 Kubernetes API。 API 服务器是 Kubernetes 控制面的前端。

Kubernetes API 服务器的主要实现是 kube-apiserver。
kube-apiserver 设计上考虑了水平伸缩，也就是说，它可通过部署多个实例进行伸缩。
你可以运行 kube-apiserver 的多个实例，并在这些实例之间平衡流量。


#### etcd

etcd 是兼具一致性和高可用性的键值数据库，作为保存 Kubernetes 所有集群数据的后台数据库。

您的 Kubernetes 集群的 etcd 数据库通常需要有个备份计划。

要了解 etcd 更深层次的信息，请参考 [etcd 文档](https://etcd.io/docs/) 。


#### kube-scheduler

kube-scheduler 是控制平面组件，负责监视新创建的、未指定运行节点（node）的 Pods，选择节点让 Pod 在上面运行。

调度决策考虑的因素包括单个 Pod 和 Pod 集合的资源需求、硬件/软件/策略约束、亲和性和反亲和性规范、数据位置、工作负载间的干扰和最后时限。


#### kube-controller-manager

kube-controller-manager 是在主节点上运行 控制器 的组件。它通过 api-server 监控集群的公共状态，并致力于将当前状态转变为期望状态。

从逻辑上讲，每个控制器都是一个单独的进程， 但是为了降低复杂性，它们都被编译到同一个可执行文件，并在一个进程中运行。

这些控制器包括:

 - 节点控制器（Node Controller）: 负责在节点出现故障时进行通知和响应。
 - 副本控制器（Replication Controller）: 负责为系统中的每个副本控制器对象维护正确数量的 Pod。
 - 端点控制器（Endpoints Controller）: 填充端点 (Endpoints) 对象(即加入 Service 与 Pod)。
 - 服务帐户和令牌控制器（Service Account & Token Controllers）: 为新的命名空间创建默认帐户和 API 访问令牌。


### cloud-controller-manager

云控制器管理器是指嵌入特定云的控制逻辑的 控制平面组件。

云控制器管理器允许您链接聚合到云提供商的应用编程接口中， 并分离出相互作用的组件与您的集群交互的组件。
cloud-controller-manager 仅运行特定于云平台的控制回路。
如果你在自己的环境中运行 Kubernetes，或者在本地计算机中运行学习环境， 所部署的环境中不需要云控制器管理器。

与 kube-controller-manager 类似，cloud-controller-manager 将若干逻辑上独立的控制回路组合到同一个可执行文件中，供你以同一进程的方式运行。
你可以对其执行水平扩容（运行不止一个副本）以提升性能或者增强容错能力。

下面的控制器都包含对云平台驱动的依赖：

 - 节点控制器（Node Controller）: 用于在节点终止响应后检查云提供商以确定节点是否已被删除
 - 路由控制器（Route Controller）: 用于在底层云基础架构中设置路由
 - 服务控制器（Service Controller）: 用于创建、更新和删除云提供商负载均衡器


### Node组件

节点组件在每个节点上运行，维护运行的 Pod 并提供 Kubernetes 运行环境。

#### kubelet

一个在集群中每个节点（node）上运行的代理。 它保证容器（containers）都 运行在 Pod 中。

kubelet 接收一组通过各类机制提供给它的 PodSpecs，确保这些 PodSpecs 中描述的容器处于运行状态且健康。

kubelet 不会管理不是由 Kubernetes 创建的容器。

### kube-proxy

kube-proxy 是集群中每个节点上运行的网络代理，实现 Kubernetes 服务（Service） 概念的一部分。

kube-proxy 维护节点上的网络规则。这些网络规则允许从集群内部或外部的网络会话与 Pod 进行网络通信。

如果操作系统提供了数据包过滤层并可用的话，kube-proxy 会通过它来实现网络规则。否则， kube-proxy 仅转发流量本身。

### 容器运行时 (Container Runtime)

容器运行环境是负责运行容器的软件。

Kubernetes 支持多个容器运行环境: Docker、 containerd、CRI-O 以及任何实现 Kubernetes CRI (容器运行环境接口)。


### 插件 （Addons）

插件使用 Kubernetes 资源（DaemonSet、 Deployment等）实现集群功能。

因为这些插件提供集群级别的功能，插件中命名空间域的资源属于 kube-system 命名空间。

下面是最常用的几个插件。有关可用插件的完整列表，请参见
[插件（Addons）](https://kubernetes.io/zh/docs/concepts/cluster-administration/addons/) 。

#### DNS

尽管其他插件都并非严格意义上的必需组件，但几乎所有 Kubernetes 集群都应该 有集群 DNS， 因为很多示例都需要 DNS 服务。

集群 DNS 是一个 DNS 服务器，和环境中的其他 DNS 服务器一起工作，它为 Kubernetes 服务提供 DNS 记录。

Kubernetes 启动的容器自动将此 DNS 服务器包含在其 DNS 搜索列表中。

#### Web界面（仪表盘）

[Dashboard](https://kubernetes.io/zh/docs/tasks/access-application-cluster/web-ui-dashboard/)
是Kubernetes 集群的通用的、基于 Web 的用户界面。
它使用户可以管理集群中运行的应用程序以及集群本身并进行故障排除。

#### 容器资源监控

[容器资源监控](https://kubernetes.io/zh/docs/tasks/debug-application-cluster/resource-usage-monitoring/)
将关于容器的一些常见的时间序列度量值保存到一个集中的数据库中，并提供用于浏览这些数据的界面。

#### 集群层面日志

[集群层面日志](https://kubernetes.io/zh/docs/concepts/cluster-administration/logging/)
机制负责将容器的日志数据 保存到一个集中的日志存储中，该存储能够提供搜索和浏览接口。

## Kubernetes API

Kubernetes 控制面 的核心是 API 服务器。 API 服务器负责提供 HTTP API，以供用户、集群中的不同部分和集群外部组件相互通信。

Kubernetes API 使你可以查询和操纵 Kubernetes API 中对象（例如：Pod、Namespace、ConfigMap 和 Event）的状态。

大部分操作都可以通过 [kubectl](https://kubernetes.io/zh/docs/reference/kubectl/overview/) 命令行接口
或 类似 [kubeadm](https://kubernetes.io/zh/docs/reference/setup-tools/kubeadm/)
这类命令行工具来执行， 这些工具在背后也是调用 API。不过，你也可以使用 REST 调用来访问这些 API。

如果你正在编写程序来访问 Kubernetes API，可以考虑使用
[客户端库](https://kubernetes.io/zh/docs/reference/using-api/client-libraries/) 。

### OpenAPI 规范

完整的 API 细节是用 [OpenAPI](https://www.openapis.org/) 来表述的。

Kubernetes API 服务器通过 /openapi/v2 提供 OpenAPI 规范。 你可以按照下表所给的请求头部，指定响应的格式：

|头部|可选值|说明|
|---|---|----|
|Accept-Encoding|gzip|不指定此头部也是可以的|
|Accept|application/com.github.proto-openapi.spec.v2@v1.0+protobuf|主要用于集群内部|
|Accept|*|提供application/json|
|Accept|application/json|默认值|

Kubernetes 为 API 实现了一种基于 Protobuf 的序列化格式，主要用于集群内部通信。

关于此格式的详细信息，可参考
[Kubernetes Protobuf 序列化](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/api-machinery/protobuf.md)
设计提案。
每种模式对应的接口描述语言（IDL）位于定义 API 对象的 Go 包中。


### API变更

任何成功的系统都要随着新的使用案例的出现和现有案例的变化来成长和变化。
为此，Kubernetes 的功能特性设计考虑了让 Kubernetes API 能够持续变更和成长的因素。

Kubernetes 项目的目标是**不要引发现有客户端的兼容性问题**，并在一定的时期内维持这种兼容性，以便其他项目有机会作出适应性变更。

一般而言，新的 API 资源和新的资源字段可以被频繁地添加进来。删除资源或者字段则要遵从
[API 废弃策略](https://kubernetes.io/zh/docs/reference/using-api/deprecation-policy/) 。

关于什么是兼容性的变更、如何变更 API 等详细信息，可参考
[API 变更](https://git.k8s.io/community/contributors/devel/sig-architecture/api_changes.md#readme) 。


### API 组和版本

为了简化删除字段或者重构资源表示等工作，Kubernetes 支持多个 API 版本，
每一个版本都在不同 API 路径下，例如 /api/v1 或 /apis/rbac.authorization.k8s.io/v1alpha1。

版本化是在 API 级别而不是在资源或字段级别进行的，目的是为了
确保 API 为系统资源和行为提供清晰、一致的视图，并能够控制对已废止的和/或实验性 API 的访问。

为了便于演化和扩展其 API，Kubernetes 实现了 可被
[启用或禁用](https://kubernetes.io/zh/docs/reference/using-api/#enabling-or-disabling)
的 
[API 组](https://kubernetes.io/zh/docs/reference/using-api/#api-groups) 。

API 资源之间靠 API 组、资源类型、名字空间（对于名字空间作用域的资源而言）和 名字来相互区分。
API 服务器可能通过多个 API 版本来向外提供相同的下层数据， 并透明地完成不同 API 版本之间的转换。
所有这些不同的版本实际上都是同一资源 的（不同）表现形式。
例如，假定同一资源有 v1 和 v1beta1 版本， 使用 v1beta1 创建的对象则可以使用 v1beta1 或者 v1 版本来读取、更改 或者删除。

关于 API 版本级别的详细定义，请参阅 [API 版本参考](https://kubernetes.io/zh/docs/reference/using-api/#api-versioning) 。


### API 扩展

有两种途径来扩展 Kubernetes API：

1. 你可以使用
   [自定义资源](https://kubernetes.io/zh/docs/concepts/extend-kubernetes/api-extension/custom-resources/) 
   来以声明式方式定义 API 服务器如何提供你所选择的资源 API。
2. 你也可以选择实现自己的
   [聚合层](https://kubernetes.io/zh/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)
   来扩展 Kubernetes API。


## 使用 Kubernetes 对象





