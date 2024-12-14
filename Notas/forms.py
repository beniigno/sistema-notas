from django import forms
from django.contrib.auth.models import User
from .models import Docente, Curso,Nota, Indicador, CursoIndicador, Matricula, RegistrarEstudiante

# forms.py

class DocenteForm(forms.ModelForm):
    # Selecciona un usuario existente de Django (campo combo)
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), required=True, empty_label="Seleccionar usuario")
    
    class Meta:
        model = Docente
        fields = ['dni_docente', 'especialidad', 'telefono', 'usuario']

# forms.py

class EstudianteForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), required=True, empty_label="Seleccionar usuario")

    class Meta:
        model = RegistrarEstudiante
        fields = ['dni_estudiante', 'programa_estudios', 'periodo_academico', 'usuario']
       

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['codigo', 'nombre_curso', 'descripcion', 'creditos', 'docente']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_curso': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'creditos': forms.NumberInput(attrs={'class': 'form-control'}),
            'docente': forms.TextInput(attrs={'class': 'form-control'}),
            
        }



class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['estudiante', 'curso', 'indicador', 'calificacion']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'indicador': forms.Select(attrs={'class': 'form-control'}),
            'calificacion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

# forms.py


class IndicadorForm(forms.ModelForm):
    class Meta:
        model = Indicador
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# forms.py


class CursoIndicadorForm(forms.ModelForm):
    class Meta:
        model = CursoIndicador
        fields = ['curso', 'docente', 'indicador']
        widgets = {
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'docente': forms.Select(attrs={'class': 'form-control'}),
            'indicador': forms.Select(attrs={'class': 'form-control'}),
        }

# forms.py


class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ['estudiante', 'curso', 'ciclo']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'ciclo': forms.TextInput(attrs={'class': 'form-control'}),
        }
