# Python HTTP请求重试机制

## 概述

我们都知道，Python 中有一个非常强大的 HTTP 请求的第三方库，就是 `requests` 库。

`requests` 库可以帮助我们轻松的发送各种 HTTP 请求。

但是，我们都知道，HTTP 是一种网络协议，既然依赖网络，那就一定不会是永远稳定的。

因此，我们经常需要做的一个事情就是在发送请求时，可以增加容错机制，而最常用的容错机制就是 **重试** 了。

在本文中，我们将会讲解如何优雅的使用 `requests` 库进行请求重试。

## HTTPAdapter 与 Retry

对于 `requests` 库而言，添加重启策略其实很简单，我们仅需要创建一个 HTTPAdapter 并传递 Session 生效即可。

一个 demo 示例如下：

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)

response = session.get("https://en.wikipedia.org/w/api.php")
```

对于一个默认的 Retry 类而言，本身已经提供了相对合理的默认值，但是它其实是高度可配置的。

下面，我们来详细说明一下 Retry 类可以接收的配置参数。

 - total: 总计重试的次数，默认为10。
 - status_forcelist: 针对指定的 HTTP 响应码进行重试，默认为 [413, 429, 503]。
 - method_whitelist: 需要进行重试的 HTTP 请求类型，默认为除去 POST 之外的外部类型。
 - backoff_factor: 用于表示在请求失败后多长时间后进行重试，计算规则为 backoff_factor * (2 ** ({number of total retries} - 1))

