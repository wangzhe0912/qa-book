# MongoCharts的安装与使用

## 安装

前置条件：

1. 已经安装Docker 18.03及以上版本。
2. 搭建一个MongoDB实例用于作为MongoChart的后端存储数据库。

Step1: 初始化swarm集群

```bash
sudo docker swarm init
```

Step2: 拉取MongoChart镜像

```bash
docker pull quay.io/mongodb/charts:19.12.1
```

Step3: 验证提前搭建的作为MongoChart的后端存储数据库的MongoDB实例是否正常工作

```bash
sudo docker run --rm quay.io/mongodb/charts:19.12.1 charts-cli test-connection 'mongodb://${ip}:${port}'
```

Step4: 创建Secret对象

```bash
echo "mongodb://${ip}:${port}" | sudo docker secret create charts-mongodb-uri -
```

Step5: 创建部署对象

MongoCharts需要使用Docker Swarm进行安装，其中Yaml文件如下:

```yaml
version: '3.3'

services:
  charts:
    image: quay.io/mongodb/charts:19.12.1
    hostname: charts
    ports:
      - 8811:80
    volumes:
      - keys:/mongodb-charts/volumes/keys
      - logs:/mongodb-charts/volumes/logs
      - db-certs:/mongodb-charts/volumes/db-certs
      - web-certs:/mongodb-charts/volumes/web-certs
    environment:
      # The presence of following 2 environment variables will enable HTTPS on Charts server.
      # All HTTP requests will be redirected to HTTPS as well.
      # To enable HTTPS, upload your certificate and key file to the web-certs volume,
      # uncomment the following lines and replace with the names of your certificate and key file.
      # CHARTS_HTTPS_CERTIFICATE_FILE: charts-https.crt
      # CHARTS_HTTPS_CERTIFICATE_KEY_FILE: charts-https.key

      # This environment variable controls the built-in support widget and
      # metrics collection in MongoDB Charts. To disable both, set the value
      # to "off". The default is "on".
      CHARTS_SUPPORT_WIDGET_AND_METRICS: 'on'
      # Directory where you can upload SSL certificates (.pem format) which
      # should be considered trusted self-signed or root certificates when
      # Charts is accessing MongoDB servers with ?ssl=true
      SSL_CERT_DIR: /mongodb-charts/volumes/db-certs
    networks:
      - backend
    secrets:
      - charts-mongodb-uri

networks:
  backend:

volumes:
  keys:
  logs:
  db-certs:
  web-certs:

secrets:
  charts-mongodb-uri:
    external: true
```

我们将其命名为 `charts-docker-swarm.yaml` 。然后执行如下命令：

```bash
sudo docker stack deploy -c charts-docker-swarm.yaml mongodb-charts
```

Step6: 检查服务是否正常部署

```bash
sudo docker service ls
```

Step7: 创建管理用户

```bash
sudo docker exec -it \
  $(sudo docker container ls --filter name=_charts -q) \
  charts-cli add-user --first-name "<First>" --last-name "<Last>" \
  --email "<user@example.com>" --password "<Password>" \
  --role "UserAdmin"
```

Step8: 登录Web页面进行查看

Web页面的地址为： `http://${host_ip}:8811`

Step9: 密钥备份相关信息 

```bash
mkdir /tmp/mongo-charts-keys
sudo docker run -it \
  --volume mongodb-charts_keys:/volume \
  --volume /tmp/mongo-charts-keys:/backup \
  quay.io/mongodb/charts:19.12.1 sh -c 'cp /volume/* /backup'
```
