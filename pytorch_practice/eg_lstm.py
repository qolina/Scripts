import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.manual_seed(1)

lstm = nn.LSTM(3, 3)
inputs = [autograd.Variable(torch.randn((1, 3))) for _ in range(5)]

hidden = (autograd.Variable(torch.randn(1, 1, 3)), 
        autograd.Variable(torch.randn((1, 1, 3))))

for i in inputs:
    out, hidden = lstm(i.view(1, 1, -1), hidden)

print "#######################"
inputs = torch.cat(inputs).view(len(inputs), 1, -1)
hidden = (autograd.Variable(torch.randn(1, 1, 3)),
        autograd.Variable(torch.randn(1, 1, 3)))
out, hidden = lstm(inputs, hidden)

print out
print hidden
