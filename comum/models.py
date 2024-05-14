from django.db import models

# Create your models here.

class Profissional(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    nome = models.CharField(max_length=100)
    cns = models.CharField(max_length=15)

    def __str__(self):
        return self.nome + ' - ' + self.cpf + ' - ' + self.cns


class Vinculo(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    competencia = models.CharField(max_length=7)
    cbo = models.CharField(max_length=100)
    cnes = models.CharField(max_length=7)


    def __str__(self):
        return self.profissional.nome + ' - ' + self.competencia + ' - ' + self.cnes + ' - ' + self.cbo



