from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.future import select
from pydantic import BaseModel

from io import BytesIO
from PIL import Image
import base64
import re

from core.database import Session
from core.auth import oauth2_schema
from core.config import settings
from models.usuario import Usuario

class TokenData(BaseModel):
    username: Optional[str] = None

def get_session():
    try:
        db = Session()
        yield db
    finally:
        db.close()


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
        token_data: TokenData = TokenData(username=username)

    except JWTError:
        raise credential_exception
    
    query = select(Usuario).filter(Usuario.id == token_data.username)
    result = db.execute(query)
    usuario: Usuario = result.scalars().unique().one_or_none()
    if usuario is None:
        raise credential_exception
    
    return usuario
    
# Função para processar a imagem
def process_image(image_data: str) -> str:
    # Extrair o formato da imagem da string base64
    image_format = re.search(r'data:image/(\w+);base64,', image_data).group(1)
    image_data = re.sub(r'data:image/\w+;base64,', '', image_data)
    image_bytes = base64.b64decode(image_data)
    
    with BytesIO(image_bytes) as image_io:
        with Image.open(image_io) as image:
            # Verifica se a imagem já é JPEG
            if image_format.lower() != 'jpeg':
                # Converte para JPEG
                image = image.convert('RGB')
            
            # Reduz a qualidade da imagem
            output_io = BytesIO()
            image.save(output_io, format='JPEG', quality=70)
            processed_image_bytes = output_io.getvalue()
    
    # Codifica a imagem processada para base64
    processed_image_base64 = base64.b64encode(processed_image_bytes).decode('utf-8')
    return f"data:image/jpeg;base64,{processed_image_base64}"
