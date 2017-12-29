from django.db import models
import uuid
from django.contrib.auth.models import User

class Task(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    id_user = models.ForeignKey(User, on_delete = models.CASCADE)
    nome = models.CharField(max_length = 50)
    descricao = models.TextField()
    prazo = models.CharField(max_length = 50)
    prioridade = models.IntegerField()
    concluida = models.IntegerField()

    def __str__(self):
        return self.nome
