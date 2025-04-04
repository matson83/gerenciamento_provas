from django.db import models
from django.conf import settings  # tem que vir antes de usar settings
# Remova a linha abaixo!
# from django.contrib.auth.models import User

class Prova(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    criada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participantes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="provas_designadas")

class Questao(models.Model):
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE, related_name="questoes")
    enunciado = models.TextField()

class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name="alternativas")
    texto = models.CharField(max_length=255)
    correta = models.BooleanField(default=False)

class Resposta(models.Model):
    participante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE)

    def esta_correta(self):
        return self.alternativa.correta
