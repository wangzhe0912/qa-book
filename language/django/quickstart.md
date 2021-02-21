# Django快速上手

了解了Django的基本特点，并完成了相关开发环境准备后，接下来，我们将会从一个最简单的示例开始进行Django的学习。

## 创建第一个项目

Step1: 创建一个会议室管理项目，项目名称为meetingroom.

```shell
django-admin startproject meetingroom
cd meetingroom
```

Step2: 启动项目

```shell
python manage.py runserver 0.0.0.0:8080
```

Step3: 开发浏览器，访问 http://127.0.0.1:8080。

正常情况下，你会看到如下内容：

![homepage](./pictures/homepage.png)


## 初识后台管理系统

Django的一大优势是其自带了一个强大的后台管理系统，及时不写一行前端代码，也能够有一个配套的Web页面进行相关的管理操作。

下面，我们就来了解一下Django的后台管理系统吧。

打开浏览器，访问 http://127.0.0.1:8080/admin ，你将会看到如下登录框：

![login](./pictures/login.png)

但是，我们好像还没有创建任何用户呢！

下面，我们就先来创建一个用户。

创建用户之前，我们首先需要初始化Django内置表的数据库。

Ps: 由于Django默认使用了sqlite数据库，因此，再前期的实验环节，我们就不在额外搭建数据库了，而是使用默认的sqlite数据库。

初始化内置表的数据库的命令如下：

```shell
python3 manage.py migrate
# Operations to perform:
#   Apply all migrations: admin, auth, contenttypes, sessions
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying auth.0001_initial... OK
#   Applying admin.0001_initial... OK
#   Applying admin.0002_logentry_remove_auto_add... OK
#   Applying admin.0003_logentry_add_action_flag_choices... OK
#   Applying contenttypes.0002_remove_content_type_name... OK
#   Applying auth.0002_alter_permission_name_max_length... OK
#   Applying auth.0003_alter_user_email_max_length... OK
#   Applying auth.0004_alter_user_username_opts... OK
#   Applying auth.0005_alter_user_last_login_null... OK
#   Applying auth.0006_require_contenttypes_0002... OK
#   Applying auth.0007_alter_validators_add_error_messages... OK
#   Applying auth.0008_alter_user_username_max_length... OK
#   Applying auth.0009_alter_user_last_name_max_length... OK
#   Applying auth.0010_alter_group_name_max_length... OK
#   Applying auth.0011_update_proxy_permissions... OK
#   Applying auth.0012_alter_user_first_name_max_length... OK
#   Applying sessions.0001_initial... OK
```

可以看到，我们创建了admin, auth, contenttypes, sessions等相关的数据库表。

下面，我们就可以使用命令行来添加用户了：

```shell
python3 ./manage.py createsuperuser
# Username: missshi  
# Email address: wangzhe0912@tju.edu.cn
# Password: 
# Password (again): 
# Superuser created successfully.
```

可以看到，输出`createsuperuser`子命令后，会提供交互式命令行接收用户名、邮箱、密码等相关参数。

全部信息输入完成后，我们想要创建的用户也就创建完成了，下面我们可以用刚才创建的用户登录看看。

登录成功后，正常情况下你将会看到如下页面：

![main](./pictures/main.png)

可以看到，在这个页面中，我们可以看到Groups和Users两种对象，这些都是Django框架内置的功能。

此时，如果你点击Users进入到User列表页面的话，还能够看到你刚才创建的用户。

甚至，你已经可以在这个页面中进行用户、用户组的创建和管理了。是不是非常赞呢？


## 编写一个应用

下面，我们需要编写一个职位管理系统的应用，这个应用需要实现的功能为管理员能够发布职位。


### 数据建模

在应用开发前，我们首先需要对核心数据对象进行建模，即针对核心对象，设置它有哪些字段等。

对于我们的职位管理系统的应用而言，最核心的对象就是职位了。

一条职位记录应该包括如下字段：

1. 职位名称
2. 类别
3. 工作地点
4. 职位职责
5. 职位要求
6. 发布人
7. 发布日期
8. 修改日期

### 创建应用

当我们对数据建模完成后，我们就需要创建应用了。

创建应用同样用到的是`manage.py`脚本：

```shell
python manage.py startapp jobs
```

执行该命令后，我们可以看到会自动在当前目录中创建一个`jobs`的子目录。

可以看到，每个创建的app目录下都会自动生成如下文件：

```
admin.py
apps.py
models.py
tests.py
views.py
migrations目录
```

Ps: 需要注意的是，我们每创建一个应用后，需要修改整个项目的settings.py文件，并在其中的`INSTALLED_APPS`中增加对应app的名称，如`jobs`。

### 定义models文件

下面，我们需要修改jobs目录下的`models.py`文件，将我们针对职位建立的模型转化为代码写入`models.py`文件中。

```python
from django.db import models
from django.contrib.auth.models import User

JobTypes = [
    (0,"技术类"),
    (1,"产品类"),
    (2,"运营类"),
    (3,"设计类"),
    (4,"市场营销类")
]

Cities = [
    (0,"北京"),
    (1,"上海"),
    (2,"深圳"),
    (3,"杭州"),
    (4,"广州")
]

class Job(models.Model):
    """
    # 职位建模 
    """
    job_type = models.SmallIntegerField(blank=False, choices=JobTypes, verbose_name="职位类别")
    job_name = models.CharField(max_length=250, blank=False, verbose_name="职位名称")
    job_city = models.SmallIntegerField(choices=Cities, blank=False, verbose_name="工作地点")
    job_responsibility = models.TextField(max_length=1024, verbose_name="职位职责")
    job_requirement = models.TextField(max_length=1024, blank=False, verbose_name="职位要求")
    creator = models.ForeignKey(User, verbose_name="创建人", null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name="修改日期", auto_now=True)
```

其中，models中定义了多种数据格式，如SmallInteger、Char、Text、DateTime等，另外ForeignKey表示外键引用，主要用户表与表的关联，例如此处creator就对应着系统内部的用户。

上述做用到的参数的作用如下：

1. blank表示是否允许为空。
2. choices表示对于枚举类型而言可以选的值，接收一个数组参数，每个数组元素又是有(value, alias)的元组组成的。
3. verbose_name表示其别名，可以在admin管理后台中可见。
4. max_length表示字符串最大的长度。
5. on_delete参数主要用户外键引用，表示当引用的对象被删除后，相关的记录应该如何处理，SET_NULL表示关联数据被删除后，设置该字段为null。另外，当on_delete为SET_NULL时，需要设置该字段允许为空，即null=True
6. 

### 将Model注册当管理后台

上面的步骤中，我们创建了Job对应的Model相关的定义，但是为了能让我们的管理后台可以支持model的增、删、改、查等操作，我们需要将model注册到管理后台。

我们需要修改jobs目录下的`admin.py`文件:

```python
from django.contrib import admin
from jobs.models import Job

admin.site.register(Job)
```

### 同步数据库结构

上面，我们虽然已经定义了models对象，并注册到了管理后台，此时你访问管理后台应该也已经可以看到Jobs菜单了。

但是点击查询Jobs信息时，一定会看到一些报错，这是为什么呢？

答案是我们虽然定义了数据对象，但是并没有在数据库中创建对应的表，导致Django在按照数据结构进行读写数据库时一定会引发报错。

下面，我们来看一下如何同步数据库，我们还是用到了`manage.py`脚本。

Step1: 生成同步脚本

```shell
python3 ./manage.py makemigrations
```

执行该命令后，可以看到，我们会在Job对应的migrations目录下生成一个`0001_initial.py`脚本，这个就是创建数据库的工具。

Step2: 执行同步脚本，同步数据库

```shell
python3 ./manage.py migrate
```

执行该命令后，相当于执行了刚才生成的`0001_initial.py`脚本，真实的在数据库中创建了对应的job表。

### 体验一下吧

下面，我们再次打开admin后台页面，我们就已经可以直接用后台管理页面进行Job相关的管理了。
