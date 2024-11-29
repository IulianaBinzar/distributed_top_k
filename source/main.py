from StreamForwarder import StreamForwarder
from Site import Site
import logging
import random

from distributed_top_k.source.HeavyKeeper import HeavyKeeper


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    k = 10
    sites = {site_id: Site(site_id, k) for site_id in range(3)}
    stream_forwarder = StreamForwarder(sites)
    with open('./input/mixed_wc_day51_3.log', 'r', encoding='ISO-8859-1') as stream:
        logging.info("Parsing stream.")
        stream_forwarder.forward_to_site(stream)


if __name__ == "__main__":
    main()
