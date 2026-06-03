import numpy as np
import matplotlib.pyplot as plt

# 定义函数 f(x, y)
def f(x, y):
    return (x**2 - y**2) / (x**2 + y**2)**2

# 创建 x 和 y 的网格
x = np.linspace(0.01, 1, 400)  # 避免除零，从0.01开始
y = np.linspace(0.01, 1, 400)
X, Y = np.meshgrid(x, y)

# 计算 z 值
Z = f(X, Y)

# 绘制图像
plt.figure(figsize=(8, 6))
cp = plt.contourf(X, Y, Z, levels=50, cmap='RdBu')
plt.colorbar(cp)
plt.title(r'$f(x, y) = \frac{x^2 - y^2}{(x^2 + y^2)^2}$')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
