from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session


from app import crud, schemas, models, deps

router = APIRouter()


@router.get("/{episode_id}", response_model=schemas.Episode)
async def purchase_episode(
    db: Session = Depends(deps.get_db),
    user_info: Dict[str, Any] = Depends(deps.get_current_active_user),
    main_service: deps.MainService = Depends(),
    library_service: deps.LibraryService = Depends(),
    *,
    episode_id: int
):
    """
    Purchase episode
    """
    episode = await main_service.get_episode(episode_id=episode_id)
    consumer = crud.consumer.get(db, id=user_info['user'].id)
    if consumer.cash < episode.price:
        raise HTTPException(status_code=400, detail='Insufficient cache')
    await library_service.create_purchased_episode(
        episode_id=episode_id, 
        token=user_info['token']
    )
    current_cash = consumer.cash-episode.price
    crud.consumer.update(
        db, 
        db_obj=consumer, 
        obj_in=schemas.ConsumerUpdate(cash=current_cash)
    )

    return episode
