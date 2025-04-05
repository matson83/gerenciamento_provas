from ninja import Router
from ninja_jwt.authentication import JWTAuth
from provas.models import Prova, ProvaParticipante
from provas.schemas import ProvaOut
from typing import List

router = Router(tags=["Participante"])

@router.get("/minhas", response=List[ProvaOut], auth=JWTAuth())
def minhas_provas(request):
    usuario = request.auth

    provas = Prova.objects.filter(provaparticipante__participante=usuario).prefetch_related("questoes__alternativas")

    return provas
