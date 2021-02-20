# micro-python环境联网与HTTP请求

我们已经了解了micro-python在ESP32S开发板上的一些基本使用了。

下面，我们要做的是对ESP32S开发版联网，并尝试发送http请求。

## micro-python联网

```python
import network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)   # 启用wifi模块
wifi.scan()         # 扫描当前可用的wifi网络
wifi.isconnected()  # 判断当前wifi是否连接
wifi.connect('你家中Wi-Fi的SSID', '你家中Wi-Fi密码')  # 连接wifi 
wifi.isconnected()  # 判断当前wifi是否连接
```

需要说明的是：

```python
wifi.connect('你家中Wi-Fi的SSID', '你家中Wi-Fi密码')
```

是一个异步连接Wifi的任务，可能该命令执行完成后，wifi仍然处于连接中，此时查询connect状态仍然是False，需要等待一阵查询才能成为True。

Ps：**重要说明，wifi的开启与连接仅限于本次运行中，对开发板断电重连后，需要重新开启WIfi。**

## micro-python中的HTTP请求

在micro-python中，内置了一个urequests库。

它与Python中的requests库非常类似，使用方式几乎一致。

例如：

```python
import urequests as requests
res = requests.get(url='http://www.baidu.com/')
print(res.content)
```
