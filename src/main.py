import torch.optim
import yaml
import logging
import boto3
import io

from network_monitor import NetworkMonitor
from stream_forwarder import StreamForwarder
from site_processor import Site

from utils.pipeline_utils import node_failure_simulation
from utils.pipeline_utils import train_model

def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s",
        handlers = [
            logging.FileHandler("../output/logfile_2files.log"),
            logging.StreamHandler()
        ]
    )
    with open('../config.yaml', 'r') as conf_file:
        conf = yaml.safe_load(conf_file)

    k = conf['k']
    node_count = conf['node_count']
    batch_size = conf['batch_size']

    # List log files in S3 bucket
    s3_bucket = "fifa-access-logs-25"
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=s3_bucket)
    log_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.log')]
    logging.info(F"Response: {response}")
    logging.info(f"Found log files: {log_files}")

    network_monitor = NetworkMonitor(
        k,
        node_count,
        batch_size,
        conf['step_size']
    )

    optimizer = torch.optim.AdamW(
        network_monitor.fallback_mechanism.parameters(),
        lr=conf['learning_rate'],
        weight_decay=conf['weight_decay']
    )

    sites = {
        site_id: Site(site_id, k, network_monitor) for site_id in range(node_count)
    }
    stream_forwarder = StreamForwarder(sites)

    # Process each log file from S3
    # log_files = ["wc_day46_5_mixed.log", "wc_day48_6_mixed.log"]
    for log_file in log_files:
        logging.info(f"Processing {log_file} from S3")
        s3_object = s3_client.get_object(Bucket=s3_bucket, Key=log_file)
        log_stream = io.StringIO(s3_object['Body'].read().decode('ISO-8859-1'))

        inference_due = 0
        for line_id, line in enumerate(log_stream):
            stream_forwarder.forward_to_site(line)
            logging.debug(f"Network monitor state:\n")
            logging.debug(f"{network_monitor.single_top_k}")
            if len(network_monitor.sliding_window_df) >= batch_size:
                if inference_due >= conf['inference_frequency'] * batch_size:
                    node_failure_simulation(network_monitor)
                    inference_due = 0
                    continue
                inference_due += 1
                train_model(network_monitor, optimizer, epochs=conf['epochs'])


if __name__ == "__main__":
    main()
