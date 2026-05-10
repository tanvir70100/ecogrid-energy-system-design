from datetime import datetime
from typing import Dict, Any
from event_bus import EventBus


class SmartMeterService:
    """
    Smart Meter Integration Service.
    Responsibility:
    - Receive smart meter readings
    - Validate energy generation and consumption values
    - Publish MeterReadingReceived events
    This service is separated from Marketplace logic to avoid coupling
    high-frequency IoT ingestion with trading decisions.
    """

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def receive_meter_reading(
        self,
        meter_id: str,
        household_id: str,
        energy_generated_kwh: float,
        energy_consumed_kwh: float
    ) -> Dict[str, Any]:

        # Receive and validate a smart meter reading
        if energy_generated_kwh < 0 or energy_consumed_kwh < 0:
            raise ValueError("Energy values cannot be negative.")

        surplus_energy = energy_generated_kwh - energy_consumed_kwh

        event = {
            "event_type": "MeterReadingReceived",
            "meter_id": meter_id,
            "household_id": household_id,
            "energy_generated_kwh": energy_generated_kwh,
            "energy_consumed_kwh": energy_consumed_kwh,
            "surplus_energy_kwh": surplus_energy,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.event_bus.publish(event)
        return event
