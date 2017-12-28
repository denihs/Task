from django.db import models

class User(models.Model):
    email = models.CharField(max_length = 200)
    username = models.CharField(max_length = 200)
    password = models.CharField(max_length = 50)

    def __str__(self):
        return self.username

class Task(models.Model):
    id_user = models.ForeignKey(User, on_delete = models.CASCADE)
    nome = models.CharField(max_length = 50)
    descricao = models.TextField()
    prazo = models.CharField(max_length = 50)
    prioridade = models.IntegerField()
    concluida = models.IntegerField()

    def __str__(self):
        return self.nome
