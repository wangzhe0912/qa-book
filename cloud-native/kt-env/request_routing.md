# Mesh基础知识及请求路由

想要了解 KT-env 相关的功能和使用，首先需要了解一下什么是 mesh 以及请求路由相关的功能。

## ServiceMesh 相关介绍

首先，我们来了解一下大家对 ServiceMesh 的定义：

**服务网格（Service Mesh）是处理服务间通信的基础设施层。
它负责构成现代云原生应用程序的复杂服务拓扑来可靠地交付请求。
在实践中，Service Mesh 通常以轻量级网络代理阵列的形式实现，
这些代理与应用程序代码部署在一起，对应用程序来说无需感知代理的存在。**

ServiceMesh 通常有如下特点：

 - 它是应用程序间通信的中间层。
 - 轻量级网络代理。
 - 应用程序无感知。
 - 解耦应用程序的重试/超时、监控、追踪和服务发现。

ServiceMesh 仅仅是一种定义和概念，而关于 ServiceMesh 的具体实现，则有多种不同的服务实现方式，例如 Istio, Linkerd。

其中，Istio 是目前最流行 ServiceMesh 服务了，我们也将会继续对 Istio 来进行详细的说明。

## Istio 概述

Istio 是 ServiceMesh 的一种实现。

Istio 服务网格从逻辑上分为数据平面和控制平面。

 - 数据平面: 由一组智能代理（Envoy）组成，被部署为 Sidecar。这些代理负责协调和控制微服务之间的所有网络通信。它们还收集和报告所有网格流量的遥测数据。
 - 控制平面: 管理并配置代理来进行流量路由。


下图展示了组成每个平面的不同组件：

![request_routing1](./pictures/request_routing1.svg)

### Envoy

Istio 使用 Envoy 代理的扩展版本。Envoy 是用 C++ 开发的高性能代理，用于协调服务网格中所有服务的入站和出站流量。
Envoy 代理是唯一与数据平面流量交互的 Istio 组件。

Envoy 代理被部署为服务的 Sidecar，在逻辑上为服务增加了 Envoy 的许多内置特性，例如：

 - 动态服务发现
 - 负载均衡
 - TLS
 - HTTP/2 与 grpc 代理
 - 熔断器
 - 健康检查
 - 基于百分比流量分割的分阶段发布
 - 故障注入
 - 丰富的监控指标

这种 Sidecar 部署允许 Istio 可以执行策略决策，并提取丰富的遥测数据，接着将这些数据发送到监视系统以提供有关整个网格行为的信息。

Sidecar 代理模型还允许您向现有的部署添加 Istio 功能，而不需要重新设计架构或重写代码。

由 Envoy 代理启用的一些 Istio 的功能和任务包括：

 - 流量控制功能：通过丰富的 HTTP、gRPC、WebSocket 和 TCP 流量路由规则来执行细粒度的流量控制。
 - 网络弹性特性：重试设置、故障转移、熔断器和故障注入。
 - 安全性和身份认证特性：执行安全性策略，并强制实行通过配置 API 定义的访问控制和速率限制。
 - 基于 WebAssembly 的可插拔扩展模型，允许通过自定义策略执行和生成网格流量的遥测。

### Istiod

Istiod 提供服务发现、配置和证书管理。

Istiod 将控制流量行为的高级路由规则转换为 Envoy 特定的配置，并在运行时将其传播给 Sidecar。
Pilot 提取了特定平台的服务发现机制，并将其综合为一种标准格式，任何符合 Envoy API 的 Sidecar 都可以使用。

Istio 可以支持发现多种环境，如 Kubernetes 或 VM。

您可以使用 Istio 流量管理 API 让 Istiod 重新构造 Envoy 的配置，以便对服务网格中的流量进行更精细的控制。

Istiod 安全通过内置的身份和凭证管理，实现了强大的服务对服务和终端用户认证。
您可以使用 Istio 来升级服务网格中未加密的流量。
使用 Istio，运营商可以基于服务身份而不是相对不稳定的第 3 层或第 4 层网络标识符来执行策略。
此外，您可以使用 Istio 的授权功能控制谁可以访问您的服务。

Istiod 还充当证书授权（CA），并生成证书以允许在数据平面中进行安全的 mTLS 通信。

## Istio 请求路由控制

Istio 提供的核心功能之一就是 **服务发现** 。

Istio 简单的规则配置和流量路由允许您控制服务之间的流量和 API 调用过程。
Istio 简化了服务级属性（如熔断器、超时和重试）的配置，并且让它轻而易举的执行重要的任务（如 A/B 测试、金丝雀发布和按流量百分比划分的分阶段发布）。

例如，在 Istio 中，有两个非常重要的概念，**VirtualService** 和 **DestinationRule**。

通过合理的 **VirtualService** 和 **DestinationRule** 的配置，可以实现根据指定 uri, 指定的 headers 信息等等来配置对应的下游地址。

可以参考如下示例: [Istio 请求路由](https://istio.missshi.com/chap03/request_routing.html)

### Service 、 VirtualService 、 DestinationRule 关系介绍

Service 是 K8s 中的核心概念之一，它是 K8s 中默认的服务发现机制。
具体来说，K8s 中的 Service 对应于一组指定标签的 Pod 实例，发向该 Service 的请求会被自动转发到对应的 Pod 实例上。

虽然，K8s 中的 Service 已经具备了基本的服务发现的能力，但实际上这种基本的服务发现能力远远无法满足业务对流量治理相关能力，
例如，特定的路由策略、网络重试等功能。

因此，Istio 的出现就是为了进一步提升流量治理的能力，而在 Istio 中，最核心的两个概念就是 VirtualService 和 DestinationRule 了。

其中: 

 - VirtualService 的目的是定义一组要在访问 host 时应用的流量路由规则，每个路由规则定义了特定协议流量的匹配规则。如果流量的匹配规则满足的话，则将其发送到配置中定义的目标服务（或其子集/版本）中，此外，还包括了HTTP超时控制、重试、镜像、修改headers等。
 - DestinationRule 的目的定义在路由发生后应用于服务流量的策略。 这些规则指定负载均衡的配置、来自 sidecar 的连接池大小和异常检测设置，以检测和从负载均衡池中驱逐不健康的实例。


VirtualService 故名思义就是虚拟服务，VirtualService 中定义了一系列针对指定服务的流量路由规则。
每个路由规则都是针对特定协议的匹配规则。
如果流量符合这些特征，就会根据规则发送到服务注册表中的目标服务（或者目标服务的子集或版本）。

DestinationRule 是基于已有的 K8s Service 进行 Pod 下的细粒度的分组。
例如，可以将一个 Service 下的 Pod 根据 label 等信息再次分为多个 subset，从而可以在 VirtualService 对流量进行 subset 级别的细粒度分发。

也就是说：**VirtualService 和 DestinationRule 都是基于已有的 K8s Service 的条件下进行的功能扩展，必须保证 K8s Service 已经存在。**
而在消息具体发送的过程中，envoy 会默认劫持流量并发送给对应的 Pod 实例，而非依赖 kube-proxy 进行请求下发。

示例的 DestinationRule 配置文件如下：

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: flaskapp.books.svc.cluster.local
spec:
  host: flaskapp.books.svc.cluster.local
  subsets:
  - name: subset-v1
    labels:
      version: v1
  - name: subset-v2
    labels:
      version: v2
```

它可以将 books namespace 下的 flaskapp 的 service 下关联的 Pod 进行细粒度的分组，
其中 subset-v1 中包含所有 labels 中 version 为 v1 的 Pod，subset-v2 中包含所有 labels 中 version 为 v2 的 Pod。

VirtualService 的配置文件如下：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: flaskapp-policy
spec:
  hosts:
  -  flaskapp.books.svc.cluster.local
  http:
  - route:
    - destination:
        host: flaskapp.books.svc.cluster.local
        subset: subset-v2
    match:
    - headers:
        end-user:
          exact: jason
  - route:
    - destination:
        host: flaskapp.books.svc.cluster.local
        subset: subset-v1
```

我们来看一下这个 VirtualService 的配置做了什么事情：
它扩展了 books namespace 下原有 K8s Service flaskapp 的路由策略，当请求的 headers 中包括 end-user 且值为 jason 的话，
则将对应请求发送给 subset-v2 分组的 Pod 实例，否则的话，则将对应请求发送给 subset-v1 分组的 Pod 实例。
