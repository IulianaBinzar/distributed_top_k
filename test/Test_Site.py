import unittest
import logging
from datetime import datetime

from Site import Site
import datetime

class TestSite(unittest.TestCase):
    def test_extract_time(self):
        test_log = "[15/Jun/1998:10:53:39 +2300] /images/hm_btm_arw02.gif 1"
        mySite = Site(0, 4)
        extracted_time = mySite.extract_time(test_log)
        expected_time = datetime.datetime(year=1998, month=6, day=14,
                                          hour=11, minute=53, second=39,
                                          tzinfo=datetime.timezone.utc)
        self.assertEqual(expected_time, extracted_time)