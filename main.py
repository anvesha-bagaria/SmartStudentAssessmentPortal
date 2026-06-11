from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from auth import verify_token
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os


app=FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")