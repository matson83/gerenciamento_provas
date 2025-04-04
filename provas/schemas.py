from ninja import Schema
from typing import List

class AlternativaOut(Schema):
    id: int
    texto: str

class QuestaoOut(Schema):
    id: int
    enunciado: str
    alternativas: List[AlternativaOut]

class ProvaOut(Schema):
    id: int
    titulo: str
    descricao: str
    questoes: List[QuestaoOut]

class ProvaCreate(Schema):
    titulo: str
    descricao: str

class QuestaoCreate(Schema):
    enunciado: str
    alternativas: List[str]
    correta: int  # índice da alternativa correta

class RespostaCreate(Schema):
    questao_id: int
    alternativa_id: int

class AtribuirParticipantesSchema(Schema):
    prova_id: int
    participantes_ids: List[int]

class RespostaOut(Schema):
    questao_id: int
    enunciado: str
    alternativa_escolhida: str
    correta: bool

class RankingEntry(Schema):
    participante_id: int
    nome: str
    acertos: int
