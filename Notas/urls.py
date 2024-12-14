from django.urls import path
from . import views
from Notas.views import formularioContacto
from .views import reporteEstudiante


urlpatterns = [
    path('', views.index, name='index'),
    path('inicio/', views.inicio, name='inicio'),
    path('validar/', views.validar, name='validar'),
    path('panelEstudiante/', views.validar, name='panelEstudiante'),
    path('salir', views.salir, name='salir'),
    path('formularioContacto/', views.formularioContacto, name='formularioContacto'),
    path('contactar/', views.contactar, name='contactar'), 
    path('reporteEstudiante/<str:dni_estudiante>/', reporteEstudiante, name='reporteEstudiante'),
    path('obtener-datos-unidad/', views.obtener_datos_unidad, name='obtener_datos_unidad'),
    path('seleccionar-docente/', views.seleccionar_docente, name='seleccionar_docente'),
    path('passwordReset/', views.passwordReset, name='password-reset'),
    path('panel_docente/', views.panel_docente, name='panel_docente'),
    path('registrar_estudiante/', views.registrar_estudiante, name='registrar_estudiante'), 
    path('register/', views.register_user_view, name='register_user'),
    path('registrar_docente/', views.registrar_docente, name='registrar_docente'),
    path('registrar_curso/', views.registrar_curso, name='registrar_curso'),
    path('registrar_nota/', views.registrar_nota, name='registrar_nota'),
    path('registrar_indicador/', views.registrar_indicador, name='registrar_indicador'),
    path('registrar_curso_indicador/', views.registrar_curso_indicador, name='registrar_curso_indicador'),
    path('registrar_matricula/', views.registrar_matricula, name='registrar_matricula'),

]
