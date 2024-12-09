from network_monitor import NetworkMonitor
from stream_forwarder import StreamForwarder
from model_training import Model
from site_processor import Site
import logging



def main():
    # Values to configure
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    node_count = 3
    k = 15

    network_monitor = NetworkMonitor(k, node_count)
    model = Model()
    sites = {site_id: Site(site_id, k, network_monitor) for site_id in range(node_count)}
    stream_forwarder = StreamForwarder(sites)
    with open('./../input/mixed_wc_day51_3.log', 'r', encoding='ISO-8859-1') as stream:
        logging.info("Parsing stream:")
        stream_forwarder.forward_to_site(stream)


if __name__ == "__main__":
    main()
