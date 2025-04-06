from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from accounts.models import Prova, Questao, Alternativa, Resposta
from django.contrib.auth.models import User
from .schemas import *
from typing import List
from ninja.errors import HttpError
from accounts.auth import JWTAuth
from provas.routers import include_routers
from ninja import NinjaAPI

router = Router()

api = NinjaAPI()

include_routers(api)

admin_router = Router(auth=JWTAuth())

class ParticipanteOut(Schema):
    id: int
    username: str

@admin_router.get("/participantes", response=List[ParticipanteOut])
def listar_participantes(request):
    if not request.auth or getattr(request.auth, "role", "") != "ADMIN":
        raise HttpError(403, "Acesso negado")

    participantes = User.objects.filter(role="PARTICIPANTE")
    return participantes

def is_admin(user):
    return user.is_authenticated and user.is_staff

def is_participante(user):
    return user.is_authenticated and not user.is_staff

@router.get("/", response=List[ProvaOut])
def listar_provas(request):
    user = request.user
    if is_admin(user):
        provas = Prova.objects.prefetch_related("questoes__alternativas").all()
    else:
        provas = user.provas_designadas.prefetch_related("questoes__alternativas").all()
    return provas

@router.post("/", response=ProvaOut)
def criar_prova(request, data: ProvaCreate):
    if not is_admin(request.user):
        return {"error": "Apenas administradores podem criar provas"}
    prova = Prova.objects.create(**data.dict(), criada_por=request.user)
    return prova

@router.post("/{prova_id}/questoes/")
def adicionar_questao(request, prova_id: int, data: QuestaoCreate):
    if not is_admin(request.user):
        return {"error": "Apenas administradores podem criar questões"}
    prova = get_object_or_404(Prova, id=prova_id)
    questao = Questao.objects.create(prova=prova, enunciado=data.enunciado)
    alternativas = []
    for i, texto in enumerate(data.alternativas):
        alternativas.append(
            Alternativa(questao=questao, texto=texto, correta=(i == data.correta))
        )
    Alternativa.objects.bulk_create(alternativas)
    return {"success": "Questão criada com sucesso"}

@router.post("/responder/")
def responder_questao(request, data: RespostaCreate):
    if not is_participante(request.user):
        return {"error": "Apenas participantes podem responder"}
    questao = get_object_or_404(Questao, id=data.questao_id)
    alternativa = get_object_or_404(Alternativa, id=data.alternativa_id, questao=questao)
    Resposta.objects.update_or_create(
        participante=request.user,
        questao=questao,
        defaults={"alternativa": alternativa}
    )
    return {"success": "Resposta registrada"}

from django.db.models import Count, Q

# 👥 Atribuir participantes a uma prova (admin only)
@router.post("/atribuir/")
def atribuir_participantes(request, data: AtribuirParticipantesSchema):
    if not is_admin(request.user):
        return {"error": "Apenas administradores podem atribuir provas"}

    prova = get_object_or_404(Prova, id=data.prova_id)
    users = User.objects.filter(id__in=data.participantes_ids)
    prova.participantes.add(*users)
    return {"success": f"{users.count()} participante(s) atribuídos à prova"}

# 👀 Visualizar respostas
@router.get("/respostas/{prova_id}/", response=List[RespostaOut])
def ver_respostas(request, prova_id: int):
    prova = get_object_or_404(Prova, id=prova_id)
    user = request.user

    if is_admin(user):
        respostas = Resposta.objects.filter(questao__prova=prova)
    else:
        respostas = Resposta.objects.filter(questao__prova=prova, participante=user)

    output = []
    for resposta in respostas.select_related("questao", "alternativa"):
        output.append(RespostaOut(
            questao_id=resposta.questao.id,
            enunciado=resposta.questao.enunciado,
            alternativa_escolhida=resposta.alternativa.texto,
            correta=resposta.alternativa.correta
        ))
    return output

# 🧠 Score individual
@router.get("/score/{prova_id}/")
def calcular_score(request, prova_id: int):
    user = request.user
    respostas = Resposta.objects.filter(participante=user, questao__prova_id=prova_id)
    acertos = sum([r.esta_correta() for r in respostas])
    return {"acertos": acertos, "total": respostas.count()}

# 🏆 Ranking por prova
@router.get("/ranking/{prova_id}/", response=List[RankingEntry])
def ranking_participantes(request, prova_id: int):
    if not is_admin(request.user):
        return {"error": "Apenas administradores podem ver o ranking"}

    respostas = Resposta.objects.filter(questao__prova_id=prova_id)
    participantes = User.objects.filter(resposta__questao__prova_id=prova_id).distinct()

    ranking = []
    for user in participantes:
        user_respostas = respostas.filter(participante=user)
        acertos = sum([r.esta_correta() for r in user_respostas])
        ranking.append(RankingEntry(
            participante_id=user.id,
            nome=user.username,
            acertos=acertos
        ))

    # ordena por acertos decrescentes
    return sorted(ranking, key=lambda x: x.acertos, reverse=True)

# provas/routers.py
from .routers import admin_router as provas_admin_router


def include_routers(api):
    api.add_router("/provas/admin", provas_admin_router)
