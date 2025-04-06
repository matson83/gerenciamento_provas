from ninja import NinjaAPI, Schema
from accounts.auth import AuthBearer  # ✅ certo agora
from django.contrib.auth import authenticate
from ninja_jwt.tokens import RefreshToken
from .models import CustomUser
from typing import List
from provas.models import Prova
from ninja import Schema
from django.db.models import Prefetch
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from provas.models import ProvaParticipante, Resposta
from provas.schemas import ResponderProvaSchema
from provas.routers import include_routers

api = NinjaAPI()
include_routers(api)

# Schemas
class LoginSchema(Schema):
    username: str
    password: str

class RegisterSchema(Schema):
    username: str
    password: str
    email: str
    role: str

class ProvaResumo(Schema):
    id: int
    titulo: str
    descricao: str

class ParticipanteDashboard(Schema):
    id: int
    username: str
    provas: List[ProvaResumo]

@api.post("/auth/registro")
def registrar(request, payload: RegisterSchema):
    if payload.role not in [CustomUser.Role.ADMIN, CustomUser.Role.PARTICIPANTE]:
        raise HttpError(400, "Tipo de usuário inválido")
    
    user = CustomUser.objects.create_user(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        role=payload.role
    )
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": {
            "username": user.username,
            "role": user.role
        }
    }

@api.post("/auth/login")
def login(request, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if not user:
        raise HttpError(401, "Credenciais inválidas")
    
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": {
            "username": user.username,
            "role": user.role
        }
    }

@api.get("/admin/dashboard", auth=AuthBearer())
def dashboard_admin(request):
    if not request.auth.is_admin():
        raise HttpError(403, "Acesso restrito a administradores")

    participantes = CustomUser.objects.filter(role="PARTICIPANTE").prefetch_related(
        "provas__prova"
    )

    result = []
    for p in participantes:
        provas = [{"id": pp.prova.id, "titulo": pp.prova.titulo} for pp in p.provas.all()]
        result.append({
            "id": p.id,
            "username": p.username,
            "provas": provas
        })

    return result


@api.get("/participante/dashboard", auth=AuthBearer())
def dashboard_participante(request):
    user = request.auth
    if not user.is_authenticated or user.role != "PARTICIPANTE":
        raise HttpError(403, "Acesso restrito a participantes")
    
    provas_participante = user.provas.select_related("prova").all()
    
    provas = [
        {
            "id": pp.prova.id,
            "titulo": pp.prova.titulo,
            "descricao": pp.prova.descricao
        }
        for pp in provas_participante
    ]

    return {
        "message": f"Olá {user.username}",
        "provas_atribuidas": provas
    }

@api.post("/participante/responder", auth=AuthBearer())
def responder_prova(request, payload: ResponderProvaSchema):
    user = request.auth

    if user.role != "PARTICIPANTE":
        raise HttpError(403, "Apenas participantes podem responder provas")

    prova_participante = ProvaParticipante.objects.filter(
        prova_id=payload.prova_id,
        participante=user
    ).first()

    if not prova_participante:
        raise HttpError(404, "Prova não atribuída a este participante")

    acertos = 0
    total = len(payload.respostas)

    for resposta in payload.respostas:
        obj, _ = Resposta.objects.update_or_create(
            prova_atribuida=prova_participante,
            questao_id=resposta.questao_id,
            defaults={"alternativa_escolhida_id": resposta.alternativa_id}
        )
        # Verificar se a alternativa escolhida está correta
        if obj.alternativa_escolhida.correta:
            acertos += 1

    nota = round((acertos / total) * 100, 2)

    return {
        "message": "Respostas registradas e prova corrigida",
        "acertos": acertos,
        "total_questoes": total,
        "nota_percentual": nota
    }

@api.get("/admin/ranking/{prova_id}", auth=AuthBearer())
def ranking_por_prova(request, prova_id: int):
    if not request.auth.is_admin():
        raise HttpError(403, "Apenas administradores podem acessar o ranking")

    participantes = ProvaParticipante.objects.filter(prova_id=prova_id).select_related("participante")

    ranking = []

    for pp in participantes:
        respostas = Resposta.objects.filter(prova_atribuida=pp).select_related("alternativa_escolhida")
        total = respostas.count()
        acertos = sum(1 for r in respostas if r.alternativa_escolhida and r.alternativa_escolhida.correta)

        ranking.append({
            "participante": pp.participante.username,
            "acertos": acertos,
            "total": total,
            "nota": round((acertos / total) * 100, 2) if total else 0
        })

    ranking.sort(key=lambda x: x["nota"], reverse=True)

    return {
        "prova_id": prova_id,
        "ranking": ranking
    }


