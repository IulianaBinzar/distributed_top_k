from cryptography.fernet import Fernet
from collections import defaultdict
import random

class HeavyKeeper:
    def __init__(self, k):
        """
        Params for fine-tuning
        b - decay factor - 0.8 in the paper
        hash_keys - hashing keys - 2 in the paper
        hash_size - size of the hash table - 10000 in the paper
        """
        self.b = 0.8
        self.hash_keys = [Fernet.generate_key() for _ in range(3)]
        self.hash_size = 5000
        # Other initialisations
        self.k = k # length of the list being kept
        self.sketch = [[(None, 0)
                        for _ in range(self.hash_size)]
                       for _ in range(len(self.hash_keys))]
        self.current_top_k = []

    def get_hashed_top_k(self) -> list[bytes]:
        hashed_result = list(self.current_top_k)
        hashed_result.sort(reverse=True)
        return hashed_result

    def get_string_top_k(self, hash_key: bytes) -> list[str]:
        hashed_result = self.get_hashed_top_k()
        fernet = Fernet(hash_key)
        string_result = [fernet.decrypt(x) for x in hashed_result]
        return string_result

    def url_fingerprint(self, accessed_url: str, hash_key: bytes):
        url_bytes = accessed_url.encode('utf-8')
        fernet = Fernet(hash_key)
        byte_encrypted_url = fernet.encrypt(url_bytes)
        int_encrypted_url = int.from_bytes(byte_encrypted_url, byteorder="big")
        return int_encrypted_url

    def process_log(self, accesed_url: str):
        true_count = 0

        for i, x in enumerate(self.hash_keys):
            fingerprint = self.url_fingerprint(accesed_url, x)
            hash_index = fingerprint % self.hash_size
            sketch_fp, sketch_counter = self.sketch[i][hash_index]
            if not sketch_counter:
                self.sketch[i][hash_index] = (fingerprint, 1)
                true_count = min(true_count, 1)
            elif sketch_fp == fingerprint:
                sketch_counter += 1
                self.sketch[i][hash_index] = (fingerprint, sketch_counter)
                true_count = min(true_count, sketch_counter)
            else:
                decay_probability = sketch_counter ** (-self.b)
                if decay_probability > random.random():
                    sketch_counter -= 1
                    if sketch_counter > 0:
                        self.sketch[i][hash_index] = (sketch_fp, sketch_counter)
                    else:
                        self.sketch[i][hash_index] = (fingerprint, 1)
                        true_count = min(true_count, 1)

            for i, (freq, heap_item) in enumerate(self.current_top_k):
                if heap_item == accesed_url:
                    self.current_top_k[i] = (freq, accesed_url)
                    heapq.heapify(self.current_top_k)
                else:
                    heapq.heappush(self.current_top_k, (true_count, accesed_url))

            if len(self.current_top_k) > self.k:
                heapq.heapop(self.current_top_k)
