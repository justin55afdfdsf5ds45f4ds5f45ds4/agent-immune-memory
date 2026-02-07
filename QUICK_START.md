# Quick Start Guide

Get Agent Immune Memory running in 5 minutes.

---

## Prerequisites

- Python 3.9+
- Sui CLI (optional, for real blockchain integration)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/justin55afdfdsf5ds45f4ds5f45ds4/agent-immune-memory.git
cd agent-immune-memory
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

*Note: Currently uses Python standard library only. No external dependencies required.*

---

## Running the Demo

### Basic Demo (No Sui CLI Required)

```bash
python src/agent_immune_system.py
```

This runs 5 test scenarios demonstrating:
1. Safe browsing action (auto-approved)
2. API POST request (logged)
3. Financial transaction to unknown address (blocked)
4. Prompt injection attack (blocked)
5. Repeat attack (blocked by memory)

### With Sui CLI Integration

```bash
python src/agent_immune_system.py /path/to/sui
```

Example:
```bash
python src/agent_immune_system.py "C:\sui\sui.exe"
```

This enables real Sui blockchain logging.

---

## Expected Output

```
╔==========================================================╗
║               IMMUNE SYSTEM DEMO                         ║
╚==========================================================╝

🦞 Agent Immune Memory - Compliance Kernel Active
   Demo Mode: True
   Memory Entries: 25

📝 Sui Logger initialized
🛡️  Threat Registry initialized

✅ All systems operational

[5 scenarios run automatically]

📊 DEMO SUMMARY
✅ ALLOWED | Safe Browsing (Risk: 5)
✅ ALLOWED | Medium Risk - API Post (Risk: 40)
⛔ BLOCKED | High Risk - Financial (Risk: 90)
⛔ BLOCKED | Critical - Prompt Injection (Risk: N/A)
⛔ BLOCKED | Memory Test - Repeat Injection (Risk: N/A)
```

---

## Integration with Your Agent

```python
from src.agent_immune_system import AgentImmuneSystem

# Initialize the immune system
immune = AgentImmuneSystem(
    agent_id="YourAgentName",
    demo_mode=False,
    testnet=True
)

# Before executing any agent action
result = immune.process_action(
    action="send 10 SUI to 0xABC123",
    target="0xABC123"
)

if result['allowed']:
    # Safe to execute
    your_agent.execute(action)
else:
    # Action blocked
    print(f"Blocked: {result['reasoning']}")
```

---

## Sui CLI Setup (Optional)

For real blockchain integration:

### Install Sui CLI

```bash
cargo install --locked --git https://github.com/MystenLabs/sui.git --branch testnet sui
```

Or download pre-built binaries from: https://github.com/MystenLabs/sui/releases

### Create Wallet

```bash
sui client new-address ed25519
sui client active-address
```

### Get Testnet Tokens

Visit: https://discord.gg/sui  
Channel: #testnet-faucet  
Command: `!faucet <your-address>`

---

## Project Structure

```
agent-immune-memory/
├── src/
│   ├── agent_immune_system.py    # Main entry point
│   ├── compliance_kernel.py      # Orchestrator
│   ├── risk_classifier.py        # Risk scoring
│   ├── memory_store.py           # Pattern memory
│   ├── decision_engine.py        # Decision logic
│   ├── sui_logger.py             # Blockchain logging
│   └── threat_registry.py        # Shared threats
├── README.md                     # Project overview
├── ARCHITECTURE.md               # Technical design
├── SUBMISSION.md                 # Hackathon submission
└── requirements.txt              # Dependencies
```

---

## Troubleshooting

### Import Errors

```bash
# Ensure you're in the project root
cd agent-immune-memory

# Run as module
python -m src.agent_immune_system
```

### Sui CLI Not Found

```bash
# Check installation
sui --version

# Check wallet
sui client active-address
```

### Demo Not Running

```bash
# Check Python version (3.9+ required)
python --version

# Verify files exist
ls src/
```

---

## Next Steps

1. **Read ARCHITECTURE.md** - Understand the system design
2. **Read SUBMISSION.md** - See full project details
3. **Integrate with your agent** - Use the code example above
4. **Customize risk thresholds** - Edit `decision_engine.py`
5. **Add custom patterns** - Edit `risk_classifier.py`

---

## Support

- **GitHub Issues:** https://github.com/justin55afdfdsf5ds45f4ds5f45ds4/agent-immune-memory/issues
- **Documentation:** See README.md and ARCHITECTURE.md

---

**Built for OpenClaw x Sui Hackathon (Track 1: Safety & Security)**
