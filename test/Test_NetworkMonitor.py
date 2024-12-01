import unittest
from datetime import datetime

from NetworkMonitor import NetworkMonitor


class TestNetworkMonitor(unittest.TestCase):
    def test_receive_top_k(self):
        network_monitor = NetworkMonitor(5)
        top_k_site1 = [(9, "a"), (8, "b"), (4, "c")]
        top_k_site2 = [(9, "a"), (8, "b"), (4, "c")]
        top_k_site3 = [(3, "j"), (2, "i"), (1, "x")]
        network_monitor.receive_top_k(0, top_k_site1, datetime.now())
        network_monitor.receive_top_k(0, top_k_site2, datetime.now())
        network_monitor.receive_top_k(0, top_k_site3, datetime.now())
        res_corr_matrix = network_monitor.correlate_node_results()
        self.assertEqual(res_corr_matrix, None)
        # TODO fix this