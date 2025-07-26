import numpy as np

# 输入
x = np.array([0.5, 0.3])

# 权重
w = {
    'w1': 0.2, 'w2': -0.4,
    'w3': 0.5, 'w4': 0.6,
    'w5': 0.1, 'w6': -0.5,
    'w7': -0.3, 'w8': 0.8
}

# 激活函数：sigmoid
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# 前向传播
h1_input = w['w1'] * x[0] + w['w2'] * x[1]
h2_input = w['w3'] * x[0] + w['w4'] * x[1]
h1 = sigmoid(h1_input)
h2 = sigmoid(h2_input)

o1_input = w['w5'] * h1 + w['w6'] * h2
o2_input = w['w7'] * h1 + w['w8'] * h2
o1 = sigmoid(o1_input)
o2 = sigmoid(o2_input)

# 输出结果
print("NumPy实现：")
print("输入: x1, x2:", x)
print("输出: y1, y2:", np.array([o1, o2]))
