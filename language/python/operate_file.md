# Python自动检测文件编码格式并打开文件

在 Python 中，我们常常会遇到一个问题，就是读取文件内容时，提示我们编码格式不正确，无法正常解析。

那么，针对这种情况有没有通用的解决办法呢？当时是有的。

## chardet

在 Python 中，有一个第三方库 chardet 专门用于文本内容的编码格式检测: chardet 。

其基本的使用示例如下:

```python
import chardet

file_path = "operate_file.md"

with open(file_path, "rb") as f:
    print(chardet.detect(f.read()))
```

其得到的输出格式如下:

```
{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
```

其中，encoding 就是我们需要的文件的编码格式，confidence 表示置信度。

因此，我们只需要处理一个文件时，首先先读取文件的二进制格式，然后用 chardet 检测文件的编码格式，在用得到的编码格式读写文件即可。

## 完成示例

一个完整的示例如下:

```python
import chardet

file_path = "operate_file.md"

# 计算编码格式
with open(file_path, "rb") as f:
    encoding = chardet.detect(f.read())["encoding"]

# 读文件
with open(file_path, "r", encoding=encoding) as f:
    content = f.read()

# 写文件
with open(file_path, "w", encoding=encoding) as f:
    f.write(content)
```
