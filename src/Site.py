import logging
import datetime
from datetime import timedelta

from HeavyKeeper import HeavyKeeper

class Site:
    def __init__(self, site_id, k):
        self.site_id = site_id
        self.k = k
        self.site_heavy_keeper = HeavyKeeper(self.k)
        self.last_report_time = None

    def process_log(self, log_line: str) -> None:
        log_url = self.extract_url(log_line)
        log_time = self.extract_time(log_line)
        # logging.info(f"Site {self.site_id} accessed url: {log_url} at {log_time}")
        self.site_heavy_keeper.process_log(log_url)
        if not self.last_report_time:
            self.last_report_time = log_time
        if log_time - self.last_report_time > timedelta(minutes=1):
            self.last_report_time = log_time
            logging.info(f"Site {self.site_id} top k at {log_time}:")
            logging.info(self.site_heavy_keeper.get_string_top_k())

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
