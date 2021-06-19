# Linux 下添加定时任务

很多时候，我们需要在 Linux 系统中添加各种各样的定时任务。
比如定时数据备份等一系列操作。

那么，本文将会讲解如何在 Linux 系统中添加定时任务。

## 一次性定时任务

一次性定时任务是指希望在一个指定的时间点执行一个某个任务/命令。

一次性定时任务的投放比较简单，主要用到了 `at` 命令。

首先，在终端输入 `at ${time}` 表示将在指定时间投放命令。

例如: `at 18:45`。

接下来，会进入一个交互式的命令行中可以输入想要执行的命令，例如:

```shell
echo "123" > /tmp/task
```

然后，按 Control + D 提交对应的任务。

此时，我们可以通过 `atq` 命令查询当前等待执行的定时任务。

等到了我们具体设定的时间后，之前提交的定时命令则会按时执行。

## 周期性定时任务

除了一次性定时任务外，我们其实更常用的是一个周期性的定时任务。

比如每天临晨3点进行一次数据备份，每周一上午10点清理一次日志等等，这些都要用到定时任务。

对于周期性定时任务而言，我们需要用到的命令则是 `crontab`。

例如，配置定时任务: `crontab -e`，查看现有的定时任务: `crontab -l` 等。

周期性定时任务中，配置文件的格式如下：

```shell
分钟 小时 日期 月份 星期 执行的命令
```

也就是说，每个周期性定时任务都对应上述六个字段。

例如:

```shell
* * * * * /usr/bin/date >> /tmp/date.txt
```

上述配置表示在每分钟都执行一次 `date` 命令，并将标准输出追加到 `/tmp/date.txt` 文件中。

Ps: 在指定 `分钟 小时 日期 月份 星期` 时，可以用 `*` 表示通配。

想要看到周期性定时任务的执行详情，可以查询 `/var/log/cron` 文件进行查询。

此外，在指定 `分钟 小时 日期 月份 星期` 时，还可以用 `,` 或 `-` 来进行一些更通用的表示。

例如:

```shell
* * * * 1,3 /usr/bin/date >> /tmp/date.txt
```

上述配置表示在每周一和周三每分钟都执行一次 `date` 命令，并将标准输出追加到 `/tmp/date.txt` 文件中。

```shell
* * * * 1-5 /usr/bin/date >> /tmp/date.txt
```

上述配置表示在每周一到周五每分钟都执行一次 `date` 命令，并将标准输出追加到 `/tmp/date.txt` 文件中。

Ps: 定时任务的配置文件其实是存储在 `/var/spool/cron/` 目录下，文件名为定时任务创建的用户的用户名。


## 任务加锁 flock

很多时候，我们不希望一个命令再上一次运行还没有退出的时候，下一次运行就被启动了起来。

这个时候，一种常用的处理方法是用一个 "锁" 机制。

而在 Linux 中， flock 就是一个可以直接使用的锁工具。

我们可以准备一个脚本 `sleep.sh`:

```shell
#!/usr/bin/env bash
sleep 1000
```

使用如下命令执行:

```shell
flock -xn "/tmp/sleep.lock" -c "bash sleep.sh"
```

此时，该命令会一直前台执行并始终等待。

这时，我们再打开一个新的终端，执行相同的命令:

```shell
flock -xn "/tmp/sleep.lock" -c "bash sleep.sh"
```

你会发现这个命令立马就退出了，这是因为之前的进程已经对文件进行了加锁，新的命令获取不到文件锁，直接退出了。

此时，如果停止掉之前启动的命令，再次再新窗口中启动该命令时，你会发现命令已经可以正常运行了。