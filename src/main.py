from event_bus import EventBus
from smart_meter_service import SmartMeterService
from marketplace_service import MarketplaceService
from settlement_service import SettlementService


def main():
    event_bus = EventBus()

    smart_meter_service = SmartMeterService(event_bus)
    marketplace_service = MarketplaceService(event_bus)
    settlement_service = SettlementService(event_bus)

    smart_meter_service.receive_meter_reading(
        meter_id="MTR-1001",
        household_id="HOUSE-001",
        energy_generated_kwh=12.5,
        energy_consumed_kwh=7.0
    )

    print("\n*******Completed Trades*******")
    for trade in marketplace_service.get_completed_trades():
        print(trade)

    print("\n*******Completed Settlements*******")
    for settlement in settlement_service.get_settlements():
        print(settlement)

    print("\n*******Event Log*******")
    for event in event_bus.get_event_log():
        print(event)


if __name__ == "__main__":
    main()
