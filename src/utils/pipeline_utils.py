import torch
import logging
from itertools import product
from utils.common_utils import report_node_failure, evaluate_top_k, multi_label_loss
from fallback_mechanism import FallbackMechanism

def slide_df_window(network_monitor):
    network_monitor.sliding_window_df = network_monitor.sliding_window_df[network_monitor.step_size:].reset_index(drop=True)

def node_failure_simulation(network_monitor):
    network_monitor.fallback_mechanism.eval()
    with torch.no_grad():
        tensor, mask, target_tensor = network_monitor.prepare_and_validate_tensor()
        slide_df_window(network_monitor)
        predictions = network_monitor.fallback_mechanism(tensor)  # raw logits
        probabilities = torch.sigmoid(predictions)  # convert logits to probabilities
        pred_ids = torch.topk(probabilities, network_monitor.k, dim=-1).indices[0].tolist()
        target_indices = (target_tensor[0] == 1).nonzero(as_tuple=True)[0].tolist()
        report_node_failure(pred_ids, target_indices, network_monitor.k, detailed=True)

def train_model(network_monitor, optimizer, epochs):
    logging.debug("Processing new batch")
    tensor, mask, target_tensor = network_monitor.prepare_and_validate_tensor()
    slide_df_window(network_monitor)
    network_monitor.train_fallback_mechanism(tensor, mask, target_tensor, optimizer, epochs)