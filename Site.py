import logging
import datetime

class Site:
    def __init__(self, site_id):
        self.site_id = site_id

    def get_log(self, log_line: str) -> None:
        log_url = self.extract_url(log_line)
        log_time = self.extract_time(log_line)
        logging.info(f"Site {self.site_id} accessed url: {log_url} at {log_time}")

    def extract_url(self, log_line: str) -> str:
        log_url = log_line.strip().split(" ")[2]
        return log_url

    def extract_time(self, log_line: str):
        log_timestamp = datetime.datetime.strptime(
            log_line.strip().split(" ")[0],
            "[%d/%b/%Y:%H:%M:%S"
        )
        offset =datetime.datetime.strptime(
            log_line.strip().split(" ")[1],
            "%z]"
        )
        log_timestamp.replace(tzinfo=offset.tzinfo)
        return log_timestamp
