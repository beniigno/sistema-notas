from django.contrib import admin
from .models import User, Docente, RegistrarEstudiante, Curso, Indicador, Nota, Matricula,CursoIndicador


# Registro de los modelos para la administración de Django
admin.site.register(Docente)
admin.site.register(RegistrarEstudiante)
admin.site.register(Curso)
admin.site.register(Indicador)
admin.site.register(Nota)
admin.site.register(Matricula)
admin.site.register(CursoIndicador)
