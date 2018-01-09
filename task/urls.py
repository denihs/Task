from django.conf.urls import url
from django.conf.urls import include
from . import views

app_name = 'task'

urlpatterns = [
    #Url da pagina pessoal
    url(r'^Denilson/$', views.pessoal, name = 'pessoal'),

    #URLS que trata basicamente do login
    url(r'^$', views.index, name = 'index'),
    url(r'^login/$', views.login, name = "login"),
    url(r'^cadastrar/$', views.cadastrar, name = "cadastrar"),
    url(r'^desogar/$', views.deslogar, name = "deslogar"),

    #Urls para recuperação de senhas
    url(r'^esqueciminhasenha/$', views.recoverSenha, name = "recoverSenha"),
    url(r'^validarCodigo/$', views.validarCodigo, name = "validarCodigo"),
    url(r'^esqueciMinhaSenha/verificarCodigo/$', views.verificarCodigo, name = "verificarCodigo"),
    url(r'^esqueciMinhaSenha/verificarCodigo/novaSenha/$', views.novasenha, name = "novasenha"),

    #url do perfil do usuario
    url(r'^perfil/$', views.perfil, name = "perfil"),
    url(r'^trocarSenha/$', views.trocarSenha, name = "trocarSenha"),
    url(r'^validaNovaSenha/trocarSenha/$', views.validaNovaSenha, name = "validaNovaSenha"),

    #url que mostra todas as tarefas
    url(r'^tarefas/$', views.tarefas, name ='tarefas' ),

    #url do formulario
    url(r'^tarefa-edit/$', views.formulario, name = 'formulario'),

    #url do cadastro de formulario, onde se faz a validação do formulario
    url(r'^errorUpdate/$', views.cadastrarFormulario, name = 'cadastrarFormulario'),

    #urls que mostram e termitem edição de tarefa
    url(r'^detalhes/(?P<pk>[0-9a-f-]+)/$', views.detail, name = "detail"),
    url(r'^detalhes/editarDados/(?P<pk>[0-9a-f-]+)/$', views.editarDados, name = "editarDados"),
    url(r'^salvarEdicaoDados/(?P<pk>[0-9a-f-]+)/$', views.salvarEdicaoDados, name = "salvarEdicaoDados"),

    #Urls que controlam a exclusão de uma tarefa
    url(r'^exclusaoDefinitiva/(?P<pk>[0-9a-f-]+)/$', views.exclusaoDefinitiva, name = "exclusaoDefinitiva"),

    #Urls que controlam a exclusão de uma tarefa
    url(r'^perfil/mudarImagemPerfil$', views.mudarImagemPerfil, name = 'mudarImagemPerfil')
]
