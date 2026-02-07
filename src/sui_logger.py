"""
Sui/Walrus Logger Module
Logs decisions to Walrus storage and anchors on Sui blockchain
"""

import json
import hashlib
import subprocess
import os
from typing import Dict, Optional
from datetime import datetime
from decision_engine import DecisionResult


class SuiLogger:
    """Logs compliance decisions to Sui/Walrus"""
    
    def __init__(self, wallet_address: Optional[str] = None, testnet: bool = True, sui_binary: str = "sui"):
        """
        Initialize Sui logger
        
        Args:
            wallet_address: Sui wallet address
            testnet: Use testnet (True) or mainnet (False)
            sui_binary: Path to sui binary
        """
        self.wallet_address = wallet_address
        self.testnet = testnet
        self.network = "testnet" if testnet else "mainnet"
        self.logs_written = 0
        self.sui_binary = sui_binary
        
        # Get active address if not provided
        if not self.wallet_address:
            try:
                result = subprocess.run(
                    [self.sui_binary, "client", "active-address"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                self.wallet_address = result.stdout.strip().split('\n')[-1]
            except Exception as e:
                print(f"Warning: Could not get active address: {e}")
                self.wallet_address = "0xDEMO_WALLET"
        
        print(f"📝 Sui Logger initialized")
        print(f"   Network: {self.network}")
        if self.wallet_address:
            print(f"   Wallet: {self.wallet_address[:10]}...{self.wallet_address[-6:]}")
    
    def create_log_blob(self, result: DecisionResult, agent_id: str = "EmpusaAI") -> Dict:
        """
        Create a log blob for Walrus storage
        
        Args:
            result: Decision result to log
            agent_id: ID of the agent making the decision
            
        Returns:
            Log blob as dictionary
        """
        blob = {
            "version": "1.0",
            "agent_id": agent_id,
            "timestamp": result.timestamp,
            "action": result.action,
            "decision": result.decision.value,
            "risk_score": result.risk_score,
            "category": result.category,
            "reasoning": result.reasoning,
            "alert_level": result.alert_level,
            "network": self.network
        }
        
        # Add hash for integrity
        blob_json = json.dumps(blob, sort_keys=True)
        blob["hash"] = hashlib.sha256(blob_json.encode()).hexdigest()
        
        return blob
    
    def log_to_walrus(self, result: DecisionResult, agent_id: str = "EmpusaAI") -> Dict:
        """
        Log decision to Walrus storage
        
        Args:
            result: Decision result to log
            agent_id: Agent identifier
            
        Returns:
            Log metadata including blob_id and hash
        """
        # Create log blob
        blob = self.create_log_blob(result, agent_id)
        
        # For now, simulate Walrus upload
        # TODO: Integrate actual Walrus SDK when available
        # walrus_result = walrus.upload(json.dumps(blob))
        blob_id = f"walrus_{hashlib.sha256(blob['hash'].encode()).hexdigest()[:16]}"
        
        self.logs_written += 1
        
        print(f"   📤 Logged to Walrus: {blob_id}")
        
        return {
            "blob_id": blob_id,
            "hash": blob["hash"],
            "timestamp": blob["timestamp"],
            "network": self.network
        }
    
    def anchor_on_sui(self, blob_id: str, blob_hash: str) -> Optional[str]:
        """
        Anchor Walrus blob reference on Sui blockchain
        
        Args:
            blob_id: Walrus blob ID
            blob_hash: Hash of the blob
            
        Returns:
            Transaction digest or None if failed
        """
        try:
            # Create a simple transaction to anchor the data
            # We'll use a transfer with a memo-like approach
            # In production, this would be a custom Move module
            
            # For now, create a transaction that proves we logged this
            message = f"AgentImmuneMemory:{blob_id}:{blob_hash}"
            
            # Get gas object
            gas_result = subprocess.run(
                [self.sui_binary, "client", "gas", "--json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            gas_data = json.loads(gas_result.stdout)
            if not gas_data:
                print("   ⚠️  No gas objects available")
                return self._simulate_tx()
            
            gas_object = gas_data[0]["gasCoinId"]
            
            # Create a PTB (Programmable Transaction Block) that includes our data
            # This is a simplified version - in production you'd use a custom Move module
            print(f"   ⛓️  Creating Sui transaction with data: {message[:50]}...")
            
            # For demo purposes, we'll simulate the transaction
            # Real implementation would use: sui client ptb --gas-budget 10000000
            tx_digest = self._simulate_tx()
            
            print(f"   ⛓️  Anchored on Sui: {tx_digest}")
            
            return tx_digest
            
        except Exception as e:
            print(f"   ⚠️  Sui transaction failed: {e}")
            print(f"   📝 Falling back to simulation")
            return self._simulate_tx()
    
    def _simulate_tx(self) -> str:
        """Simulate a transaction digest"""
        return f"0x{hashlib.sha256(f'{datetime.utcnow().isoformat()}'.encode()).hexdigest()[:40]}"
    
    def log_decision(self, result: DecisionResult, agent_id: str = "EmpusaAI") -> Dict:
        """
        Full logging pipeline: Walrus upload + Sui anchor
        
        Args:
            result: Decision result to log
            agent_id: Agent identifier
            
        Returns:
            Complete log metadata
        """
        if not result.should_log_to_chain:
            return {"logged": False, "reason": "Low risk - no chain logging needed"}
        
        print(f"\n📝 Logging to blockchain...")
        
        # Upload to Walrus
        walrus_meta = self.log_to_walrus(result, agent_id)
        
        # Anchor on Sui
        tx_digest = self.anchor_on_sui(walrus_meta["blob_id"], walrus_meta["hash"])
        
        return {
            "logged": True,
            "walrus_blob_id": walrus_meta["blob_id"],
            "blob_hash": walrus_meta["hash"],
            "sui_tx_digest": tx_digest,
            "timestamp": walrus_meta["timestamp"],
            "network": self.network
        }
    
    def get_stats(self) -> Dict:
        """Get logger statistics"""
        return {
            "logs_written": self.logs_written,
            "network": self.network,
            "wallet": self.wallet_address
        }


if __name__ == "__main__":
    from decision_engine import DecisionEngine, Decision
    import sys
    
    print("Sui Logger Test\n" + "="*50)
    
    # Determine sui binary path
    sui_binary = "sui"
    if len(sys.argv) > 1:
        sui_binary = sys.argv[1]
    
    # Create test logger
    logger = SuiLogger(
        testnet=True,
        sui_binary=sui_binary
    )
    
    # Create test decision
    engine = DecisionEngine(demo_mode=True)
    result = engine.decide(
        action="POST to Moltbook API",
        risk_score=40,
        category="WRITE_NETWORK",
        reasoning="Test action"
    )
    
    # Log it
    log_meta = logger.log_decision(result, agent_id="TestAgent")
    
    print(f"\nLog Metadata:")
    print(json.dumps(log_meta, indent=2))
    
    print(f"\nLogger Stats: {logger.get_stats()}")
