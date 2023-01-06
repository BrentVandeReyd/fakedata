from sqlalchemy.orm import Session

import models
import schemas
import auth

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_ip(db: Session, ip: schemas.IpCreate):
    db_ip = models.Ip(ip=ip.ip)
    db.add(db_ip)
    db.commit()
    db.refresh(db_ip)
    return db_ip

def get_ip(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ip).offset(skip).limit(limit).all()

def create_fakename(db: Session, fakenaam: schemas.ItemCreate):
    db_fake = models.Item(fakename=fakenaam.fakename,ip_id=fakenaam.ip_id)
    db.add(db_fake)
    db.commit()
    db.refresh(db_fake)
    return db_fake


def get_fakename(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def put_fakename(db: Session, fakename = schemas.Item, id = int):
    db_fakename = db.query(models.Item).filter(models.Item.id == id).first()
    db_fakename.fakename = fakename.fakename
    db.commit()
    db.refresh(db_fakename)
    return db_fakename

def delete_fakename(db: Session, id = int):
    db_fakename = db.query(models.Item).filter(models.Item.id == id).first()
    db.delete(db_fakename)
    db.commit()
    return {"detail": "name deleted"}
