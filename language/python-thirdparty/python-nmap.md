# python-nmap进行端口扫描

python-nmap是一个Python第三方库，可以用于使用nmap进行端口扫描。

它可以轻松地操作nmap进行扫描，对于想要自动执行扫描任务和报告的系统管理员而言，它将是一个理想的工具，同时它还支持nmap脚本输出。

## 安装

python-nmap作为一个Python的第三方库可以用Python标准的包管理工具进行安装：

```bash
pip3 install python-nmap
```

## 快速使用

```python
import nmap # import nmap.py module


nm = nmap.PortScanner() # 实例化 nmap.PortScanner 对象
nm.scan('127.0.0.1', '22-443') # 扫描 127.0.0.1 的 22 至 443 端口
nm.command_line() # 获取命令行指令 : nmap -oX - -p 22-443 127.0.0.1
nm.scaninfo() # 获取 nmap 扫描信息 {'tcp': {'services': '22-443', 'method': 'connect'}}
nm.all_hosts() # 获取扫描到的所有机器
nm['127.0.0.1'].hostname() # get one hostname for host 127.0.0.1, usualy the user record
nm['127.0.0.1'].hostnames() # get list of hostnames for host 127.0.0.1 as a list of dict
# [{'name':'hostname1', 'type':'PTR'}, {'name':'hostname2', 'type':'user'}]
nm['127.0.0.1'].hostname() # get hostname for host 127.0.0.1
nm['127.0.0.1'].state() # get state of host 127.0.0.1 (up|down|unknown|skipped)
nm['127.0.0.1'].all_protocols() # get all scanned protocols ['tcp', 'udp'] in (ip|tcp|udp|sctp)
nm['127.0.0.1']['tcp'].keys() # get all ports for tcp protocol
nm['127.0.0.1'].all_tcp() # get all ports for tcp protocol (sorted version)
nm['127.0.0.1'].all_udp() # get all ports for udp protocol (sorted version)
nm['127.0.0.1'].all_ip() # get all ports for ip protocol (sorted version)
nm['127.0.0.1'].all_sctp() # get all ports for sctp protocol (sorted version)
nm['127.0.0.1'].has_tcp(22) # is there any information for port 22/tcp on host 127.0.0.1
nm['127.0.0.1']['tcp'][22] # get infos about port 22 in tcp on host 127.0.0.1
nm['127.0.0.1'].tcp(22) # get infos about port 22 in tcp on host 127.0.0.1
nm['127.0.0.1']['tcp'][22]['state'] # get state of port 22/tcp on host 127.0.0.1 (open
```

## 组合使用

```python
import nmap # import nmap.py module


nm = nmap.PortScanner()
for host in nm.all_hosts():
    print('----------------------------------------------------')
    print('Host : %s (%s)' % (host, nm[host].hostname()))
    print('State : %s' % nm[host].state())

    for proto in nm[host].all_protocols():
        print('----------')
        print('Protocol : %s' % proto)

        lport = nm[host][proto].keys()
        lport.sort()
        for port in lport:
            print('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))

print('----------------------------------------------------')
# print result as CSV
print(nm.csv())


print('----------------------------------------------------')
# If you want to do a pingsweep on network 192.168.1.0/24:
nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE -PA21,23,80,3389')
hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
for host, status in hosts_list:
    print('{0}:{1}'.format(host, status))


print('----------------------------------------------------')


# Asynchronous usage of PortScannerAsync
nma = nmap.PortScannerAsync()


def callback_result(host, scan_result):
    print('------------------')
    print(host, scan_result)

    
nma.scan(hosts='192.168.1.0/30', arguments='-sP', callback=callback_result)
while nma.still_scanning():
    print("Waiting ...")
    nma.wait(2) # you can do whatever you want but I choose to wait after the end of the scan
```
