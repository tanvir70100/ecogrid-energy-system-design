from collections import defaultdict
from typing import Callable, Dict, List, Any


class EventBus:
    """
    Simple in-memory event bus used to demonstrate Event-Driven Architecture.

    In the real EcoGrid Energy architecture, this component would be replaced
    by Kafka or RabbitMQ. Services publish domain events and other services
    subscribe to events they care about.
    """

    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = defaultdict(list)
        self.event_log: List[Dict[str, Any]] = []

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        
        # Register a service handler for a specific event type.
        self.subscribers[event_type].append(handler)

    def publish(self, event: Dict[str, Any]) -> None:
        
        # Publish an event to all subscribers.
        event_type = event.get("event_type")

        if not event_type:
            raise ValueError("Event must include an 'event_type' field.")

        self.event_log.append(event)

        handlers = self.subscribers.get(event_type, [])

        for handler in handlers:
            handler(event)

    def get_event_log(self) -> List[Dict[str, Any]]:
    
        # Return all events published during execution.
        return self.event_log
