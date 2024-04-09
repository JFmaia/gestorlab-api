from typing import AsyncGenerator,Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import Session, SessionTest
from core.auth import oauth2_schema
from core.config import settings
from models.usuario import Usuario
import os
class TokenData(BaseModel):
    username: Optional[str] = None

async def get_session() -> AsyncGenerator:
    if os.getenv("TESTING"):
        async with SessionTest() as session:
            yield session
    else:
        async with Session() as session:
            yield session


## Função que descobre quem é o usuario pelo token
async def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_schema)) -> Usuario: # type: ignore
    credential_exception: HTTPException = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possícel autenticar a credencial',
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data: TokenData = TokenData(username=username)

    except JWTError:
        raise credential_exception
    
    async with db as session:
        query = select(Usuario).filter(Usuario.id == token_data.username)
        result = await session.execute(query)
        usuario: Usuario = result.scalars().unique().one_or_none()
        if usuario is None:
            raise credential_exception
        
        return usuario
