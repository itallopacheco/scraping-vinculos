from django.db import models

# Create your models here.

class Profissional(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    nome = models.CharField(max_length=100)
    cns = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.nome + ' - ' + self.cpf + ' - ' + self.cns


class Vinculo(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    competencia = models.CharField(max_length=7)
    ibge = models.CharField(max_length=7)
    uf = models.CharField(max_length=2)
    municipio = models.CharField(max_length=50)
    cbo = models.CharField(max_length=100)
    cnes = models.CharField(max_length=7)
    cnpj = models.CharField(max_length=14)
    estabelecimento = models.CharField(max_length=100)
    nat_juridica = models.CharField(max_length=100)
    gestao = models.CharField(max_length=1)
    sus = models.CharField(max_length=3)
    vinculo_estabelecimento = models.CharField(max_length=100)
    vinculo_empregador = models.CharField(max_length=100)
    detalhamento_vinculo = models.CharField(max_length=100)
    ch_outros = models.IntegerField(null=True, blank=True)
    ch_ambulatorial = models.IntegerField(null=True, blank=True)
    ch_hospitalar = models.IntegerField(null=True, blank=True)
    ch_total = models.IntegerField(null=True, blank=True)
    residente = models.CharField(max_length=3)
    preceptor = models.CharField(max_length=3)
    desligamento = models.CharField(max_length=3)

    def __str__(self):
        return self.profissional.nome + ' - ' + self.competencia + ' - ' + self.cnes + ' - ' + self.cbo



