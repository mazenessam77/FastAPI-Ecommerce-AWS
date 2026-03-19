from fastapi import APIRouter, Depends, Request, status, Header
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.services.auth import AuthService
from app.db.database import get_db
from app.schemas.auth import UserOut, Signup


router = APIRouter(tags=["Auth"], prefix="/auth")
auth_scheme = HTTPBearer()


@router.post("/signup", status_code=status.HTTP_200_OK, response_model=UserOut)
async def user_signup(
        user: Signup,
        db: Session = Depends(get_db)):
    return await AuthService.signup(db, user)


@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(
        request: Request,
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    return await AuthService.login(user_credentials, db, request)


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(
        refresh_token: str = Header(),
        db: Session = Depends(get_db)):
    return await AuthService.get_refresh_token(token=refresh_token, db=db)


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return AuthService.logout(token, db)


@router.get("/sessions", status_code=status.HTTP_200_OK)
def list_sessions(
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return AuthService.get_sessions(token, db)


@router.delete("/sessions", status_code=status.HTTP_200_OK)
def revoke_all_sessions(
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return AuthService.revoke_all_sessions(token, db)


@router.delete("/sessions/{session_id}", status_code=status.HTTP_200_OK)
def revoke_session(
        session_id: int,
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return AuthService.revoke_session(session_id, token, db)
