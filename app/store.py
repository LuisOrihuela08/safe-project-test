import threading

from app.schemas import ItemCreate, ItemResponse, ItemUpdate


class ItemStore:
    """Thread-safe in-memory store for inventory items."""

    def __init__(self) -> None:
        self._items: dict[int, dict] = {}
        self._counter: int = 0
        self._lock = threading.Lock()

    def _next_id(self) -> int:
        self._counter += 1
        return self._counter

    def get(self, item_id: int) -> ItemResponse | None:
        data = self._items.get(item_id)
        if data is None:
            return None
        return ItemResponse(**data)

    def list_active(self, skip: int = 0, limit: int = 100) -> list[ItemResponse]:
        active = [
            ItemResponse(**v)
            for v in self._items.values()
            if v["active"]
        ]
        return active[skip : skip + limit]

    def create(self, item: ItemCreate) -> ItemResponse:
        with self._lock:
            item_id = self._next_id()
            data = {"id": item_id, **item.model_dump()}
            self._items[item_id] = data
        return ItemResponse(**data)

    def update(self, item_id: int, item: ItemUpdate) -> ItemResponse | None:
        with self._lock:
            if item_id not in self._items:
                return None
            updates = item.model_dump(exclude_unset=True)
            self._items[item_id].update(updates)
        return ItemResponse(**self._items[item_id])

    def delete(self, item_id: int) -> bool:
        with self._lock:
            if item_id not in self._items:
                return False
            del self._items[item_id]
        return True

    def clear(self) -> None:
        """Reset store — useful for testing."""
        with self._lock:
            self._items.clear()
            self._counter = 0


store = ItemStore()
