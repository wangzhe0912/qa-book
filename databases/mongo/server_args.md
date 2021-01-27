# MongoDB Server命令行与配置文件解析

本节中，我们会详细剖析MongoDB Server端的启动参数/配置文件。

通过本文的学习，希望你可以详细了解如何给你的MongoDB Server设置合适的配置。

## 命令行参数初识

首先，我们来通过`mongod`自带的help来大致了解一下mongod支持哪些命令行参数。

```
mongod --help
```

可以看到打印的help信息如下：

```
Options:
  --networkMessageCompressors arg (=snappy,zstd,zlib) Comma-separated list of compressors to use for network messages

General options:
  -h [ --help ]                         Show this usage information
  --version                             Show version information
  -f [ --config ] arg                   Configuration file specifying additional options
  --configExpand arg                    Process expansion directives in config file (none, exec, rest)
  --port arg                            Specify port number - 27017 by default
  --ipv6                                Enable IPv6 support (disabled by default)
  --listenBacklog arg (=128)            Set socket listen backlog size
  --maxConns arg (=1000000)             Max number of simultaneous connections
  --pidfilepath arg                     Full path to pidfile (if not set, no pidfile is created)
  --timeZoneInfo arg                    Full path to time zone info directory, e.g. /usr/share/zoneinfo
  --nounixsocket                        Disable listening on unix sockets
  --unixSocketPrefix arg                Alternative directory for UNIX domain sockets (defaults to /tmp)
  --filePermissions arg                 Permissions to set on UNIX domain socket file - 0700 by default
  --fork                                Fork server process
  -v [ --verbose ] [=arg(=v)]           Be more verbose (include multiple times for more verbosity e.g. -vvvvv)
  --quiet                               Quieter output
  --logpath arg                         Log file to send write to instead of stdout - has to be a file, not directory
  --syslog                              Log to system's syslog facility instead of file or stdout
  --syslogFacility arg                  syslog facility used for mongodb syslog message
  --logappend                           Append to logpath instead of over-writing
  --logRotate arg                       Set the log rotation behavior (rename|reopen)
  --timeStampFormat arg                 Desired format for timestamps in log messages. One of iso8601-utc or iso8601-local
  --setParameter arg                    Set a configurable parameter
  --bind_ip arg                         Comma separated list of ip addresses to listen on - localhost by default
  --bind_ip_all                         Bind to all ip addresses
  --noauth                              Run without security
  --transitionToAuth                    For rolling access control upgrade. Attempt to authenticate over outgoing connections and proceed regardless of success. Accept incoming connections with or without authentication.
  --slowms arg (=100)                   Value of slow for profile and console log
  --slowOpSampleRate arg (=1)           Fraction of slow ops to include in the profile and console log
  --profileFilter arg                   Query predicate to control which operations are logged and profiled
  --auth                                Run with security
  --clusterIpSourceWhitelist arg        Network CIDR specification of permitted origin for `__system` access
  --profile arg                         0=off 1=slow, 2=all
  --cpu                                 Periodically show cpu and iowait utilization
  --sysinfo                             Print some diagnostic system information
  --noscripting                         Disable scripting engine
  --notablescan                         Do not allow table scans
  --keyFile arg                         Private key for cluster authentication
  --clusterAuthMode arg                 Authentication mode used for cluster authentication. Alternatives are (keyFile|sendKeyFile|sendX509|x509)

Replication options:
  --oplogSize arg                       Size to use (in MB) for replication op log. default is 5% of disk space (i.e. large is good)

Replica set options:
  --replSet arg                         arg is <setname>[/<optionalseedhostlist>]
  --enableMajorityReadConcern [=arg(=1)] (=1) Enables majority readConcern

Sharding options:
  --configsvr                           Declare this is a config db of a cluster; default port 27019; default dir /data/configdb
  --shardsvr                            Declare this is a shard db of a cluster; default port 27018

Storage options:
  --storageEngine arg                   What storage engine to use - defaults to wiredTiger if no data files present
  --dbpath arg                          Directory for datafiles - defaults to /data/db
  --directoryperdb                      Each database will be stored in a separate directory
  --syncdelay arg (=60)                 Seconds between disk syncs
  --journalCommitInterval arg (=100)    how often to group/batch commit (ms)
  --upgrade                             Upgrade db if needed
  --repair                              Run repair on all dbs
  --journal                             Enable journaling
  --nojournal                           Disable journaling (journaling is on by default for 64 bit)
  --oplogMinRetentionHours arg (=0)     Minimum number of hours to preserve in the oplog. Default is 0 (turned off). Fractions are allowed (e.g. 1.5 hours)

AWS IAM Options:
  --awsIamSessionToken arg              AWS Session Token for temporary credentials

Free Monitoring Options:
  --enableFreeMonitoring arg            Enable Cloud Free Monitoring (on|runtime|off)
  --freeMonitoringTag arg               Cloud Free Monitoring Tags

WiredTiger options:
  --wiredTigerCacheSizeGB arg           Maximum amount of memory to allocate for cache; Defaults to 1/2 of physical RAM
  --wiredTigerJournalCompressor arg (=snappy)   Use a compressor for log records [none|snappy|zlib|zstd]
  --wiredTigerDirectoryForIndexes       Put indexes and data in different directories
  --wiredTigerCollectionBlockCompressor arg (=snappy)  Block compression algorithm for collection data [none|snappy|zlib|zstd]
  --wiredTigerIndexPrefixCompression arg (=1)  Use prefix compression on row-store leaf pages

TLS Options:
  --tlsOnNormalPorts                    Use TLS on configured ports
  --tlsMode arg                         Set the TLS operation mode (disabled|allowTLS|preferTLS|requireTLS)
  --tlsCertificateKeyFile arg           Certificate and key file for TLS
  --tlsCertificateKeyFilePassword arg   Password to unlock key in the TLS certificate key file
  --tlsClusterFile arg                  Key file for internal TLS authentication
  --tlsClusterPassword arg              Internal authentication key file password
  --tlsCAFile arg                       Certificate Authority file for TLS
  --tlsClusterCAFile arg                CA used for verifying remotes during inbound connections
  --tlsCRLFile arg                      Certificate Revocation List file for TLS
  --tlsDisabledProtocols arg            Comma separated list of TLS protocols to disable [TLS1_0,TLS1_1,TLS1_2]
  --tlsAllowConnectionsWithoutCertificates     Allow client to connect without presenting a certificate
  --tlsAllowInvalidHostnames            Allow server certificates to provide non-matching hostnames
  --tlsAllowInvalidCertificates         Allow connections to servers with invalid certificates
  --tlsFIPSMode                         Activate FIPS 140-2 mode at startup
  --tlsCertificateSelector arg          TLS Certificate in system store
  --tlsClusterCertificateSelector arg   SSL/TLS Certificate in system store for internal TLS authentication
  --tlsLogVersions arg                  Comma separated list of TLS protocols to log on connect [TLS1_0,TLS1_1,TLS1_2]
```

下面，我们来依次分析相关的参数。

