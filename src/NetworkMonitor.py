class NetworkMonitor:
    def __init__(self, k: int, node_count: int):
        self.k = k
        self.node_count = node_count
        self.node_top_k = {}