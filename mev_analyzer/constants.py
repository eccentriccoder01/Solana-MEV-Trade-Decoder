from decimal import Decimal

TOKEN_MAP = {
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC",
    "So11111111111111111111111111111111111111112": "SOL",
    "mSoLzCrK6KrAEFq3Q7t8k8k8k8k8k8k8k8k8k8k8k8k8": "mSOL",
    "Es9vMFrzaCER9sQF2Q8k4p8p8nH3c7Yw2Zrjz5kF3bG9": "USDT",
    "native": "SOL"
}

TOKEN_PRICES_USDC = {
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": Decimal("1.0"),
    "So11111111111111111111111111111111111111112": Decimal("150.0"),
    "mSoLzCrK6KrAEFq3Q7t8k8k8k8k8k8k8k8k8k8k8k8k8": Decimal("150.0"),
    "Es9vMFrzaCER9sQF2Q8k4p8p8nH3c7Yw2Zrjz5kF3bG9": Decimal("1.0")
}

PROGRAM_ID_MAP = {
    "JUP4Fb2cqiRUcaTHdrPC8h2gNsA2ETXiPDD33WcGuJB": "Jupiter",
    "METEoRA9dFZz5e6h8vLwYp6kQw6r1t4QKq5k3h8vLwYp": "Meteora",
    "4ckmDgGzLYLyEcdh5uM4a5hQKx1e5gn9wQw5G6XcE9E5": "Raydium"
}
