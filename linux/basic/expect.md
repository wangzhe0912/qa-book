# 通过expect实现无交互式的远程命令执行与远程文件传输

## 背景

在很多自动化场景中，都需要解决一个交互式输入密码的问题。例如当我们需要远程执行命令、远程传输文件等场景。
expect其实就是专门用于解决交互式命令输入的工具。

## expect详解

expect是一个自动化交互套件，主要应用于执行命令和程序时，系统以交互形式要求输入指定字符串，实现交互通信。

它的自动交互流程如下：

1. spawn启动指定进程
2. expect获取指定关键字
3. send向指定程序发送指定字符
4. 执行完成退出

expect的常用命令总结如下：

|命令|介绍|
|---|---|
spawn           |    交互程序开始后面跟命令或者指定程序
expect          |    获取匹配信息匹配成功则执行expect后面的程序动作
send exp_send   |    用于发送指定的字符串信息
exp_continue   |     在expect中多次匹配就需要用到
send_user       |    用来打印输出 相当于shell中的echo
exit            |    退出expect脚本
eof             |    expect执行结束 退出
set             |    定义变量
puts            |    输出变量
set timeout     |    设置超时时间
interact 　　　　|　　 允许用户交互


## demo示例

下面，我们通过一些非常简单的demo来演示`expect`相关的使用:

```
#!/usr/bin/expect

spawn ssh wangzhe@192.168.1.22 df -Th
expect "*password"
send "123456\n"
expect eof
```

在上面的例子中，我们将会通过用户名wangzhe，密码123456登录192.168.1.22机器，然后执行df -Th命令并返回执行结果。


## expect的安装

以Ubuntu系统为例，我们可以直接使用包管理工具进行安装:

```bash
sudo apt-get install tcl tk expect
```

## 常用模板工具

### 从本地到远程机器远程文件传输

```
#!/usr/bin/expect
set timeout 10
set host [lindex $argv 0]
set username [lindex $argv 1]
set password [lindex $argv 2]
set src_file [lindex $argv 3]
set dest_file [lindex $argv 4]
spawn scp $src_file $username@$host:$dest_file
 expect {
 "(yes/no)?"
  {
    send "yes\n"
    expect "*assword:" { send "$password\n"}
  }
 "*assword:"
  {
    send "$password\n"
  }
}
expect "100%"
expect eof
```

使用方式: 

```bash
./expect_scp ${remote_host_ip} ${remote_host_user} ${remote_host_password} ${local_file} ${remote_des_file}
# example
# ./expect_scp 192.168.1.22 wangzhe 123456 mock.tar /home/wangzhe/桌面/mock.$tag.tar
```

