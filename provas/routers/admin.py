# provas/routers/admin.py
from ninja import Router, Schema
from typing import List
from ..models import Prova, Questao, Alternativa, ProvaParticipante
from django.shortcuts import get_object_or_404
from accounts.auth import AuthBearer

router = Router(tags=["Admin"])

# Schemas
class AlternativaSchema(Schema):
    texto: str
    correta: bool

class QuestaoSchema(Schema):
    enunciado: str
    alternativas: List[AlternativaSchema]

class ProvaCreateSchema(Schema):
    titulo: str
    descricao: str = ""
    questoes: List[QuestaoSchema]

class AtribuirProvaSchema(Schema):
    prova_id: int
    participante_id: int

# Endpoint: Criar Prova
@router.post("/criar", auth=AuthBearer())
def criar_prova(request, payload: ProvaCreateSchema):
    if not request.auth.is_admin():
        return {"error": "Apenas admins podem criar provas."}

    prova = Prova.objects.create(
        titulo=payload.titulo,
        descricao=payload.descricao,
        criada_por=request.auth
    )

    for questao_data in payload.questoes:
        questao = Questao.objects.create(prova=prova, enunciado=questao_data.enunciado)
        for alt_data in questao_data.alternativas:
            Alternativa.objects.create(
                questao=questao,
                texto=alt_data.texto,
                correta=alt_data.correta
            )

    return {"message": "Prova criada com sucesso", "prova_id": prova.id}

# Endpoint: Atribuir Prova a Participante
@router.post("/atribuir", auth=AuthBearer())
def atribuir_prova(request, payload: AtribuirProvaSchema):
    if not request.auth.is_admin():
        return {"error": "Apenas admins podem atribuir provas."}
    
    prova = get_object_or_404(Prova, id=payload.prova_id)
    ProvaParticipante.objects.create(
        prova=prova,
        participante_id=payload.participante_id
    )
    return {"message": "Prova atribuída com sucesso"}
