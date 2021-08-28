from django.db import models


class Client(models.Model):
    """
    ORM para tabela Client
    """
    name = models.CharField(max_length=50)
    doc_id = models.CharField(max_length=12)

    def __str__(self):
        return self.name

