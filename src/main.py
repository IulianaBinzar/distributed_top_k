import torch.optim

from network_monitor import NetworkMonitor
from stream_forwarder import StreamForwarder
from site_processor import Site
import logging



def main():
    # Values to configure
    logging.basicConfig(
        level=logging.WARN,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    node_count = 3
    # Node 3 is too sparsely populated, will have to change back to 4
    k = 15
    batch_size = 3
    step_size = 1

    network_monitor = NetworkMonitor(k, node_count, batch_size)
    optimizer = torch.optim.Adam(network_monitor.fallback_mechanism.parameters(), lr=0.001)
    sites = {site_id: Site(site_id, k, network_monitor) for site_id in range(node_count)}
    stream_forwarder = StreamForwarder(sites)

    with open('./../input/mixed_wc_day51_3.log', 'r', encoding='ISO-8859-1') as stream:
        logging.info("Parsing stream:")
        inference_due = 0
        for line_id, line in enumerate(stream):
            stream_forwarder.forward_to_site(line)
            if len(network_monitor.sliding_window_df) >= batch_size:
                # Inference
                if inference_due >= 10 * batch_size:
                    network_monitor.fallback_mechanism.eval()
                    with torch.no_grad():
                        tensor, mask, _ = network_monitor.prepare_and_validate_tensor()
                        network_monitor.sliding_window_df = network_monitor.sliding_window_df[step_size:].reset_index(
                            drop=True)
                        predictions = network_monitor.fallback_mechanism(tensor)
                        predicted_urls = [
                            [network_monitor.id_to_url[x.item()] for x in pred]
                            for pred in torch.topk(predictions, k=5, dim=-1).indices
                        ]
                        logging.warn(f"Predicted Top-K URLs for node 0:{predicted_urls}")
                    inference_due = 0
                    continue
                inference_due += 1
                # Training
                logging.info(f"Processing new batch")
                tensor, mask, target_tensor = network_monitor.prepare_and_validate_tensor()
                network_monitor.sliding_window_df = network_monitor.sliding_window_df[step_size:].reset_index(drop=True)
                network_monitor.train_fallback_mechanism(
                    tensor,
                    mask,
                    target_tensor,
                    optimizer,
                    epochs=1
                )



if __name__ == "__main__":
    main()
