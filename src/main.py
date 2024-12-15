import torch.optim

from network_monitor import NetworkMonitor
from stream_forwarder import StreamForwarder
from site_processor import Site
import logging

from utils.pipeline_utils import node_failure_simulation
from utils.pipeline_utils import train_model

def main():
    # Values to configure
    logging.basicConfig(
        level=logging.WARN, format="%(asctime)s %(levelname)s: %(message)s"
    )
    node_count = 3
    # Node 3 is too sparsely populated, will have to change back to 4
    k = 10
    batch_size = 4
    step_size = 1

    # Instantiations
    network_monitor = NetworkMonitor(k, node_count, batch_size, step_size)
    optimizer = torch.optim.Adam(
        network_monitor.fallback_mechanism.parameters(), lr=0.001
    )
    sites = {
        site_id: Site(site_id, k, network_monitor) for site_id in range(node_count)
    }
    stream_forwarder = StreamForwarder(sites)

    # Workflow
    with open("./../input/mixed_wc_day51_3.log", "r", encoding="ISO-8859-1") as stream:
        logging.info("Parsing stream:")
        inference_due = 0
        for line_id, line in enumerate(stream):
            stream_forwarder.forward_to_site(line)
            if len(network_monitor.sliding_window_df) >= batch_size:
                # Inference
                if inference_due >= 10 * batch_size:
                        node_failure_simulation(network_monitor)
                        inference_due = 0
                        continue
                inference_due += 1
                train_model(network_monitor, optimizer)


if __name__ == "__main__":
    main()
