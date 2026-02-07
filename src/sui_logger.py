"""
Sui/Walrus Logger Module
Logs decisions to Walrus storage and anchors on Sui blockchain
"""

import json
import hashlib
from typing import Dict, Optional
from datetime import datetime
from decision_engine import DecisionResult


class SuiLogger:
    """Logs compliance decisions to Sui/Walrus"""
    
    def __init__(self, wallet_address: Optional[str] = None, testnet: bool = True):
        """
        Initialize Sui logger
        
        Args:
            wallet_address: Sui wallet address
            testnet: Use testnet (True) or mainnet (False)
        """
        self.wallet_address = wallet_address
        self.testnet = testnet
        self.network = "testnet" if testnet else "mainnet"
        self.logs_written = 0
        
        print(f"📝 Sui Logger initialized")
        print(f"   Network: {self.network}")
        if wallet_address:
            print(f"   Wallet: {wallet_address[:10]}...{wallet_address[-6:]}")
    
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
        
        # TODO: Actual Walrus upload
        # For now, simulate with local storage
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
        # TODO: Actual Sui transaction
        # For now, simulate
        tx_digest = f"0x{hashlib.sha256(f'{blob_id}{blob_hash}'.encode()).hexdigest()[:40]}"
        
        print(f"   ⛓️  Anchored on Sui: {tx_digest}")
        
        return tx_digest
    
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
    
    print("Sui Logger Test\n" + "="*50)
    
    # Create test logger
    logger = SuiLogger(
        wallet_address="0xABC123DEF456789",
        testnet=True
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
