from fastapi import FastAPI  
from .models import SQLModel   
from .db import engine  
from .routers import users, posts, interactions 
'''
SQLModel é importado do arquivo models.py
engine é importado do arquivo db.py, vai servir para conectar o banco de dados
users, posts e interactions são os rotas que foram definidos nos arquivos users.py, posts.py e interactions.py (os 3 arquivos estão na pasta routers)
'''
# esse ponto antes do import é para indicar que o arquivo está na mesma pasta que o main.py

app = FastAPI() 

@app.on_event("startup")  
def on_startup():  
    SQLModel.metadata.create_all(engine)
'''
essa parte vai criar as tabelas do banco de dados, todos eles definidos no arquivo 'models.py
'''

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(interactions.router)
'''
essa parte vai incluir os routers que foram definidos nos arquivos 'users.py', 'posts.py' e 'interactions.py'
'''

'''
esse aquivo vai iniciar o FastAPI e garantir que o bd esteja pronto.
vai basicamente ligar as partes do projeto.
'''