from distributed_top_k.StreamForwarder import StreamForwarder


def main():
    sites = {site_id: Site(site_id) for site_id in range(3)}
    stream_forwarder = StreamForwarder(sites)
    with open('mixed_wc_day51_3.log', 'r') as stream:
        stream_forwarder.forward_to_site(stream)


