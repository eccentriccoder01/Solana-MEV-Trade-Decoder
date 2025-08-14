from decimal import Decimal
from typing import List, Dict
from .models import TokenBalance
from .constants import TOKEN_PRICES_USDC

class TokenAnalyzer:
    @staticmethod
    def parse_token_balances(data: List[Dict]) -> List[TokenBalance]:
        balances = []
        for item in data:
            try:
                ui_amount = item["uiTokenAmount"]["uiAmount"]
                balances.append(TokenBalance(
                    mint=item["mint"],
                    amount=Decimal(item["uiTokenAmount"]["amount"]),
                    ui_amount=Decimal(str(ui_amount)) if ui_amount else Decimal("0"),
                    decimals=item["uiTokenAmount"]["decimals"]
                ))
            except Exception:
                continue
        return balances

    @staticmethod
    def calculate_profit(pre: List[TokenBalance], post: List[TokenBalance]) -> Decimal:
        post_lookup = {b.mint: b.ui_amount for b in post}
        profit = Decimal("0")
        for b in pre:
            delta = post_lookup.get(b.mint, Decimal("0")) - b.ui_amount
            price = TOKEN_PRICES_USDC.get(b.mint, Decimal("0"))
            profit += delta * price
        return profit

    @staticmethod
    def extract_trade_path(pre: List[TokenBalance], post: List[TokenBalance]) -> List[str]:
        changed = []
        post_map = {b.mint: b.ui_amount for b in post}
        for b in pre:
            if abs(post_map.get(b.mint, Decimal("0")) - b.ui_amount) > Decimal("0.001"):
                changed.append(b.symbol)
        return list(set(changed))
