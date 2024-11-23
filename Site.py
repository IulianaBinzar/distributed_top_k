import logging

class Site:
    def __init__(self, site_id):
        self.site_id = site_id

    def get_log(self, log_line: str) -> None:
        logging.info(f"Site {self.site_id} received line: {log_line}")