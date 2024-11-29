import hashlib

class HeavyKeeper:
    def __init__(self, k):
        """
        Params for fine-tuning
        b - decay factor - 0.8 in the paper
        hash_algs - hashing algorithms - 2 in the paper
        hash_size - size of the hash table - 10000 in the paper

        """
        self.b = 0.8
        self.hash_algs = ['md5', 'sha1', 'sha224']
        self.hash_size = 5000
        # Other initialisations
        self.k = k # length of the list being kept
        self.sketch = [{} for x in range(len(self.hash_algs))]
        self.current_top_k = []

    def url_fingerprint(self, accessed_url: str, hash_alg: str):
        url_bytes = accessed_url.encode('utf-8')
        h = hashlib.new(hash_alg)
        h.update(url_bytes)
        return h.digest()

    def process_log(self, accesed_url: str):
        return None
