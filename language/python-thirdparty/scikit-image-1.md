# scikit-image快速入门

## scikit-image初识

scikit-image是一个基于 `numpy` 数组的Python的图像处理包。

这个包的引用方法是：

```python
import skimage
```

skimage中大多数的函数都隶属于它的子模块中，例如：

```python
from skimage import data
camera = data.camera()
```

skimage中的子模块列表及其函数列表可以参考[API文档](https://scikit-image.org/docs/stable/api/api.html)。

在scikit-image中，所有的图像都是使用numpy进行表示，例如可以用一个二维数组来表示一个灰度二维图像：

```python
type(camera)
# <type 'numpy.ndarray'>
camera.shape
# (512, 512)
```

其中，`skimage.data` 子模块中提供了一组函数用于获取各种示例图像，便于我们基于这些示例图像快速入门scikit-image的功能。

```python
coins = data.coins()
from skimage import filters
threshold_value = filters.threshold_otsu(coins)
threshold_value
# 107
```

当然，我们也可以直接将图片文件读取成为`numpy`中的Array，只需要使用`skimage.io.imread`即可。

```python
import os
filename = os.path.join(skimage.data_dir, 'moon.png')
from skimage import io
moon = io.imread(filename)
```

此外，我们还可以使用`natsort`来对图片进行排序并加载多张图片：

```python
import os
from natsort import natsorted, ns
from skimage import io
list_files = os.listdir('.')
print(list_files)
# ['01.png', '010.png', '0101.png', '0190.png', '02.png']
list_files = natsorted(list_files)
print(list_files)
# ['01.png', '02.png', '010.png', '0101.png', '0190.png']
image_list = []
for filename in list_files:
    image_list.append(io.imread(filename))
```

## scikit-image快速入门

scikit-image中图像是通过NumPy中的ndarray的数据结构来表示的。
因此，我们可以利用Numpy中很多的标准方法直接对数据进行处理：

```python
from skimage import data
camera = data.camera()
type(camera)
# <type 'numpy.ndarray'>
```

例如，计算图片的形状与像素点数：

```python
camera.shape
# (512, 512)
camera.size
# 262144
```

还有计算图片的亮度的统计信息：

```python
camera.min(), camera.max()
# (0, 255)
camera.mean()
# 118.31400299072266
```

### Numpy检索

Numpy的索引可以用于数据查询和数据修改，例如：

```python
# 查询camera中第10行、第20列的元素
camera[10, 20]
# 153
# 修改camera中第3行、第10列的元素为0
camera[3, 10] = 0
```

PS：在Numpy的索引中，第一个维度`camera.shape[0]`对应的是行数、第二个维度`camera.shape[1]`对应的是列数。
另外，原点`camera[0, 0]`位于整个图像的左上角。

这种表示方法与矩阵和线性代数中的表示方法一致，但是与笛卡尔坐标不一致。

除了逐个像素处理外，我们还可以直接使用Numpy来直接查询和修改整组像素的值。

一、切片
```python
# 设置前十行为黑色（0）
camera[:10] = 0
```

二、掩码

```python
mask = camera < 87
# 将掩码为真的像素点统一设置为白色（255）
camera[mask] = 255
```

### 修改图像颜色



### 坐标变化





