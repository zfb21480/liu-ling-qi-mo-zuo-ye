import numpy as np
import matplotlib.pyplot as plt

# 1. 导入numpy库
arr1 = np.array([[1, 2], [3, 4]])
print("题1:\n", arr1)

# 2. 一维数组a
a = np.array([4, 5, 6])
print("\n题2:")
print("类型:", type(a))
print("维度大小:", a.shape)
print("第一个元素:", a[0])

# 3. 二维数组b
b = np.array([[4, 5, 6], [1, 2, 3]])
print("\n题3:")
print("维度大小:", b.shape)
print("b(0,0):", b[0][0], " b(0,1):", b[0][1], " b(1,1):", b[1][1])

# 4. 各种矩阵
print("\n题4:")
a_zeros = np.zeros((3, 3), dtype=int)
b_ones = np.ones((4, 5))
c_eye = np.eye(4)
d_rand = np.random.rand(3, 2)
print("全0矩阵a:\n", a_zeros)
print("全1矩阵b:\n", b_ones)
print("单位矩阵c:\n", c_eye)
print("随机矩阵d:\n", d_rand)

# 5. 特定二维数组
a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
print("\n题5:")
print("a矩阵:\n", a)
print("a(2,3):", a[2][3], " a(0,0):", a[0][0])

# 6. 切片赋值
b = a[0:2, 2:4]
print("\n题6:")
print("b矩阵:\n", b)
print("b(0,0):", b[0][0])

# 7. 最后两行
c = a[1:3, :]
print("\n题7:")
print("c矩阵:\n", c)
print("c第一行最后一个元素:", c[0, -1])

# 8. 特定索引抽取
a = np.array([[1, 2], [3, 4], [5, 6]])
print("\n题8:")
print("特定元素:", a[[0, 1, 2], [0, 1, 0]])

# 9. 特定索引
a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
b = np.array([0, 2, 0, 1])
print("\n题9:")
print("索引选取结果:", a[np.arange(4), b])

# 10. 每个元素+10
a[np.arange(4), b] += 10
print("\n题10:")
print("更新后的a矩阵:\n", a)

# 11. 数据类型int
x = np.array([1, 2])
print("\n题11:")
print("x的数据类型:", x.dtype)

# 12. 数据类型float
x = np.array([1.0, 2.0])
print("\n题12:")
print("x的数据类型:", x.dtype)

# 13. 矩阵加法
x = np.array([[1, 2], [3, 4]], dtype=np.float64)
y = np.array([[5, 6], [7, 8]], dtype=np.float64)
print("\n题13:")
print("x + y:\n", x + y)
print("np.add(x, y):\n", np.add(x, y))

# 14. 矩阵减法
print("\n题14:")
print("x - y:\n", x - y)
print("np.subtract(x, y):\n", np.subtract(x, y))

# 15. 矩阵乘法
print("\n题15:")
print("x * y:\n", x * y)
print("np.multiply(x, y):\n", np.multiply(x, y))
print("np.dot(x, y):\n", np.dot(x, y))

# 非方阵试试
x2 = np.array([[1, 2, 3], [4, 5, 6]])
y2 = np.array([[1, 2], [3, 4], [5, 6]])
print("非方阵 np.dot(x2, y2):\n", np.dot(x2, y2))

# 16. 矩阵除法
print("\n题16:")
print("x / y:\n", np.divide(x, y))

# 17. 开方
print("\n题17:")
print("sqrt(x):\n", np.sqrt(x))

# 18. 矩阵点乘
print("\n题18:")
print("x.dot(y):\n", x.dot(y))
print("np.dot(x, y):\n", np.dot(x, y))

# 19. 求和
print("\n题19:")
print("总和:", np.sum(x))
print("列求和:", np.sum(x, axis=0))
print("行求和:", np.sum(x, axis=1))

# 20. 平均值
print("\n题20:")
print("平均值:", np.mean(x))
print("列平均:", np.mean(x, axis=0))
print("行平均:", np.mean(x, axis=1))

# 21. 转置
print("\n题21:")
print("转置:\n", x.T)

# 22. 指数
print("\n题22:")
print("e的指数:\n", np.exp(x))

# 23. 最大值下标
print("\n题23:")
print("最大值索引:", np.argmax(x))
print("列最大索引:", np.argmax(x, axis=0))
print("行最大索引:", np.argmax(x, axis=1))

# 24. 画图：y = x*x
print("\n题24: 画图 y = x^2")
x1 = np.arange(0, 100, 0.1)
y1 = x1 * x1
plt.plot(x1, y1)
plt.title("y = x^2")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()

# 25. 画图：正弦和余弦
print("\n题25: 正弦和余弦图")
x = np.arange(0, 3 * np.pi, 0.1)
y_sin = np.sin(x)
y_cos = np.cos(x)
plt.plot(x, y_sin, label="sin(x)")
plt.plot(x, y_cos, label="cos(x)")
plt.title("正弦 vs 余弦")
plt.legend()
plt.grid(True)
plt.show()
