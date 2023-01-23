from django.shortcuts import render,redirect
from divulgar.models import Pet,Raca
from .models import PedidoAdocao
from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import send_mail
from datetime import datetime

# Create your views here.
def listar_pets(request):
    if request.method == "GET":
        #pega todos os pets que estão para adoção que não pertencem ao usuário que os cadastrou
        pets = Pet.objects.filter(status="P").exclude(usuario_id = request.user)
        racas = Raca.objects.all()


        cidade = request.GET.get('cidade')
        raca_filter = request.GET.get('raca')

        if cidade:
            pets = pets.filter(cidade__icontains=cidade)
        
        if raca_filter:
            pets = pets.filter(raca__id=raca_filter)
            raca_filter = Raca.objects.get(id=raca_filter)
        
        if cidade and raca_filter:
            pets =  pets.filter(cidade__icontains=cidade, raca_id=raca_filter)

        return render(request, 'listar_pets.html',{'pets':pets, 'racas': racas, 'cidade': cidade, 'raca_filter': raca_filter})

def pedido_adocao(request, id_pet):
    chk_user = Pet.objects.filter(usuario_id=request.user).filter(id=id_pet).count()

    if chk_user != 0:
        messages.add_message(request, constants.WARNING, "Você não pode adotar seu proprio pet!!!")
        return redirect('/adotar')
    
    """O filter retorna uma lista, mesmo usando o id para filtrar, já o get
    retorna a instÂncia do objeto em si por isso ali no else é necessário
    fazer o pet.first()"""
    pet = Pet.objects.filter(id=id_pet).filter(status="P")

    if not pet.exists():
        messages.add_message(request, constants.WARNING, "Esse pet já foi adotado :)")
        return redirect('/adotar')
    

    pedido = PedidoAdocao(pet=pet.first(),
        usuario=request.user,
        data=datetime.now()
    )

    pedido.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção realizado, você receberá um e-mail caso ele seja aprovado.')
    return redirect('/adotar')

def processa_pedido_adocao(request, id_pedido):
    status = request.GET.get('status')
    pedido = PedidoAdocao.objects.get(id=id_pedido)
    if status =="A":
        pedido.status = "AP"
        string = '''Olá, sua adoção foi aprovada. :)'''
    elif status =="R":
        pedido.status = "R"
        string = '''Olá, sua adoção foi recusada.'''
    
    pedido.save()
    if status == "A":
        pet = Pet.objects.get(id=pedido.pet_id)
        pet.status = "A"
        pet.save()

    print(pedido.usuario.email)
    email = send_mail(
        'Sua adoção foi processada', string, 'vitor@pythonando.com.br', [pedido.usuario.email,]
    )

    messages.add_message(request, constants.SUCCESS, "Pedido de adoção processado com sucesso")
    return redirect("/divulgar/ver_pedido_adocao")