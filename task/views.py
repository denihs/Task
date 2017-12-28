from django.shortcuts import render
from django.shortcuts import redirect
from .models import User, Task

#Trata da view da lista de usuarios
def index(request):
    user = User.objects.all()
    return render(request, 'task/index.html', {'user':user})
#View da lista de tarefas
def tarefas(request, pk):
    user = User.objects.get(pk = pk)
    tarefas = user.task_set.all()
    return render(request, 'task/tarefas.html', {'tarefas': tarefas, 'id': pk})

#Função que valida o formulario
# ==================== TRATA DO FORMULARIO = CRIAÇÃO DE UMA NOVA TAREFA -================================
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

def cadastrarFormulario(request, pk):
    user = User.objects.get(pk = pk)

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
            return formulario(request, pk, is_valid(request, pk)['error'], campos)

        user.task_set.create(nome = request.POST['tarefa'],
                                descricao = request.POST['descricao'],
                                prazo = request.POST['prazo'],
                                prioridade = int(request.POST['prioridade']),
                                concluida = int(request.POST['concluida'])
                            )

    return redirect('task:tarefas', pk = pk)


#Gerencia o formulario
def formulario(request, pk, error = '', campos = {'tarefa':'', 'desc': '', 'prazo': '', 'prio':'1', 'conc':'0'}, action = 'task:cadastrarFormulario', button = 'Nova Tarefa'):

        return render(request, 'task/formulario.html', { 'id': pk, 'error': error, 'campos': campos, 'action' : action, 'button': button})

# ==================== TRATA DOS DETALHES DE UMA TAREFA -================================

def salvarEdicaoDados(request, pk):
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

def editarDados(request, pk):
    tarefa = Task.objects.get(pk = pk)
    print("\n\n{}\n\n".format(tarefa.prioridade))
    campos = {
        'tarefa': tarefa.nome,
        'desc':   tarefa.descricao,
        'prazo':  tarefa.prazo,
        'prio':   str(tarefa.prioridade),
        'conc':   str(tarefa.concluida),
    }
    return formulario(request = request, pk = pk, campos = campos, action = 'task:salvarEdicaoDados', button = 'Salvar Edição')

def detail(request, pk):
    tarefa = Task.objects.get(pk = pk)
    return render(request, 'task/detail.html', {'tarefa': tarefa, 'id':pk})

# ==================== TRATA DAS REMOÇÕES -================================

def exclusaoDefinitiva(request, pk):
    tarefa = Task.objects.get(pk = pk)
    id = tarefa.id_user.id
    tarefa.delete()
    return redirect('task:tarefas', pk = id)

def remover(request, pk):
    tarefa = Task.objects.get(pk = pk)
    return render(request, 'task/exclusao.html', {'tarefa': tarefa, 'id': pk})
