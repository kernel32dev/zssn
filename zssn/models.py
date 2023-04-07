from django.db import models

# uma model hello world para testar o banco
class Ticket(models.Model):
    name = models.CharField(max_length=100)
