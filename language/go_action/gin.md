# Go Web框架gin快速上手

在本文中，我们将讲解一个流行的 Go Web 框架 gin 的快速入门与使用。

## Gin 简介

Gin 是一个用 Go (Golang) 编写的 web 框架。
Gin 最大的优点之一就是其出色的性能。

Gin 的特性：

 - 快速
 - 支持中间件（AOP编程），传入的HTTP请求可以由一系列中间件来处理，例如Logger, Auth, gzip等。
 - Crash处理
 - 入参JSON验证
 - 路由组织
 - 错误管理
 - 内置渲染
 - 可扩展


## 项目初始化与安装

首先，我们需要初始化一个项目：

```shell
cd ~/Desktop/gin-project
go mod init gin-project
```

gin 的依赖包安装非常简单:

```shell
go get -u github.com/gin-gonic/gin
```

此时，会在当前目录下生成一个 `go.mod` 和 `go.sum` 文件。

## 创建 demo 文件

下面，我们来编写一个最简单的 `gin` 的项目:

```go
package main

import "github.com/gin-gonic/gin"

func main() {
    r := gin.Default()
    r.GET("/ping", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "message": "pong",
        })
    })
    r.Run() // 监听并在 0.0.0.0:8080 上启动服务
}
```

然后，可以执行如下命令来启动服务：

```shell
go run example.go
```

接下来，我们可以打开浏览器，并访问 http://localhost:8080/ping ，是不是一个最简单的 Web 服务已经运行起来了呢？


## 编译扩展

Gin 框架默认使用了 `encoding/json` 这一 JSON 处理包，不过，我们可以在编译的过程中通过 tag 来自主指定希望使用的 JSON 包版本：

```shell
go build -tags=jsoniter .
```

Gin 默认启用 MsgPack 渲染功能。但是您可以通过指定 nomsgpack 构建标记来禁用此功能:

```shell
go build -tags=nomsgpack .
```

这一操作可以有效减少二进制执行文件的大小。

Ps: 多个tag之间可以使用,来分隔。

## 示例程序

接下来，我们将会通过一系列的示例程序来演示 gin 框架的使用。

### 支持 GET, POST, PUT, PATCH, DELETE, OPTIONS 等请求方法

```go
func main() {
	// Creates a gin router with default middleware:
	// logger and recovery (crash-free) middleware
	router := gin.Default()

	router.GET("/someGet", getting)
	router.POST("/somePost", posting)
	router.PUT("/somePut", putting)
	router.DELETE("/someDelete", deleting)
	router.PATCH("/somePatch", patching)
	router.HEAD("/someHead", head)
	router.OPTIONS("/someOptions", options)

	// By default it serves on :8080 unless a
	// PORT environment variable was defined.
	router.Run()
	// router.Run(":3000") for a hard coded port
}
```

### 获取 url 中的参数

```go
func main() {
	router := gin.Default()

	// This handler will match /user/john but will not match /user/ or /user
	router.GET("/user/:name", func(c *gin.Context) {
		name := c.Param("name")
		c.String(http.StatusOK, "Hello %s", name)
	})

	// However, this one will match /user/john/ and also /user/john/send
	// If no other routers match /user/john, it will redirect to /user/john/
	router.GET("/user/:name/*action", func(c *gin.Context) {
		name := c.Param("name")
		action := c.Param("action")
		message := name + " is " + action
		c.String(http.StatusOK, message)
	})

	// For each matched request Context will hold the route definition
	router.POST("/user/:name/*action", func(c *gin.Context) {
		c.FullPath() == "/user/:name/*action" // true
	})

	// This handler will add a new router for /user/groups.
	// Exact routes are resolved before param routes, regardless of the order they were defined.
	// Routes starting with /user/groups are never interpreted as /user/:name/... routes
	router.GET("/user/groups", func(c *gin.Context) {
		c.String(http.StatusOK, "The available groups")
	})

	router.Run(":8080")
}
```

从上述示例中，我们可以学习到：

 - 如何从 url 中提取参数。
 - url 中参数匹配的规则是，:${key} 表示不匹配空，*{key} 表示兼容匹配空。
 - url 匹配服从最短路径匹配，与 router 块的上下位置无关。


### 从 get 请求中获取 url 参数

```go
func main() {
	router := gin.Default()

	// Query string parameters are parsed using the existing underlying request object.
	// The request responds to a url matching:  /welcome?firstname=Jane&lastname=Doe
	router.GET("/welcome", func(c *gin.Context) {
		firstname := c.DefaultQuery("firstname", "Guest")  // default value
		lastname := c.Query("lastname") // shortcut for c.Request.URL.Query().Get("lastname")

		c.String(http.StatusOK, "Hello %s %s", firstname, lastname)
	})
	router.Run(":8080")
}
```

### 从 post 请求中获取 form 参数

```go
func main() {
	router := gin.Default()

	router.POST("/form_post", func(c *gin.Context) {
		message := c.PostForm("message")
		nick := c.DefaultPostForm("nick", "anonymous")

		c.JSON(200, gin.H{
			"status":  "posted",
			"message": message,
			"nick":    nick,
		})
	})
	router.Run(":8080")
}
```

此外，当form参数为map格式时，可以按照如下方式进行接收：

```go
// POST /post?ids[a]=1234&ids[b]=hello HTTP/1.1 
// Content-Type: application/x-www-form-urlencoded
// names[first]=thinkerou&names[second]=tianou

func main() {
	router := gin.Default()

	router.POST("/post", func(c *gin.Context) {

		ids := c.QueryMap("ids")
		names := c.PostFormMap("names")

		fmt.Printf("ids: %v; names: %v", ids, names)
	})
	router.Run(":8080")
}
```

### 文件上传

```go
func main() {
	router := gin.Default()
	// Set a lower memory limit for multipart forms (default is 32 MiB)
	router.MaxMultipartMemory = 8 << 20  // 8 MiB
	router.POST("/upload", func(c *gin.Context) {
		// single file
		file, _ := c.FormFile("file")
		log.Println(file.Filename)

		// Upload the file to specific dst.
		c.SaveUploadedFile(file, dst)

		c.String(http.StatusOK, fmt.Sprintf("'%s' uploaded!", file.Filename))
	})
	router.Run(":8080")
}
```

示例测试代码:

```shell
curl -X POST http://localhost:8080/upload \
  -F "file=@/Users/appleboy/test.zip" \
  -H "Content-Type: multipart/form-data"
```

### url 分组

```go
func main() {
	router := gin.Default()

	// Simple group: v1
	v1 := router.Group("/v1")
	{
		v1.POST("/login", loginEndpoint)
		v1.POST("/submit", submitEndpoint)
		v1.POST("/read", readEndpoint)
	}

	// Simple group: v2
	v2 := router.Group("/v2")
	{
		v2.POST("/login", loginEndpoint)
		v2.POST("/submit", submitEndpoint)
		v2.POST("/read", readEndpoint)
	}

	router.Run(":8080")
}
```

### 中间件的使用

```go
func main() {
	// Creates a router without any middleware by default
	r := gin.New()

	// Global middleware
	// Logger middleware will write the logs to gin.DefaultWriter even if you set with GIN_MODE=release.
	// By default gin.DefaultWriter = os.Stdout
	r.Use(gin.Logger())

	// Recovery middleware recovers from any panics and writes a 500 if there was one.
	r.Use(gin.Recovery())

	// Per route middleware, you can add as many as you desire.
	r.GET("/benchmark", MyBenchLogger(), benchEndpoint)

	// Authorization group
	// authorized := r.Group("/", AuthRequired())
	// exactly the same as:
	authorized := r.Group("/")
	// per group middleware! in this case we use the custom created
	// AuthRequired() middleware just in the "authorized" group.
	authorized.Use(AuthRequired())
	{
		authorized.POST("/login", loginEndpoint)
		authorized.POST("/submit", submitEndpoint)
		authorized.POST("/read", readEndpoint)

		// nested group
		testing := authorized.Group("testing")
		testing.GET("/analytics", analyticsEndpoint)
	}

	// Listen and serve on 0.0.0.0:8080
	r.Run(":8080")
}
```

### 请求参数与数据对象绑定

在 Go 语言中，针对 JSON, Yaml, XML 的请求体而言，我们需要设置对应的 Struct 来与之绑定并接收请求，示例如下：

```go
// Binding from JSON
type Login struct {
    User     string `form:"user" json:"user" xml:"user"  binding:"required"`
    Password string `form:"password" json:"password" xml:"password" binding:"required"`
}

func main() {
    router := gin.Default()

    // Example for binding JSON ({"user": "manu", "password": "123"})
    router.POST("/loginJSON", func(c *gin.Context) {
        var json Login
        if err := c.ShouldBindJSON(&json); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }

        if json.User != "manu" || json.Password != "123" {
            c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
            return
        }

        c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
    })

    // Example for binding XML (
    //    <?xml version="1.0" encoding="UTF-8"?>
    //    <root>
    //        <user>manu</user>
    //        <password>123</password>
    //    </root>)
    router.POST("/loginXML", func(c *gin.Context) {
        var xml Login
        if err := c.ShouldBindXML(&xml); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }

        if xml.User != "manu" || xml.Password != "123" {
            c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
            return
        }

        c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
    })

    // Example for binding a HTML form (user=manu&password=123)
    router.POST("/loginForm", func(c *gin.Context) {
        var form Login
        // This will infer what binder to use depending on the content-type header.
        if err := c.ShouldBind(&form); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }

        if form.User != "manu" || form.Password != "123" {
            c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
            return
        }

        c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
    })

    // Listen and serve on 0.0.0.0:8080
    router.Run(":8080")
}
```

此外，从上述代码中可以看出，该方法不仅仅局限于 JSON 请求，也可以同时接收 Form 请求， XML 请求等。

除了字段级别的验证，还可以根据相关内容进行进行校验来自定义校验器，
可以参考 [示例代码](https://github.com/gin-gonic/examples/tree/master/custom-validation/server.go) 。

此外，相关的功能不仅仅能 bind body 体，还可以 bind params, headers 甚至是 url 参数等。

### 研发自定义中间件

```go
func Logger() gin.HandlerFunc {
	return func(c *gin.Context) {
        // before request
		t := time.Now()
		// Set example variable
		c.Set("example", "12345")

        // request
		c.Next()

		// after request
		latency := time.Since(t)
		log.Print(latency)

		// access the status we are sending
		status := c.Writer.Status()
		log.Println(status)
	}
}

func main() {
	r := gin.New()
	r.Use(Logger())

	r.GET("/test", func(c *gin.Context) {
		example := c.MustGet("example").(string)

		// it would print: "12345"
		log.Println(example)
	})

	// Listen and serve on 0.0.0.0:8080
	r.Run(":8080")
}
```
