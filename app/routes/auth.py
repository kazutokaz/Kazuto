from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr

from app import auth, db

router = APIRouter()
security = HTTPBearer(auto_error=False)


class RegisterIn(BaseModel):
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterOut(BaseModel):
    id: int
    email: EmailStr


class MeOut(BaseModel):
    id: int
    email: EmailStr


def _get_user_by_email(email: str) -> Optional[dict]:
    con = db.connect()
    try:
        cur = con.cursor()
        cur.execute("SELECT id, email, password_hash FROM users WHERE email=?", (email,))
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        con.close()


@router.post("/register", response_model=RegisterOut)
def register(payload: RegisterIn) -> RegisterOut:
    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="password too short")

    db.init_db()
    con = db.connect()
    try:
        cur = con.cursor()
        created_at = datetime.now(timezone.utc).isoformat()
        try:
            cur.execute(
                "INSERT INTO users(email, password_hash, created_at) VALUES(?,?,?)",
                (str(payload.email), auth.hash_password(payload.password), created_at),
            )
            con.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail="email already registered") from e

        user_id = int(cur.lastrowid)
        return RegisterOut(id=user_id, email=payload.email)
    finally:
        con.close()


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn) -> TokenOut:
    db.init_db()
    u = _get_user_by_email(str(payload.email))
    if not u or not auth.verify_password(payload.password, u["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credentials",
        )

    token = auth.create_access_token(subject=str(payload.email), expires_minutes=60)
    return TokenOut(access_token=token)


def _current_email(creds: HTTPAuthorizationCredentials = Depends(security)) -> str:
    if creds is None or not creds.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")

    try:
        data = auth.decode_access_token(creds.credentials)
        sub = data.get("sub")
        if not sub:
            raise ValueError("missing sub")
        return str(sub)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token") from e


@router.get("/me", response_model=MeOut)
def me(email: str = Depends(_current_email)) -> MeOut:
    db.init_db()
    u = _get_user_by_email(email)
    if not u:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    return MeOut(id=int(u["id"]), email=u["email"])
