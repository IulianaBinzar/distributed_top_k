import logging
import datetime
from datetime import timedelta

from HeavyKeeper import HeavyKeeper

class Site:
    def __init__(self, site_id, k, network_monitor):
        self.site_id = site_id
        self.k = k
        self.site_heavy_keeper = None
        self.last_report_time = None
        self.last_hk_reset_time = None
        self.network_monitor = network_monitor

    def process_log(self, log_line: str) -> None:
        log_url = self.extract_url(log_line)
        log_time = self.extract_time(log_line)
        # logging.info(f"Site {self.site_id} accessed url: {log_url} at {log_time}")

        if not self.last_hk_reset_time or self.last_hk_reset_time - log_time > timedelta(hours=1):
            self.site_heavy_keeper = HeavyKeeper(self.k)
            self.last_hk_reset_time = log_time
            self.last_report_time = None
        self.site_heavy_keeper.process_log(log_url)

        if not self.last_report_time:
            self.last_report_time = log_time
        if log_time - self.last_report_time > timedelta(minutes=1):
            top_k = self.site_heavy_keeper.get_string_top_k()
            logging.info(f"Site {self.site_id} top k at {log_time}: {top_k}")
            self.last_report_time = log_time
            self.network_monitor.receive_top_k(self.site_id, top_k, log_time)

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
