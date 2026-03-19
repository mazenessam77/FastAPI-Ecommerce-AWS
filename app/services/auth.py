from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, Request, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models.models import User, UserSession
from app.db.database import get_db
from app.core.security import (
    verify_password, get_user_token, get_token_payload,
    get_password_hash, hash_token,
)
from app.core.config import settings
from app.utils.responses import ResponseHandler
from app.schemas.auth import Signup


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    @staticmethod
    async def login(user_credentials: OAuth2PasswordRequestForm, db: Session, request: Request):
        user = db.query(User).filter(User.username == user_credentials.username).first()
        if not user or not verify_password(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        expires_at = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        session = UserSession(
            user_id=user.id,
            refresh_token="pending",
            user_agent=request.headers.get("user-agent"),
            ip_address=request.client.host if request.client else None,
            expires_at=expires_at,
        )
        db.add(session)
        db.flush()  # get session.id before commit

        token_data = await get_user_token(id=user.id, session_id=session.id)
        session.refresh_token = hash_token(token_data.refresh_token)
        db.commit()

        return token_data

    @staticmethod
    async def signup(db: Session, user: Signup):
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        db_user = User(id=None, **user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return ResponseHandler.create_success(db_user.username, db_user.id, db_user)

    @staticmethod
    async def get_refresh_token(token: str, db: Session):
        payload = get_token_payload(token)
        user_id = payload.get('id')
        session_id = payload.get('session_id')

        if not user_id or not session_id:
            raise ResponseHandler.invalid_token('refresh')

        session = db.query(UserSession).filter(
            UserSession.id == session_id,
            UserSession.user_id == user_id,
            UserSession.is_active == True,
        ).first()

        if not session:
            raise ResponseHandler.invalid_token('refresh')

        if session.expires_at < datetime.utcnow():
            session.is_active = False
            db.commit()
            raise ResponseHandler.invalid_token('refresh')

        if session.refresh_token != hash_token(token):
            raise ResponseHandler.invalid_token('refresh')

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ResponseHandler.invalid_token('refresh')

        # Rotate refresh token
        token_data = await get_user_token(id=user.id, session_id=session.id)
        session.refresh_token = hash_token(token_data.refresh_token)
        session.expires_at = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        db.commit()

        return token_data

    @staticmethod
    def logout(token: HTTPAuthorizationCredentials, db: Session):
        payload = get_token_payload(token.credentials)
        session_id = payload.get('session_id')
        user_id = payload.get('id')

        if not session_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No session in token")

        session = db.query(UserSession).filter(
            UserSession.id == session_id,
            UserSession.user_id == user_id,
        ).first()

        if session:
            db.delete(session)
            db.commit()

        return ResponseHandler.success("Logged out successfully")

    @staticmethod
    def get_sessions(token: HTTPAuthorizationCredentials, db: Session):
        payload = get_token_payload(token.credentials)
        user_id = payload.get('id')

        sessions = db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True,
        ).all()

        return ResponseHandler.success("Active sessions", sessions)

    @staticmethod
    def revoke_session(session_id: int, token: HTTPAuthorizationCredentials, db: Session):
        payload = get_token_payload(token.credentials)
        user_id = payload.get('id')

        session = db.query(UserSession).filter(
            UserSession.id == session_id,
            UserSession.user_id == user_id,
        ).first()

        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

        db.delete(session)
        db.commit()

        return ResponseHandler.success(f"Session {session_id} revoked")

    @staticmethod
    def revoke_all_sessions(token: HTTPAuthorizationCredentials, db: Session):
        payload = get_token_payload(token.credentials)
        user_id = payload.get('id')

        db.query(UserSession).filter(UserSession.user_id == user_id).delete()
        db.commit()

        return ResponseHandler.success("All sessions revoked")
