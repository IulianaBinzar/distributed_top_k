from collections import defaultdict

import hashlib
import logging
import random
import heapq

class HeavyKeeper:
    def __init__(self, k):
        """
        Params for fine-tuning
        b - decay factor - 1.08 in the paper
        hash_keys - hashing keys - 2 in the paper
        hash_size - size of the hash table - 10000 in the paper
        """
        self.b = 1.08
        self.hash_keys = [str(random.randint(0, 2 ** 32 - 1)).encode('utf-8') for _ in range(3)]
        self.hash_size = 10000
        # Other initialisations
        self.k = k # length of the list being kept
        self.sketch = [[(None, 0)
                        for _ in range(self.hash_size)]
                       for _ in range(len(self.hash_keys))]
        self.current_top_k = []

    def get_string_top_k(self):
        hashed_result = list(self.current_top_k)
        hashed_result.sort(reverse=True)
        return hashed_result

    # def get_string_top_k(self, hash_key: bytes) -> list[str]:
    #     hashed_result = self.get_hashed_top_k()
    #     fernet = Fernet(hash_key)
    #     string_result = [fernet.decrypt(x) for x in hashed_result]
    #     return string_result

    def url_fingerprint(self, accessed_url: str, hash_key: bytes):
        url_bytes = accessed_url.encode('utf-8')
        byte_encrypted_url = hashlib.sha1(hash_key + url_bytes).digest()
        int_encrypted_url = int.from_bytes(byte_encrypted_url, byteorder="big")
        return int_encrypted_url

    def process_log(self, accesed_url: str):
        # true_count = float("inf")

        for i, x in enumerate(self.hash_keys):
            fingerprint = self.url_fingerprint(accesed_url, x)
            hash_index = fingerprint % self.hash_size
            sketch_fp, sketch_counter = self.sketch[i][hash_index]
            if not sketch_counter:
                self.sketch[i][hash_index] = (fingerprint, 1)
            elif sketch_fp == fingerprint:
                sketch_counter += 1
                self.sketch[i][hash_index] = (fingerprint, sketch_counter)
            else:
                decay_probability = self.b ** (-sketch_counter)
                if decay_probability > random.random():
                    sketch_counter -= 1
                    if sketch_counter > 0:
                        self.sketch[i][hash_index] = (sketch_fp, sketch_counter)
                    else:
                        self.sketch[i][hash_index] = (fingerprint, 1)

            true_count = self.sketch[i][hash_index][1]
            # true_count = min(true_count, self.sketch[i][hash_index][1])

            for i, (freq, heap_item) in enumerate(self.current_top_k):
                if heap_item == accesed_url:
                    self.current_top_k[i] = (true_count, accesed_url)
                    break
            else:
                heapq.heappush(self.current_top_k, (true_count, accesed_url))
            if len(self.current_top_k) > self.k:
                heapq.heappop(self.current_top_k)
