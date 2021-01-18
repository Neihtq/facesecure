import torch
import torch.nn as nn


class RefFaceEmbeddingModel(nn.Module):
    ''' Reference model for lower bound of accuracy'''
    def __init__(self):
        super(RefFaceEmbeddingModel, self).__init__()
        self.linear = nn.Linear(150528, 128)

    def l2_norm(self, input):
        input_size = input.size()
        buffer = torch.pow(input, 2)
        normp = torch.sum(buffer, 1).add_(1e-10)
        norm = torch.sqrt(normp)
        _output = torch.div(input, norm.view(-1, 1).expand_as(input))
        output = _output.view(input_size)
        return output

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.linear(x)
        features = self.l2_norm(x)

        alpha = 10
        features = features * alpha
        return features
