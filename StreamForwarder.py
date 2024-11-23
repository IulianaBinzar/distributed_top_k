class StreamForwarder:
    def __init__(self, sites):
        self.sites = sites

    def forward_to_site(self, log_file):
        for log_line in log_file:
            # log_format "timestamp timediff url log_site"
            log_site = int(log_line.strip().split(" ")[3])
            if log_site in range(0, 3):
                self.sites[log_site].get_log(log_line)
            # silently discarding logs that have invalid site codes
