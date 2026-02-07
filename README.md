# Agent Immune Memory

<p align="center">
  <img src="logo.jpg" alt="Agent Immune Memory" width="400"/>
</p>

An autonomous compliance and immune system layer for OpenClaw agents.

## What it does

Agent Immune Memory intercepts every action an OpenClaw agent attempts to execute, classifies it by risk level, checks against historical memory and a shared threat registry, and makes intelligent decisions about whether to allow, log, or block the action. All decisions are logged immutably on Sui blockchain via Walrus storage.

## Why it matters

Autonomous agents with browser and terminal control are powerful but dangerous. We built governance for agents — not just a firewall, but a decentralized immune system that gets stronger with every agent that joins the network.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  OPENCLAW AGENT                  │
│            (browser + terminal control)          │
└──────────────────────┬──────────────────────────┘
                       │ every action
                       ▼
┌─────────────────────────────────────────────────┐
│           COMPLIANCE KERNEL (middleware)         │
│                                                  │
│  1. COMMAND RISK CLASSIFIER                      │
│  2. MEMORY CHECK                                 │
│  3. DECISION ENGINE                              │
│  4. SUI ON-CHAIN LOGGER                          │
│  5. SHARED IMMUNE REGISTRY                       │
└─────────────────────────────────────────────────┘
```

## Tech Stack

- OpenClaw (agent framework)
- Sui blockchain (on-chain proof)
- Walrus (decentralized storage)
- Python 3.9+

## How it works

Every action an OpenClaw agent attempts goes through this pipeline:

1. **Risk Classification** - Action is categorized and scored (0-100)
2. **Memory Check** - System checks if similar actions were blocked before
3. **Threat Registry Query** - Checks shared registry for known threats
4. **Decision** - Auto-approve, log, require confirmation, or block
5. **Blockchain Logging** - Medium/high risk actions logged to Walrus + Sui
6. **Threat Publishing** - Blocked threats shared with all agents

## Key Features

- **Real-time Protection** - Actions validated before execution
- **Blockchain Proof** - Immutable audit trail on Sui
- **Shared Immunity** - Threats published to protect all agents
- **Learning System** - Memory improves detection over time
- **Zero Trust** - Even agent's own actions are validated

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd agent-immune-memory

# Install Python dependencies
pip install -r requirements.txt

# (Optional) Install Sui CLI for real blockchain integration
# Follow: https://docs.sui.io
```

## How to run

### Quick Demo

```bash
# Run the full system demo
python src/agent_immune_system.py
```

This will run through 5 scenarios:
1. Safe browsing (auto-approved)
2. API post (approved with logging)
3. Financial transaction (blocked in demo mode)
4. Prompt injection attack (blocked + threat published)
5. Repeat attack (blocked by threat registry)

### Use in Your Agent

```python
from src.agent_immune_system import AgentImmuneSystem

# Initialize
system = AgentImmuneSystem(
    agent_id="YourAgentName",
    wallet_address="0xYOUR_SUI_WALLET",
    demo_mode=False,  # Set to False for production
    testnet=True
)

# Process an action
result = system.process_action(
    action="send 10 SUI to 0xABC123",
    target="0xABC123"
)

if result['allowed']:
    # Execute the action
    print("Action approved")
else:
    # Block the action
    print(f"Action blocked: {result['reasoning']}")
```

## Demo

**🎥 Watch the demo:** https://www.loom.com/share/cb8c1cc4641a4e5f91e8462d024bb1c4

**🔗 Verify on-chain:** https://suiscan.xyz/testnet/account/0xe8c76a2ee8fcabb173a327a5f8228d9e18cf868ac39d2406e6e72ab13d9fba3c

**Demo highlights:**
- Real-time threat detection
- Blockchain logging to Sui/Walrus
- Shared threat registry in action
- Memory-based learning

## Sui Integration

- **Wallet Address**: [Your Sui wallet address]
- **Network**: Sui Testnet
- **Storage**: Walrus decentralized storage
- **Proof**: All decisions cryptographically anchored on-chain

## Project Structure

```
agent-immune-memory/
├── src/
│   ├── risk_classifier.py      # Action risk classification
│   ├── memory_store.py          # Local memory system
│   ├── decision_engine.py       # Decision logic
│   ├── compliance_kernel.py     # Core orchestrator
│   ├── sui_logger.py            # Sui/Walrus integration
│   ├── threat_registry.py       # Shared threat registry
│   └── agent_immune_system.py   # Complete system
├── requirements.txt
├── README.md
└── DEMO_SCRIPT.md
```

---

Built for OpenClaw x Sui Hackathon (Track 1: Safety & Security)
