from sqlmodel import SQLModel, create_engine, Session
'''
create_engine é usado para criar a conexão com o banco de dados
Session é usado para criar uma sessão com o banco de dados
'''

DATABASE_URL = "sqlite:///./rede.db" 
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
