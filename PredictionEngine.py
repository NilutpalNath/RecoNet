# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:11:42 2021

@author: Debangan Daemon
"""
import torch
from Model import AutoEncoder


# Calculate AutoEncoder outputs
class PredictionEngine:
  def __init__(self):
    self.layer_sizes = [6670, 8192, 2048, 512, 256]
    self.model = AutoEncoder(layer_sizes=self.layer_sizes, nl_type='selu', is_constrained=True, dp_drop_prob=0.0, last_layer_activations=False)
    self.model.load_state_dict(torch.load('autoEncoder.pth'))
    try:
        self.model = self.model.cuda()
    except:
        pass

  def getPredictedRatings(self, user_dat, user_dl):
    for data in user_dl:
      inputs = data
      try:
          inputs = inputs.cuda()
      except:
          pass
      inputs = inputs.float()

      outputs = self.model(inputs)
      break

    return outputs.cpu().detach().numpy()