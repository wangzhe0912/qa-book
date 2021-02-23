# DjangoRestFramework快速入门

## 概述

在我们之前的讲解中，我们曾经提到过目前大部分的项目是前后端分离的，即后端提供标准的接口，前端通过调用接口获取数据并进行渲染。

同时，随时目前微服务架构的不断流行，一个项目中可能会包含很多个功能模块，多个功能模块之间大部分也都是通过接口进行相互调用的。

而之前我们一直学习的View层其实更注重于Template渲染等相关的功能。

为了能够更加方便的实现标准化的HTTP接口，Django提供了一套专门的框架Django REST Framework用于快速提供REST风格的HTTP接口供外部访问。

## Django REST Framework概述

Django REST Framework提供了一套丰富的框架，可以让我们轻松的：

1. 提供标准的开放API
2. 配置合适的权限控制

## 安装

Step1: 安装Django REST Framework相关的依赖库

```shell
pip3 install djangorestframework
pip3 install markdown
pip3 install django-filter
```

Step2: 在项目的`settings.py`的`INSTALLED_APPS`中增加`rest_framework`。

Step3: 添加REST接口页面的登录、退出视图注册到项目的`urls.py`中:

```python
urlpatterns = [
    ...
    path(r'^api-auth/', include("rest_framework.urls")),
]
```

Step4: 在项目的`settings.py`文件中增加`REST_FRAMEWORK`相关配置：

```python
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
```

上述配置表示rest framework的默认接口权限为标准的auth鉴权且针对未授权用户开放只读权限。

到此为止，我们的Django REST Framework就已经开发完成了。

## Django REST Framework快速上手

下面，我们来通过一个实例演示如何通过Django REST Framework来提供对应的接口。

其实，使用过程非常简单，我们只需要将对应的model注册到url中即可，省去了View的阶段。

具体来说，修改项目的`urls.py`文件，增加如下内容：

```python
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User                                        # 对应哪个模型
        fields = ['url', 'username', 'email', 'is_staff']   # 返回哪些字段

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'jobs', JobViewSet)


urlpatterns = [
    ...
    path('api/', include(router.urls)),
]
```

可以看到，我们在上述代码中，分别创建了User和Job的Serializer和ViewSet，并将其注册到路由。

此时，直接访问`http://127.0.0.1:8080/api/` 地址，你就已经可以看到REST Framework相关的API页面并进行操作了。

## Django REST Framework自定义接口

可以看到，在上面的例子中，我们会非常少的代码就实现了将模型映射到接口中，并对外提供。

但你应该会发现，上面的例子中仅仅是将模型映射到接口并直接对外暴露，这会导致我们无法加入自定义的业务逻辑。

例如，有时我们一个业务操作可能会涉及到多张表的增、删、改、查操作等，这时应该怎么处理呢？

Django REST Framework其实也提供了一种自定义接口逻辑的方法，我们以下面的例子进行说明：

```python
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_self_task(request):
    """
    # 获取当前的设备的Task任务
    """
    if request.method == "GET":
        host_ip = request.GET["host_ip"]
    else:
        host_ip = request.data["host_ip"]
    return Response({"code": 200, "host_ip": host_ip})


urlpatterns = [
    path('api/get_self_task', get_self_task)
]
```

可以看到，在上面的例子中，我们定义了一个`get_self_task`函数，这个函数可以接收GET和POST请求。

对于GET请求，从url中获取host_ip信息，对于POST请求，从body中获取host_ip信息，并将相关结果进行返回。

其中，`@permission_classes([IsAuthenticated])`是必不可少的，因为我们之前的`settings.py` 中设置的相关权限的配置，因此需要在所有自定义的api_view函数中都需要增加该装饰器。


## 参考资源

1. [Django REST Framework官方](https://www.django-rest-framework.org)

