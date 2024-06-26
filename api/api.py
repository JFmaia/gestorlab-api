from fastapi import APIRouter
from api.endpoints import usuario, laboratorio, projeto, permissao

api_router = APIRouter()

api_router.include_router(usuario.router, prefix='/usuarios', tags=["usuarios"])
api_router.include_router(laboratorio.router, prefix='/laboratorios' ,tags=["laboratorios"])
api_router.include_router(projeto.router, prefix='/projetos' ,tags=["projetos"])
api_router.include_router(permissao.router, prefix='/permissoes' ,tags=["permissoes"])