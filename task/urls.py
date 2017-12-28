from django.conf.urls import url
from . import views

app_name = 'task'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^tarefas/(?P<pk>\d+)/$', views.tarefas, name ='tarefas' ),
    url(r'^formulario/(?P<pk>\d+)/$', views.formulario, name = 'formulario'),
    url(r'^cadastrarFormulario/(?P<pk>\d+)/$', views.cadastrarFormulario, name = 'cadastrarFormulario'),
    url(r'^detalhes/(?P<pk>\d+)/$', views.detail, name = "detail"),
    url(r'^editarDados/(?P<pk>\d+)/$', views.editarDados, name = "editarDados"),
    url(r'^salvarEdicaoDados/(?P<pk>\d+)/$', views.salvarEdicaoDados, name = "salvarEdicaoDados"),
    url(r'^remover/(?P<pk>\d+)/$', views.remover, name = "remover"),
    url(r'^exclusaoDefinitiva/(?P<pk>\d+)/$', views.exclusaoDefinitiva, name = "exclusaoDefinitiva"),
]
