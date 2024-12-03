from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt
from datetime import datetime, timedelta
import jwt
from typing import Optional
from models.usuario import UsuarioDB  # Ajuste conforme a estrutura do projeto

# Configurações de segurança
SECRET_KEY = "sua_chave_secreta"  # Substitua por uma chave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

# Função para criar token de acesso
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Função para verificar a senha
def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)

# Função para buscar usuário por e-mail ou telefone
def get_user_by_email_or_phone(login_usuario: str):
    return UsuarioDB.get_or_none(
        (UsuarioDB.email_usuario == login_usuario) |
        (UsuarioDB.telefone_usuario == login_usuario)
    )

# Função para autenticar usuário
def authenticate_user(login_usuario: str, password: str):
    user = get_user_by_email_or_phone(login_usuario)
    if not user or not verify_password(password, user.senha_usuario):
        return False
    return user

# Função para pegar o usuário atual com base no token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = get_user_by_email_or_phone(email)
    if user is None:
        raise credentials_exception
    return user

# Função para verificar se o usuário é root (tipo_usuario = "0")
def is_root(user: UsuarioDB):
    return user.tipo_usuario == "0"

# Função para verificar se o usuário é admin (tipo_usuario = "1" ou "2")
def is_admin(user: UsuarioDB):
    return user.tipo_usuario in ["1", "2"]

# Função para obter o usuário a partir do token
def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return get_user_by_email_or_phone(email)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
