from crypthography.Fernet import Fernet

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
        self.sketch = [{} for x in range(len(self.hash_algs))]
        self.current_top_k = []

    def get_hashed_top_k(self) -> List[int]:
        hashed_result = list(self.current_top_k)
        hashed_result.sort(reverse=True)
        return hashed_result

    def get_string_top_k(self, hash_key: bytes) -> List[int]:
        fernet = Fernet(hash_key)
        hashed_result = list(self.current_top_k)
        hashed_result.sort(reverse=True)
        string_result = [fernet.decrypt(x) for x in hashed_result]
        return string_result

    def url_fingerprint(self, accessed_url: str, hash_key: bytes):
        url_bytes = accessed_url.encode('utf-8')
        fernet = Fernet(hash_key)
        encrypted_url = fernet.encrypt(url_bytes)
        return encrypted_url

    def process_log(self, accesed_url: str):

        return None
