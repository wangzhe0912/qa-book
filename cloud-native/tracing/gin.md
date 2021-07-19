# 基于Go gin框架的http headers透传

在本文中，我们将会介绍在 Gin HTTP 框架中，如何能够简单快速的实现 headers 的透传方案。

## 原理分析

对于任何一个微服务而言，想要实现 headers 的透传的话，也是主要分三步：

 - 接收 HTTP 请求时，从请求中读取中 headers 信息。
 - 将 headers 在程序内部进行保存和传播。
 - 发送 HTTP 请求时，将内部传播的 headers 在客户端请求加入并发送出去。

此外，为了避免在各个请求接收和请求发送中，都需要进行相关的改动，我们在程序实现中应该按照 AOP 的思想，一次改动全场生效。

### 请求读取

首先，在 Gin 框架中，支持通过 middleware 的中间件方式在接收 http 请求处理的前后增加自定义逻辑。

因此，我们可以通过自定义 middleware 来读取请求头，并自身维护一个 Context 上下游对象，其中记录着对应的请求头信息。

```go
func Middleware() gin.HandlerFunc {
	return handler
}

func handler(c *gin.Context) {
	headersWithFirst := make(map[string]string, len(c.Request.Header))

	for k, v := range c.Request.Header {
		if len(v) > 0 {
			headersWithFirst[k] = v[0]
		}
	}

	carrier := cp.Extract(headersWithFirst)
	if len(carrier) > 0 {
		c.Request = c.Request.WithContext(context.WithValue(c.Request.Context(), cp.InternalContextKey{}, carrier))
	}

	c.Next()
}
```

### 请求内部传播

由于在读取请求 header 中，我们对原有的 Context 进行了扩展，将 headers 信息记录到了 `c.Request.Context()` 中。

因此，在仅接着的的 Context 上下文传递中，需要使用 `c.Request.Context()` 来代替 `c` 进行上下文传递即可。

例如：

```go
func TestApi(c *gin.Context) {
	SelfFunction1(c.Request.Context())
}
```

### 请求发送

在 Go 语言发送 http 请求时，默认基于的是 `net/http` 库，但是 `net/http` 库本身在发送请求时，无法基于 Context 上下文进行行为定制。
而我们其实是希望在 http 客户端发送请求时，可以从 context 上下文中获取对应的请求头信息并增加到 header 中传递出去。

因此，我们需要使用一个官方提供的http库 `golang.org/x/net/context/ctxhttp` 来代替原有lib库发送HTTP请求。

示例如下：

```go
resp, err := ctxhttp.Get(c.Request.Context(), client, "http://127.0.0.1:8080/test")
```

其中，ctxhttp 与 http 的功能基本相同，唯一的差别在于需要主动传递 `context` 上下文和实例化的 `client` 对象。

至此为止，我们其实只是传递了对应的上下文到`ctxhttp`中，但实际上还并没有实现http 客户端发送请求时，
可以从 context 上下文中获取对应的请求头信息并增加到 header 中传递出去。

因此，下面我们需要对 `http.Client` 对象进行一次扩展，实现可以自动从 context 上下文中获取对应的请求头信息并增加到 header 中传递出去。

示例代码如下：

```go
func WrapClient(c *http.Client) *http.Client {
	if c == nil {
		c = http.DefaultClient
	}
	copied := *c

	copied.Transport = WrapRoundTripper(copied.Transport)

	return &copied
}

func WrapRoundTripper(r http.RoundTripper) http.RoundTripper {
	if r == nil {
		r = http.DefaultTransport
	}
	return &roundTripper{rt: r}
}

type roundTripper struct {
	rt http.RoundTripper
}

func (s *roundTripper) RoundTrip(r *http.Request) (*http.Response, error) {
	carrier := r.Context().Value(cp.InternalContextKey{})
	headers := cp.Inject(carrier)

	for k, v := range headers {
		r.Header.Set(k, v)
	}

	return s.rt.RoundTrip(r)
}
```

在上述代码中，我们定义了一个 `WrapClient` 函数，它可以对已有的 `http.Client` 进行扩展，
具体来说，可以从上下文中获取对应的 headers 信息，然后注入到请求发送的 header 体中。

具体到使用中，其实非常简单，只需要对 http.Client 进行一次 Wrap 即可：

```gopackage main
import cphttp "github.com/AminoApps/context-propagation-go/module/context-propagation-http"
import "golang.org/x/net/context/ctxhttp"

client := cphttp.WrapClient(&http.Client{})

// Please use the ctxhttp to wrap the request.
resp, err := ctxhttp.Get(ctx, client, "http://127.0.0.1:8080/test")
```

## 实战

最后，我们以一个实战的示例来演示对于一个 gin 框架的项目而言，是如何实现 headers 透传的：

```go
package main

import (
	cp "github.com/AminoApps/context-propagation-go"
	cpgin "github.com/AminoApps/context-propagation-go/module/context-propagation-gin"
	cphttp "github.com/AminoApps/context-propagation-go/module/context-propagation-http"
	"github.com/gin-gonic/gin"
	"golang.org/x/net/context/ctxhttp"
	"net/http"
)

func main() {
	r := gin.New()
	r.Use(cpgin.Middleware())

	r.GET("/JSON", func(c *gin.Context) {
		value := cp.GetValueFromContext(c.Request.Context(), "easyenv")
		println("token: ", value)
		//callback is x
		client := cphttp.WrapClient(&http.Client{})
		resp, err := ctxhttp.Get(c.Request.Context(), client, "http://127.0.0.1:8080/test")
		println("resp: ", resp, err)
		// Will output  :   x({\"foo\":\"bar\"})
		c.JSON(http.StatusOK, resp)
	})

	// Listen and serve on 0.0.0.0:8080
	r.Run(":8080")
}
```

相关的实现也可以参考 [在 Go 的 Gin WEB 框架中如何实现 headers 透传](https://github.com/AminoApps/context-propagation-go) 。
