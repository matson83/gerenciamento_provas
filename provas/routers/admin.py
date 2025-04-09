from ninja import Router, Schema
from typing import List
from ..models import Prova, Questao, Alternativa, ProvaParticipante
from django.shortcuts import get_object_or_404
from accounts.auth import AuthBearer

router = Router(tags=["Admin"])
