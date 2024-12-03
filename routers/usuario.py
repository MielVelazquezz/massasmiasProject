from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.usuario import (
    UsuarioRead,
    UsuarioCreate,
    UsuarioReadList,
    UsuarioUpdate,
    LoginResponse
)
from models.usuario import UsuarioDB
from auth import (
    create_access_token,
    authenticate_user,
    # get_user_from_token,
    get_current_user  # Adicionei essa função que estava faltando
)
from passlib.hash import bcrypt

router = APIRouter(
    prefix='/usuarios', tags=['USUÁRIOS']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

@router.post('', response_model=UsuarioRead)
def criar_usuario(novo_usuario: UsuarioCreate):
    novo_usuario.senha_usuario = bcrypt.hash(novo_usuario.senha_usuario)
    usuario = UsuarioDB.create(**novo_usuario.model_dump())
    return usuario

@router.get('', response_model=UsuarioReadList)
def listar_usuario():
    usuarios = UsuarioDB.select()
    return {'usuarios': usuarios}

@router.get('/{id_usuario}', response_model=UsuarioRead)
def listar_usuario_por_id(id_usuario: int):
    usuario = UsuarioDB.get_or_none(UsuarioDB.id_usuario == id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.patch('/{id_usuario}', response_model=UsuarioRead)
def atualizar_usuario(id_usuario: int, usuario_atualizado: UsuarioUpdate):
    usuario = UsuarioDB.get_or_none(UsuarioDB.id_usuario == id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Atualizar campos conforme enviados
    usuario.nome_usuario = usuario_atualizado.nome_usuario or usuario.nome_usuario
    usuario.email_usuario = usuario_atualizado.email_usuario or usuario.email_usuario
    usuario.telefone_usuario = usuario_atualizado.telefone_usuario or usuario.telefone_usuario
    usuario.endereco_usuario = usuario_atualizado.endereco_usuario or usuario.endereco_usuario
    usuario.tipo_usuario = usuario_atualizado.tipo_usuario or usuario.tipo_usuario

    if usuario_atualizado.senha_usuario:
        usuario.senha_usuario = bcrypt.hash(usuario_atualizado.senha_usuario)

    usuario.save()
    return usuario

@router.delete('/{id_usuario}', response_model=UsuarioRead)
def excluir_usuario(id_usuario: int):
    usuario = UsuarioDB.get_or_none(UsuarioDB.id_usuario == id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    usuario.delete_instance()
    return usuario

@router.post("/login", response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")

    access_token = create_access_token(data={"sub": user.email_usuario, "tipo_usuario": user.tipo_usuario, "id_usuario": user.id_usuario})

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        tipo_usuario=user.tipo_usuario,
        id_usuario=user.id_usuario
    )


@router.get("/me/")
def get_logged_user(current_user= Depends(get_current_user)):
    print(current_user)
    return {
        "nome": current_user.nome_usuario,
        "email": current_user.email_usuario,
        "tipo_usuario": current_user.tipo_usuario,
        "id_usuario": current_user.id_usuario
    }

@router.get("/no-user/")
def no_user():
    return {
        "nome": "Visitante",  # Nome genérico para visitantes não logados
    }

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # Lógica para invalidar o token, se necessário
    return {"message": "Deslogado com sucesso"}