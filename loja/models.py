from django.db import models
from django.contrib.auth.models import User

class Mensagem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.texto[:20]}"
