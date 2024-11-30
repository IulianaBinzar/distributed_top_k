import logging
import datetime

from distributed_top_k.src.HeavyKeeper import HeavyKeeper

class Site:
    def __init__(self, site_id, k):
        self.site_id = site_id
        self.k = k
        self.site_heavy_keeper = HeavyKeeper(self.k)
        self.processed_logs = 0

    def process_log(self, log_line: str) -> None:
        log_url = self.extract_url(log_line)
        log_time = self.extract_time(log_line)
        logging.info(f"Site {self.site_id} accessed url: {log_url} at {log_time}")
        accessed_url = self.extract_url(log_line)
        self.site_heavy_keeper.process_log(accessed_url)
        self.processed_logs += 1
        # logging.info(f"HK{self.HeavyKeeper.get_string_top_k()}")
        if self.processed_logs == 50:
            logging.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            logging.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            logging.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            logging.info(f"Site {self.site_id} top-k: {self.site_heavy_keeper.get_string_top_k()}")
            logging.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            logging.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            logging.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            self.processed_logs = 0

    def extract_url(self, log_line: str) -> str:
        log_url = log_line.strip().split(" ")[2]
        return log_url

    def extract_time(self, log_line: str):
        time_str = log_line.strip().split(" ")[0]
        offset_str = log_line.strip().split(" ")[1]
        log_timestamp = datetime.datetime.strptime(
            time_str + " " + offset_str,
            "[%d/%b/%Y:%H:%M:%S %z]"
        )
        utc_timestamp = log_timestamp.astimezone(datetime.timezone.utc)
        return utc_timestamp