from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime 
import enum

# 3 classes vão ser relacionadas a User:
# USER vai representar a tabela no de usuários no banco de dados
'''
no id temos o uso do optional, que basicamente indica que o id permite que o campo seja nulo 
ENQUANTO o usuário não for criado no banco de dados. APÓS a criação, o id deixará de ser nulo.
o id do usuário começa em 0

no username temos o uso do index para facilitar buscas no banco de dados, 
o unique para garantir que não existam dois usuários com o mesmo nome, 
já o nullable vai indicar que o campo não pode ser nulo.

password é o campo que vai guardar a senha do usuário :D
'''
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False, min_length=3, max_length=20)
    password: str 

# UserCreate vai ser usada para criar um novo usuário
class UserCreate(SQLModel):
    username: str
    password: str

#UserLogin vai ser usada para fazer o login do usuário
# essas duas classes auxiliares não estarão presentes no banco de dados, elas vão ser usadas na validação dos dados
class UserLogin(SQLModel):
    username: str
    password: str

#---------------------------------------------------------------------------------------------

# 2 classes vão ser relacionadas a Post:
# Post vai respresentar a tabela de posts no banco de dados
'''
id do posto segue o mesmo padrão do id do usuário, mas nesse caso o id começa em 1
content é o conteúdo do post, que não pode ser nulo, uma vez que ele foi criado e alguma coisa foi postada e tal
image e video url são opcionais, pois o usuário pode apenas postar um texto, que está em content.
user_id é uma foreign key que vai referenciar o id do User que fez o post
created_at é a data de criação do post, que vai ser preenchida automaticamente com a data atual
updated_at é a data de atualização do post, que vai ser preenchida automaticamente com a data atual, caso o post seja atualizado (nao consegui implementar ainda)
'''
class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str 
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

# PostCreate vai ser usada para criar um novo post
class PostCreate(SQLModel):  
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    content: str  
    user_id: int

# talvez isso rode a questao do updated_at, mas não tenho certeza
'''
class PostUpdate(SQLModel):
    content: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None

'''

#---------------------------------------------------------------------------------------------

# 3 classes vão ser relacionadas a Interaction:
# InteractionType vai representar os tipos de interação que o usuário pode ter com o post
class InterationType(str, enum.Enum):
    like= "like"
    dislike = "dislike"
    love = "love"
    funny = "hahaha"
    hate = "🍅"

# Interaction vai representar a tabela de interações no banco de dados
'''
O id da interação segue o mesmo padrão do id do usuário e do id do post, e nesse caso também começa em 1
post_id é uma foreign key que vai referenciar o id do Post que foi interagido
user_id é uma foreign key que vai referenciar o id do User que fez a interação
type são os tipos de interação instanciados na classe InterationType
'''
class Interaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    user_id: int = Field(foreign_key="user.id")
    type: InterationType

# InteractionCreate vai ser usada para criar uma nova interação
class InteractionCreate(SQLModel):
    user_id: int
    post_id: int
    type: InterationType

#---------------------------------------------------------------------------------------------

# PostWithCounts vai representar a tabela de posts com as contagens de interações
class PostWithCounts(SQLModel):
    id: int
    content: str
    user_id: int
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    likes: int
    loves: int
    dislikes: int
    funny: int
    hates: int
