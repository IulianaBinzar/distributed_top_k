import logging
from os import times
from datetime import timedelta
import pandas as pd

class NetworkMonitor:
    def __init__(self, k: int, node_count: int):
        self.k = k
        self.node_top_k = {}
        self.node_count = node_count
        self.latest_data_collected = [False for _ in range(self.node_count)]

    def receive_top_k(self, node_id, top_k, timestamp):
        """
         Converts top_k lists to panda dataframes for further processing
        """
        logging.info(f"Network Monitor received top-k for node {node_id} at timestamp {timestamp}: {top_k}")
        top_k_dataframe = pd.DataFrame(columns=["timestamp",
                                                "url",
                                                "frequency"])
        for freq, item in top_k:
            top_k_dataframe = pd.concat([
                top_k_dataframe,
                pd.DataFrame({"timestamp": [timestamp],
                              "url": [item],
                              "frequency": [freq]})
            ], ignore_index=True)

        self.node_top_k[node_id] = top_k_dataframe
        self.latest_data_collected[node_id] = True
        logging.info(f"Node {node_id} dataframe: \n{self.node_top_k[node_id]}")

        # if not self.last_aggregate_time:
        #     self.last_aggregate_time = timestamp
        #
        # if timestamp - self.last_aggregate_time > timedelta(minutes=10):
        #     self.correlate_node_results()
        #     self.last_aggregate_time = timestamp

    #     if all(self.latest_data_collected):
    #         self.correlate_node_results()
    #         self.latest_data_collected = [False for _ in range(self.node_count)]
    #
    #
    # def correlate_node_results(self):
    #     unique_urls = set()
    #     for x, dataframe in self.node_top_k.items():
    #         unique_urls.update(dataframe["url"].unique())
    #     unique_urls = sorted(unique_urls)
    #     ranked_dataframe = pd.DataFrame(index=unique_urls)
    #     for site_id, df in self.node_top_k.items():
    #         ranked_urls = df.sort_values(by="frequency", ascending=False)["url"].reset_index(drop=True)
    #         rank_dict = {url: rank + 1 for rank, url in enumerate(ranked_urls)}
    #         ranked_dataframe[f"Node_{site_id}"] = ranked_dataframe.index.map(rank_dict)
    #     ranked_dataframe = ranked_dataframe.fillna(0)
    #     correlation_matrix = ranked_dataframe.corr(method='spearman')
    #     return correlation_matrix

