from collections import defaultdict
from collections.abc import Callable
from typing import TypeVar, cast


EventT = TypeVar("EventT")


class EventDispatcher:
    def __init__(self) -> None:
        self._handlers: dict[type[object], list[Callable[[object], None]]] = defaultdict(list)

    def register(
        self,
        event_type: type[EventT],
        handler: Callable[[EventT], None],
    ) -> None:
        self._handlers[event_type].append(cast(Callable[[object], None], handler))

    def dispatch(self, event: object) -> None:
        for handler in tuple(self._handlers.get(type(event), ())):
            handler(event)