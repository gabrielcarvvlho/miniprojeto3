from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ..models import Interaction, InteractionCreate, Post, User
from ..db import get_session

router = APIRouter(prefix="/interactions")

@router.post("/")
def create_interaction(interaction: InteractionCreate, session: Session = Depends(get_session)):
    # Ver se o post existe
    post = session.get(Post, interaction.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado.")
    # Ver se o usuário existe
    user = session.get(User, interaction.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    # Ver se já existe interação desse tipo para esse usuário e post :D
    existing = session.exec(
        select(Interaction).where(
            (Interaction.user_id == interaction.user_id) &
            (Interaction.post_id == interaction.post_id) &
            (Interaction.type == interaction.type)
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuário já fez essa interação nesse post.")
    new_interaction = Interaction(
        user_id=interaction.user_id,
        post_id=interaction.post_id,
        type=interaction.type
    )
    session.add(new_interaction)
    session.commit()
    session.refresh(new_interaction)
    return new_interaction