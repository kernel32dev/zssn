from django.db import models

class Sobrevivente(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]
    nome = models.CharField(name='nome', max_length=100)
    sexo = models.CharField(name='sexo', max_length=1, choices=SEXO_CHOICES)
    latitude = models.DecimalField(name='latitude', null=True, max_digits=10, decimal_places=6)
    longitude = models.DecimalField(name='longitude', null=True, max_digits=10, decimal_places=6)
    infectado = models.DateTimeField(name='infectado', null=True)
    def __str__(self):
        return f"Sobrevivente(nome = {self.nome}, sexo = {self.sexo}, latitude = {self.latitude}, longitude = {self.longitude}, infectado = {self.infectado})"

# o registro do tipo de item, permitindo com que um admin adicione novos tipos de itens
class ItemComercial(models.Model):
    nome = models.CharField(max_length=100)
    pontos = models.IntegerField()
    def __str__(self):
        return f"ItemComercial(nome = {self.nome}, pontos = {self.pontos})"

# relatos de sobreviventes de que um outro sobrevivente esta infectado
class Relato(models.Model):
    relator = models.ForeignKey(Sobrevivente, name='relator', related_name='relator', on_delete=models.CASCADE)
    relatado = models.ForeignKey(Sobrevivente, name='relatado', related_name='relatado', on_delete=models.CASCADE)
    data = models.DateTimeField(name='data', auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['relator', 'relatado'], name='unique_relator_relatado'
            )
        ]
    def __str__(self):
        return f"Relato(relator = {self.relator} ({self.relator.nome}), relatado = {self.relatado} ({self.relatado.nome}), data = {self.data})"

# um registro que indica quanto de um item o sobrevivente tem
class Inventario(models.Model):
    dono = models.ForeignKey(Sobrevivente, name='dono', on_delete=models.CASCADE)
    item = models.ForeignKey(ItemComercial, name='item', on_delete=models.CASCADE)
    quant = models.IntegerField(name='quant')
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['dono', 'item'], name='unique_dono_item'
            )
        ]
    def __str__(self):
        return f"Inventario(dono = {self.dono} ({self.dono.nome}), item = {self.item} ({self.item.nome}), quant = {self.quant})"
