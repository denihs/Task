from django.shortcuts import render
from django.shortcuts import redirect
from .models import Task

from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
#Função que verifica se tem usuario logado no sistema
def user_log(request):
    if not request.user.is_authenticated:
        return redirect('task:index')
#View da lista de tarefas
def tarefas(request):
    user = User.objects.get(username = request.user)
    tarefas = user.task_set.all()
    return render(request, 'task/tarefas.html', {'tarefas': tarefas, 'id': user.id})

# ==================== TRATA DOS USUARIOS -================================
#Trata da view da lista de usuarios
def index(request):
    if request.user.is_authenticated:
        return redirect('task:tarefas')
    return render(request, 'task/index.html')

#Responsavel pelo login do usuario
@require_POST
def login(request):
    try:
        user = User.objects.get(email=request.POST['email'])
    except:
        return redirect('task:index')
    else:
        autentic = authenticate(request, username=user.username, password=request.POST["password"])
        if autentic is not None:
            auth_login(request, autentic)
            return redirect('task:tarefas')

        return redirect('task:index')

@login_required
def deslogar(request):
    logout(request)
    return redirect('task:index')
# ==================== TRATA DO FORMULARIO = CRIAÇÃO DE UMA NOVA TAREFA -================================
#Função que valida o formulario
def is_valid(request, pk):

    if request.POST['tarefa'].strip() == "":
        return {'valid': False, 'error': 'O nome da tarefa é obrigatório'};

    if len(request.POST['tarefa']) > 50:
        return {'valid': False, 'error': 'O nome deve ter no maximo 50 caracteres'};

    if len(request.POST['prazo']) > 50:
        return {'valid': False, 'error': 'O prazo deve ter no maximo 50 caracteres'};

    if not "concluida" in request.POST:
        request.POST = request.POST.copy()
        request.POST['concluida'] = 0

    return {'valid': True, 'error': ''};
@login_required
def cadastrarFormulario(request):
    user_log(request)
    user = User.objects.get(pk = request.user.id)

    if request.method == 'POST':
        pk = user.id
        if not is_valid(request, pk)['valid']:
            #Recuperação dos dados ja digitados
            if not "concluida" in request.POST:
                request.POST = request.POST.copy()
                request.POST['concluida'] = 0

            campos = {
                'tarefa': request.POST['tarefa'],
                'desc':   request.POST['descricao'],
                'prazo':  request.POST['prazo'],
                'prio':   request.POST['prioridade'],
                'conc':   request.POST['concluida'],
            }
            return formulario(request, is_valid(request, pk)['error'], campos)

        user.task_set.create(nome = request.POST['tarefa'],
                                descricao = request.POST['descricao'],
                                prazo = request.POST['prazo'],
                                prioridade = int(request.POST['prioridade']),
                                concluida = int(request.POST['concluida'])
                            )
    return redirect('task:tarefas')
@login_required
#Gerencia o formulario
def formulario(request,pk = '', error = '', campos = {'tarefa':'', 'desc': '', 'prazo': '', 'prio':'1', 'conc':'0'}, action = 'task:cadastrarFormulario', button = 'Nova Tarefa'):
    user_log(request)
    return render(request, 'task/formulario.html', { 'id': pk, 'error': error, 'campos': campos, 'action' : action, 'button': button})


# ==================== TRATA DOS DETALHES DE UMA TAREFA -================================
@login_required
def salvarEdicaoDados(request, pk):
    user_log(request)
    tarefa = Task.objects.get(pk = pk)

    if request.method == 'POST':
        if not is_valid(request, pk)['valid']:
            #Recuperação dos dados ja digitados
            if not "concluida" in request.POST:
                request.POST = request.POST.copy()
                request.POST['concluida'] = 0

            campos = {
                'tarefa': request.POST['tarefa'],
                'desc':   request.POST['descricao'],
                'prazo':  request.POST['prazo'],
                'prio':   request.POST['prioridade'],
                'conc':   request.POST['concluida'],
            }
            return formulario(request, pk, is_valid(request, pk)['error'], campos, action = 'task:salvarEdicaoDados', button = 'Salvar Edição')

    tarefa.nome = request.POST['tarefa']
    tarefa.descricao = request.POST['descricao']
    tarefa.prazo = request.POST['prazo']
    tarefa.prioridade = int(request.POST['prioridade'])
    tarefa.concluida = int(request.POST['concluida'])
    tarefa.save()

    return redirect('task:detail', pk = pk)
@login_required
def editarDados(request, pk):
    user_log(request)
    tarefa = Task.objects.get(pk = pk)
    campos = {
        'tarefa': tarefa.nome,
        'desc':   tarefa.descricao,
        'prazo':  tarefa.prazo,
        'prio':   str(tarefa.prioridade),
        'conc':   str(tarefa.concluida),
    }
    return formulario(request = request, pk = tarefa.id, campos = campos, action = 'task:salvarEdicaoDados', button = 'Salvar Edição')
@login_required
def detail(request, pk):
    user_log(request)
    tarefa = Task.objects.get(pk = pk)
    return render(request, 'task/detail.html', {'tarefa': tarefa, 'id':pk})

# ==================== TRATA DAS REMOÇÕES -================================
@login_required
def exclusaoDefinitiva(request, pk):
    user_log(request)

    tarefa = Task.objects.get(pk = pk)
    id = tarefa.id_user.id
    tarefa.delete()
    return redirect('task:tarefas')
@login_required
def remover(request, pk):
    user_log(request)
    tarefa = Task.objects.get(pk = pk)
    return render(request, 'task/exclusao.html', {'tarefa': tarefa, 'id': pk})
