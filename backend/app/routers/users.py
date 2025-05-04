from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ..models import User, UserCreate, UserLogin
from ..db import get_session
'''
User, UserCreate e UserLogin são importados do arquivo models.py
get_session é importado do arquivo db.py, vai servir para conectar com o banco de dados
'''
router = APIRouter(prefix="/users")

@router.post("/register")
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # Verifica se já existe um usuário com esse username
    statement = select(User).where(User.username == user.username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nome de usuário já existe.")

    # Cria um novo usuário a partir do modelo UserCreate
    new_user = User(username=user.username, password=user.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
'''
ROTA DE REGISTRO DE USUÁRIO
Recebe um objeto UserCreate, contendo nome e senha do usuário.
Esse if serve pra verificar se o nome já existe no banco
    Existindo um usuário com o mesmo nome, ele retorna um erro 400, informando que o nome já existe.
    Caso contrário, ele cria um novo usuário a partir do modelo UserCreate, adiciona o novo usuário à sessão e faz o commit para salvar as alterações no banco de dados.
Por fim, ele retorna o novo usuário criado.
'''


@router.post("/login")
def login(
    data: UserLogin,
    session: Session = Depends(get_session)
):
    statement = select(User).where(User.username == data.username)
    user = session.exec(statement).first()
    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Nome de usuário ou senha incorretos.")
    return {"message": "Login realizado com sucesso!", "user_id": user.id}

'''
ROTA DE LOGIN DE USUÁRIO
Recebe um objeto UserLogin, contendo nome e senha do usuário.
Busca o usuário pelo username
Se não encontrar ou a senha estiver incorreta, retorna um erro 401, informando que o nome ou a senha estão incorretos.
Caso contrario, retorna mensagem dizendo que deu certo junto com o id do usuário.
'''
