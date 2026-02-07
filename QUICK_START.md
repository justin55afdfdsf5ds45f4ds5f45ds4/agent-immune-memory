# Quick Start Guide

## Immediate Next Steps

### 1. Test the System (5 minutes)

```bash
cd agent-immune-memory
python src/agent_immune_system.py
```

You should see:
- 5 scenarios running automatically
- Risk scores and decisions
- Blockchain logging simulation
- Final statistics

### 2. Install Real Sui/Walrus SDKs (30 minutes)

**Sui CLI:**
```bash
# Follow: https://docs.sui.io/guides/developer/getting-started/sui-install
# Or use cargo:
cargo install --locked --git https://github.com/MystenLabs/sui.git --branch mainnet sui
```

**Verify:**
```bash
sui --version
```

**Create/Import Wallet:**
```bash
sui client new-address ed25519
sui client active-address
```

**Get Testnet SUI:**
- Go to: https://discord.gg/sui
- Use #testnet-faucet channel
- Request: `!faucet <your-address>`

**Walrus SDK:**
```bash
# Follow: https://docs.walrus.site/
pip install pysui  # Includes Walrus support
```

### 3. Update Sui Logger with Real Integration (1 hour)

Edit `src/sui_logger.py`:

```python
# Replace TODO sections with actual Sui SDK calls
from pysui import SuiClient, SuiConfig

class SuiLogger:
    def __init__(self, wallet_address, testnet=True):
        self.client = SuiClient(SuiConfig.testnet() if testnet else SuiConfig.mainnet())
        # ... rest of implementation
```

### 4. Record Demo Video (1 hour)

**Tools needed:**
- Screen recorder (OBS Studio, Loom, or built-in)
- Sui testnet explorer open in browser
- Terminal ready

**Follow:** `DEMO_SCRIPT.md`

**Tips:**
- Practice once before recording
- Keep it under 3 minutes
- Show the on-chain proof clearly
- Speak clearly and confidently

### 5. Prepare Submission (30 minutes)

**Update SUBMISSION.md with:**
- [ ] Your Sui wallet address
- [ ] Demo video link
- [ ] GitHub repository URL
- [ ] Any additional features you added

**Update README.md with:**
- [ ] Demo video link
- [ ] Installation instructions
- [ ] Your wallet address

### 6. Submit to DeepSurge (15 minutes)

1. Go to: https://www.deepsurge.xyz/hackathons/cd96178d-5e11-4d56-9f02-1bf157de2552/register
2. Fill in all fields
3. Copy content from `SUBMISSION.md`
4. Attach demo video
5. Verify wallet address
6. Submit before Feb 11, 11:00 PM PST

### 7. Post to Moltbook (15 minutes)

**Use the posts from:** `MOLTBOOK_POST.md`

**API call:**
```python
import requests

headers = {
    "Authorization": "Bearer moltbook_sk_TesA4Q2GybEIt9fHUb0Uw0kr_CqOGCD3",
    "Content-Type": "application/json"
}

# Post 1: Announcement
data = {
    "content": "[Copy from MOLTBOOK_POST.md - Post 1]",
    "community": "sui"
}

response = requests.post(
    "https://www.moltbook.com/api/v1/posts",
    headers=headers,
    json=data
)
print(response.json())
```

---

## Current Status

✅ **Completed:**
- Core compliance kernel
- Risk classifier (6 categories)
- Memory system with pattern matching
- Decision engine with thresholds
- Sui/Walrus logger (stub ready)
- Shared threat registry
- Full integration demo
- Documentation

⏳ **Remaining:**
- Install real Sui/Walrus SDKs
- Replace stubs with actual SDK calls
- Record demo video
- Submit to DeepSurge
- Post to Moltbook

---

## Time Estimates

| Task | Time | Priority |
|------|------|----------|
| Test current system | 5 min | HIGH |
| Install Sui CLI | 30 min | HIGH |
| Get testnet SUI | 10 min | HIGH |
| Update Sui logger | 1 hour | MEDIUM |
| Record demo | 1 hour | HIGH |
| Prepare submission | 30 min | HIGH |
| Submit to DeepSurge | 15 min | HIGH |
| Post to Moltbook | 15 min | MEDIUM |

**Total: ~3.5 hours of focused work**

---

## Troubleshooting

### Python Import Errors
```bash
# Make sure you're in the right directory
cd agent-immune-memory

# Run with module path
python -m src.agent_immune_system
```

### Sui CLI Issues
```bash
# Check installation
sui --version

# Check active address
sui client active-address

# Check balance
sui client gas
```

### Demo Recording Issues
- Use OBS Studio (free, powerful)
- Record at 1080p minimum
- Test audio before full recording
- Keep terminal font size large

---

## Success Criteria

Before submitting, verify:
- [ ] Demo runs without errors
- [ ] Video is under 3 minutes
- [ ] On-chain proof is visible
- [ ] All links work
- [ ] Wallet address is correct
- [ ] Submission is complete
- [ ] Posted to Moltbook

---

## Contact

**Moltbook:** https://moltbook.com/u/EmpusaAI  
**Twitter:** @Justin_lords  
**API Key:** (stored in ACCESS.md)

---

**You've got this! The hard part is done. Now just polish and submit. 🚀**
