from datetime import datetime
from typing import Dict, Any, List
from event_bus import EventBus


class MarketplaceService:
    """
    Marketplace Service.
    Responsibility:
    - Consume meter events
    - Identify available surplus energy
    - Match seller energy with buyer demand
    - Publish TradeCompleted events
    This service does not collect raw IoT data. It only reacts to clean
    domain events from the Smart Meter Integration Service.
    """

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.completed_trades: List[Dict[str, Any]] = []

        self.event_bus.subscribe("MeterReadingReceived", self.handle_meter_reading)

    def handle_meter_reading(self, event: Dict[str, Any]) -> None:
    
        # Create a trade if surplus energy is available.
        surplus_energy = event["surplus_energy_kwh"]

        if surplus_energy <= 0:
            return

        trade = {
            "event_type": "TradeCompleted",
            "trade_id": f"TRD-{event['meter_id']}-{len(self.completed_trades) + 1}",
            "seller_household_id": event["household_id"],
            "buyer_household_id": "BUYER-001",
            "energy_kwh": surplus_energy,
            "price_per_kwh": 0.28,
            "total_amount": round(surplus_energy * 0.28, 2),
            "timestamp": datetime.utcnow().isoformat()
        }

        self.completed_trades.append(trade)
        self.event_bus.publish(trade)

    def get_completed_trades(self) -> List[Dict[str, Any]]:
        return self.completed_trades
