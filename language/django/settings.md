# Django配置文件详解

在本文中，我们主要来讲解Django的配置文件。

Django 的配置文件包含 Django 应用的所有配置项。
本文档介绍配置是如何生效的，以及哪些设置项是可配置的。

## 配置文件位置

在我们创建一个django项目时，会在django项目目录下创建一个与项目同名的文件夹，并在该文件夹下有一个`settings.py`文件。

这个`settings.py`就是我们项目的默认配置文件。

## 配置文件字段说明

### DEBUG

默认为False。表示是否开启调试模式，布尔值。

Ps: 永远不要在 DEBUG 开启的情况下将网站部署到生产中。

调试模式的主要功能之一是显示详细的错误页面。如果你的应用程序在 DEBUG 为 True 时引发了异常，Django 会显示一个详细的回溯，包括很多关于你的环境的元数据，比如所有当前定义的 Django 配置（来自 settings.py）。

### ALLOWED_HOSTS

声明当前 Django 网站可以服务的主机 / 域名的字符串列表。

这个列表中的值可以是完全限定的名称（例如 'www.example.com），在这种情况下，它们将与请求的 Host 头完全匹配（不区分大小写，不包括端口）。

以`.`开头的值可以用作子域通配符，例如: '.example.com' 将匹配 example.com、www.example.com 和 example.com 的任何其他子域。

'*' 的值将匹配任何东西，在这种情况下，你要负责提供你自己的 Host 头的验证。

Ps：

1. 当 DEBUG为`True` 和 ALLOWED_HOSTS 为空时，主机将根据 ['.localhost', '127.0.0.1', '[::1]'] 进行验证。
2. 当 DEBUG为`False`时，ALLOWED_HOSTS不允许为空。

### INSTALLED_APPS

一个字符串的列表，表示在这个 Django 项目中所有被启用的应用。

默认的应用包括：

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Ps: 需要注意的是，所有自己创建的应用都需要添加至 `INSTALLED_APPS` 中，应用才能生效。


### MIDDLEWARE

MIDDLEWARE表示需要用到的中间件列表，默认为：

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```


### TEMPLATES

一个包含所有 Django 模板引擎的配置的列表。列表中的每一项都是一个字典，包含了各个引擎的选项。

默认为：

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```


### DATABASES

一个包含所有数据库配置的字典，用于 Django。它是一个嵌套的字典，其内容是将一个数据库别名映射到一个包含单个数据库选项的字典中。

DATABASES默认的配置为：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

它表示使用项目目录下的`db.sqlite3`文件作为sqlite数据库进行数据存储。

当连接到其他数据库后端时，如 MariaDB、MySQL、Oracle 或 PostgreSQL，将需要额外的连接参数。

例如，一个PostgreSQL的配置如下：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

### LANGUAGE_CODE

表示当前项目的语言，默认为`en-us`，表示美国英语。

如果想改为中文，可以设置为`zh-hans`。

Ps: USE_I18N 必须是激活状态，该配置才会有效果。


### TIME_ZONE

表示当前项目的时区，默认为`UTC`时间。

为了能使得项目时间本土化，我们可以把TIME_ZONE的值设置为`Asia/Shanghai`。


## 指定配置文件

上文提到过，与项目同名的文件夹下的`settings.py`文件是Django项目默认的配置文件。

但有时我们希望指定某个其他文件为配置文件时，可以通过`DJANGO_SETTINGS_MODULE`环境变量进行设置。

`DJANGO_SETTINGS_MODULE` 的值是一个符合 Python 语法的路径，例如 `mysite.settings`。

Ps：要注意配置模块应位于 Python 的 import 搜索路径 中。

## 在项目代码内使用settings

在具体的Django应用中, 通过引入 django.conf.settings 使用配置, 例:

```python
from django.conf import settings

if settings.DEBUG:
    # Do something
    pass
```
