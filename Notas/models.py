from django.db import models
from django.contrib.auth.models import User  

# Tabla Docente
class Docente(models.Model):
    dni_docente = models.CharField(max_length=20, unique=True)  # DNI del docente único
    especialidad = models.CharField(max_length=100, blank=True, null=True)  # Especialidad del docente
    telefono = models.CharField(max_length=20, blank=True, null=True)  # Teléfono
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con User (uno a uno)

    def __str__(self):
        return f"{self.usuario.username} - {self.dni_docente}" 

# Tabla RegistrarEstudiante (antes Estudiante)
class RegistrarEstudiante(models.Model):
    dni_estudiante = models.CharField(max_length=20, unique=True)  # DNI del estudiante único
    programa_estudios = models.CharField(max_length=100)  # Programa de estudios
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con User (uno a uno)
    periodo_academico = models.CharField(max_length=100, default=2024-2025)

    def __str__(self):
        return f"{self.usuario.username} - {self.dni_estudiante}"

# Tabla Curso
class Curso(models.Model):
    codigo = models.CharField(max_length=50, unique=True)  # Código único del curso
    nombre_curso = models.CharField(max_length=200)  # Nombre del curso
    descripcion = models.TextField(blank=True, null=True)  # Descripción del curso
    creditos = models.PositiveIntegerField()  # Créditos del curso
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)  # Relación con Docente

    def __str__(self):
        return self.nombre_curso
    
    # Tabla Indicador
class Indicador(models.Model):
    nombre = models.CharField(max_length=200)  # Nombre del indicador
    descripcion = models.TextField(blank=True, null=True)  # Descripción del indicador

    def __str__(self):
        return self.nombre
    
class CursoIndicador(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)  # Relación con Curso
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)  # Relación con Docente
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE)  # Relación con Indicador

    def __str__(self):
        return f"{self.curso.nombre_curso} - {self.docente.usuario.username} - {self.indicador.nombre}"    

# Tabla Nota
class Nota(models.Model):
    estudiante = models.ForeignKey(RegistrarEstudiante, on_delete=models.CASCADE)  # Relación con RegistrarEstudiante
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)  # Relación con Curso
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE)  # Relación con Indicador
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)  # Calificación

    def __str__(self):
        return f"Nota de {self.estudiante} en {self.curso}"

# Tabla Matricula
class Matricula(models.Model):
    estudiante = models.ForeignKey(RegistrarEstudiante, on_delete=models.CASCADE)  # Relación con RegistrarEstudiante
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)  # Relación con Curso
    fecha_matricula = models.DateField(auto_now_add=True)  # Fecha de matrícula
    ciclo = models.CharField(max_length=20)  # Ciclo académico

    def __str__(self):
        return f"Matrícula de {self.estudiante} en {self.curso}"
