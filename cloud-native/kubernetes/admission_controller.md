# Kubernetes 准入控制机制

## 准入控制器概述

准入控制器是指当用户请求通过认证和授权之后，对象被持久化之前拦截 apiserver 的请求。

准入控制器可以可以执行"验证"和"变更"操作。
其中，"变更"操作是指可以修改被接收的对象的meta信息。

默认的控制器代码是编译进入 `kube-apiserver` 二进制文件的，只能由集群管理员配置。

准入控制过程分为两个阶段。

第一阶段，运行"变更"准入控制器。

第二阶段，运行"验证"准入控制器。

Ps: 某些控制器既是变更准入控制器又是验证准入控制器。

如果任何一个阶段的任何控制器拒绝了该请求，则整个请求将立即被拒绝，并向终端用户返回一个错误。

## 启用/关闭一个准入控制器

`kube-apiserver` 的 `enable-admission-plugins` 参数接受一个以逗号分隔的准入控制插件顺序列表。

```sh
kube-apiserver --enable-admission-plugins=NamespaceLifecycle,LimitRanger
```

上述命令中启用了 `NamespaceLifecycle` 和 `LimitRanger` 准入控制插件。

同样，`disable-admission-plugins` 参数也可以将传入的（以逗号分隔的） 准入控制插件列表禁用，即使是默认启用的插件也会被禁用。

```sh
kube-apiserver --disable-admission-plugins=PodNodeSelector,AlwaysDeny
```

我们可以查询哪些准入控制插件是默认启用的:

```sh
kube-apiserver -h | grep enable-admission-plugins
```

这些准入控制器都是 kubernetes 内置推荐的准入控制器。

## 内置准入控制器功能概述



## 自定义准入控制器

除了上述我们提到的 Kubernetes 中内置的准入控制器插件外，Kubernetes 还提供了一种可以自定义开发的准入控制插件，
它是通过在运行时所配置的 webhook 的形式来运行的。

准入 Webhook 是一种用于接收准入请求并对其进行处理的 HTTP 回调机制。

我们可以定义两种类型的准入 webhook:

 - "验证"性质的准入 Webhook
 - "修改"性质的准入 Webhook

修改性质的准入 Webhook 会先被调用。
它们可以更改发送到 API 服务器的对象以执行自定义的设置默认值操作。

在完成了所有对象修改并且 API 服务器也验证了所传入的对象之后，
验证性质的 Webhook 会被调用，并通过拒绝请求的方式来强制实施自定义的策略。

## 准入 Webhook 实战

准入 Webhook 本质上是集群控制平面的一部分。
因此，对于准入 Webhook 的编写，应该非常是谨慎的编写和部署。
下面，我们来看看如何快速编写一个 Webhook 。

准入 Webhook 生效需要具备如下条件:

 - Kubernetes 集群版本至少为 v1.16
 - 确保启用 MutatingAdmissionWebhook 和 ValidatingAdmissionWebhook 控制器。

### 示例准入 webhook 应用

对于一个准入 webhook 而言，需要包含如下三个步骤:

1. 编写一个准入 webhook 应用。
2. 部署 webhook 应用。
3. 配置对应的 WebhookConfiguration 。


在如下代码中，包含了 [admission webhook 服务器](https://github.com/qa-tools-famliy/admission-webhook-example) 的示例实现。

具体来说，webhook 处理由 apiserver 发送的 AdmissionReview 请求，并且将其决定作为 AdmissionResponse 对象以相同版本发送回去。

下面，我们来一个示例的 `ValidatingWebhookConfiguration` 的配置:

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: "pod-policy.example.com"
webhooks:
- name: "pod-policy.example.com"
  rules:   # webhook 生效范围
  - apiGroups:   [""]         # "" 表示核心组，*匹配所有组
    apiVersions: ["v1"]       # * 匹配所有组
    operations:  ["CREATE"]   # 支持 CREATE, UPDATE, DELETE, CONNECT, *
    resources:   ["pods"]     # "*" 匹配所有资源，但不包括子资源。"*/*" 匹配所有资源，包括子资源。"pods/*" 匹配 pod 的所有子资源。"*/status" 匹配所有 status 子资源。
    scope:       "Namespaced"  # 表示 namespace 级别生效, Cluster表示集群有效, * 表示全局生效
  clientConfig:  # Webhook 的地址
    service:
      namespace: "example-namespace"
      name: "example-service"
    caBundle: "Ci0tLS0tQk...<base64-encoded PEM bundle containing the CA that signed the webhook's serving certificate>...tLS0K"
  admissionReviewVersions: ["v1", "v1beta1"]
  sideEffects: None
  timeoutSeconds: 5  # 超时时间默认为 10s
```

当 apiserver 收到与 rules 相匹配的请求时，apiserver 按照 clientConfig 中指定的方式向 webhook 发送一个 admissionReview 请求。

创建 webhook 配置后，系统将花费几秒钟使新配置生效。

那么，apiserver 发送给 webhook 服务器的请求的格式是什么样的呢？一个示例如下：

```
{
  "apiVersion": "admission.k8s.io/v1",
  "kind": "AdmissionReview",
  "request": {
    # 唯一标识此准入回调的随机 uid
    "uid": "705ab4f5-6393-11e8-b7cc-42010a800002",

    # 传入完全正确的 group/version/kind 对象
    "kind": {"group":"autoscaling","version":"v1","kind":"Scale"},
    # 修改 resource 的完全正确的的 group/version/kind
    "resource": {"group":"apps","version":"v1","resource":"deployments"},
    # subResource（如果请求是针对 subResource 的）
    "subResource": "scale",

    # 在对 API 服务器的原始请求中，传入对象的标准 group/version/kind
    # 仅当 webhook 指定 `matchPolicy: Equivalent` 且将对 API 服务器的原始请求转换为 webhook 注册的版本时，这才与 `kind` 不同。
    "requestKind": {"group":"autoscaling","version":"v1","kind":"Scale"},
    # 在对 API 服务器的原始请求中正在修改的资源的标准 group/version/kind
    # 仅当 webhook 指定了 `matchPolicy：Equivalent` 并且将对 API 服务器的原始请求转换为 webhook 注册的版本时，这才与 `resource` 不同。
    "requestResource": {"group":"apps","version":"v1","resource":"deployments"},
    # subResource（如果请求是针对 subResource 的）
    # 仅当 webhook 指定了 `matchPolicy：Equivalent` 并且将对 API 服务器的原始请求转换为该 webhook 注册的版本时，这才与 `subResource` 不同。
    "requestSubResource": "scale",

    # 被修改资源的名称
    "name": "my-deployment",
    # 如果资源是属于名字空间（或者是名字空间对象），则这是被修改的资源的名字空间
    "namespace": "my-namespace",

    # 操作可以是 CREATE、UPDATE、DELETE 或 CONNECT
    "operation": "UPDATE",

    "userInfo": {
      # 向 API 服务器发出请求的经过身份验证的用户的用户名
      "username": "admin",
      # 向 API 服务器发出请求的经过身份验证的用户的 UID
      "uid": "014fbff9a07c",
      # 向 API 服务器发出请求的经过身份验证的用户的组成员身份
      "groups": ["system:authenticated","my-admin-group"],
      # 向 API 服务器发出请求的用户相关的任意附加信息
      # 该字段由 API 服务器身份验证层填充，并且如果 webhook 执行了任何 SubjectAccessReview 检查，则应将其包括在内。
      "extra": {
        "some-key":["some-value1", "some-value2"]
      }
    },

    # object 是被接纳的新对象。
    # 对于 DELETE 操作，它为 null。
    "object": {"apiVersion":"autoscaling/v1","kind":"Scale",...},
    # oldObject 是现有对象。
    # 对于 CREATE 和 CONNECT 操作，它为 null。
    "oldObject": {"apiVersion":"autoscaling/v1","kind":"Scale",...},
    # options 包含要接受的操作的选项，例如 meta.k8s.io/v CreateOptions、UpdateOptions 或 DeleteOptions。
    # 对于 CONNECT 操作，它为 null。
    "options": {"apiVersion":"meta.k8s.io/v1","kind":"UpdateOptions",...},

    # dryRun 表示 API 请求正在以 `dryrun` 模式运行，并且将不会保留。
    # 带有副作用的 Webhook 应该避免在 dryRun 为 true 时激活这些副作用。
    # 有关更多详细信息，请参见 http://k8s.io/docs/reference/using-api/api-concepts/#make-a-dry-run-request
    "dryRun": false
  }
}
```

Webhook 使用 HTTP 200 状态码、Content-Type: application/json 和一个包含 AdmissionReview 对象的 JSON 序列化格式来发送响应。

该 AdmissionReview 对象与发送的版本相同，且其中包含的 response 字段已被有效填充。

response 至少必须包含以下字段：

 - uid，从发送到 webhook 的 request.uid 中复制而来
 - allowed，设置为 true 或 false

一个最简单允许请求的示例如下:

```
{
  "apiVersion": "admission.k8s.io/v1",
  "kind": "AdmissionReview",
  "response": {
    "uid": "<value from request.uid>",
    "allowed": true
  }
}
```

Webhook 禁止请求的最简单响应示例：

```
{
  "apiVersion": "admission.k8s.io/v1",
  "kind": "AdmissionReview",
  "response": {
    "uid": "<value from request.uid>",
    "allowed": false
  }
}
```

当拒绝请求时，Webhook 可以使用 status 字段自定义 http 响应码和返回给用户的消息。示例如下：

```
{
  "apiVersion": "admission.k8s.io/v1",
  "kind": "AdmissionReview",
  "response": {
    "uid": "<value from request.uid>",
    "allowed": false,
    "status": {
      "code": 403,
      "message": "You cannot do this because it is Tuesday and your name starts with A"
    }
  }
}
```

当允许请求时，mutating准入 Webhook 也可以选择修改传入的对象。
这是通过在响应中使用 patch 和 patchType 字段来完成的。
当前唯一支持的 patchType 是 JSONPatch，其中的 patch 字段包含一个以 base64 编码的 JSON patch 操作数组。

例如，设置 `spec.replicas` 的单个补丁操作将是:

```json
[{"op": "add", "path": "/spec/replicas", "value": 3}]
```

如果以 Base64 形式编码，结果将是 `W3sib3AiOiAiYWRkIiwgInBhdGgiOiAiL3NwZWMvcmVwbGljYXMiLCAidmFsdWUiOiAzfV0=` 。

因此，添加该标签的 webhook 响应为：

```json
{
  "apiVersion": "admission.k8s.io/v1",
  "kind": "AdmissionReview",
  "response": {
    "uid": "<value from request.uid>",
    "allowed": true,
    "patchType": "JSONPatch",
    "patch": "W3sib3AiOiAiYWRkIiwgInBhdGgiOiAiL3NwZWMvcmVwbGljYXMiLCAidmFsdWUiOiAzfV0="
  }
}
```
