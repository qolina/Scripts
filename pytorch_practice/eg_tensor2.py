
import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.manual_seed(1)

#V_data = [1, 2, 3]
#V = torch.Tensor(V_data)
#print V
#
#M_data = [[1, 2, 3], [4, 5, 6]]
#M = torch.Tensor(M_data)
#print M
#
#T_data = [[[1, 2], [3, 4]],
#        [[5, 6],[7, 8]]]
#T = torch.Tensor(T_data)
#print T
#
#x = torch.randn(3, 4, 5)
#print x
#
#x = torch.Tensor([1, 2, 3])
#y = torch.Tensor([4, 5, 6])
#z = x+y
#print z
#
#x_1 = torch.randn(2, 5)
#y_1 = torch.randn(3, 5)
#z_1 = torch.cat([x_1, y_1])
#print z_1
#
#x_2 = torch.randn(2, 3)
#y_2 = torch.randn(2, 5)
#z_2 = torch.cat([x_2, y_2], 1)
#print z_2
#
#x = torch.randn(2, 3, 4)
#print x
#print x.view(2, 12)
#print x.view(2, -1)

x = autograd.Variable(torch.Tensor([1, 2, 3]), requires_grad=True)
print x.data
y = autograd.Variable(torch.Tensor([4, 5, 6]), requires_grad=True)
z = x+y
print z.data
print z.creator

s = z.sum()
print s
print s.creator

s.backward()
print x.grad
