# Generated by Django 4.2 on 2023-04-15 16:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_inventario_itemcomercial_relato_sobrevivente_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sessao',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('validade', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='sobrevivente',
            name='sal',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sobrevivente',
            name='senha',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sobrevivente',
            name='infectado',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sobrevivente',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='sobrevivente',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True),
        ),
        migrations.AddConstraint(
            model_name='sobrevivente',
            constraint=models.UniqueConstraint(fields=('nome',), name='unique_nome'),
        ),
        migrations.AddField(
            model_name='sessao',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.sobrevivente'),
        ),
    ]