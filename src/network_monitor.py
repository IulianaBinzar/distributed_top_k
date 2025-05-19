from collections import defaultdict
import pandas as pd
import logging
import torch

from fallback_mechanism import FallbackMechanism
from utils.common_utils import df_to_tensors, multi_label_loss

class NetworkMonitor:
    def __init__(self, k: int, node_count: int, batch_size: int, step_size: int):
        self.k = k
        self.single_top_k = defaultdict(list)
        self.node_count = node_count
        self.latest_data_timestamp = None
        self.latest_data_collected = [False for _ in range(self.node_count)]
        self.window_size = batch_size
        self.step_size = step_size
        self.sliding_window_df = pd.DataFrame(columns=["timestamp"] + [f"node_{x}_top_k" for x in range(self.node_count)])
        self.unique_urls = set()
        self.url_to_id = defaultdict(int)
        self.id_to_url = defaultdict(str)
        self.vocab_size = 10000
        self.fallback_mechanism = FallbackMechanism(
            input_size=k * node_count,
            output_size=self.vocab_size,
            hidden_size=128,
            num_layers=2,
            dropout=0.2,
        )

    def receive_top_k(self, node_id, top_k, timestamp):
        logging.debug(f"Network Monitor received top-k for node {node_id} at timestamp {timestamp}: {top_k}")
        top_k_list = []
        for freq, item in top_k:
            if item not in self.unique_urls:
                self.unique_urls.add(item)
                item_code = len(self.unique_urls)  # 1-based indexing
                self.url_to_id[item] = item_code
                self.id_to_url[item_code] = item
            top_k_list.append(self.url_to_id[item])
        self.single_top_k[node_id] = top_k_list
        self.latest_data_collected[node_id] = True
        logging.debug(f"Node {node_id} data: {self.single_top_k[node_id]}")

        if not self.latest_data_timestamp:
            self.latest_data_timestamp = timestamp
        if all(self.latest_data_collected):
            self.prepare_data_for_model()
            self.latest_data_collected = [False for _ in range(self.node_count)]
            self.latest_data_timestamp = None

    def prepare_data_for_model(self, step_size=5):
        new_row = {"timestamp": self.latest_data_timestamp}
        for i in range(self.node_count):
            new_row[f"node_{i}_top_k"] = self.single_top_k[i]
        new_row_df = pd.DataFrame([new_row])
        if not len(self.sliding_window_df):
            self.sliding_window_df = new_row_df
        else:
            self.sliding_window_df = pd.concat([self.sliding_window_df, new_row_df], ignore_index=True)

    def prepare_and_validate_tensor(self):
        data_frame = self.sliding_window_df.copy().drop(columns="timestamp")
        input_tensor, mask = df_to_tensors(data_frame, self.window_size, self.node_count, self.k)
        target_column = "node_0_top_k"
        last_top_k = data_frame[target_column].iloc[-1]
        if not isinstance(last_top_k, list):
            last_top_k = [last_top_k]
        target_vector = torch.zeros(self.vocab_size, dtype=torch.float32)
        for item_id in last_top_k:
            idx = item_id - 1
            if 0 <= idx < self.vocab_size:
                target_vector[idx] = 1.0
        target_tensor = target_vector.unsqueeze(0)
        return input_tensor, mask, target_tensor

    def train_fallback_mechanism(self, input_tensor, mask, target_tensor, optimizer, epochs):
        self.fallback_mechanism.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            output = self.fallback_mechanism(input_tensor)
            loss = multi_label_loss(output, target_tensor)
            logging.debug(f"Epoch {epoch + 1}, Loss: {loss.item()}")
            loss.backward()
            optimizer.step()
            logging.debug(f"Output Logits: {output}")
            logging.debug(f"Target Multi-Hot: {target_tensor}")
