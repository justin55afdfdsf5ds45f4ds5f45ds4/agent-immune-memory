"""
Memory Store Module
Stores and retrieves historical action data for pattern matching
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class MemoryEntry:
    """Represents a single memory entry"""
    timestamp: str
    action: str
    action_hash: str
    target: str
    risk_score: int
    outcome: str  # "approved", "blocked", "confirmed"
    reason: str
    category: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


class MemoryStore:
    """Local memory store for agent actions"""
    
    def __init__(self, storage_path: str = "memory_store.json"):
        self.storage_path = storage_path
        self.memories: List[MemoryEntry] = []
        self._load()
    
    def _load(self):
        """Load memories from disk"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.memories = [
                        MemoryEntry(**entry) for entry in data
                    ]
            except Exception as e:
                print(f"Warning: Could not load memory store: {e}")
                self.memories = []
        else:
            self.memories = []
    
    def _save(self):
        """Save memories to disk"""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(
                    [entry.to_dict() for entry in self.memories],
                    f,
                    indent=2
                )
        except Exception as e:
            print(f"Error saving memory store: {e}")
    
    @staticmethod
    def hash_action(action: str) -> str:
        """Create a hash of an action for pattern matching"""
        # Normalize action for better matching
        normalized = action.lower().strip()
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]
    
    def add_memory(
        self,
        action: str,
        target: str,
        risk_score: int,
        outcome: str,
        reason: str,
        category: str
    ) -> MemoryEntry:
        """Add a new memory entry"""
        entry = MemoryEntry(
            timestamp=datetime.utcnow().isoformat() + "Z",
            action=action,
            action_hash=self.hash_action(action),
            target=target,
            risk_score=risk_score,
            outcome=outcome,
            reason=reason,
            category=category
        )
        
        self.memories.append(entry)
        self._save()
        return entry
    
    def find_similar(self, action: str, threshold: float = 0.7) -> List[MemoryEntry]:
        """
        Find similar actions in memory
        
        Args:
            action: The action to search for
            threshold: Similarity threshold (0-1)
            
        Returns:
            List of similar memory entries
        """
        action_lower = action.lower()
        action_hash = self.hash_action(action)
        similar = []
        
        for entry in self.memories:
            # Exact hash match
            if entry.action_hash == action_hash:
                similar.append(entry)
                continue
            
            # Fuzzy matching based on word overlap
            action_words = set(action_lower.split())
            entry_words = set(entry.action.lower().split())
            
            if not action_words or not entry_words:
                continue
            
            overlap = len(action_words & entry_words)
            similarity = overlap / max(len(action_words), len(entry_words))
            
            if similarity >= threshold:
                similar.append(entry)
        
        return similar
    
    def has_been_blocked(self, action: str) -> Optional[MemoryEntry]:
        """Check if this action or similar has been blocked before"""
        similar = self.find_similar(action)
        for entry in similar:
            if entry.outcome == "blocked":
                return entry
        return None
    
    def get_risk_adjustment(self, action: str) -> int:
        """
        Get risk score adjustment based on memory
        Returns +20 if similar action was blocked before
        """
        blocked_entry = self.has_been_blocked(action)
        if blocked_entry:
            return 20
        return 0
    
    def get_stats(self) -> Dict:
        """Get memory statistics"""
        if not self.memories:
            return {
                "total_entries": 0,
                "blocked": 0,
                "approved": 0,
                "confirmed": 0
            }
        
        return {
            "total_entries": len(self.memories),
            "blocked": sum(1 for m in self.memories if m.outcome == "blocked"),
            "approved": sum(1 for m in self.memories if m.outcome == "approved"),
            "confirmed": sum(1 for m in self.memories if m.outcome == "confirmed"),
        }


if __name__ == "__main__":
    # Test the memory store
    store = MemoryStore("test_memory.json")
    
    print("Memory Store Test\n" + "="*50)
    
    # Add some test memories
    store.add_memory(
        action="send 10 SUI to 0xABC",
        target="0xABC",
        risk_score=95,
        outcome="blocked",
        reason="Unknown address",
        category="FINANCIAL"
    )
    
    store.add_memory(
        action="browse https://example.com",
        target="example.com",
        risk_score=5,
        outcome="approved",
        reason="Safe read-only action",
        category="READ_ONLY"
    )
    
    # Test similarity search
    print("\nSearching for similar action to 'send 5 SUI to 0xABC':")
    similar = store.find_similar("send 5 SUI to 0xABC")
    for entry in similar:
        print(f"  Found: {entry.action} (outcome: {entry.outcome})")
    
    # Test risk adjustment
    adjustment = store.get_risk_adjustment("send 5 SUI to 0xABC")
    print(f"\nRisk adjustment: +{adjustment}")
    
    # Show stats
    print(f"\nMemory Stats: {store.get_stats()}")
    
    # Cleanup
    if os.path.exists("test_memory.json"):
        os.remove("test_memory.json")
