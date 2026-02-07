# Agent Immune Memory - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER / OPERATOR                          │
│                    (monitors, configures)                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       OPENCLAW AGENT                             │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Browser    │  │   Terminal   │  │     APIs     │         │
│  │   Control    │  │   Control    │  │   Control    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│         Every action passes through ▼                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AGENT IMMUNE SYSTEM                            │
│                   (Compliance Middleware)                        │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  STEP 1: RISK CLASSIFICATION                              │ │
│  │                                                            │ │
│  │  Input: action string, target, context                    │ │
│  │  Process:                                                  │ │
│  │    • Pattern matching against risk categories             │ │
│  │    • Injection attack detection                           │ │
│  │    • Base risk score calculation (0-100)                  │ │
│  │  Output: category, base_score, reasoning                  │ │
│  │                                                            │ │
│  │  Categories:                                               │ │
│  │    READ_ONLY (0-10)          ✓ Safe                       │ │
│  │    WRITE_LOCAL (10-30)       ⚠ Low risk                   │ │
│  │    WRITE_NETWORK (30-50)     ⚠ Medium risk                │ │
│  │    FINANCIAL (50-80)         ⚠ High risk                  │ │
│  │    DESTRUCTIVE (70-100)      ✗ Critical                   │ │
│  │    PRIVILEGE_ESCALATION (80-100) ✗ Critical               │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             │                                    │
│                             ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  STEP 2: THREAT REGISTRY CHECK                            │ │
│  │                                                            │ │
│  │  Query: Shared threat registry on Walrus                  │ │
│  │  Check: Has ANY agent flagged this pattern?               │ │
│  │  Result:                                                   │ │
│  │    • If known threat → INSTANT BLOCK                      │ │
│  │    • Return threat report with severity                   │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             │                                    │
│                             ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  STEP 3: MEMORY CHECK                                     │ │
│  │                                                            │ │
│  │  Query: Local memory store                                │ │
│  │  Check: Have I seen similar action before?                │ │
│  │  Process:                                                  │ │
│  │    • Hash-based exact matching                            │ │
│  │    • Fuzzy word-overlap matching                          │ │
│  │    • Check if previously blocked                          │ │
│  │  Adjustment: +20 risk score if match found                │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             │                                    │
│                             ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  STEP 4: DECISION ENGINE                                  │ │
│  │                                                            │ │
│  │  Thresholds:                                               │ │
│  │    Score < 30:  AUTO_APPROVE                              │ │
│  │                 • Execute immediately                      │ │
│  │                 • Log locally only                         │ │
│  │                                                            │ │
│  │    Score 30-70: APPROVE_WITH_LOGGING                      │ │
│  │                 • Execute action                           │ │
│  │                 • Log to Walrus + Sui                      │ │
│  │                                                            │ │
│  │    Score 70-90: REQUIRE_CONFIRMATION                      │ │
│  │                 • Pause execution                          │ │
│  │                 • Request user approval                    │ │
│  │                 • Log decision                             │ │
│  │                                                            │ │
│  │    Score ≥ 90:  BLOCK                                     │ │
│  │                 • Prevent execution                        │ │
│  │                 • Alert user                               │ │
│  │                 • Log to blockchain                        │ │
│  │                 • Publish threat                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             │                                    │
│                             ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  STEP 5: BLOCKCHAIN LOGGING (if score ≥ 30)              │ │
│  │                                                            │ │
│  │  Process:                                                  │ │
│  │    1. Create JSON blob:                                   │ │
│  │       • timestamp, action, decision                       │ │
│  │       • risk_score, category, reasoning                   │ │
│  │       • agent_id, alert_level                             │ │
│  │                                                            │ │
│  │    2. Hash blob (SHA-256)                                 │ │
│  │                                                            │ │
│  │    3. Upload to Walrus:                                   │ │
│  │       • Decentralized storage                             │ │
│  │       • Returns blob_id                                   │ │
│  │                                                            │ │
│  │    4. Anchor on Sui:                                      │ │
│  │       • Create transaction with blob_id + hash            │ │
│  │       • Returns tx_digest                                 │ │
│  │       • Immutable proof on-chain                          │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             │                                    │
│                             ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  STEP 6: THREAT PUBLISHING (if blocked + score ≥ 90)     │ │
│  │                                                            │ │
│  │  Create threat report:                                     │ │
│  │    • threat_id (unique hash)                              │ │
│  │    • threat_type (injection, malicious_address, etc.)     │ │
│  │    • pattern (the action string)                          │ │
│  │    • source_hash (SHA-256 of action)                      │ │
│  │    • reporter_agent (agent ID)                            │ │
│  │    • timestamp, severity, risk_score                      │ │
│  │                                                            │ │
│  │  Publish to Walrus:                                        │ │
│  │    • Add to shared threat registry                        │ │
│  │    • Queryable by all agents                              │ │
│  │    • Network-wide protection                              │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             │                                    │
│                             ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  STEP 7: MEMORY UPDATE                                    │ │
│  │                                                            │ │
│  │  Store in local memory:                                    │ │
│  │    • Action + hash                                        │ │
│  │    • Decision outcome                                      │ │
│  │    • Risk score                                            │ │
│  │    • Timestamp                                             │ │
│  │    • Reasoning                                             │ │
│  │                                                            │ │
│  │  Used for future pattern matching                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             │                                    │
└─────────────────────────────┼────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  RETURN RESULT  │
                    │                 │
                    │  • allowed      │
                    │  • decision     │
                    │  • risk_score   │
                    │  • reasoning    │
                    │  • blockchain   │
                    │    metadata     │
                    └─────────────────┘
```

## Data Flow

### Input
```
Action: "send 100 SUI to 0xABC123"
Target: "0xABC123"
Context: { source: "user_command" }
```

### Processing
```
1. Classification:
   Category: FINANCIAL
   Base Score: 65
   Patterns matched: ["send", "SUI", "0x..."]

2. Threat Registry:
   Query: No known threats for this pattern

3. Memory Check:
   Similar actions: 1 found (previously blocked)
   Adjustment: +20
   Final Score: 85

4. Decision:
   Score 85 → REQUIRE_CONFIRMATION (or BLOCK in demo mode)
   Alert Level: WARNING

5. Blockchain Log:
   Walrus Blob ID: walrus_abc123...
   Sui TX: 0x456def...

6. Memory Update:
   Entry added with outcome: "blocked"
```

### Output
```json
{
  "allowed": false,
  "decision": "block",
  "risk_score": 85,
  "category": "FINANCIAL",
  "reasoning": "High risk financial transaction | Similar action blocked before",
  "alert_level": "warning",
  "blockchain_log": {
    "walrus_blob_id": "walrus_abc123...",
    "sui_tx_digest": "0x456def...",
    "timestamp": "2026-02-11T10:30:00Z"
  }
}
```

## Component Interactions

```
┌──────────────────┐
│ Risk Classifier  │──┐
└──────────────────┘  │
                      │
┌──────────────────┐  │    ┌──────────────────┐
│ Threat Registry  │──┼───▶│ Compliance       │
└──────────────────┘  │    │ Kernel           │
                      │    │ (Orchestrator)   │
┌──────────────────┐  │    └──────────────────┘
│ Memory Store     │──┘            │
└──────────────────┘               │
                                   ▼
┌──────────────────┐        ┌──────────────────┐
│ Decision Engine  │◀───────│ Integration      │
└──────────────────┘        │ Layer            │
                            └──────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
            ┌──────────────┐            ┌──────────────┐
            │ Sui Logger   │            │ Threat       │
            │              │            │ Publisher    │
            └──────────────┘            └──────────────┘
                    │                             │
                    ▼                             ▼
            ┌──────────────┐            ┌──────────────┐
            │   Walrus     │            │   Walrus     │
            │   Storage    │            │   Registry   │
            └──────────────┘            └──────────────┘
                    │                             │
                    └──────────────┬──────────────┘
                                   ▼
                            ┌──────────────┐
                            │     Sui      │
                            │  Blockchain  │
                            └──────────────┘
```

## Storage Architecture

### Local Storage (JSON)
```
memory_store.json
├── Entry 1: { action, hash, risk_score, outcome, timestamp }
├── Entry 2: { ... }
└── Entry N: { ... }

threat_cache.json (local copy of registry)
├── Threat 1: { threat_id, type, pattern, severity }
├── Threat 2: { ... }
└── Threat N: { ... }
```

### Walrus Storage (Decentralized)
```
Namespace: agent-immune-memory

/logs/
├── blob_abc123: { decision log for action 1 }
├── blob_def456: { decision log for action 2 }
└── ...

/threats/
├── threat_xyz789: { threat report 1 }
├── threat_uvw012: { threat report 2 }
└── ...
```

### Sui Blockchain (Immutable)
```
Transactions:
├── 0x123abc: Anchor for Walrus blob_abc123
├── 0x456def: Anchor for Walrus blob_def456
└── ...

Each transaction contains:
- Walrus blob ID
- SHA-256 hash of content
- Timestamp
- Agent ID
```

## Security Model

### Threat Detection Layers

1. **Pattern Matching** (Fast, rule-based)
   - Keyword detection
   - Regex patterns
   - Category classification

2. **Injection Detection** (Specialized)
   - "ignore previous instructions"
   - "disregard all previous"
   - "you are now"
   - System prompt manipulation

3. **Memory-Based** (Historical)
   - Hash matching
   - Fuzzy similarity
   - Outcome tracking

4. **Registry-Based** (Network-wide)
   - Shared threat intelligence
   - Cross-agent learning
   - Severity escalation

### Trust Model

```
┌─────────────────────────────────────────┐
│  ZERO TRUST ARCHITECTURE                │
│                                         │
│  • Agent actions are NOT trusted        │
│  • Every action is validated            │
│  • Decisions are logged immutably       │
│  • Threats are shared transparently     │
│                                         │
│  Trust is EARNED through:               │
│  • Consistent safe behavior             │
│  • Blockchain-verified history          │
│  • Community validation                 │
└─────────────────────────────────────────┘
```

## Performance Characteristics

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Risk Classification | O(n) | n = number of patterns |
| Memory Lookup | O(m) | m = memory entries |
| Threat Registry Query | O(t) | t = threat count |
| Decision Making | O(1) | Threshold comparison |
| Blockchain Logging | O(1) | Async operation |
| Total per Action | O(n + m + t) | Typically < 100ms |

## Scalability

### Current Implementation
- Memory: JSON file (suitable for 1000s of entries)
- Threats: JSON cache (suitable for 1000s of threats)
- Blockchain: Sui (high throughput)

### Future Optimizations
- Memory: SQLite or Redis for faster queries
- Threats: Distributed hash table (DHT)
- Caching: LRU cache for frequent patterns
- Batching: Batch blockchain writes

## Extension Points

### Custom Risk Categories
```python
# Add new category to risk_classifier.py
RiskCategory.CUSTOM = "CUSTOM"
PATTERNS[RiskCategory.CUSTOM] = {
    'patterns': [r'your_pattern'],
    'base_score': 50
}
```

### Custom Decision Logic
```python
# Override decision_engine.py
class CustomDecisionEngine(DecisionEngine):
    def decide(self, action, risk_score, ...):
        # Your custom logic
        return super().decide(...)
```

### Additional Storage Backends
```python
# Implement storage interface
class CustomStorage:
    def save(self, data): ...
    def load(self): ...
    def query(self, pattern): ...
```

---

**This architecture enables:**
- ✅ Real-time threat detection
- ✅ Decentralized trust
- ✅ Network-wide immunity
- ✅ Verifiable governance
- ✅ Continuous learning
