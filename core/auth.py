from pytz import timezone
from typing import Optional, List 
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.orm import Session
from jose import jwt

from models.__all_models import Usuario
from core.config import settings
from core.security import verificar_senha

from pydantic import EmailStr

oauth2_schema = OAuth2PasswordBearer (
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)

def autenticar(email: EmailStr, senha:str, db: Session) -> Optional[Usuario]:
    query = select(Usuario).filter(Usuario.ativo == True).filter(Usuario.email == email)
    result = db.execute(query)
    usuario: Usuario = result.scalars().unique().one_or_none()

    if not usuario:
        return None
    if not verificar_senha(senha, usuario.senha):
        return None
    
    return usuario
    

def criar_token(tipo_token: str, tempo_vida: timedelta, sub:str) -> str:
    payload = {}

    rn = timezone('America/Fortaleza') 
    expira = datetime.now(tz=rn) + tempo_vida

    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=rn)
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def criar_token_acesso(sub: str) -> str:
    return criar_token(
        tipo_token = 'access_token',
        tempo_vida= timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )