import unittest
from datetime import datetime

from NetworkMonitor import NetworkMonitor


class TestNetworkMonitor(unittest.TestCase):
    def test_receive_top_k(self):
        network_monitor = NetworkMonitor(5, 3)
        top_k_site12 = [(9, "a"), (8, "b"), (4, "c")]
        top_k_site3 = [(3, "j"), (2, "i"), (1, "x")]
        top_k_site12_2 = [(91, "a1"), (81, "b1"), (41, "c1")]
        top_k_site3_2 = [(31, "j1"), (12, "i1"), (1, "x1")]
        test_timestamp = datetime.now()
        test_timestamp2 = datetime.now()
        network_monitor.receive_top_k(0, top_k_site12, test_timestamp)
        network_monitor.receive_top_k(1, top_k_site12, test_timestamp)
        network_monitor.receive_top_k(2, top_k_site3, test_timestamp)
        network_monitor.receive_top_k(0, top_k_site12_2, test_timestamp2)
        network_monitor.receive_top_k(1, top_k_site3, test_timestamp2)
        network_monitor.receive_top_k(2, top_k_site3_2, test_timestamp2)
        res_corr_matrix = network_monitor.correlate_node_results()
        self.assertEqual(3, len(res_corr_matrix))
        # TODO fix this