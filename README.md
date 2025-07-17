# Professional MEV Transaction Analyser for Solana

A sophisticated, production-ready tool for analyzing Maximum Extractable Value (MEV) patterns in Solana blockchain transactions. This analyzer provides comprehensive insights into arbitrage opportunities, sandwich attacks, and other MEV strategies.

## Features

- **Async Architecture**: High-performance async I/O for concurrent transaction analysis
- **Rich CLI Interface**: Beautiful terminal output with progress indicators and colored formatting
- **Comprehensive MEV Detection**: Multiple pattern recognition algorithms with confidence scoring
- **Robust Error Handling**: Graceful handling of API failures with retry logic
- **Type Safety**: Full type hints and Pydantic models for data validation
- **Extensible Design**: Clean architecture supporting easy addition of new MEV patterns
- **Professional Logging**: Structured logging with configurable levels

## 🛠️ Installation

```bash
# Clone the repository
git clone <repository-url>
cd mev-analyzer

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export HELIUS_API_KEY="your-helius-api-key"
```

## 📊 Usage

### CLI Commands

**Analyze Recent Transactions:**
```bash
python main.py analyze --address JUP4Fb2cqiRUcaTHdrPC8h2gNsA2ETXiPDD33WcGuJB --limit 10
```

**Analyze Single Transaction:**
```bash
python main.py single 5VERv8NMvzbJMEkV8xnrLkEaWRtSz9CosKDYjCJjBRCN
```

**Get Help:**
```bash
python main.py --help
```

### Programmatic Usage

```python
import asyncio
from main import SolanaRPCClient, TransactionAnalyzer, Config

async def analyze_transaction_example():
    # Initialize components
    rpc_client = SolanaRPCClient(Config.HELIUS_ENDPOINT)
    analyzer = TransactionAnalyzer(rpc_client)
    
    # Analyze a transaction
    summary = await analyzer.analyze_transaction("your-signature-here")
    
    if summary:
        print(f"MEV Detected: {summary.is_mev}")
        print(f"Pattern: {summary.mev_pattern.value}")
        print(f"Profit: {summary.profit_usdc} USDC")
        print(f"Confidence: {summary.confidence_score:.2%}")

# Run the analysis
asyncio.run(analyze_transaction_example())
```

## 📈 MEV Pattern Detection

The analyzer detects various MEV patterns:

- **Multi-platform Arbitrage**: Price differences across DEXs
- **Backrun Detection**: Following profitable transactions
- **High PnL Patterns**: Transactions with unusually high profits
- **Sandwich Attacks**: Front/back-running user transactions
- **Liquidation MEV**: Profitable liquidations

Each detection includes a confidence score (0-100%) based on multiple factors.

## 🔧 Configuration

### Environment Variables

```bash
HELIUS_API_KEY=your-helius-api-key  # Required: Helius RPC API key
LOG_LEVEL=INFO                      # Optional: Logging level
```

### Customization

- **Token Registry**: Add new tokens in `TokenRegistry.TOKEN_MAP`
- **Platform Detection**: Extend `PlatformRegistry.PROGRAM_ID_MAP`
- **MEV Patterns**: Add new patterns in `MEVClassifier.classify_transaction`

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=main tests/

# Type checking
mypy main.py
```

## 🔍 Example Output

```
╭─ ✓ MEV DETECTED ─────────────────────────────────────────────────────────╮
│                                                                          │
│ Transaction: 5VERv8NMvzbJMEkV8xn...                                       │
│ Wallet: 9WzDXwBbmkg8ZTbNMq...                                           │
│ Timestamp: 2024-01-15 14:30:22                                          │
│ Trade Path: USDC → SOL → USDT                                           │
│ Platforms: Jupiter, Raydium                                             │
│ Profit (USDC): 12.3456                                                  │
│ Pattern: Multi-platform arbitrage                                       │
│ Confidence: 85%                                                          │
│                                                                          │
╰──────────────────────────────────────────────────────────────────────────╯
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. MEV analysis involves financial data and should not be used as the sole basis for trading decisions. Always conduct your own research and consider the risks involved.

## 🔗 Resources

- [Helius API Documentation](https://docs.helius.xyz/)
- [Solana Web3.js Documentation](https://solana-labs.github.io/solana-web3.js/)
- [MEV Research Papers](https://github.com/flashbots/mev-research)

## 📞 Support

For questions, issues, or contributions, please open an issue on GitHub or contact the maintainers.