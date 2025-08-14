import os

class Config:
    HELIUS_API_KEY = os.getenv("HELIUS_API_KEY", "")
    HELIUS_ENDPOINT = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
    DEFAULT_PROGRAM = "JUP4Fb2cqiRUcaTHdrPC8h2gNsA2ETXiPDD33WcGuJB"
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    LOG_LEVEL = "INFO"
