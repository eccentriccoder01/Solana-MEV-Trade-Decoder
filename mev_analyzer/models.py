from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, validator

from .constants import TOKEN_MAP

class MEVPattern(Enum):
    MULTI_PLATFORM_ARBITRAGE = "Multi-platform arbitrage"
    BACKRUN = "Backrun detected"
    HIGH_PNL = "High PnL indicates MEV"
    SANDWICH_ATTACK = "Sandwich attack"
    LIQUIDATION = "Liquidation MEV"
    UNKNOWN = "Unknown pattern"
    NO_MEV = "No MEV detected"

@dataclass
class TokenBalance:
    mint: str
    amount: Decimal
    ui_amount: Decimal
    decimals: int
    symbol: str = ""

    def __post_init__(self):
        if not self.symbol:
            self.symbol = TOKEN_MAP.get(self.mint, self.mint[:4] + "..." + self.mint[-4:])

@dataclass
class TransactionSummary:
    signature: str
    wallet: str
    timestamp: datetime
    trade_path: List[str]
    platforms: List[str]
    profit_usdc: Decimal
    is_mev: bool
    mev_pattern: MEVPattern
    confidence_score: float
    gas_fees: Decimal = Decimal("0")
    token_balances_pre: List[TokenBalance] = field(default_factory=list)
    token_balances_post: List[TokenBalance] = field(default_factory=list)
    raw_logs: List[str] = field(default_factory=list)

class TransactionData(BaseModel):
    signature: str
    slot: int
    block_time: Optional[int] = None
    transaction: Dict[str, Any]
    meta: Dict[str, Any]

    @validator('signature')
    def validate_signature(cls, v):
        if not v or len(v) < 80:
            raise ValueError("Invalid transaction signature")
        return v
