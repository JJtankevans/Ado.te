# Generated by Django 4.1.5 on 2023-01-16 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('divulgar', '0002_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('estado', models.CharField(max_length=80)),
                ('cidade', models.CharField(max_length=80)),
                ('telefone', models.CharField(max_length=14)),
                ('status', models.CharField(choices=[('P', 'Para adoção'), ('A', 'Adotado')], max_length=1)),
                ('foto', models.ImageField(upload_to='fotos_pets')),
                ('raca', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='divulgar.raca')),
                ('tags', models.ManyToManyField(to='divulgar.tag')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
