from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import database, models
from ...schemas import client as schemas
from ..deps import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.ClientResponse)
def create_client(
    client: schemas.ClientCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_client = models.Client(**client.model_dump(), user_id=current_user.id)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@router.get("/", response_model=List[schemas.ClientResponse])
def get_clients(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Client).filter(models.Client.user_id == current_user.id).all()


@router.patch("/{client_id}", response_model=schemas.ClientResponse)
def update_client(
        client_id: int,
        client_update: schemas.ClientBase,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    db_client = db.query(models.Client).filter(models.Client.id == client_id,
                                               models.Client.user_id == current_user.id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Клієнта не знайдено")

    for key, value in client_update.model_dump(exclude_unset=True).items():
        setattr(db_client, key, value)

    db.commit()
    db.refresh(db_client)
    return db_client


@router.delete("/{client_id}", status_code=204)
def delete_client(
        client_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    db_client = db.query(models.Client).filter(models.Client.id == client_id,
                                               models.Client.user_id == current_user.id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Клієнта не знайдено")

    db.delete(db_client)
    db.commit()
    return None