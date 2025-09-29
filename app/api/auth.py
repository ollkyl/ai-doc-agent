from fastapi import APIRouter, Depends
from app.schemas.auth import UserCreate

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(request: UserCreate):
    return {"message": "Login endpoint", "user": request}


@router.post("/register")
async def register(request: UserCreate):
    return {"message": "Register endpoint", "user": request}


@router.post("/logout")
async def logout():
    return {"message": "Logout endpoint"}
