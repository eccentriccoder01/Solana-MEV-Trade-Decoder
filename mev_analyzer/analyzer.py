import logging
from datetime import datetime
from typing import Optional

from .models import TransactionSummary
from .token import TokenAnalyzer
from .platform import PlatformDetector
from .classifier import MEVClassifier
from .rpc import SolanaRPCClient

class TransactionAnalyzer:
    def __init__(self, rpc_client: SolanaRPCClient):
        self.rpc_client = rpc_client
        self.token_analyzer = TokenAnalyzer()
        self.platform_detector = PlatformDetector()
        self.classifier = MEVClassifier()
        self.logger = logging.getLogger(__name__)

    async def analyze_transaction(self, signature: str) -> Optional[TransactionSummary]:
        try:
            tx_data = await self.rpc_client.get_transaction(signature)
            if not tx_data:
                self.logger.warning(f"No transaction data found for {signature}")
                return None

            msg = tx_data.transaction.get("message", {})
            meta = tx_data.meta

            pre_bal = self.token_analyzer.parse_token_balances(meta.get("preTokenBalances", []))
            post_bal = self.token_analyzer.parse_token_balances(meta.get("postTokenBalances", []))

            profit = self.token_analyzer.calculate_profit(pre_bal, post_bal)
            path = self.token_analyzer.extract_trade_path(pre_bal, post_bal)
            platforms = self.platform_detector.detect_platforms(msg.get("instructions", []), meta.get("innerInstructions", []))
            logs = meta.get("logMessages", [])

            is_mev, pattern, confidence = self.classifier.classify(platforms, profit, logs, path)

            return TransactionSummary(
                signature=signature,
                wallet=msg.get("accountKeys", [{}])[0].get("pubkey", "Unknown"),
                timestamp=datetime.fromtimestamp(tx_data.block_time) if tx_data.block_time else datetime.now(),
                trade_path=path,
                platforms=platforms,
                profit_usdc=profit,
                is_mev=is_mev,
                mev_pattern=pattern,
                confidence_score=confidence,
                token_balances_pre=pre_bal,
                token_balances_post=post_bal,
                raw_logs=logs
            )

        except Exception as e:
            self.logger.error(f"Failed to analyze transaction {signature}: {e}")
            return None
