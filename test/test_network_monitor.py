import unittest
from datetime import datetime

from network_monitor import NetworkMonitor


class TestNetworkMonitor(unittest.TestCase):
    def test_receive_top_k(self):
        network_monitor = NetworkMonitor(5, 3)
        top_k_site01 = [(9, "a"), (8, "b"), (4, "c")]
        top_k_site2 = [(3, "j"), (2, "i"), (1, "x")]
        for _ in range(4):
            test_timestamp = datetime.now()
            network_monitor.receive_top_k(0, top_k_site01, test_timestamp)
            network_monitor.receive_top_k(1, top_k_site01, test_timestamp)
            network_monitor.receive_top_k(2, top_k_site2, test_timestamp)
        reported_dataframe = network_monitor.sliding_window_df
        self.assertEqual(4, len(reported_dataframe))
        self.assertEqual([1, 2, 3], reported_dataframe["node_1_top_k"].iloc[2])
