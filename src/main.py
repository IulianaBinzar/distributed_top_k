import torch.optim

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
    epochs = 10
    batch_size = 20

    network_monitor = NetworkMonitor(k, node_count)
    model = Model()
    optimizer = torch.optim.Adam(network_monitor.fallback_mechanism.parameters(), lr=0.001)
    sites = {site_id: Site(site_id, k, network_monitor) for site_id in range(node_count)}
    stream_forwarder = StreamForwarder(sites)

    with open('./../input/mixed_wc_day51_3.log', 'r', encoding='ISO-8859-1') as stream:
        logging.info("Parsing stream:")
        for line_id, line in enumerate(stream):
            stream_forwarder.forward_to_site(line)
            if len(network_monitor.sliding_window_df) >= batch_size:
                logging.info(f"Processing new batch")
                batch, mask, target_tensor = network_monitor.prepare_data_for_model()
                network_monitor.model.train_fallback_mechanism(
                    network_monitor.fallback_mechanism,
                    batch,
                    mask,
                    target_tensor,
                    optimizer,
                    epochs=1
                )
            if line_id % (batch_size * 10) == 0:
                network_monitor.fallback_mechanism.eval()
                with torch.no_grad():
                    batch, mask, _ = network_monitor.prepare_data_for_model(step_size=0)
                    predictions = network_monitor.fallback_mechanism(batch)
                    predicted_urls = [
                        [network_monitor.id_to_url[x.item()] for x in pred]
                        for pred in torch.topk(predictions, k=5, dim=-1).indices
                    ]
                    logging.info(f"Predicted Top-K URLs for node 0:{predicted_urls}")


if __name__ == "__main__":
    main()
