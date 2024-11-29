# from distributed_top_k.StreamForwarder import StreamForwarder
# from distributed_top_k.Site import Site

from StreamForwarder import StreamForwarder
from Site import Site
import logging

from distributed_top_k.HeavyKeeper import HeavyKeeper


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    # k = 10
    # sites = {site_id: Site(site_id, k) for site_id in range(3)}
    # stream_forwarder = StreamForwarder(sites)
    # with open('mixed_wc_day51_3.log', 'r', encoding='ISO-8859-1') as stream:
    #     logging.info("Parsing stream.")
    #     stream_forwarder.forward_to_site(stream)
    k = 3
    myHK = HeavyKeeper(k)
    myHK.process_log("aaa")
    myHK.process_log("aaa")
    myHK.process_log("aaa")
    myHK.process_log("bbb")
    myHK.process_log("aaa")
    myHK.process_log("ccc")
    myHK.process_log("ccc")
    myHK.process_log("ddd")
    logging.info(f"top-k: {myHK.get_string_top_k()}")
    myHK.get_string_top_k()

if __name__ == "__main__":
    main()
