# micro-python快速入门

从本节开始，我们将会以micro-python为基本，带你快速了解如何用micro-python来进行相关的嵌入式软件的开发。

你可能会觉得奇怪：嗯？嵌入式开发为什么不用 C 语言？

主要原因是，我不希望开发语言成为实战项目的障碍。先不说 C 语言本身的难度，光是它需要交叉编译的特性和不够便捷的调试方式，就已经很影响效率了。

相比之下，使用比较简单的 Python 语言，开发和调试都会非常方便。当然，选择 Python 还有别的好处，你在后面的实战过程中可以逐渐感受到。

不过，你可能还是不放心：嵌入式硬件的计算资源都非常有限，在开发板上面运行 Python 代码可行吗？

这确实是一个挑战，好在 [MicroPython](https://docs.micropython.org/) 项目已经提供了解决方案。

MicroPython 是专门为嵌入式系统打造的 Python 实现。它完整实现了 Python3.4 的语言特性，部分支持 Python3.5 的特性。在标准库方面，MicroPython 实现了 Python 语言的一个子集，另外还增加了与底层硬件交互的库模块。

参考资源：

1. [MicroPython](https://docs.micropython.org/) 官方文档。
