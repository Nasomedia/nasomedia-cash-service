from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session


from app import crud, schemas, models, deps

router = APIRouter()

@router.get("/{consumer_id}", response_model=schemas.Consumer)
def read_consumer(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    *,
    consumer_id: int
):
    """
    Retrieve consumer
    """
    consumer = crud.consumer.get(db, id=consumer_id)
    return consumer


@router.get("/me", response_model=schemas.Consumer)
def read_consumer_me(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve consumer me
    """
    consumer = crud.consumer.get(db, id=user.id)
    return consumer


@router.post("", response_model=schemas.Consumer)
def create_consumer(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_user),
    *,
    consumer_in: schemas.ConsumerCreate
):
    """
    Create new consumer
    """
    consumer = crud.consumer.create_with_user(db, obj_in=consumer_in, user_id=user.id)
    return consumer


@router.put("/{consumer_id}", response_model=schemas.Consumer)
def update_consumer(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    *,
    consumer_id: int,
    consumer_in: schemas.ConsumerUpdate
):
    """
    Update consumer
    """
    consumer = crud.consumer.get(db, id=consumer_id)
    if not consumer:
        raise HTTPException(status_code=404, detail="Consumer not found")
    consumer = crud.consumer.update(db, db_obj=consumer, obj_in=consumer_in)
    return consumer


@router.put("/me", response_model=schemas.Consumer)
def update_consumer(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_user),
    *,
    consumer_in: schemas.ConsumerUpdate
):
    """
    Update consumer
    """
    consumer = crud.consumer.get(db, id=user.id)
    if not consumer:
        raise HTTPException(status_code=404, detail="Consumer not found")
    consumer = crud.consumer.update(db, db_obj=consumer, obj_in=consumer_in)
    return consumer


@router.delete("/{consumer_id}", response_model=schemas.Consumer)
def delete_consumer(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    *,
    consumer_id: int,
):
    "Delete consumer"
    consumer = crud.consumer.get(db, id=consumer_id)
    if not consumer:
        raise HTTPException(status_code=404, detail="Consumer not found")
    consumer = crud.consumer.delete(db, id=consumer_id)
    return consumer


@router.delete("/me", response_model=schemas.Consumer)
def delete_consumer_me(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_user),
):
    "Delete consumer me"
    consumer = crud.consumer.get(db, id=user.id)
    if not consumer:
        raise HTTPException(status_code=404, detail="Consumer not found")
    consumer = crud.consumer.delete(db, id=user.id)
    return consumer
