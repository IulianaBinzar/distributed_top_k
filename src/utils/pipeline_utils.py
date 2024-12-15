import torch
import logging

from utils.common_utils import report_node_failure

def slide_df_window(network_monitor):
    network_monitor.sliding_window_df = (
        network_monitor.sliding_window_df[network_monitor.step_size:].reset_index(
            drop=True
        )
    )

def node_failure_simulation(network_monitor):
    network_monitor.fallback_mechanism.eval()
    with torch.no_grad():
        tensor, mask, target_tensor = (
            network_monitor.prepare_and_validate_tensor()
        )
        slide_df_window(network_monitor)
        predictions = network_monitor.fallback_mechanism(tensor)
        pred_ids = [
            [x.item() for x in pred]
            for pred in torch.topk(predictions, network_monitor.k, dim=-1).indices
        ]
        pred_ids = pred_ids[0]
        actual_ids = target_tensor.to(torch.int).tolist()[0]
        report_node_failure(pred_ids, actual_ids, network_monitor.k, detailed=True)

def train_model(network_monitor, optimizer):
    logging.info(f"Processing new batch")
    tensor, mask, target_tensor = (
        network_monitor.prepare_and_validate_tensor()
    )
    slide_df_window(network_monitor)
    network_monitor.train_fallback_mechanism(
        tensor, mask, target_tensor, optimizer, epochs=1
    )