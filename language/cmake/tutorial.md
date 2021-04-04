# Cmake入门教程

## 引言

CMake教程提供了分步指南，其中涵盖了CMake可以解决的常见构建系统问题。

了解示例项目中各个主题如何协同将对后续的工作非常有帮助。

示例的教程文档和源代码可以 [目录](../../src/language/cmake/tutorial) 中找到。

每个步骤都有其自己的子目录，该子目录下的 init 目录包含可用作起点的示例代码，目录下的 final 目录包含了该步骤结束后的完整代码。

教程示例是渐进式的，因此每个步骤都为上一步提供了完整的解决方案。

## 第一步: 基本出发点

最基本的项目是从源代码文件来构建可执行文件。

对于一个最简单的项目，只需要三行CMakeLists.txt文件。
这将是本教程的起点。

下面，在 [step1/init目录](../../src/language/cmake/tutorial/step1/init) 中创建一个CMakeLists.txt文件，如下所示：

```cmake
# Cmake 的版本要求声明
cmake_minimum_required(VERSION 3.10)

# set the project name
project(Tutorial)

# add the executable
add_executable(Tutorial tutorial.cxx)
```

Ps: 此示例在CMakeLists.txt文件中使用小写命令。 CMake支持大写，小写和大小写混合命令。

step1/init 目录中提供了 `tutorial.cxx` 的源代码，可用于计算数字的平方根。

### 添加版本号和配置头文件

我们将添加的第一个功能是为我们的可执行文件和项目提供版本号。
尽管我们可以仅在源代码中执行此操作，但是使用CMakeLists.txt可以提供更大的灵活性。

首先，修改 `CMakeLists.txt` 文件以使用 `project()` 命令设置项目名称和版本号。

```cmake
cmake_minimum_required(VERSION 3.10)

# set the project name and version
project(Tutorial VERSION 1.0)
```

然后，配置头文件以将版本号传递给源代码：

```cmake
configure_file(TutorialConfig.h.in TutorialConfig.h)
```

由于已配置的文件将被写入二进制树，因此我们必须将该目录添加到路径列表中以搜索包含文件。

将以下行添加到 `CMakeLists.txt` 文件的末尾：

```cmake
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )
```

使用您喜欢的编辑器，在源目录中使用以下内容创建 `TutorialConfig.h.in`：

```cpp
// the configured options and settings for Tutorial
#define Tutorial_VERSION_MAJOR @Tutorial_VERSION_MAJOR@
#define Tutorial_VERSION_MINOR @Tutorial_VERSION_MINOR@
```

当 CMake 配置此头文件时，@Tutorial_VERSION_MAJOR@ 和 @Tutorial_VERSION_MINOR@ 的值将被替换，从而生成 `TutorialConfig.h` 文件。

接下来，修改 `tutorial.cxx` 以引用配置的头文件 `TutorialConfig.h`。

最后，让我们通过更新 `tutorial.cxx` 来打印出可执行文件的名称和版本号，如下所示：

```c++
  if (argc < 2) {
    // report version
    std::cout << argv[0] << " Version " << Tutorial_VERSION_MAJOR << "."
              << Tutorial_VERSION_MINOR << std::endl;
    std::cout << "Usage: " << argv[0] << " number" << std::endl;
    return 1;
  }
```

### 指定 C++ 版本

接下来，通过在 `tutorial.cxx` 中用 `std :: stod` 替换 `atof`，将一些C ++ 11功能添加到我们的项目中。

同时，删除 `#include <cstdlib>` 引用。

```c++
const double inputValue = std::stod(argv[1]);
```

我们将需要在 `CMake` 代码中明确声明使用的 C++ 版本。

在 `CMake` 中启用对特定 C++ 标准的支持的最简单方法是使用 `CMAKE_CXX_STANDARD`变量。

对于本教程，将 `CMakeLists.txt` 文件中的 `CMAKE_CXX_STANDARD` 变量设置为11，并将 `CMAKE_CXX_STANDARD_REQUIRED` 设置为True。

确保在对 `add_executable` 的调用上方添加 `CMAKE_CXX_STANDARD` 声明。

```cmake
cmake_minimum_required(VERSION 3.10)

# set the project name and version
project(Tutorial VERSION 1.0)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
```

### 构建和测试

下面，我们来运行 `cmake` 可执行文件或 `cmake-gui` 来配置项目，然后使用所选的构建工具对其进行构建。

例如:

```shell
cd ./tutorial/step1/init
mkdir build
cd ./build
# 运行 cmake 来配置项目并生成构建文件
cmake ..
# 实际运行编译/链接功能，等同于 make
cmake --build .
```

最后，我们来运行一些 Case 测试一下吧:

```shell
./Tutorial 4294967296
./Tutorial 10
./Tutorial
```


## 第二步: 添加一个 Lib 库


## 第三步: 添加 Lib 库的使用要求


## 第四步: 安装和测试

### 安装规则

### 测试支持


## 第五步: 添加系统自检


## 第六步: 添加自定义命令和生成的文件


## 第七步: 构建安装程序


## 第八步: 添加对仪表板的支持


## 第九步: 混合静态链接和共享链接


## 第十步: 添加生成器表达式


## 第十一步: 添加导出配置


## 第十二步: 打包调试和发布







