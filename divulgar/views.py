from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Tag,Raca,Pet
from adotar.models import PedidoAdocao
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

import re

from django.http import HttpResponse


# Create your views here.
@login_required
def novo_pet(request):


    if request.method == "GET":
        tags = Tag.objects.all()
        racas =  Raca.objects.all()
        return render(request, 'novo_pet.html', {'tags': tags, 'racas': racas})
    elif request.method == "POST":

        #Prestar atenção na captura de dado abaixo
        foto = request.FILES.get("foto")
    
        nome = request.POST.get("nome")
        descricao = request.POST.get("descricao")
        es = request.POST.get("estado")
        cd = request.POST.get("cidade")
        fone = request.POST.get("telefone")

        #Prestar atenção na captura de dado abaixo
        tags_list = request.POST.getlist("tags")
        raca = request.POST.get("raca")

        # VALIDAÇÃO DOS DADOS DE MANEIRA BEM SIMPLISTA
        if(len(nome.strip()) == 0 or len(descricao.strip()) == 0 or len(es.strip()) == 0 or len(cd.strip()) == 0 or len(fone.strip()) == 0):
            tags = Tag.objects.all()
            racas =  Raca.objects.all()
            
            messages.add_message(request, constants.WARNING, "Preencha todos os campos por favor!")
            return render(request, "novo_pet.html",{'tags': tags, 'racas': racas})
        
        # VALIDAÇÃO DO NUMERO DE TELEFON
        fone_pattern = ("^\([1-9]{2}\)(?:[2-8]|[1-9])[0-9]{8}$")
        resposta = re.search(fone_pattern, fone.strip())
        if(not resposta):
            tags = Tag.objects.all()
            racas =  Raca.objects.all()
            messages.add_message(request, constants.INFO, "O numero de telefone está preenchido errado por favor preencha no seguinte padrão (XX)XXXXXXXXX")
            return render(request, "novo_pet.html",{'tags': tags, 'racas': racas})

        # VALIDAÇÃO DO ARQUIVO DE FOTO AINDA PRECISA SER FEITA !!
        
        """Cria um um objeto do models Pet e passa as infos para ele
        vale ressaltar q o usuário já é passado dentro da request """
        try:
            pet = Pet(
                usuario = request.user,
                nome = nome,
                descricao = descricao,
                estado = es,
                cidade = cd,
                telefone = fone,
                foto = foto,
                raca_id = raca
            )

            pet.save()
            """Isso aqui itera sobre a lista de tags vindas do formulário pega o id delas da tabela de TAG na linha 72
            em seguida adiciona na tabela PET no campo tag só q como é um ManyToMany o Django reconhece e insere na tabela
            que foi gerada para este relacionamento(pode-se verificar isso no arquivo do SQLite ali)"""
            for tag_id in tags_list:
                tag = Tag.objects.get(id=tag_id)
                pet.tags.add(tag)
        
            pet.save()
            tags = Tag.objects.all()
            racas =  Raca.objects.all()
            messages.add_message(request, constants.SUCCESS, "Pet adicionado com sucesso!")
            return render(request, 'novo_pet.html',{'tags': tags, 'racas': racas})
        except:
            messages.add_message(request, constants.ERROR, "Erro interno do sistema")
            return render(request, 'novo_pet.html',{'tags': tags, 'racas': racas})
        
    return HttpResponse("Funcionou")

@login_required
def seus_pets(request):

    if (request.method == "GET"):
        pets = Pet.objects.filter(usuario=request.user)
        return render(request,'seus_pets.html',{'pets':pets})

@login_required
def remover_pet(request,id):

    pet = Pet.objects.get(id=id)

    if not pet.usuario == request.user:
        messages.add_message(request,constants.ERROR, "Esse pet não é seu seu/sua safado(a)!")
        return redirect('/divulgar/seus_pets')

    pet.delete()
    messages.add_message(request,constants.SUCCESS, "Pet removido com sucesso!")
    return redirect('/divulgar/seus_pets')

def ver_pet(request, id):
    if request.method == "GET":
        chk_pedidos = PedidoAdocao.objects.filter(pet_id=id).filter(usuario_id=request.user).exclude(status="R").count()
        
        pet = Pet.objects.get(id = id)

        if chk_pedidos != 0:
            messages.add_message(request, constants.INFO, "Você já solictou adoção para este pet, por favor aguarde")
            return render(request,"ver_pet.html", {'pet': pet, 'pedido': 'feito'})

        return render(request, "ver_pet.html", {'pet': pet, 'pedido': 'recusado'})

def ver_pedido_adocao(request):
    if request.method=="GET":
        pedidos = PedidoAdocao.objects.exclude(usuario=request.user).filter(status="AG")
        
        if pedidos.count() == 0:
            messages.add_message(request,constants.INFO, "Seus pets não tem solicição de adoção :(")
            return render(request, "ver_pedido_adocao.html")
        
        return render(request, "ver_pedido_adocao.html", {'pedidos':pedidos})

def dashboard(request):
    if request.method == "GET":
        return render(request, 'dashboard.html')


@csrf_exempt
def api_adocoes_solicitadas_por_raca(request):
    racas = Raca.objects.all()

    qtd_adocoes = []
    qtde_adocoes_aceitas =[]
    for raca in racas:
        """Ele faz o filter por pet que é uma FK e dentro da tabela pet e
        dentro da tabela pet a coluna raca é uma FK para a tabela raca por isso
        ele usa os 2 underline para dizer pegue a coluna tal q leva a tal tabela
        e dessa tabela pegue tal coluna"""
        adocoes = PedidoAdocao.objects.filter(pet__raca=raca).count()
        adocoes_aceitas = PedidoAdocao.objects.filter(pet__raca=raca).filter(status="AP").count()
        qtd_adocoes.append(adocoes)
        qtde_adocoes_aceitas.append(adocoes_aceitas)

    racas = [raca.raca for raca in racas]
    data = {
        "adocoes_feitas": {
            'qtd_adocoes': qtd_adocoes,
            'labels': racas
        },
        "adocoes_aceitas": {
            "qtde_aceitas":qtde_adocoes_aceitas,
            'labels_aceitas':racas
        }
    }

    return JsonResponse(data)
