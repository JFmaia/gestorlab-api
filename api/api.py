from fastapi import APIRouter
from api.endpoints import usuario, laboratorio, projeto, permissao, genero, pending, endereco

api_router = APIRouter()

api_router.include_router(usuario.router, prefix='/usuarios', tags=["usuarios"])
api_router.include_router(laboratorio.router, prefix='/laboratorios' ,tags=["laboratorios"])
api_router.include_router(projeto.router, prefix='/projetos' ,tags=["projetos"])
api_router.include_router(permissao.router, prefix='/permissoes' ,tags=["permissoes"])
api_router.include_router(genero.router, prefix='/generos' ,tags=["generos"])
api_router.include_router(pending.router, prefix='/pendentes' ,tags=["pendentes"])
api_router.include_router(endereco.router, prefix='/enderecos' ,tags=["enderecos"])