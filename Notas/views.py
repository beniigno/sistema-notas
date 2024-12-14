from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth import logout, authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.contrib.auth.models import User

from .models import User, Docente, RegistrarEstudiante, Matricula, Indicador, Nota, Curso, CursoIndicador
from .forms import EstudianteForm, DocenteForm, CursoForm, NotaForm, IndicadorForm, CursoIndicadorForm, MatriculaForm

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def validar(request):
    return render(request, 'validar.html')

@login_required
def index(request):
    usuario = request.user  # Usuario autenticado

    # Verifica si el usuario es un docente
    if hasattr(usuario, 'docente'):
        # Redirige al formulario de registro de estudiantes si es docente
        dni_docente = usuario.docente.dni_docente
        return render(request, 'docente/panelDocente.html', {
            'listarUsuario': usuario,
            'dni_docente': dni_docente,
        })

    # Verifica si el usuario es un estudiante
    elif hasattr(usuario, 'registrarestudiante'):
        # Redirige al panel del estudiante si es estudiante
        dni_estudiante = usuario.registrarestudiante.dni_estudiante
        return render(request, 'panelBase/panelEstudiante.html', {
            'listarUsuario': usuario,
            'dni_estudiante': dni_estudiante,
        })

    # Si no es docente ni estudiante, puedes manejar el caso
    else:
        return render(request, 'panelBase/acceso_denegado.html', {
            'mensaje': 'No tiene un rol asignado en el sistema.',
        })

def salir(request):
    logout(request)
    return redirect('accounts/login/')

def contactar(request):
    # Obtener todos los docentes desde la base de datos
    docentes = Docente.objects.all()

    # Si el formulario es enviado
    if request.method == "POST":
        docente_id = request.POST.get("docente")
        asunto = request.POST["txtAsunto"]
        mensaje = request.POST["txtMensaje"]
        email = request.POST["txtEmail"]
        
        # Aquí puedes hacer lo que necesites con los datos, como enviar el email
        # Ejemplo: enviar el correo (esto depende de tu lógica de envío de correos)
        
        # Redirigir a una página de éxito o volver con un mensaje de éxito
        return render(request, "panelBase/contactoExitoso.html")

    # Pasar la lista de docentes al contexto
    context = {
        'docentes': docentes,
    }

    return render(request, 'panelBase/formularioContacto.html', context)

def formularioContacto(request):
    return render(request, 'panelBase/formularioContacto.html')

def reporteEstudiante(request, dni_estudiante):
    # Obtener el estudiante por su DNI
    estudiante = get_object_or_404(RegistrarEstudiante, dni_estudiante=dni_estudiante)

    # Obtener los cursos en los que el estudiante está matriculado
    matriculas = Matricula.objects.filter(estudiante=estudiante)
    cursos = Curso.objects.filter(matricula__in=matriculas).distinct()

    # Obtener los docentes relacionados con los cursos (si es necesario)
    docentes = Docente.objects.filter(curso__in=cursos).distinct()
    
    # Obtener las unidades disponibles (cursos)
    unidades = Curso.objects.all()
    ciclo = matriculas.first().ciclo if matriculas.exists() else "No disponible"

    indicador = Indicador.objects.first()

    # Contexto para pasar a la plantilla (sin los datos dinámicos)
    context = {
        'estudiante': estudiante,
        'ciclo': ciclo,
        'cursos': cursos,  # Solo pasas los cursos en los que está matriculado el estudiante
        'docentes': docentes,  # Si aún necesitas los docentes en el contexto
        'unidades': unidades,  # Pasas las unidades para el desplegable
        'indicador' : indicador,
    }

    return render(request, 'panelBase/reporteEstudiante.html', context)

def obtener_datos_unidad(request):
    # Obtener el ID de la unidad seleccionada
    unidad_id = request.GET.get('unidad_id')  # El ID de la unidad será pasado como parámetro GET
    if not unidad_id:
        return JsonResponse({'error': 'Unidad no proporcionada'}, status=400)
    
    try:
        curso = Curso.objects.get(id=unidad_id)  # Buscar el curso por el ID
    except Curso.DoesNotExist:
        return JsonResponse({'error': 'Curso no encontrado'}, status=404)
    
    # Obtener el docente relacionado con este curso
    docente = Docente.objects.filter(curso=curso).first()
    docente_info = f"{docente.usuario.first_name} {docente.usuario.last_name}" if docente else "No disponible"

    # Obtener las notas para este curso
    notas = Nota.objects.filter(curso=curso)
    calificaciones = [nota.calificacion for nota in notas]

    # Calcular el promedio de las calificaciones
    if calificaciones:
        promedio = sum(calificaciones) / len(calificaciones)
    else:
        promedio = "No disponible"

    # Retornar los datos como un JSON
    return JsonResponse({
        'docente': docente_info,
        'creditos': curso.creditos,
        'horas': curso.horas if hasattr(curso, 'horas') else 'No disponible',
        'notas': calificaciones if calificaciones else "No disponible",
        'promedio': promedio
    })

def seleccionar_docente(request):
    docentes = Docente.objects.all()  # Trae todos los docentes, puedes cambiarlo por un filtro específico si es necesario
    
    return render(request, 'panelBace/formularioContacto.html', {'docentes': docentes})

def obtener_datos_unidad(request):
    unidad_id = request.GET.get('unidad_id')
    if not unidad_id:
        return JsonResponse({'error': 'Unidad no proporcionada'}, status=400)

    try:
        curso = Curso.objects.get(id=unidad_id)
    except Curso.DoesNotExist:
        return JsonResponse({'error': 'Curso no encontrado'}, status=404)

    # Obtener el docente relacionado con este curso
    docente = curso.docente
    docente_info = f"{docente.usuario.first_name} {docente.usuario.last_name}" if docente else "No disponible"

    # Obtener los indicadores asociados al curso (entre 1 a 5)
    indicadores = CursoIndicador.objects.filter(curso=curso).select_related('indicador')
    
    # Para cada indicador, obtendremos las notas del estudiante
    indicadores_data = []
    for indicador in indicadores:
        # Obtener las notas para este indicador
        notas = Nota.objects.filter(curso=curso, indicador=indicador.indicador)
        calificaciones = [float(nota.calificacion) for nota in notas]
        
        # Calcular el promedio del indicador
        promedio_indicador = round(sum(calificaciones) / len(calificaciones), 2) if calificaciones else 0
        
        indicadores_data.append({
            'descripcion': indicador.indicador.descripcion,
            'notas': calificaciones,
            'promedio': promedio_indicador
        })

    # Obtener las notas totales para el alumno (todas las notas de todos los indicadores)
    notas_totales = [nota.calificacion for nota in Nota.objects.filter(curso=curso)]
    promedio_general = round(sum(notas_totales) / len(notas_totales), 2) if notas_totales else 0

    # Retornar los datos como un JSON
    return JsonResponse({
        'docente': docente_info,
        'creditos': curso.creditos,
        'horas': curso.horas if hasattr(curso, 'horas') else 'No disponible',
        'promedio': promedio_general,
        'indicadores': indicadores_data  # Aseguramos que los indicadores y sus notas sean devueltos correctamente
    })


# _--------------------------------------------------------------------------------------------------------------
def panel_docente(request):
    # Lógica para la vista
    return render(request, 'panel_docente.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('registrar_estudiante')
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def passwordReset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            try:
                # Buscar al usuario existente
                user = User.objects.get(username=username)
                user.set_password(password)  # Actualizar la contraseña
                user.save()
                messages.success(request, 'Contraseña actualizada exitosamente.')
                return redirect('login')  # Redirigir al login
            except User.DoesNotExist:
                messages.error(request, 'El usuario no existe.')

    return render(request, 'registration/password_reset.html')

def registrar_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo estudiante en la base de datos
            return redirect('docente/panelDocente')  # Redirige a la lista de estudiantes o alguna otra vista
    else:
        form = EstudianteForm()

    return render(request, 'docente/registrar_estudiante.html', {'form': form})

from .models import Nota, Curso, RegistrarEstudiante, Indicador

def registrar_nota_view(request):
    if request.method == 'POST':
        estudiante_id = request.POST['estudiante']
        curso_id = request.POST['curso']
        indicador_id = request.POST['indicador']
        calificacion = request.POST['calificacion']
        Nota.objects.create(
            estudiante_id=estudiante_id,
            curso_id=curso_id,
            indicador_id=indicador_id,
            calificacion=calificacion
        )
        messages.success(request, 'Nota registrada correctamente')
        return redirect('home')
    estudiantes = RegistrarEstudiante.objects.all()
    cursos = Curso.objects.all()
    indicadores = Indicador.objects.all()
    return render(request, 'docente/registrar_nota.html', {
        'estudiantes': estudiantes,
        'cursos': cursos,
        'indicadores': indicadores
    })

def home_view(request):
    return render(request, 'docente/registrar_estudiante.html')  # Asegúrate de tener un archivo 'home.html' en tu carpeta de templates

def register_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
        else:
            # Crear el usuario
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            login(request, user)  # Inicia sesión automáticamente después del registro
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('login')  # Redirigir al login o a la página principal

    return render(request, 'docente/register.html')

def registrar_docente(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Docente registrado con éxito.")
            return redirect('docente/panelDocente')  # Redirige a la vista deseada
    else:
        form = DocenteForm()

    return render(request, 'docente/registrar_docente.html', {'form': form})

def registrar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('docente/panelDocente')  # Cambia 'success' por la URL de éxito que prefieras
    else:
        form = CursoForm()

    return render(request, 'docente/registrar_curso.html', {'form': form})

def registrar_nota(request):
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('docente/panelDocente')  # Puedes cambiar 'success' por la URL a la que quieres redirigir después de guardar
    else:
        form = NotaForm()

    return render(request, 'docente/registrar_nota.html', {'form': form})

def registrar_indicador(request):
    if request.method == 'POST':
        form = IndicadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Puedes cambiar 'success' por la URL a la que deseas redirigir después de guardar
    else:
        form = IndicadorForm()

    return render(request, 'docente/registrar_indicador.html', {'form': form})

def registrar_curso_indicador(request):
    if request.method == 'POST':
        form = CursoIndicadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('docente/panelDocente')  # Redirige a una página de éxito (puedes cambiar 'success' por la URL que desees)
    else:
        form = CursoIndicadorForm()

    return render(request, 'docente/registrar_curso_indicador.html', {'form': form})

def registrar_matricula(request):
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('docente/panelDocente')  # Redirige a la URL de éxito (puedes cambiar 'success' por cualquier otra URL que desees)
    else:
        form = MatriculaForm()

    return render(request, 'docente/registrar_matricula.html', {'form': form})
