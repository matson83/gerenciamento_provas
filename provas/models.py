from django.db import models
from django.conf import settings

class Prova(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    criada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

class Questao(models.Model):
    prova = models.ForeignKey(Prova, related_name="questoes", on_delete=models.CASCADE)
    enunciado = models.TextField()

class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, related_name="alternativas", on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    correta = models.BooleanField(default=False)


class ProvaParticipante(models.Model):
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    participante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    respondida = models.BooleanField(default=False)

    class Meta:
        unique_together = ('prova', 'participante')


class Resposta(models.Model):
    prova_atribuida = models.ForeignKey(ProvaParticipante, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    alternativa_escolhida = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
