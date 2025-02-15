import torch.optim
import yaml
import logging

from network_monitor import NetworkMonitor
from stream_forwarder import StreamForwarder
from site_processor import Site

from utils.pipeline_utils import node_failure_simulation
from utils.pipeline_utils import train_model

def main():
    logging.basicConfig(
        level=logging.WARN, format="%(asctime)s %(levelname)s: %(message)s"
    )
    with open('config.yaml', 'r') as conf_file:
        conf = yaml.safe_load(conf_file)

    k = conf['k']
    node_count = conf['node_count']
    batch_size = conf['batch_size']

    network_monitor = NetworkMonitor(
        k,
        node_count,
        batch_size,
        conf['step_size'])

    optimizer = torch.optim.AdamW(
        network_monitor.fallback_mechanism.parameters(),
        lr=conf['learning_rate'],
        weight_decay=conf['weight_decay']
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
                if inference_due >= conf['inference_frequency'] * batch_size:
                    node_failure_simulation(network_monitor)
                    inference_due = 0
                    continue
                inference_due += 1
                train_model(network_monitor, optimizer, epochs=conf['epochs'])

if __name__ == "__main__":
    main()
