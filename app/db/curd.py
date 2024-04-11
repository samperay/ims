from sqlalchemy.orm import Session

from app.model import models

# server crud
# TODO: create a new file in db directory for server crud operations

async def get_server_by_id(db: Session, server_id: int):
    return db.query(models.Server).filter(models.Server.id == server_id).first()


async def get_server_by_hostname(db: Session, hostname: str):
    return db.query(models.Server).filter(models.Server.hostname == hostname).first()


# storage crud
# TODO: create a new file in db directory for storage crud operations

async def get_storage_by_id(db: Session, storage_id: int):
    return db.query(models.Storage).filter(models.Storage.id == storage_id).first()

