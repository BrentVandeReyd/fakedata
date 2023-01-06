from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import os
import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi import FastAPI
from pydantic import BaseModel
import json
from faker import Faker
from faker.providers import internet
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost/",
    "http://localhost:8080/",
    "https://localhost.tiangolo.com/",
    "http://127.0.0.1:5500/",
    "https://brentvandereyd.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)

print("We are in the main.......")
if not os.path.exists('.\sqlitedb'):
    print("Making folder.......")
    os.makedirs('.\sqlitedb')

print("Creating tables.......")
models.Base.metadata.create_all(bind=engine)
print("Tables created.......")

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/ip/", response_model=schemas.Ip)
def create_ip(ip: schemas.IpCreate, db: Session = Depends(get_db)):
    return crud.create_ip(db=db, ip=ip)

@app.get("/ip/", response_model=list[schemas.Ip])
def read_ip(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_ip(db, skip=skip, limit=limit)
    return items


@app.post("/fakename/", response_model=schemas.Item)
def create_fakename(naam: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_fakename(db=db, fakenaam=naam)

@app.get("/fakename/", response_model=list[schemas.Item])
def read_fakename(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_fakename(db, skip=skip, limit=limit)
    return items


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #Try to authenticate the user
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Add the JWT case sub with the subject(user)
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    #Return the JWT as a bearer token to be placed in the headers
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.put("/fakename/{id}", response_model=schemas.Item)
def put_fakename(id: int, fakename: schemas.ItemEdit, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_fakename = crud.put_fakename(db, fakename, id=id)
    return db_fakename

@app.delete("/fakename/{id}")
def delete_order(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    fakename = crud.delete_fakename(db, id=id)
    return fakename