import unittest
from datetime import datetime

from NetworkMonitor import NetworkMonitor


class TestNetworkMonitor(unittest.TestCase):
    def test_receive_top_k(self):
        network_monitor = NetworkMonitor(5, 3)
        top_k_site01 = [(9, "a"), (8, "b"), (4, "c")]
        top_k_site2 = [(3, "j"), (2, "i"), (1, "x")]
        test_timestamp = datetime.now()
        network_monitor.receive_top_k(0, top_k_site01, test_timestamp)
        network_monitor.receive_top_k(1, top_k_site01, test_timestamp)
        network_monitor.receive_top_k(2, top_k_site2, test_timestamp)
        # res_corr_matrix = network_monitor.correlate_node_results()
        # self.assertEqual(1, int(res_corr_matrix["Node_0"]["Node_1"]))
        # self.assertNotEqual(1, int(res_corr_matrix["Node_0"]["Node_2"]))
        reported_dataframe = network_monitor.sliding_window_df
        self.assertEqual(3, len(reported_dataframe))
