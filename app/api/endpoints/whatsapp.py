from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.whatsapp_service import send_whatsapp_message
from app.schemas.client import ClientOut
from app.db.models.client import Client
from app.db.session import get_db
from app.core.security import get_current_active_user

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

class WhatsAppMessage(BaseModel):
    client_id: int
    message: str

@router.post("/send", status_code=status.HTTP_200_OK)
def send_message(
    payload: WhatsAppMessage,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    client = db.query(Client).filter(Client.id == payload.client_id).first()
    if not client or not client.phone:
        raise HTTPException(status_code=404, detail="Cliente não encontrado ou sem telefone")
    status_code = send_whatsapp_message(phone=client.phone, message=payload.message)
    if status_code not in (200, 201):
        raise HTTPException(status_code=500, detail="Falha ao enviar mensagem via WhatsApp")
    return {"detail": "Mensagem enviada com sucesso"}
