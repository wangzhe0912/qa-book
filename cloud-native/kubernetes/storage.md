# Kubernetes PV/PVC/StorageClass 杂谈

在本文中，我们将会对 PV、PVC 以及 StorageClass 相关的概念与使用依次进行讲解与说明。

## 卷 Volume

在了解 PV、PVC 等概念之前，我们首先要了解的一个基础概念就是 Volume 。

在 K8s 中，Container 中的文件在磁盘上是临时存放的，这给 Container 中运行的较重要的应用程序带来一些问题。
问题之一是当容器崩溃时文件丢失，即当容器崩溃时 kubelet 会重新启动容器， 但容器会以干净的状态重启。
第二个问题会在同一 Pod 中运行多个容器时，希望多个容器之间可以共享文件。

Kubernetes 卷（Volume） 这一抽象概念能够解决这两个问题。

Kubernetes 支持很多类型的卷。 一个 Pod 可以同时使用任意数目的卷类型。
其中，临时卷类型的生命周期与 Pod 相同，但持久卷可以比 Pod 的存活期长。
即当 Pod 不再存在时，Kubernetes 也会销毁临时卷；不过 Kubernetes 不会销毁持久卷。
对于给定 Pod 中任何类型的卷，在容器重启期间数据都不会丢失。

卷的核心是一个目录，其中可能存有数据，Pod 中的容器可以访问该目录中的数据。
所采用的特定的卷类型将决定该目录如何形成的、使用何种介质保存数据以及目录中存放的内容。

使用卷时, 在 .spec.volumes 字段中设置为 Pod 提供的卷，并在 .spec.containers[*].volumeMounts 字段中声明卷在容器中的挂载位置。
容器中的进程看到的是由它们的 Docker 镜像和卷组成的文件系统视图。
Docker 镜像 位于文件系统层次结构的根部。各个卷则挂载在镜像内的指定路径上。
卷不能挂载到其他卷之上，也不能与其他卷有硬链接。
同时，Pod 配置中的每个容器必须独立指定各个卷的挂载位置。

下面，我们来针对一些简单的卷类型进行示例讲解。

### emptyDir 卷

emptyDir 卷是一种最简单的卷了，它本身没有其他任何的外部依赖，可以在 K8s 集群中直接使用。

当 Pod 分派到某个 Node 上时，emptyDir 卷会被创建，并且在 Pod 在该节点上运行期间，卷一直存在。 
就像其名称表示的那样，卷最初是空的。
尽管 Pod 中的容器挂载 emptyDir 卷的路径可能相同也可能不同，但这些容器都可以读写 emptyDir 卷中相同的文件。
当 Pod 因为某些原因被从节点上删除时，emptyDir 卷中的数据也会被永久删除。

emptyDir 卷看起来非常简单，那它有什么用呢？

 - 缓存空间，例如基于磁盘的归并排序。
 - 为耗时较长的计算任务提供检查点，以便任务能方便地从崩溃前状态恢复执行。
 - 在 Web 服务器容器服务数据时，保存内容管理器容器获取的文件。

取决于你的环境，emptyDir 卷存储在该节点所使用的介质上；这里的介质可以是磁盘或 SSD 或网络存储。
此外，你可以将 emptyDir.medium 字段设置为 "Memory"，以告诉 Kubernetes 为你挂载 tmpfs（基于 RAM 的文件系统）。
虽然 tmpfs 速度非常快，但是要注意它与磁盘不同。
tmpfs 在节点重启时会被清除，并且你所写入的所有文件都会计入容器的内存消耗，受容器内存限制约束。

一个使用 emptyDir 的示例 Pod 如下:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: k8s.gcr.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir: {}
```

### NFS 卷

nfs 卷能将 NFS (网络文件系统) 挂载到你的 Pod 中。 
不像 emptyDir 那样会在删除 Pod 的同时也会被删除，nfs 卷的内容在删除 Pod 时会被保存，卷只是被卸载。
这意味着 nfs 卷可以被预先填充数据，并且这些数据可以在 Pod 之间共享。

Ps: 与 emptyDir 卷不同，在正式使用 NFS 卷之前，你必须运行自己的 NFS 服务器并将目标 share 导出备用。

## Persistent Volume 介绍

了解了 Volume 的概念后，我们来继续了解一下什么是 Persistent Volume 。

存储的管理是一个与计算实例的管理完全不同的问题。
PersistentVolume 子系统为用户 和管理员提供了一组 API，将存储如何供应的细节从其如何被使用中抽象出来。
为了实现这点，我们引入了两个新的 API 资源：PersistentVolume 和 PersistentVolumeClaim。

持久卷（PersistentVolume，PV）是集群中的一块存储，可以由管理员事先供应，或者使用存储类（Storage Class）来动态供应。
持久卷是集群资源，就像节点也是集群资源一样。
PV 持久卷和普通的 Volume 一样，也是使用卷插件来实现的，只是它们拥有独立于任何使用 PV 的 Pod 的生命周期。

持久卷申领（PersistentVolumeClaim，PVC）表达的是用户对存储的请求。概念上与 Pod 类似。
Pod 会耗用节点资源，而 PVC 申领会耗用 PV 资源。
Pod 可以请求特定数量的资源（CPU 和内存）；同样 PVC 申领也可以请求特定的大小和访问模式
（例如，可以要求 PV 卷能够以 ReadWriteOnce、ReadOnlyMany 或 ReadWriteMany 模式之一来挂载，参见访问模式）。

尽管 PersistentVolumeClaim 允许用户消耗抽象的存储资源，
常见的情况是针对不同的需求用户需要的是具有不同属性（如，性能）的 PersistentVolume 卷。 
集群管理员需要能够提供不同性质的 PersistentVolume，并且这些 PV 卷之间的差别不仅限于卷大小和访问模式，
同时又不能将卷是如何实现的这些细节暴露给用户。 
为了满足这类需求，就有了存储类（StorageClass）资源。

## PV 和 PVC 的生命周期

PV 卷是集群中的资源，PVC 申领是对这些资源的请求，也被用来执行对资源的申领检查。 PV 卷和 PVC 申领之间的互动遵循如下生命周期：

**供应**

PV 卷的供应有两种方式：静态供应或动态供应。

静态供应是指集群管理员创建若干 PV 卷。
这些卷对象带有真实存储的细节信息，并且对集群用户可用（可见）。
PV 卷对象存在于 Kubernetes API 中，可供用户消费（使用）。

动态供应是指如果管理员所创建的所有静态 PV 卷都无法与用户的 PersistentVolumeClaim 匹配， 集群可以尝试为该 PVC 申领动态供应一个存储卷。
这一供应操作是基于 StorageClass 来实现的：PVC 申领必须请求某个存储类，同时集群管理员必须已经创建并配置了该类，这样动态供应卷的动作才会发生。
如果 PVC 申领指定存储类为 ""，则相当于为自身禁止使用动态供应的卷。

**绑定**

用户创建一个带有特定存储容量和特定访问模式需求的 PersistentVolumeClaim 对象；
在动态供应场景下，这个 PVC 对象可能已经创建完毕。
主控节点中的控制回路监测新的 PVC 对象，寻找与之匹配的 PV 卷（如果可能的话）， 并将二者绑定到一起。

如果为了新的 PVC 申领动态供应了 PV 卷，则控制回路总是将该 PV 卷绑定到这一 PVC 申领。
否则，用户总是能够获得他们所请求的资源，只是所获得的 PV 卷可能会超出所请求的配置。

一旦绑定关系建立，则 PersistentVolumeClaim 绑定就是排他性的，无论该 PVC 申领是如何与 PV 卷建立的绑定关系。
PVC 申领与 PV 卷之间的绑定是一种一对一的映射，实现上使用 ClaimRef 来记述 PV 卷 与 PVC 申领间的双向绑定关系。

如果找不到匹配的 PV 卷，PVC 申领会无限期地处于未绑定状态。当与之匹配的 PV 卷可用时，PVC 申领会被绑定。 
例如，即使某集群上供应了很多 50 Gi 大小的 PV 卷，也无法与请求 100 Gi 大小的存储的 PVC 匹配。
当新的 100 Gi PV 卷被加入到集群时，该 PVC 才有可能被绑定。

**使用**

Pod 将 PVC 申领当做存储卷来使用。集群会检视 PVC 申领，找到所绑定的卷，并为 Pod 挂载该卷。
对于支持多种访问模式的卷，用户要在 Pod 中以卷的形式使用申领时指定期望的访问模式。

一旦用户有了申领对象并且该申领已经被绑定，则所绑定的 PV 卷在用户仍然需要它期间一直属于该用户。
用户通过在 Pod 的 volumes 块中包含 persistentVolumeClaim 节区来指定 Pod 访问所申领的 PV 卷。

**保护使用中的存储对象**

保护使用中的存储对象（Storage Object in Use Protection）这一功能特性的目的是确保
仍被 Pod 使用的 PersistentVolumeClaim（PVC）对象及其所绑定的 PersistentVolume（PV）对象在系统中不会被删除，
因为这样做可能会引起数据丢失。

Ps: 当使用某 PVC 的 Pod 对象仍然存在时，认为该 PVC 仍被此 Pod 使用。

如果用户删除被某 Pod 使用的 PVC 对象，该 PVC 申领不会被立即移除。
PVC 对象的移除会被推迟，直至其不再被任何 Pod 使用。
此外，如果管理员删除已绑定到某 PVC 申领的 PV 卷，该 PV 卷也不会被立即移除。
PV 对象的移除也要推迟到该 PV 不再绑定到 PVC。

你可以看到当 PVC 的状态为 Terminating 且其 Finalizers 列表中包含 kubernetes.io/pvc-protection 时，PVC 对象是处于被保护状态的。

```shell
kubectl describe pvc hostpath
# Name:          hostpath
# Namespace:     default
# StorageClass:  example-hostpath
# Status:        Terminating
# Volume:
# Labels:        <none>
# Annotations:   volume.beta.kubernetes.io/storage-class=example-hostpath
#                volume.beta.kubernetes.io/storage-provisioner=example.com/hostpath
# Finalizers:    [kubernetes.io/pvc-protection]
# ...
```

**回收**

当用户不再使用其存储卷时，他们可以从 API 中将 PVC 对象删除，从而允许该资源被回收再利用。
PersistentVolume 对象的回收策略告诉集群，当其被从申领中释放时如何处理该数据卷。
目前，数据卷可以被 Retained（保留）、 Deleted（删除） 或 Retain（保留，即将废弃，建议用动态供应替换）。

回收策略 Retain 使得用户可以手动回收资源。
当 PersistentVolumeClaim 对象被删除时，PersistentVolume 卷仍然存在，对应的数据卷被视为"已释放（released）"。
由于卷上仍然存在这前一申领人的数据，该卷还不能用于其他申领。
管理员可以通过下面的步骤来手动回收该卷：

1. 删除 PersistentVolume 对象。此时，与之相关的、位于外部基础设施中的存储资产 （例如 AWS EBS、GCE PD、Azure Disk 或 Cinder 卷）在 PV 删除之后仍然存在。
2. 根据情况，手动清除所关联的存储资产上的数据。
3. 手动删除所关联的存储资产；如果你希望重用该存储资产，可以基于存储资产的定义创建新的 PersistentVolume 卷对象。

删除策略 Delete 会将 PersistentVolume 对象从 Kubernetes 中移除，
同时也会从外部基础设施（如 AWS EBS、GCE PD、Azure Disk 或 Cinder 卷）中移除所关联的存储资产。
动态供应的卷会继承其 StorageClass 中设置的回收策略，该策略默认为 Delete。

**预留PV**

通过在 PersistentVolumeClaim 中指定 PersistentVolume，你可以声明该特定 PV 与 PVC 之间的绑定关系。
如果该 PersistentVolume 存在且未被通过其 claimRef 字段预留给 PersistentVolumeClaim，
则该 PersistentVolume 会和该 PersistentVolumeClaim 绑定到一起。

此时，绑定操作不会考虑某些卷匹配条件是否满足，包括节点亲和性等等。
但是，控制面仍然会检查存储类、访问模式和所请求的存储尺寸都是合法的。

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: foo-pvc
  namespace: foo
spec:
  storageClassName: "" # 此处须显式设置空字符串，否则会被设置为默认的 StorageClass
  volumeName: foo-pv
  ...
```

此方法无法对 PersistentVolume 的绑定特权做出任何形式的保证。
如果有其他 PersistentVolumeClaim 可以使用你所指定的 PV，则你应该首先预留该存储卷。
你可以将 PV 的 claimRef 字段设置为相关的 PersistentVolumeClaim 以确保其他 PVC 不会绑定到该 PV 卷。

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: foo-pv
spec:
  storageClassName: ""
  claimRef:
    name: foo-pvc
    namespace: foo
  ...
```

如果你想要使用 claimPolicy 属性设置为 Retain 的 PersistentVolume 卷时，包括你希望复用现有的 PV 卷时，这点是很有用的。


**扩充PVC申领**

当我们 PVC 已经申请下来后，如果发现卷的大小不足时，还可以对 PVC 申请进行扩容。

目前支持 PVC 的卷类型包括：

 - gcePersistentDisk
 - awsElasticBlockStore
 - Cinder

等等。

只有当 PVC 的存储类中将 allowVolumeExpansion 设置为 true 时，你才可以扩充该 PVC 申领。例如：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gluster-vol-default
provisioner: kubernetes.io/glusterfs
parameters:
  resturl: "http://192.168.10.100:8080"
  restuser: ""
  secretNamespace: ""
  secretName: ""
allowVolumeExpansion: true
```

如果要为某 PVC 请求较大的存储卷，可以编辑 PVC 对象，设置一个更大的尺寸值。
这一编辑操作会触发为下层 PersistentVolume 提供存储的卷的扩充。

Ps: Kubernetes 不会创建新的 PV 卷来满足此申领的请求，而是将现有的卷调整大小。


## 持久卷类型

PV 持久卷是用插件的形式来实现的。Kubernetes 目前支持以下插件：

 - local - 节点上挂载的本地存储设备
 - csi - 容器存储接口 (CSI)
 - glusterfs - Glusterfs 卷
 - cephfs - CephFS volume

等等。

## 持久卷属性

每个 PV 对象都包含 spec 部分和 status 部分，分别对应卷的规约和状态。
PersistentVolume 对象的名称必须是合法的 DNS 子域名.

示例如下：

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv0003
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: slow
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    path: /tmp
    server: 172.17.0.2
```

Ps: 在集群中使用持久卷存储通常需要一些特定于具体卷类型的辅助程序。
在这个例子中，PersistentVolume 是 NFS 类型的，因此需要辅助程序 /sbin/mount.nfs 来支持挂载 NFS 文件系统。

### capacity

一般而言，每个 PV 卷都有确定的存储容量。 容量属性是使用 PV 对象的 capacity 属性来设置的。

目前，存储大小是可以设置和请求的唯一资源。 未来可能会包含 IOPS、吞吐量等属性。

### volumeMode

针对 PV 持久卷，Kubernetes 支持两种 volumeMode : 

 - Filesystem
 - Block

其中，volumeMode 是一个可选的 API 参数，默认为 Filesystem 。

volumeMode 属性设置为 Filesystem 的卷会被 Pod 挂载（Mount） 到某个目录。
如果卷的存储来自某块设备而该设备目前为空，Kuberneretes 会在第一次挂载卷之前 在设备上创建文件系统。

### accessModes

PersistentVolume 卷可以用资源提供者所支持的任何方式挂载到宿主系统上。
提供者（驱动）的能力不同，每个 PV 卷的访问模式都会设置为对应卷所支持的模式值。
例如，NFS 可以支持多个读写客户，但是某个特定的 NFS PV 卷可能在服务器上以只读的方式导出。
每个 PV 卷都会获得自身的访问模式集合，描述的是特定 PV 卷的能力。

其中，访问模式包括：

 - ReadWriteOnce -- 卷可以被一个节点以读写方式挂载；
 - ReadOnlyMany -- 卷可以被多个节点以只读方式挂载；
 - ReadWriteMany -- 卷可以被多个节点以读写方式挂载。

### persistentVolumeReclaimPolicy

目前的回收策略有：

 - Retain -- 手动回收
 - Recycle -- 基本擦除 (rm -rf /thevolume/*)
 - Delete -- 诸如 AWS EBS、GCE PD、Azure Disk 或 OpenStack Cinder 卷这类关联存储资产也被删除

目前，仅 NFS 和 HostPath 支持回收（Recycle）。 AWS EBS、GCE PD、Azure Disk 和 Cinder 卷都支持删除（Delete）。

### storageClassName

每个 PV 可以属于某个类（Class），通过将其 storageClassName 属性设置为某个 StorageClass 的名称来指定。 
特定类的 PV 卷只能绑定到请求该类存储卷的 PVC 申领。
未设置 storageClassName 的 PV 卷没有类设定，只能绑定到那些没有指定特定存储类的 PVC 申领。

### mountOptions

Kubernetes 管理员可以指定持久卷被挂载到节点上时使用的附加挂载选项。

Ps: 并非所有持久卷类型都支持挂载选项。

Kubernetes 不对挂载选项执行合法性检查。如果挂载选项是非法的，挂载就会失败。

### nodeAffinity

对于 local 类型的挂载，我们还可以指定 nodeAffinity 。
Kubernetes 调度器使用 PersistentVolume 的 nodeAffinity 信息来将使用 local 卷的 Pod 调度到正确的节点。

示例如下：

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: example-pv
spec:
  capacity:
    storage: 100Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Delete
  storageClassName: local-storage
  local:
    path: /mnt/disks/ssd1
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - example-node
```

### Phase

每个卷会处于以下阶段（Phase）之一：

 - Available（可用）-- 卷是一个空闲资源，尚未绑定到任何申领；
 - Bound（已绑定）-- 该卷已经绑定到某申领；
 - Released（已释放）-- 所绑定的申领已被删除，但是资源尚未被集群回收；
 - Failed（失败）-- 卷的自动回收操作失败。

其中，命令行接口能够显示绑定到某 PV 卷的 PVC 对象。

## PVC 介绍

每个 PVC 对象都有 spec 和 status 部分，分别对应申领的规约和状态。
PersistentVolumeClaim 对象的名称必须是合法的 DNS 子域名.

一个示例 PVC 如下：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 8Gi
  storageClassName: slow
  selector:
    matchLabels:
      release: "stable"
    matchExpressions:
      - {key: environment, operator: In, values: [dev]}
```


## PVC 用于 Volume

Pod 可以将 PVC 作为卷来使用，并藉此访问存储资源。
申领必须位于使用它的 Pod 所在的同一名字空间内。 
集群在 Pod 的名字空间中查找申领，并使用它来获得申领所使用的 PV 卷。 之后，卷会被挂载到宿主上并挂载到 Pod 中。

示例如下：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: myfrontend
      image: nginx
      volumeMounts:
      - mountPath: "/var/www/html"
        name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: myclaim
```

## StorageClass 介绍

StorageClass 为管理员提供了描述存储 "类" 的方法。 
不同的类型可能会映射到不同的服务质量等级或备份策略，或是由集群管理员制定的任意策略。
Kubernetes 本身并不清楚各种类代表的什么。这个类的概念在其他存储系统中有时被称为 "配置文件"。

## StorageClass 说明

每个 StorageClass 都包含 provisioner、parameters 和 reclaimPolicy 字段， 
这些字段会在 StorageClass 需要动态分配 PersistentVolume 时会使用到。

StorageClass 对象的命名很重要，用户使用这个命名来请求生成一个特定的类。
当创建 StorageClass 对象时，管理员设置 StorageClass 对象的命名和其他参数，一旦创建了对象就不能再对其更新。

管理员可以为没有申请绑定到特定 StorageClass 的 PVC 指定一个存储类，例如:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
reclaimPolicy: Retain
allowVolumeExpansion: true
mountOptions:
  - debug
volumeBindingMode: Immediate
```

### provisioner

每个 StorageClass 都有一个 Provisioner ，它用来决定使用哪个卷插件制备 PV ，该字段必须指定。

kubernetes 内置了一系列 Provisioner ，但是如果内置的 Provisioner 如果无法满足你的使用场景，
你还可以运行和指定外部制备器，这些独立的程序遵循由 Kubernetes 定义的规范。

### reclaimPolicy

由 StorageClass 动态创建的 PersistentVolume 会在类的 reclaimPolicy 字段中指定回收策略，可以是 Delete 或者 Retain。
如果 StorageClass 对象被创建时没有指定 reclaimPolicy，它将默认为 Delete。

通过 StorageClass 手动创建并管理的 PersistentVolume 会使用它们被创建时指定的回收政策。

### allowVolumeExpansion

PersistentVolume 可以配置为可扩展。将此功能设置为 true 时，允许用户通过编辑相应的 PVC 对象来调整卷大小。

当下层 StorageClass 的 allowVolumeExpansion 字段设置为 true 时，部分类型的卷支持卷扩展。

### mountOptions

由 StorageClass 动态创建的 PersistentVolume 将使用类中 mountOptions 字段指定的挂载选项。

如果卷插件不支持挂载选项，却指定了挂载选项，则 provisioner 操作会失败。

挂载选项在 StorageClass 和 PV 上都不会做验证，如果其中一个挂载选项无效，那么这个 PV 挂载操作就会失败。

### volumeBindingMode

volumeBindingMode 字段控制了卷绑定和动态提供 PV 应该发生在什么时候。

默认情况下，Immediate 模式表示一旦创建了 PersistentVolumeClaim 也就完成了卷绑定和动态制备。
对于由于拓扑限制而非集群所有节点可达的存储后端，PersistentVolume 会在不知道 Pod 调度要求的情况下绑定或者制备。

集群管理员可以通过指定 WaitForFirstConsumer 模式来解决此问题。
该模式将延迟 PersistentVolume 的绑定和制备，直到使用该 PersistentVolumeClaim 的 Pod 被创建。
PersistentVolume 会根据 Pod 调度约束指定的拓扑来选择或制备。

## 动态卷供应

动态卷供应允许按需创建 PV 。
如果没有动态供应，集群管理员必须手动地联系他们的云或存储提供商来创建新的存储卷，
然后在 Kubernetes 集群创建 PersistentVolume 对象来表示这些卷。
动态供应功能消除了集群管理员预先配置存储的需要。 
相反，它在用户请求时自动供应存储。

动态卷供应的实现基于 storage.k8s.io API 组中的 StorageClass API 对象。
集群管理员可以根据需要定义多个 StorageClass 对象，每个对象指定一个 provisioner， provisioner 向卷供应商提供在创建卷时需要的数据卷信息及相关参数。

要启用动态供应功能，集群管理员需要为用户预先创建一个或多个 StorageClass 对象。
StorageClass 对象定义当动态供应被调用时，哪一个驱动将被使用和哪些参数将被传递给驱动。

示例如下：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
```

用户通过在 PersistentVolumeClaim 中包含存储类来请求动态供应的存储。
用户现在能够而且应该使用 PersistentVolumeClaim 对象的 storageClassName 字段。
这个字段的值必须能够匹配到集群管理员配置的 StorageClass 名称，示例如下：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: claim1
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: slow
  resources:
    requests:
      storage: 30Gi
```

该声明会自动供应一块类似 SSD 的永久磁盘。 在删除该声明后，这个卷也会被销毁。

此外，可以在群集上启用动态卷供应，以便在未指定存储类的情况下动态设置所有声明。
集群管理员可以通过以下方式启用此行为：

 - 标记一个 StorageClass 为默认；
 - 确保 DefaultStorageClass 准入控制器在 API 服务端被启用。

管理员可以通过向其添加 storageclass.kubernetes.io/is-default-class 注解来将特定的 StorageClass 标记为默认。 
当集群中存在默认的 StorageClass 并且用户创建了一个未指定 storageClassName 的 PersistentVolumeClaim 时，
DefaultStorageClass 准入控制器会自动向其中添加指向默认存储类的 storageClassName 字段。

Ps: 群集上最多只能有一个 默认存储类，否则无法创建没有明确指定 storageClassName 的 PersistentVolumeClaim。

## 实战演示

下面，我们通过一个示例来演示 PV、PVC 以及 StorageClass 的相关功能与使用。

### local-path-provisioner 部署

为了能够正常使用 PV 相关的功能，我们首先需要搭建一个 Provisioner 服务来给我们提供持久卷。

此处，我们使用 local-path-provisioner 来提供持久卷，官方文档请参考 [local-path-provisioner](https://github.com/rancher/local-path-provisioner) 。

```shell
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
```

在该 yaml 中，定义了 local-path-provisioner 的 Namespace, ServiceAccount, ClusterRole, ClusterRoleBinding, 
Deployment, ConfigMap 以及 StorageClass 。

其中，我们重点关注一下 StorageClass 对象的配置信息：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-path
provisioner: rancher.io/local-path
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
```

根据之前的学习内容，我们可以知道，在这个 yaml 中，我们定义了一个 StorageClass ，名称是 local-path ，
reclaimPolicy 为 Delete，volumeBindingMode为 PVC 被声明使用时才创建。

接下来，我们可以查询 Pod 的状态，直到 Pod 成功运行：

```shell
kubectl -n local-path-storage get pod
```

此时，我们依赖的 provisioner 已经部署完成，同时 StorageClass 也已经创建好了，下面，我们就具体来演示一下如何使用吧！

### 使用 StorageClass 自动创建 PV 并绑定

第一步，我们首先需要创建一个 PVC 用于申请一块磁盘资源，示例 yaml 文件如下：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: wangzhe-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: local-path
  volumeMode: Filesystem
```

接下来，我们可以 apply 该 yaml 文件使其生效:

```shell
kubectl apply -f pvc.yaml
```

此时，查询该对应的 pvc 的状态，可以发现该状态其实是 unbound 的。

```shell
kubectl get pvc
```

这时由于在安装 provisioner 时，对应创建的 StorageClass 中 volumeBindingMode 配置是 WaitForFirstConsumer 而不是 Immediate 导致的。

下面，我们来创建一个 Deployment ，其中该 Pod 使用了刚刚创建的 PVC，yaml 文件内容如下:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flaskapp-pvc
spec:
  selector:
    matchLabels:
      app: flaskapp-pvc
  replicas: 1
  template:
    metadata:
      labels:
        app: flaskapp-pvc
    spec:
      containers:
      - name: flaskapp
        image: dustise/flaskapp
        imagePullPolicy: IfNotPresent
        env:
        - name: version
          valueFrom:
            configMapKeyRef:
              name: game-demo
              key: player_initial_lives
        volumeMounts:
        - name: config
          mountPath: "/config"
          readOnly: true
      volumes:
        - name: config
          persistentVolumeClaim:
            claimName: wangzhe-pvc
```

可以看到，在该 yaml 文件的 Pod spec 配置中，我们定义了一个 volumes，并关联到了我们刚才创建的 PVC 上。
同时，我们还将该 Volume 挂载到了Container的指定目录下。

下面，我们 apply 该 yaml 文件:

```shell
kubectl apply -f flask_deployments.yaml
```

此时，再次查询对应的 PVC 的状态，就可以发现对应的 PVC 的状态已经是 Bound 了，同样，进入容器后，你也可以看到对应的卷。

Ps: 删除 Pod / Deployment 时，不会自动删除对应的 PV 和 PVC 。如果希望删除指定的 PV / PVC ，需要主动来指定并删除它们。

### 手动创建 PV 并绑定和使用

除了通过 StorageClass 来自动动态生成 PV 之外，我们来可以主动申请 PV 并绑定 PVC 和使用。

首先，创建 `pv.yaml` 文件如下：

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: wangzhe-pv
spec:
  accessModes:
  - ReadWriteOnce
  capacity:
    storage: 10Gi
  claimRef:
    apiVersion: v1
    kind: PersistentVolumeClaim
    name: wangzhe-pvc-2
    namespace: books
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - hostname1
  persistentVolumeReclaimPolicy: Delete
  storageClassName: ""
  volumeMode: Filesystem
  local:
    path: /home/data/wangzhe-pv
```

Ps: 此时，我们需要在对应的机器上创建该目录 `/home/data/wangzhe-pv` 。

接下来，查询对应的 PV 状态，预期状态应该会变为 Available 。

下面，我们来创建一个 pvc 来绑定对应的 PV。

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: wangzhe-pvc-2
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: ""
  volumeMode: Filesystem
```

此时，再次查询对应的 PV 、 PVC 状态，可以看到二者的状态都已经是 Bound 了。

下面，我们来创建对应的 Deployment 来使用对应的 PVC:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flaskapp-pvc-3
spec:
  selector:
    matchLabels:
      app: flaskapp-pvc-3
  replicas: 1
  template:
    metadata:
      labels:
        app: flaskapp-pvc-3
    spec:
      containers:
      - name: flaskapp
        image: dustise/flaskapp
        imagePullPolicy: IfNotPresent
        volumeMounts:
        - name: config
          mountPath: "/config"
          readOnly: true
      volumes:
        - name: config
          persistentVolumeClaim:
            claimName: wangzhe-pvc-2
```

下面，我们就可以进入该容器，并在目录中进行响应的操作啦~
