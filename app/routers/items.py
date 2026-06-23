from fastapi import APIRouter, HTTPException, status

from app.schemas import ItemCreate, ItemResponse, ItemUpdate
from app.store import store

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemResponse])
def list_items(skip: int = 0, limit: int = 100) -> list[ItemResponse]:
    return store.list_active(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int) -> ItemResponse:
    item = store.get(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate) -> ItemResponse:
    return store.create(item)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate) -> ItemResponse:
    updated = store.update(item_id, item)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return updated


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    deleted = store.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
