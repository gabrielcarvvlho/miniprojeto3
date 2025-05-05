from fastapi import APIRouter, HTTPException, Depends  
from sqlmodel import Session, select  
from ..models import Post, PostCreate, Interaction, PostWithCounts
from ..db import get_session  
from fastapi import Body 

router = APIRouter(prefix="/posts")  

@router.post("/")
def create_post(post: PostCreate, session: Session = Depends(get_session)):
    new_post = Post(content=post.content, user_id=post.user_id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post
'''
Cria um novo post usando POST
Recebe aquela classe PostCreate do arquivo models.py tendo o conteudo e o id do usuario que criou o post
Cria um objeto Post salva no banco de dados e retorna o novo post criado
'''

@router.get("/")
def list_posts(session: Session = Depends(get_session)):
    posts = session.exec(select(Post)).all()
    return posts
'''
Com o método GET, retorna todos os posts do banco de dados
'''

@router.get("/user/{user_id}")
def list_user_posts(user_id: int, session: Session = Depends(get_session)):
    posts = session.exec(select(Post).where(Post.user_id == user_id)).all()
    return posts
'''
Usando o método GET, essa função retorna todos os posts de um determinado usuário
'''

@router.get("/feed", response_model=list[PostWithCounts])
def list_posts_with_counts(session: Session = Depends(get_session)):
    posts = session.exec(select(Post)).all()
    result = []
    for post in posts:
        interactions = session.exec(
            select(Interaction).where(Interaction.post_id == post.id)
        ).all()
        counts = {
            "like": 0,
            "love": 0,
            "dislike": 0,
            "funny": 0,
            "hate": 0
        }
        for inter in interactions:
            counts[inter.type] += 1
        result.append(PostWithCounts(
            id=post.id,
            content=post.content,
            user_id=post.user_id,
            image_url=post.image_url,
            video_url=post.video_url,
            likes=counts["like"],
            loves=counts["love"],
            dislikes=counts["dislike"],
            funny=counts["funny"],
            hates=counts["hate"]
        ))
    return result
'''
Com o método GET, a função retorna os posts mostrando cada um com a contagem de interações
vai ser legal para no front-end mostrar a quantidade de interações que cada post teve
Para cada post, ele busca as interações e conta quantas de cada tipo existem.

'''

@router.get("/{post_id}")
def get_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado.")
    return post
'''
Uso do GET para buscar um post específico atraves do seu id
'''

@router.put("/{post_id}")  
def update_post(  
    post_id: int,  
    post_data: PostCreate,  
    user_id: int = Body(..., embed=True),  
    session: Session = Depends(get_session)  
):  
    post = session.get(Post, post_id)  
    if not post:  
        raise HTTPException(status_code=404, detail="Post não encontrado.")  
    if post.user_id != user_id:  
        raise HTTPException(status_code=403, detail="Você só pode editar seus próprios posts.")  
    post.content = post_data.content  
    # Atualize outros campos se quiser  
    session.commit()  
    session.refresh(post)  
    return post
'''
Uso do método PUT para atualizar um post que ja existe
Recebe o id do post, os novos dados 
verifica se o post é válido e se o usuário que vai editar é o autor
'''

from fastapi import Query

@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    user_id: int = Query(..., description="ID do usuário que está tentando deletar"),
    session: Session = Depends(get_session)
):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado.")
    if post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Você só pode deletar seus próprios posts.")
    session.delete(post)
    session.commit()
    return {"message": "Post deletado com sucesso."}

'''
Usa o método DELETE para deletar um post :D
'''