import logging
import random
import unittest

from heavy_keeper import HeavyKeeper

class Test_HeavyKeeper(unittest.TestCase):
    def test_process_log(self):

        test_input = []
        for i in range(1001):
            for _ in range(i):
                test_input.append(str(i))
        random.shuffle(test_input)

        myHK = HeavyKeeper(10)
        for x in test_input:
            myHK.process_log(x)

        top_k = myHK.get_string_top_k()
        self.assertEqual(top_k[0][1], "1000")

