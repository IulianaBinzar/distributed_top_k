from NetworkMonitor import NetworkMonitor
from StreamForwarder import StreamForwarder
from Site import Site
import logging
import random

from HeavyKeeper import HeavyKeeper


def main():
    # Values to configure
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    node_count = 3
    k = 5

    network_monitor = NetworkMonitor(k, node_count)
    sites = {site_id: Site(site_id, k, network_monitor) for site_id in range(node_count)}
    stream_forwarder = StreamForwarder(sites)
    with open('./../input/mixed_wc_day51_3.log', 'r', encoding='ISO-8859-1') as stream:
        logging.info("Parsing stream:")
        stream_forwarder.forward_to_site(stream)


if __name__ == "__main__":
    main()
