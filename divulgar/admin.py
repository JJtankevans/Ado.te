from django.contrib import admin
from .models import Raca,Tag,Pet

# Register your models here.

"""Essa linha adiciona a model(tabela) como "dominio" do superadmin
ser possivel ela ser editada pelos super usuarios"""
admin.site.register(Raca)
admin.site.register(Tag)
admin.site.register(Pet)