import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from .config import Config
from .models import TransactionData
from .exceptions import APIError

class SolanaRPCClient:
    def __init__(self):
        self.endpoint = Config.HELIUS_ENDPOINT
        self.timeout = aiohttp.ClientTimeout(total=Config.REQUEST_TIMEOUT)
        self.max_retries = Config.MAX_RETRIES
        self.logger = logging.getLogger(__name__)

    async def make_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession(timeout=self.timeout) as session:
                    async with session.post(self.endpoint, json=payload) as response:
                        response.raise_for_status()
                        data = await response.json()
                        if "error" in data:
                            raise APIError(f"RPC Error: {data['error']}")
                        return data
            except aiohttp.ClientError as e:
                self.logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                if attempt == self.max_retries - 1:
                    raise APIError(f"Failed after {self.max_retries} attempts: {e}")
                await asyncio.sleep(2 ** attempt)
        return {}

    async def get_signatures_for_address(self, address: str, limit: int = 5) -> List[Dict[str, Any]]:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [address, {"limit": limit}]
        }
        result = await self.make_request(payload)
        return result.get("result", [])

    async def get_transaction(self, signature: str) -> Optional[TransactionData]:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [signature, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]
        }
        result = await self.make_request(payload)
        tx_data = result.get("result")
        if not tx_data:
            return None
        tx_data["signature"] = signature
        return TransactionData(**tx_data)
