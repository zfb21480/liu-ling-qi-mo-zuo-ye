import torch
import torch.nn.functional as F

# 输入
x = torch.tensor([0.5, 0.3])

# 权重
w1, w2 = 0.2, -0.4
w3, w4 = 0.5, 0.6
w5, w6 = 0.1, -0.5
w7, w8 = -0.3, 0.8

# 前向传播
h1_input = w1 * x[0] + w2 * x[1]
h2_input = w3 * x[0] + w4 * x[1]
h1 = torch.sigmoid(h1_input)
h2 = torch.sigmoid(h2_input)

o1_input = w5 * h1 + w6 * h2
o2_input = w7 * h1 + w8 * h2
o1 = torch.sigmoid(o1_input)
o2 = torch.sigmoid(o2_input)

# 输出
print("\nPyTorch实现：")
print("输入: x1, x2:", x)
print("输出: y1, y2:", torch.tensor([o1, o2]))
