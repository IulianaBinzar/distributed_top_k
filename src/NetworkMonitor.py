import logging
import pandas as pd

class NetworkMonitor:
    def __init__(self, k: int, node_count: int):
        self.k = k
        self.node_count = node_count
        self.node_top_k = {}

    def receive_top_k(self, node_id, top_k, timestamp):
        if node_id not in self.node_top_k:
            self.node_top_k[node_id] = pd.DataFrame(columns=["timestamp",
                                                             "item",
                                                             "frequency"])

        for item, freq in top_k:
            self.node_top_k[node_id] = pd.concat([
                self.node_top_k[node_id],
                pd.DataFrame({"timestamp": [timestamp],
                              "item": [item],
                              "frequency": [freq]})
            ], ignore_index=True)

            logging.info(f"Received top-k for node {node_id} at timestamp {timestamp}: {top_k}")
