import uuid
from django.db import models

class Sobrevivente(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]
    nome = models.CharField(name='nome', max_length=100)
    sexo = models.CharField(name='sexo', max_length=1, choices=SEXO_CHOICES)
    latitude = models.DecimalField(name='latitude', null=True, blank=True, max_digits=10, decimal_places=6)
    longitude = models.DecimalField(name='longitude', null=True, blank=True, max_digits=10, decimal_places=6)
    infectado = models.DateTimeField(name='infectado', null=True, blank=True)
    # sha256 da senha concatenada com o sal
    senha = models.CharField(name='senha', max_length=64)
    sal = models.CharField(name='sal', max_length=16)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nome'], name='unique_nome'
            )
        ]
    def __str__(self):
        return f"Sobrevivente(nome = {self.nome}, sexo = {self.sexo}, latitude = {self.latitude}, longitude = {self.longitude}, infectado = {self.infectado})"
    def save(self, *args, **kwargs):
        if not self.latitude: self.latitude = None
        if not self.longitude: self.longitude = None
        if not self.infectado: self.infectado = None
        super(Sobrevivente, self).save(*args, **kwargs)

# o registro do tipo de item, permitindo com que um admin adicione novos tipos de itens
class ItemComercial(models.Model):
    nome = models.CharField(max_length=100)
    pontos = models.IntegerField()
    def __str__(self):
        return f"ItemComercial(nome = {self.nome}, pontos = {self.pontos})"

# relatos de sobreviventes de que um outro sobrevivente esta infectado
class Relato(models.Model):
    relator = models.ForeignKey(Sobrevivente, name='relator', null=True, related_name='relator', on_delete=models.SET_NULL)
    relatado = models.ForeignKey(Sobrevivente, name='relatado', related_name='relatado', on_delete=models.CASCADE)
    data = models.DateTimeField(name='data', auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['relator', 'relatado'], name='unique_relator_relatado'
            )
        ]
    def __str__(self):
        return f"Relato(relator = {self.relator}, relatado = {self.relatado}, data = {self.data})"

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
        return f"Inventario(dono = {self.dono}, item = {self.item}, quant = {self.quant})"

class Sessao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Sobrevivente, name='usuario', on_delete=models.CASCADE)
    validade = models.DateTimeField(name='validade')
    def __str__(self):
        return f"Sessao(usuario = {self.usuario}, validade = {self.validade})"

class Oferta(models.Model):
    vendedor = models.ForeignKey(Sobrevivente, name='vendedor', on_delete=models.CASCADE)
    def __str__(self):
        return f"Oferta(vendedor = {self.vendedor})"

class OfertaItem(models.Model):
    oferta = models.ForeignKey(Oferta, name='oferta', on_delete=models.CASCADE)
    item = models.ForeignKey(ItemComercial, name='item', on_delete=models.CASCADE)
    quant = models.IntegerField(name='quant')
    def __str__(self):
        return f"OfertaItem(oferta = {self.oferta}, item = {self.item}, quant = {self.quant})"
