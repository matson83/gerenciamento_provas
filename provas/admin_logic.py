# provas/admin_logic.py
from ninja import Router
from provas.models import Prova
from provas.schemas import ProvaIn, ProvaOut
from django.contrib.auth import get_user_model
from ninja.security import HttpBearer

User = get_user_model()
admin_router = Router(tags=["Admin"])

class AdminAuth(HttpBearer):
    def authenticate(self, request, token):
        user = User.objects.filter(token=token).first()
        if user and user.role == 'admin':
            request.user = user
            return token

@admin_router.post("/provas/", response=ProvaOut, auth=AdminAuth())
def criar_prova(request, payload: ProvaIn):
    prova = Prova.objects.create(
        titulo=payload.titulo,
        descricao=payload.descricao,
        criada_por=request.user
    )
    return prova
