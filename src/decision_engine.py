"""
Decision Engine Module
Makes decisions about whether to allow, log, or block actions
"""

from enum import Enum
from typing import Dict, Tuple
from dataclasses import dataclass
from datetime import datetime


class Decision(Enum):
    AUTO_APPROVE = "auto_approve"
    APPROVE_WITH_LOGGING = "approve_with_logging"
    REQUIRE_CONFIRMATION = "require_confirmation"
    BLOCK = "block"


@dataclass
class DecisionResult:
    """Result of a decision"""
    decision: Decision
    risk_score: int
    category: str
    reasoning: str
    timestamp: str
    action: str
    should_log_to_chain: bool
    alert_level: str  # "none", "info", "warning", "critical"
    
    def to_dict(self) -> Dict:
        return {
            "decision": self.decision.value,
            "risk_score": self.risk_score,
            "category": self.category,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp,
            "action": self.action,
            "should_log_to_chain": self.should_log_to_chain,
            "alert_level": self.alert_level
        }


class DecisionEngine:
    """Makes decisions about agent actions based on risk scores"""
    
    # Decision thresholds
    THRESHOLD_AUTO_APPROVE = 30
    THRESHOLD_CONFIRMATION = 70
    THRESHOLD_BLOCK = 90
    
    def __init__(self, demo_mode: bool = False):
        """
        Initialize decision engine
        
        Args:
            demo_mode: If True, auto-deny instead of requiring confirmation
        """
        self.demo_mode = demo_mode
        self.decision_count = 0
    
    def decide(
        self,
        action: str,
        risk_score: int,
        category: str,
        reasoning: str,
        memory_match: bool = False
    ) -> DecisionResult:
        """
        Make a decision about an action
        
        Args:
            action: The action being evaluated
            risk_score: Risk score from classifier
            category: Risk category
            reasoning: Classification reasoning
            memory_match: Whether similar action was found in memory
            
        Returns:
            DecisionResult with decision and metadata
        """
        self.decision_count += 1
        
        # Determine decision based on risk score
        if risk_score < self.THRESHOLD_AUTO_APPROVE:
            decision = Decision.AUTO_APPROVE
            alert_level = "none"
            should_log = False
            decision_reasoning = "Low risk - auto-approved"
            
        elif risk_score < self.THRESHOLD_CONFIRMATION:
            decision = Decision.APPROVE_WITH_LOGGING
            alert_level = "info"
            should_log = True
            decision_reasoning = "Medium risk - approved with enhanced logging"
            
        elif risk_score < self.THRESHOLD_BLOCK:
            if self.demo_mode:
                decision = Decision.BLOCK
                alert_level = "warning"
                should_log = True
                decision_reasoning = "High risk - blocked (demo mode)"
            else:
                decision = Decision.REQUIRE_CONFIRMATION
                alert_level = "warning"
                should_log = True
                decision_reasoning = "High risk - requires user confirmation"
                
        else:  # risk_score >= THRESHOLD_BLOCK
            decision = Decision.BLOCK
            alert_level = "critical"
            should_log = True
            decision_reasoning = "Critical risk - BLOCKED"
        
        # Add memory context to reasoning
        if memory_match:
            decision_reasoning += " | Similar action found in memory"
        
        # Combine reasoning
        full_reasoning = f"{reasoning} | {decision_reasoning}"
        
        return DecisionResult(
            decision=decision,
            risk_score=risk_score,
            category=category,
            reasoning=full_reasoning,
            timestamp=datetime.utcnow().isoformat() + "Z",
            action=action,
            should_log_to_chain=should_log,
            alert_level=alert_level
        )
    
    def format_decision(self, result: DecisionResult) -> str:
        """Format decision result for display"""
        symbols = {
            "none": "✓",
            "info": "ℹ",
            "warning": "⚠",
            "critical": "✗"
        }
        
        symbol = symbols.get(result.alert_level, "?")
        
        lines = [
            f"\n{symbol} DECISION #{self.decision_count}",
            f"Action: {result.action}",
            f"Risk Score: {result.risk_score}",
            f"Category: {result.category}",
            f"Decision: {result.decision.value.upper()}",
            f"Alert Level: {result.alert_level.upper()}",
            f"Reasoning: {result.reasoning}",
        ]
        
        if result.should_log_to_chain:
            lines.append("📝 Will be logged to Sui/Walrus")
        
        return "\n".join(lines)
    
    def get_stats(self) -> Dict:
        """Get decision statistics"""
        return {
            "total_decisions": self.decision_count,
            "demo_mode": self.demo_mode
        }


if __name__ == "__main__":
    # Test the decision engine
    engine = DecisionEngine(demo_mode=True)
    
    print("Decision Engine Test\n" + "="*50)
    
    test_cases = [
        ("browse website", 5, "READ_ONLY", "Safe read action"),
        ("post to API", 40, "WRITE_NETWORK", "Network write"),
        ("send crypto", 75, "FINANCIAL", "Financial transaction"),
        ("rm -rf with injection", 95, "DESTRUCTIVE", "Injection detected"),
    ]
    
    for action, score, category, reasoning in test_cases:
        result = engine.decide(action, score, category, reasoning)
        print(engine.format_decision(result))
        print()
