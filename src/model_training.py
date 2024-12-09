from torch import nn
import torch.nn.functional as F
import logging

def masked_loss(output, target, mask):
    loss = F.cross_entropy(output, target, reduction="none")
    mask_loss = loss * mask
    return mask_loss.sum() / mask.sum()

class Model(nn.Module):
    def train_fallback_mechanism(self, model, input_tenosr, mask, target_tensor, optimizer, epochs):
        model.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            output = model(input_tenosr)
            loss = masked_loss(output, target_tensor, mask)
            loss.backward()
            optimizer.step()
            logging.info(f"Epoch {epoch + 1}, Loss: {loss.item()}")

