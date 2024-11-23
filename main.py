# from distributed_top_k.StreamForwarder import StreamForwarder
# from distributed_top_k.Site import Site

from StreamForwarder import StreamForwarder
from Site import Site
import logging

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    sites = {site_id: Site(site_id) for site_id in range(3)}
    stream_forwarder = StreamForwarder(sites)
    logging.info("OOOfffff")
    with open('mixed_wc_day51_3.log', 'r', encoding='ISO-8859-1') as stream:
        logging.info("Opened the stream")
        stream_forwarder.forward_to_site(stream)

if __name__ == "__main__":
    main()
