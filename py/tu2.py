import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 定义函数 f(x, y)
def f(x, y):
    return 100*(x**2 - y**2) / (x**2 + y**2)**2

# 创建 x 和 y 的网格
x = np.linspace(0.01, 1, 400)  # 避免除零，从0.01开始
y = np.linspace(0.01, 1, 400)
X, Y = np.meshgrid(x, y)

# 计算 z 值
Z = f(X, Y)

# 绘制三维图像
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制表面图
surf = ax.plot_surface(X, Y, Z, cmap='RdBu', edgecolor='none')
ax.set_title(r'$f(x, y) = \frac{x^2 - y^2}{(x^2 + y^2)^2}$')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x, y)')

# 设置 z 轴范围
ax.set_zlim(-10, 10)

# 添加颜色条
cbar = fig.colorbar(surf, shrink=0.5, aspect=5, format='%.2f')
cbar.set_ticks(np.linspace(-10, 10, num=11))

plt.show()
