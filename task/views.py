from django.shortcuts import render
from django.shortcuts import redirect
from .models import Task
from .models import Perfil

from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout

from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template

from random import randint



def pessoal(request):
    return render(request, "task/Denilson.html")

#Função que verifica se tem usuario logado no sistema
def user_log(request):
    if not request.user.is_authenticated:
        return redirect('task:index')

#View da lista de tarefas
def tarefas(request):
    user = User.objects.get(email = request.user.email)
    tarefas = user.task_set.all().order_by("-date")
    return render(request, 'task/tarefas/tarefas.html', {'tarefas': tarefas, 'id': user.id})

# ==================== TRATA DOS USUARIOS = LOGIN/CADASTRO -================================
#Renderiza o template inicioal da pagina
def index(request, erro = "", campos = {"username": "", "email": "", "password": "", "first_name": "", "last_name": "", "passwordAgain":""} ):
    if request.user.is_authenticated:
        return redirect('task:tarefas')
    return render(request, 'task/index.html', {"erro": erro, "campos":campos} )

#Responsavel pelo login do usuario
@require_POST
def login(request, trocarSenha = 0):
    try:
        if trocarSenha == 0:#Se for diferente de zero significa que o user trocou de senha, então refazemos o login de forma automatica
            user = User.objects.get(email=request.POST['email'])
        else:
            user = User.objects.get(username = request.user)#Caso seja uma troca de senha
    except User.DoesNotExist:
        try:
            user = User.objects.get(username=request.POST['email'])
        except:
            return index(request = request, erro = "Email ou senha inválida")

    autentic = authenticate(request, username=user.username, password=request.POST["password"])
    if autentic is not None:
        auth_login(request, autentic)
        if trocarSenha == 0:
            return redirect('task:tarefas')
        else:
            return redirect('task:perfil')#Caso seja uma troca de senha retornamos para o perfil
    return index(request = request, erro = "Email ou senha inválida")

#Faz as devidas validações e depois, se tudo okay, insere o novo user
@require_POST
def cadastrar(request):
    #Verifica se ja existe o usuario no sistema
    try:
        user = User.objects.get(username = request.POST['username'])
        if user:
            return retornarCadastro(request = request, erro = "Username já em uso")
    except User.DoesNotExist:
        try:
            user = User.objects.get(email = request.POST['email'])
            if user:
                return retornarCadastro(request = request, erro = "Email já cadastrado")
        except User.DoesNotExist:

            if not validacaoCadastro(request)['resposta']:
                return retornarCadastro(request, validacaoCadastro(request)['error'])

            novoUsuario = User.objects.create_user(
                username = request.POST['username'],
                email = request.POST['email'],
                password = request.POST['password'].strip(),
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
            )
            novoUsuario.save()
            return login(request)
#Faz uma simples validação nos campos de senha e usuario
def validacaoCadastro(request):
    if request.POST['password'] != request.POST['passwordAgain']:
        return ({"resposta": False, "error": "As senhas não são iguais!"} )

    if request.POST['password'].strip() == '' or len(request.POST['password'].strip()) < 8:
        return ({"resposta": False, "error": "Senha deve conter 8 ou mais caracteres"} )

    if request.POST['username'].strip() == '':
        return ({"resposta": False, "error": "Username é obrigatório"} )


    return ({"resposta": True, "error": ""} )
#Quando ocorre erro no cadastro de um usuario, recuperamos os dados ja inseridos
def retornarCadastro(request, erro):
    campos = {
        "username": request.POST['username'],
        "email": request.POST['email'],
        "password": request.POST['password'],
        "first_name": request.POST['first_name'],
        "last_name": request.POST['last_name'],
        "passwordAgain": request.POST['passwordAgain'],
    }
    return index(request = request, erro = erro, campos = campos)
#Deloga o usuario
@login_required
def deslogar(request):
    logout(request)
    return redirect('task:index')

# ==================== TRATA DOS USUARIOS = RECUPEÇÃO DE SENHA -================================
#Renderiza a templete de recuperação de senhas
def recoverSenha(request, erro = ''):
    return render(request, 'task/recuperacaoSenha/recuperarSenha.html', {'erro': erro})

#Função que vai gerar um codigo e enviar por email para o user
@require_POST
def validarCodigo(request, erro = '', verificarCodigo = 0):
    if verificarCodigo == 0:#Se for diferente de zero significa que o codigo foi inserido errado
        try:
            user = User.objects.get(email = request.POST['email_username'])
        except:
            try:
                user = User.objects.get(username = request.POST['email_username'])
            except:
                return recoverSenha(request = request, erro = "Email ou Username não encontrado")

        global codigo_recupecao_senha
        global old_request

        codigo_recupecao_senha = randint(100000, 999999)#Gera Codigo
        old_request = request #Salva o request para quando a senha for trocada redirecionarmos o usuario

        subject = "Recuperação de senha"
        to = [user.email]
        from_email = 'lembreme.assitente@gmail.com'
        ctx = {
            'user': user,
            'codigo': codigo_recupecao_senha,
        }
        message = get_template('task/mail/mail.html').render(ctx)
        msg = EmailMessage(subject, message, to=to, from_email = from_email)
        msg.content_subtype = 'html'
        msg.send()

    return render(request, 'task/recuperacaoSenha/verificarCodigo.html', {'erro': erro})

#verificação do codigo que foi enviado por email
@require_POST
def verificarCodigo(request, erro = '', novasenha = 0):

    if novasenha == 0:#Quando diferente de zero significa que houve na inserção da nova senha
        try:
            int( request.POST['codigo'].strip() )
        except:
            return validarCodigo(request = request, erro = 'Favor insira o codigo', verificarCodigo = 1)
        else:
            if  codigo_recupecao_senha != int(request.POST['codigo']):
                return validarCodigo(request = request, erro = 'Codigo invalido', verificarCodigo = 1)
            else:
                global old_request
                try:
                    user = User.objects.get(email = old_request.POST['email_username'])
                except:
                    try:
                        user = User.objects.get(username = old_request.POST['email_username'])
                    except:
                        user = ''
                return render(request, 'task/recuperacaoSenha/novasenha.html', {'user': user, 'erro': erro})
    return render(request, 'task/recuperacaoSenha/novasenha.html', { 'erro': erro})

#Faz uma radida verificação da senha e depois muda ela no basco
@require_POST
def novasenha(request):
    if request.POST['password'] != request.POST['passwordAgain']:
        return verificarCodigo(request = request, erro = 'As senhas informadas não são iguais', novasenha = 1)

    if request.POST['password'].strip() == '' or len(request.POST['password'].strip()) < 8:
        return verificarCodigo(request = request, erro = "Senha deve conter 8 ou mais caracteres", novasenha = 1)

    global old_request

    try:
        user = User.objects.get(email = old_request.POST['email_username'])
    except:
        try:
            user = User.objects.get(username = old_request.POST['email_username'])
        except:
            user = ''
    user.set_password(request.POST['password'])
    user.save()
    return index(request=request, erro = "Senha alterada com sucesso")


# ==================== TRATA DO PERFIL DOS USUARIOS -================================
#Renderiza o templete do perfil
@login_required
def perfil(request):
    user = User.objects.get(username = request.user)
    try:
        avatar = Perfil.objects.get(id_user_id = user.id)
    except:
        avatar = ''
    return render(request, 'task/perfil/perfil.html', {"user":user, "avatar": avatar})
#Renderiza o template para a troca de senha
def trocarSenha(request, erro = ''):
    return render(request,'task/perfil/trocarSenha.html', {'error': erro})

#Faz as validações para a troca de senha
@require_POST
def validaNovaSenha(request):
    user =  authenticate(request, username=request.user, password=request.POST["senha_atual"])
    if user != None:
        if request.POST['password'] != request.POST['passwordAgain']:
            return trocarSenha(request = request, erro = 'As senhas informadas não são iguais')

        if request.POST['password'].strip() == '' or len(request.POST['password'].strip()) < 8:
            return trocarSenha(request = request, erro = "Senha deve conter 8 ou mais caracteres")
        user.set_password(request.POST['password'])
        user.save()
        return login(request = request, trocarSenha = 1)
    return trocarSenha(request = request, erro = "Senha atual invalida")

@require_POST
def mudarImagemPerfil(request):
    # print("%"*50)
    # print(request.FILES)
    # print("=-"*30)
    try:
        avatar = Perfil.objects.get(id_user_id = request.user.id)
        avatar.image = request.FILES["image_avatar"]
        avatar.save();
    except Perfil.DoesNotExist:
        user = request.user
        user.perfil_set.create(image=request.FILES["image_avatar"], id_user_id=user.id)
    return redirect('task:perfil')
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

#Trata da inserção de uma nova tarefa
@login_required
def cadastrarFormulario(request):
    user_log(request)
    user = User.objects.get(pk = request.user.id)

    if request.method == 'POST':
        pk = user.id
        if not is_valid(request, pk)['valid']:
            #Recuperação dos dados ja digitados para o caso de existir algum dado invalido
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

            return formulario(request = request, error =  is_valid(request, pk)['error'],campos = campos)

        user.task_set.create(nome = request.POST['tarefa'],
                                descricao = request.POST['descricao'],
                                prazo = request.POST['prazo'],
                                prioridade = int(request.POST['prioridade']),
                                concluida = int(request.POST['concluida'])
                            )
    return redirect('task:tarefas')

#Renderiza o formulario de inserção de tarefas
@login_required
def formulario(request,pk = '', error = '', campos = {'tarefa':'', 'desc': '', 'prazo': '', 'prio':'1', 'conc':'0'}, action = 'task:cadastrarFormulario', button = 'Nova Tarefa'):
    user_log(request)
    return render(request, 'task/tarefas/formulario.html', { 'id': pk, 'error': error, 'campos': campos, 'action' : action, 'button': button})


# ==================== TRATA DOS DETALHES DE UMA TAREFA -================================
#Responsavel pelos dados que vão ser editados
@login_required
def salvarEdicaoDados(request, pk):
    user_log(request)
    tarefa = Task.objects.get(pk = pk)

    if request.method == 'POST':
        #Recuperação dos dados ja digitados caso existir algum dado invalido
        if not is_valid(request, pk)['valid']:
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
            return formulario(request = request, pk = pk,error = is_valid(request, pk)['error'],campos =  campos, action = 'task:salvarEdicaoDados', button = 'Salvar Edição')
    #Editando e salvando as mudanças no banco
    tarefa.nome = request.POST['tarefa']
    tarefa.descricao = request.POST['descricao']
    tarefa.prazo = request.POST['prazo']
    tarefa.prioridade = int(request.POST['prioridade'])
    tarefa.concluida = int(request.POST['concluida'])
    tarefa.save()

    return redirect('task:detail', pk = pk)

#Recupera os dados do banco para passa-los no formulario
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

#Renderiza uma tarefa em detalhes
@login_required
def detail(request, pk):
    user_log(request)
    tarefa = Task.objects.get(pk = pk)
    return render(request, 'task/tarefas/detail.html', {'tarefa': tarefa, 'id':pk})

# ==================== TRATA DAS REMOÇÕES -================================
#Remove uma tarefa do banco
@login_required
def exclusaoDefinitiva(request, pk):
    user_log(request)

    tarefa = Task.objects.get(pk = pk)
    id = tarefa.id_user.id
    tarefa.delete()
    return redirect('task:tarefas')


#=========================== VARIAVEIS =================================
codigo_recupecao_senha = ''
old_request = ''
