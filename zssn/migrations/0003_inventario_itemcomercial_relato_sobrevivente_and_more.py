# Generated by Django 4.2 on 2023-04-07 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zssn', '0002_rename_tickets_ticket_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quant', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ItemComercial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('pontos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Relato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sobrevivente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=10, null=True)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=10, null=True)),
                ('infectado', models.DateTimeField(null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
        migrations.AddField(
            model_name='relato',
            name='relatado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relatado', to='zssn.sobrevivente'),
        ),
        migrations.AddField(
            model_name='relato',
            name='relator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relator', to='zssn.sobrevivente'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='dono',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zssn.sobrevivente'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zssn.itemcomercial'),
        ),
        migrations.AddConstraint(
            model_name='relato',
            constraint=models.UniqueConstraint(fields=('relator', 'relatado'), name='unique_relator_relatado'),
        ),
        migrations.AddConstraint(
            model_name='inventario',
            constraint=models.UniqueConstraint(fields=('dono', 'item'), name='unique_dono_item'),
        ),
    ]