import logging
from os import times
from datetime import timedelta
import pandas as pd

class NetworkMonitor:
    def __init__(self, k: int):
        self.k = k
        self.node_top_k = {}
        self.last_aggregate_time = None

    def receive_top_k(self, node_id, top_k, timestamp):
        """
         Converts top_k lists to panda dataframes for further processing
        """
        logging.debug(f"Network Monitor received top-k for node {node_id} at timestamp {timestamp}: {top_k}")
        if node_id not in self.node_top_k:
            self.node_top_k[node_id] = pd.DataFrame(columns=["timestamp",
                                                             "item",
                                                             "frequency"])
        for freq, item in top_k:
            self.node_top_k[node_id] = pd.concat([
                self.node_top_k[node_id],
                pd.DataFrame({"timestamp": [timestamp],
                              "item": [item],
                              "frequency": [freq]})
            ], ignore_index=True)

        logging.debug(f"Node {node_id} dataframe: \n{self.node_top_k[node_id]}")

        if not self.last_aggregate_time:
            self.last_aggregate_time = timestamp

        if timestamp - self.last_aggregate_time > timedelta(minutes=10):
            self.correlate_node_results()
            self.last_aggregate_time = timestamp


    def correlate_node_results(self):
        global_dataframe = pd.concat(self.node_top_k, keys=self.node_top_k.keys(), names=["site_id", "row_index"])
        global_dataframe.reset_index(level="row_index", drop=True, inplace=True)
        global_dataframe = global_dataframe.pivot_table(index="timestamp", columns="site_id", values="frequency", aggfunc="sum")
        global_dataframe = global_dataframe.fillna(0)
        correlation_matrix = global_dataframe.corr()
        logging.info(f"Combined data \n {global_dataframe}")
        logging.info(f"Correlation matrix \n {correlation_matrix}")
        return correlation_matrix

