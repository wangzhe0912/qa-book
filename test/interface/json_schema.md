# JSON Schema在接口测试中的应用

## JSON Schema简介


## JSON Schema初探

下面，我们将会以Python3为例，演示如何使用JSON Schema来帮助我们进行用例结构断言。

第一步，我们首先需要安装第三方库 `jsonschema`:

```bash
pip install jsonschema
```

接下来，我们可以看一个JSON Schema校验的例子:

```python
from jsonschema import validate

schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"}
    }
}

validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema)

validate(instance={"name" : "Eggs", "price" : "Invalid"}, schema=schema)

```

可以看到，对于第一个validate函数，执行时没有任何异常。
而对于第二个validate函数，执行时会抛出异常，即price字段期望是number类型，但是目前是string类型。


## JSON Schema Generator部署与使用


## JSON Schema高级用法

