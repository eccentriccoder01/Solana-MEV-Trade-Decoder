from decimal import Decimal
from typing import List, Tuple
from .models import MEVPattern

class MEVClassifier:
    @staticmethod
    def classify(platforms: List[str], profit: Decimal, logs: List[str], path: List[str]) -> Tuple[bool, MEVPattern, float]:
        if len(platforms) > 1 and profit > Decimal("0.01"):
            return True, MEVPattern.MULTI_PLATFORM_ARBITRAGE, 0.85
        if any("backrun" in log.lower() for log in logs):
            return True, MEVPattern.BACKRUN, 0.75
        if profit > Decimal("1.0"):
            return True, MEVPattern.HIGH_PNL, 0.70
        if len(path) >= 3 and profit > Decimal("0.05"):
            return True, MEVPattern.SANDWICH_ATTACK, 0.60
        if profit > Decimal("0.1"):
            return True, MEVPattern.UNKNOWN, 0.40
        return False, MEVPattern.NO_MEV, 0.95
