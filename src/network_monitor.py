from collections import defaultdict

import pandas as pd
import logging

from fallback_mechanism import FallbackMechanism
from utils import prepare_and_validate_tensor

class NetworkMonitor:
    def __init__(self, k: int, node_count: int):
        self.k = k
        self.single_top_k = defaultdict(list)
        self.node_count = node_count
        self.latest_data_timestamp = None
        self.latest_data_collected = [False for _ in range(self.node_count)]
        self.window_size = 20
        self.sliding_window_df = pd.DataFrame(columns=["timestamp"] +
                                                      [f"node_{x}_top_k" for x in range(self.node_count)])
        self.unique_urls = set()
        self.url_to_id = defaultdict(int)
        self.id_to_url = defaultdict(str)
        self.fallback_mechanism = FallbackMechanism(input_size=k * node_count,
                                                    output_size=k,
                                                    hidden_size=64,
                                                    num_layers=2,
                                                    dropout=0.2
                                                    )

    def receive_top_k(self, node_id, top_k, timestamp):
        """
         Converts top_k lists to panda dataframes for further processing
        """
        logging.debug(f"Network Monitor received top-k for node {node_id} at timestamp {timestamp}: {top_k}")
        top_k_list = []
        for freq, item in top_k:
            if item not in self.unique_urls:
                self.unique_urls.add(item)
                item_code = len(self.unique_urls)
                self.url_to_id[item] = item_code
                self.id_to_url[item_code] = item
            top_k_list.append(self.url_to_id[item])
        self.single_top_k[node_id] = top_k_list
        self.latest_data_collected[node_id] = True
        logging.info(f"Node {node_id} dataframe: \n{self.single_top_k[node_id]}")

        if not self.latest_data_timestamp:
            self.latest_data_timestamp = timestamp
        if all(self.latest_data_collected):
            self.prepare_data_for_model()
            self.latest_data_collected = [False for _ in range(self.node_count)]
            self.latest_data_timestamp = None

    def prepare_data_for_model(self, step_size=5):
        new_row ={"timestamp": self.latest_data_timestamp}
        for i in range(self.node_count):
            new_row[f"node_{i}_top_k"] = self.single_top_k[i]
        new_row_df = pd.DataFrame([new_row])
        if not len(self.sliding_window_df):
            self.sliding_window_df = new_row_df
        else:
            self.sliding_window_df = pd.concat([self.sliding_window_df, new_row_df], ignore_index=True)
        if len(self.sliding_window_df) >= self.window_size:
            batch, mask = prepare_and_validate_tensor(self.sliding_window_df,
                                  self.window_size,
                                  self.node_count,
                                  self.k
                                  )
            self.sliding_window_df = self.sliding_window_df[step_size:].reset_index(drop=True)
            return batch, mask
