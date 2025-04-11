from http.client import HTTPException
from ninja import NinjaAPI, Schema
from accounts.auth import AuthBearer
from django.contrib.auth import authenticate
from ninja_jwt.tokens import RefreshToken
from .models import CustomUser
from typing import List
from provas.models import Prova, Questao, Alternativa
from ninja import Schema
from django.db.models import Prefetch
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from provas.models import ProvaParticipante, Resposta
from provas.schemas import ResponderProvaSchema
from provas.routers import include_routers
from typing import Optional

api = NinjaAPI()
include_routers(api)

# Schemas Lofin e Registro
class LoginSchema(Schema):
    username: str
    password: str

class RegisterSchema(Schema):
    username: str
    password: str
    email: str
    role: str

# Schemas Prova

class ProvaParticipanteUpdate(Schema):
    respondida: Optional[bool] = None
    score: Optional[float] = None

class ProvaParticipanteOut(Schema):
    id: int
    participante_id: int
    prova_id: int
    respondida: bool
    score: Optional[float]

    class Config:
        orm_mode = True


class AlternativaUpdateSchema(Schema):
    id: Optional[int] = None
    texto: Optional[str] = None
    correta: Optional[bool] = None

class QuestaoUpdateSchema(Schema):
    id: Optional[int] = None
    enunciado: Optional[str] = None
    alternativas: Optional[List[AlternativaUpdateSchema]] = None

class ProvaUpdateSchema(Schema):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    questoes: Optional[List[QuestaoUpdateSchema]] = None

class AlternativaSchema(Schema):
    id: Optional[int] = None  
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
    participantes_ids: List[int]


################ Modulo Login e Registro

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


################ Modulo Admin Provas e Questões

@api.get("admin/provas", auth=AuthBearer())
def listar_provas(request):
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

@api.get("admin/provas/participantes_controle", response=List[ProvaParticipanteOut])
def listar_participantes_controle(request):
    return ProvaParticipante.objects.all()

@api.put("admin/provas/participantes_controle/{participacao_id}", response=ProvaParticipanteOut)
def editar_participante(request, participacao_id: int, data: ProvaParticipanteUpdate):
    participacao = get_object_or_404(ProvaParticipante, id=participacao_id)

    if data.respondida is not None:
        participacao.respondida = data.respondida
    if data.score is not None:
        participacao.score = data.score

    participacao.save()
    return participacao

@api.delete("admin/provas/participantes_controle/{participacao_id}")
def remover_participante(request, participacao_id: int):
    participacao = get_object_or_404(ProvaParticipante, id=participacao_id)
    participacao.delete()
    return {"success": True, "message": "Participante removido da prova."}

@api.get("/admin/provas/detalhes/{prova_id}", auth=AuthBearer())
def detalhes_prova(request, prova_id: int):
    if not request.auth.is_admin():
        raise HttpError(403, "Apenas administradores podem acessar os detalhes da prova")

    prova = get_object_or_404(Prova, id=prova_id)
    questoes = prova.questoes.prefetch_related("alternativas").all()

    resultado = {
        "id": prova.id,
        "titulo": prova.titulo,
        "descricao": prova.descricao,
        "questoes": []
    }

    for questao in questoes:
        alternativas = [
            {
                "id": alt.id,
                "texto": alt.texto,
                "correta": alt.correta
            } for alt in questao.alternativas.all()
        ]
        resultado["questoes"].append({
            "id": questao.id,
            "enunciado": questao.enunciado,
            "alternativas": alternativas
        })

    return resultado




@api.post("admin/provas/criar", auth=AuthBearer())
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

@api.post("admin/provas/atribuir", auth=AuthBearer())
def atribuir_prova(request, payload: AtribuirProvaSchema):
    if not request.auth.is_admin():
        return {"error": "Apenas admins podem atribuir provas."}
    
    prova = get_object_or_404(Prova, id=payload.prova_id)
    
    atribuicoes = []
    for participante_id in payload.participantes_ids:
        atribuicao, created = ProvaParticipante.objects.get_or_create(
            prova=prova,
            participante_id=participante_id
        )
        atribuicoes.append({
            "participante_id": participante_id,
            "status": "criado" if created else "já existia"
        })

    return {
        "message": "Prova atribuída com sucesso",
        "atribuidos": atribuicoes
    }

@api.put("admin/provas/{prova_id}", auth=AuthBearer())
def editar_prova(request, prova_id: int, payload: ProvaUpdateSchema):
    if not request.auth.is_admin():
        return {"error": "Apenas admins podem editar provas."}

    prova = get_object_or_404(Prova, id=prova_id)
    prova.titulo = payload.titulo
    prova.descricao = payload.descricao
    prova.save()

    if payload.questoes:
        for questao_data in payload.questoes:
            if questao_data.id:
                questao = Questao.objects.filter(id=questao_data.id, prova=prova).first()
                if questao:
                    if questao_data.enunciado:
                        questao.enunciado = questao_data.enunciado
                    questao.save()

                    if questao_data.alternativas:
                        for alt_data in questao_data.alternativas:
                            alternativa = Alternativa.objects.filter(id=alt_data.id, questao=questao).first()
                            if alternativa:
                                if alt_data.texto is not None:
                                    alternativa.texto = alt_data.texto
                                if alt_data.correta is not None:
                                    alternativa.correta = alt_data.correta
                                alternativa.save()
                else:
                    raise HTTPException(status_code=404, detail=f"Questão com id {questao_data.id} não encontrada.")
            else:
                # Cria nova questão
                nova_questao = Questao.objects.create(
                    prova=prova,
                    enunciado=questao_data.enunciado or ""
                )
                if questao_data.alternativas:
                    for alt_data in questao_data.alternativas:
                        Alternativa.objects.create(
                            questao=nova_questao,
                            texto=alt_data.texto or "",
                            correta=alt_data.correta or False
                        )


    return {"message": "Prova atualizada com sucesso"}

@api.delete("admin/provas/{prova_id}", auth=AuthBearer())
def deletar_prova(request, prova_id: int):
    if not request.auth.is_admin():
        return {"error": "Apenas admins podem deletar provas."}
    
    prova = get_object_or_404(Prova, id=prova_id)
    prova.delete()
    return {"message": "Prova deletada com sucesso"}


################# Modulo Admin Questões (Editar e Deletar)

@api.put("/admin/provas/{prova_id}/questoes/{questao_id}", auth=AuthBearer())
def editar_questao(request, prova_id: int, questao_id: int, payload: QuestaoUpdateSchema):
    if not request.auth.is_admin():
        raise HttpError(403, "Apenas admins podem editar questões.")

    questao = get_object_or_404(Questao, id=questao_id, prova_id=prova_id)
    questao.enunciado = payload.enunciado
    questao.save()

    alternativas_existentes = {a.id: a for a in questao.alternativas.all()}

    for alt_data in payload.alternativas:
        if alt_data.id:
            alt = alternativas_existentes.get(alt_data.id)
            if not alt:
                raise HttpError(404, f"Alternativa com id {alt_data.id} não pertence à questão")
            alt.texto = alt_data.texto
            alt.correta = alt_data.correta
            alt.save()
        else:
            Alternativa.objects.create(
                questao=questao,
                texto=alt_data.texto,
                correta=alt_data.correta
            )

    return {"message": "Questão atualizada com sucesso"}


@api.delete("admin/provas/{prova_id}/questoes/{questao_id}", auth=AuthBearer())
def deletar_questao(request, prova_id:int ,questao_id: int):
    if not request.auth.is_admin():
        raise HttpError(403, "Apenas admins podem deletar questões.")

    questao = get_object_or_404(Questao, id=questao_id)
    questao.delete()

    return {"message": "Questão deletada com sucesso"}

################ Modulo Admin Alternativas (Editar e Deletar)

@api.put("/admin/provas/{prova_id}/questoes/{questao_id}/alternativas/{alternativa_id}", auth=AuthBearer())
def editar_alternativas(
    request,
    prova_id: int,
    questao_id: int,
    alternativa_id: int,
    payload: AlternativaUpdateSchema
):
    if not request.auth.is_admin():
        raise HttpError(403, "Apenas admins podem editar alternativas.")

    prova = get_object_or_404(Prova, id=prova_id)
    questao = get_object_or_404(Questao, id=questao_id, prova=prova)

    alternativa = get_object_or_404(Alternativa, id=alternativa_id, questao=questao)

    alternativa.texto = payload.texto
    alternativa.correta = payload.correta
    alternativa.save()

    return {
        "message": "Alternativa atualizada com sucesso.",
        "alternativa_id": alternativa.id
    }

@api.delete("/admin/provas/{prova_id}/questoes/{questao_id}/alternativas/{alternativa_id}", auth=AuthBearer())
def deletar_alternativa(request, prova_id:int,questao_id:int,alternativa_id: int):
    if not request.auth.is_admin():
        raise HttpError(403, "Apenas admins podem deletar alternativas.")

    alternativa = get_object_or_404(Alternativa, id=alternativa_id)
    alternativa.delete()

    return {"message": "Alternativa deletada com sucesso"}

################ Modulo Participante Dashboard

@api.get("/participante/dashboard", auth=AuthBearer())
def dashboard_participante(request):
    user = request.auth

    if not user.is_authenticated or user.role != "PARTICIPANTE":
        raise HttpError(403, "Acesso restrito a participantes")

    provas_participante = (
        user.provas.select_related("prova")
        .prefetch_related("prova__questoes__alternativas")
        .all()
    )

    provas = []

    for pp in provas_participante:
        prova = pp.prova
        questoes_data = []

        for questao in prova.questoes.all():
            alternativas_data = [
                {
                    "id": alt.id,
                    "texto": alt.texto
                }
                for alt in questao.alternativas.all()
            ]

            questoes_data.append({
                "id": questao.id,
                "enunciado": questao.enunciado,
                "alternativas": alternativas_data
            })

        provas.append({
            "id": prova.id,
            "titulo": prova.titulo,
            "descricao": prova.descricao,
            "respondida": pp.respondida,
            "score": pp.score,
            "questoes": questoes_data
        })

    return {
        "message": f"Olá {user.username}",
        "provas_atribuidas": provas
    }

############### Modulo Participante Responder Provas

@api.post("/participante/responder/{prova_id}", auth=AuthBearer())
def responder_prova(request,prova_id:int, payload: ResponderProvaSchema):
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
            # prova_atribuida=prova_participante,
            questao_id=resposta.questao_id,
            defaults={"alternativa_id": resposta.alternativa_id}
        )
        if obj.alternativa.correta:
            acertos += 1

    nota = round((acertos / total) * 100, 2)

    return {
        "message": "Respostas registradas e prova corrigida",
        "acertos": acertos,
        "total_questoes": total,
        "nota_percentual": nota
    }

@api.put("participante/editar/{prova_id}", auth=AuthBearer())
def editar_respostas(request, prova_id: int, payload: ResponderProvaSchema):
    usuario = request.auth

    if request.auth.role != "PARTICIPANTE":
        raise HttpError(403, "Apenas participantes podem editar respostas.")

    if prova_id != payload.prova_id:
        raise HttpError(400, "ID da prova no path e no corpo não coincidem.")

    prova = get_object_or_404(Prova, id=prova_id)

    Resposta.objects.filter(usuario=usuario, questao__prova=prova).delete()

    for r in payload.respostas:
        questao = get_object_or_404(Questao, id=r.questao_id, prova=prova)
        alternativa = get_object_or_404(Alternativa, id=r.alternativa_id, questao=questao)

        Resposta.objects.create(
            usuario=usuario,
            questao=questao,
            alternativa=alternativa
        )

    respostas = Resposta.objects.filter(usuario=usuario, questao__prova=prova).select_related("alternativa")
    total_questoes = Questao.objects.filter(prova=prova).count()
    acertos = sum(1 for r in respostas if r.alternativa.correta)
    nota_percentual = (acertos / total_questoes) * 100 if total_questoes > 0 else 0.0


    return {
        "message": "Respostas editadas com sucesso",
        "acertos": acertos,
        "total_questoes": total_questoes,
        "nota_percentual": nota_percentual
    }

################ Modulo Admin Ranking

@api.get("/admin/ranking/{prova_id}", auth=AuthBearer())
def ranking_por_prova(request, prova_id: int):
    if not request.auth.is_admin():
        raise HttpError(403, "Apenas administradores podem acessar o ranking")

    participantes = ProvaParticipante.objects.filter(
        prova_id=prova_id
    ).select_related("participante")

    ranking = []

    for pp in participantes:
        respostas = Resposta.objects.filter(
            usuario=pp.participante,
            questao__prova_id=prova_id
        ).select_related("alternativa")

        total = respostas.count()
        acertos = sum(1 for r in respostas if r.alternativa and r.alternativa.correta)

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



