import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from event_bus import EventBus
from smart_meter_service import SmartMeterService
from marketplace_service import MarketplaceService
from settlement_service import SettlementService


def test_full_event_flow_creates_trade_and_settlement():
    event_bus = EventBus()

    smart_meter_service = SmartMeterService(event_bus)
    marketplace_service = MarketplaceService(event_bus)
    settlement_service = SettlementService(event_bus)

    smart_meter_service.receive_meter_reading(
        meter_id="MTR-2001",
        household_id="HOUSE-002",
        energy_generated_kwh=15.0,
        energy_consumed_kwh=10.0
    )

    trades = marketplace_service.get_completed_trades()
    settlements = settlement_service.get_settlements()
    event_log = event_bus.get_event_log()

    assert len(trades) == 1
    assert len(settlements) == 1

    assert trades[0]["event_type"] == "TradeCompleted"
    assert trades[0]["energy_kwh"] == 5.0

    assert settlements[0]["event_type"] == "SettlementCompleted"
    assert settlements[0]["status"] == "COMPLETED"

    event_types = [event["event_type"] for event in event_log]

    assert "MeterReadingReceived" in event_types
    assert "TradeCompleted" in event_types
    assert "SettlementCompleted" in event_types


def test_no_trade_created_when_no_surplus_energy():
    event_bus = EventBus()
    smart_meter_service = SmartMeterService(event_bus)
    marketplace_service = MarketplaceService(event_bus)
    settlement_service = SettlementService(event_bus)

    smart_meter_service.receive_meter_reading(
        meter_id="MTR-3001",
        household_id="HOUSE-003",
        energy_generated_kwh=5.0,
        energy_consumed_kwh=8.0
    )
    assert len(marketplace_service.get_completed_trades()) == 0
    assert len(settlement_service.get_settlements()) == 0
