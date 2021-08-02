# openresty的安装

下面，我们来了解一下 OpenResty 的安装方法。

## 使用包管理系统直接安装

安装 OpenResty 最简单的方式就是通过各个操作系统中自带的包管理工作来安装了。

例如，对于 MacOS，可以使用 brew 来安装，对于 CentOS，可以使用 yum 来安装，对于 Ubuntu 而言，可以使用 apt 来安装等等。

需要注意的是，在使用包管理工具来安装 OpenResty 时，我们通过用的不是操作系统内置的源，而是会使用 OpenResty 提供的仓库。

以 MacOS 系统为例，安装方式如下：

```sh
brew tap openresty/brew
brew install openresty
```

以 CentOS 系统为例，安装方式如下:

```sh
# add the yum repo:
wget https://openresty.org/package/centos/openresty.repo
sudo mv openresty.repo /etc/yum.repos.d/
# update the yum index:
sudo yum check-update
# install
sudo yum install openresty
sudo yum install openresty-resty
# query related package
sudo yum --disablerepo="*" --enablerepo="openresty" list available
```

## 源码编译安装

我们都知道，包管理器直接安装的 OpenResty 是没有办法自主控制编译选项的。
这对我们的使用场景是非常不友好的。

下面，我们就来看一下如何通过源码的方式来编译 OpenResty 吧。

Step1: 安装 pcre

```sh
wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.42.tar.bz2
tar xjf pcre-8.42.tar.bz2
cd pcre-8.42
./configure --prefix=/home/work/openresty-dependency/pcre --disable-cpp --enable-jit --enable-utf --enable-unicode-properties
make -j24 V=1 > /dev/stderr
make install

rm -rf /home/work/openresty-dependency/pcre/bin
rm -rf /home/work/openresty-dependency/pcre/share
rm -f /home/work/openresty-dependency/pcre/lib/*.la
rm -f /home/work/openresty-dependency/pcre/lib/*pcrecpp*
rm -f /home/work/openresty-dependency/pcre/lib/*pcreposix*
rm -rf /home/work/openresty-dependency/pcre/lib/pkgconfig
```

Step2: 安装 zlib 

```sh
wget http://www.zlib.net/zlib-1.2.11.tar.xz
tar xf zlib-1.2.11.tar.xz
cd zlib-1.2.11
 ./configure --prefix=/home/work/openresty-dependency/zlib
make -j24 \
CFLAGS='-O3 -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g' \
SFLAGS='-O3 -fPIC -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g' > /dev/stderr
make install
rm -rf /home/work/openresty-dependency/zlib/share/
rm -f /home/work/openresty-dependency/zlib/lib/*.la
rm -rf /home/work/openresty-dependency/zlib/lib/pkgconfig/
```

Step3: 安装 openssl

```sh
wget https://www.openssl.org/source/openssl-1.1.0j.tar.gz
wget https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-1.1.0d-sess_set_get_cb_yield.patch --no-check-certificate
wget https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-1.1.0j-parallel_build_fix.patch --no-check-certificate
tar zxf openssl-1.1.0j.tar.gz
cd openssl-1.1.0j

patch -p1 < ../openssl-1.1.0d-sess_set_get_cb_yield.patch
patch -p1 < ../openssl-1.1.0j-parallel_build_fix.patch

./config \
    no-threads shared zlib -g \
    enable-ssl3 enable-ssl3-method \
    --prefix=/home/work/openresty-dependency/openssl \
    --libdir=lib \
    -I%/home/work/openresty-dependency/zlib/include \
    -L%/home/work/openresty-dependency/zlib/lib \
    -Wl,-rpath,/home/work/openresty-dependency/zlib/lib:/home/work/openresty-dependency/openssl/lib
make -j24
make install_sw

rm -f /home/work/openresty-dependency/openssl/bin/c_rehash
rm -rf /home/work/openresty-dependency/openssl/lib/pkgconfig
```

Step4: 编译安装 OpenResty

```sh
wget https://openresty.org/download/openresty-1.15.8.1.tar.gz
tar zxf openresty-1.15.8.1.tar.gz
cd openresty-1.15.8.1
./configure \
    --prefix=/home/work/openresty \
    --with-cc-opt="-DNGX_LUA_ABORT_AT_PANIC \
                -I/home/work/openresty-dependency/zlib/include \
                -I/home/work/openresty-dependency/pcre/include \
                -I/home/work/openresty-dependency/openssl/include" \
    --with-ld-opt="-L/home/work/openresty-dependency/zlib/lib \
                -L/home/work/openresty-dependency/pcre/lib \
                -L/home/work/openresty-dependency/openssl/lib \
                -Wl,-rpath,/home/work/openresty-dependency/zlib/lib:/home/work/openresty-dependency/pcre/lib:/home/work/openresty-dependency/openssl/lib" \
    --with-pcre-jit \
    --without-http_rds_json_module \
    --without-http_rds_csv_module \
    --without-lua_rds_parser \
    --with-stream \
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-http_v2_module \
    --without-mail_pop3_module \
    --without-mail_imap_module \
    --without-mail_smtp_module \
    --with-http_stub_status_module \
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_auth_request_module \
    --with-http_secure_link_module \
    --with-http_random_index_module \
    --with-http_gzip_static_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gunzip_module \
    --with-threads \
    --with-luajit-xcflags='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT' \
    -j24
make -j24
make install
```

至此，我们的 OpenResty 就已经成功安装完成了，快来试试吧！
