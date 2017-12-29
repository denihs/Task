from django.conf.urls import url
from . import views

app_name = 'task'

urlpatterns = [
    #URLS que trata basicamente do login
    url(r'^$', views.index, name = 'index'),
    url(r'^login/$', views.login, name = "login"),
    url(r'^desogar/$', views.deslogar, name = "deslogar"),

    #url que mostra todas as tarefas
    url(r'^tarefas/$', views.tarefas, name ='tarefas' ),

    #url do formulario
    url(r'^tarefa-edit/$', views.formulario, name = 'formulario'),

    #url do cadastro de formulario, onde se faz a validação do formulario
    url(r'^errorUpdate/$', views.cadastrarFormulario, name = 'cadastrarFormulario'),

    #urls que mostram e termitem edição de tarefa
    url(r'^detalhes/(?P<pk>[0-9a-f-]+)/$', views.detail, name = "detail"),
    url(r'^editarDados/(?P<pk>[0-9a-f-]+)/$', views.editarDados, name = "editarDados"),
    url(r'^salvarEdicaoDados/(?P<pk>[0-9a-f-]+)/$', views.salvarEdicaoDados, name = "salvarEdicaoDados"),

    #Urls que controlam a exclusão de uma tarefa
    url(r'^remover/(?P<pk>[0-9a-f-]+)/$', views.remover, name = "remover"),
    url(r'^exclusaoDefinitiva/(?P<pk>[0-9a-f-]+)/$', views.exclusaoDefinitiva, name = "exclusaoDefinitiva"),
]
