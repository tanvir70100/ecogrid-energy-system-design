from datetime import datetime
from typing import Dict, Any, List
from event_bus import EventBus


class SettlementService:
    """
    Financial Settlement Service.
    Responsibility:
    - Consume TradeCompleted events
    - Process financial settlement
    - Publish SettlementCompleted or SettlementFailed events
    In a real system, this service would integrate with a payment gateway.
    """

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.settlements: List[Dict[str, Any]] = []

        self.event_bus.subscribe("TradeCompleted", self.handle_trade_completed)

    def handle_trade_completed(self, event: Dict[str, Any]) -> None:
    
        #Process payment settlement for a completed energy trade.
        if event["total_amount"] <= 0:
            settlement_event = {
                "event_type": "SettlementFailed",
                "trade_id": event["trade_id"],
                "reason": "Invalid settlement amount.",
                "timestamp": datetime.utcnow().isoformat()
            }
            self.event_bus.publish(settlement_event)
            return

        settlement_event = {
            "event_type": "SettlementCompleted",
            "settlement_id": f"SET-{event['trade_id']}",
            "trade_id": event["trade_id"],
            "seller_household_id": event["seller_household_id"],
            "buyer_household_id": event["buyer_household_id"],
            "amount": event["total_amount"],
            "status": "COMPLETED",
            "timestamp": datetime.utcnow().isoformat()
        }

        self.settlements.append(settlement_event)
        self.event_bus.publish(settlement_event)

    def get_settlements(self) -> List[Dict[str, Any]]:
        return self.settlements
