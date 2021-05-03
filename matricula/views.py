from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import *


import datetime


from .models import *


def index(request):
    return render(request, "matricula/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        # Check if authentication successful    
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        elif (username is not "" or password is not ""):            
            return render(request, "matricula/login.html", {
                "message": "*El nombre de usuario o contraseña son incorrectos. Inténtelo de nuevo."
            })
        else:
            return render(request, "matricula/login.html", {
            "message": "*Introduzca un nombre de usuario y una contraseña."
        })

    else:
        return render(request, "matricula/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@user_passes_test(lambda u: u.is_superuser)
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "matricula/register.html", {
                "message": "Las contraseñas deben coincidir."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "matricula/register.html", {
                "message": "El usuario ingresado ya se encuentra registrado."
            })
        return HttpResponseRedirect(reverse("register"))
    else:
        return render(request, "matricula/register.html", {'admins': User.objects.all()})

@login_required(login_url='/login')
def editarAdmin(request, id):
    administrador = User.objects.get(id = id)
    if request.method == "POST":
        
        #User.objects.filter(id=id).update(username = request.POST["username"], email = request.POST["email"], first_name = request.POST["first_name"], last_name = request.POST["last_name"], password = request.POST["password"])
        administrador.username = request.POST["username"]
        administrador.email = request.POST["email"]
        administrador.first_name = request.POST["first_name"]
        administrador.last_name = request.POST["last_name"]
        administrador.set_password(request.POST["password"])
        administrador.save()

        confirmation = request.POST["confirmation"]
        
        if request.POST["password"] != confirmation:
            return render(request, "matricula/editaradmin.html", {
                "message": "Las contraseñas deben coincidir."
            })
        else:
            #administrador.save()
            
            return HttpResponseRedirect(reverse("listaadmins"))

        # Attempt to create new user
    else:
        return render(request, "matricula/editaradmin.html", {'admins': User.objects.all(), 'form':administrador})
    

@login_required(login_url='/login')
def listarAdmins(request):
    
    return render(request, "matricula/listaadmins.html", {'admins': User.objects.all()})

@login_required(login_url='/login')
def desactivarAdmin(request, id):
    administrador = User.objects.get(id=id)   
    if request.method == "POST":        
        if(administrador.is_active):
            administrador.is_active =  False    
        else:
            administrador.is_active = True

        administrador.save()
        return HttpResponseRedirect("../listaadmins")
    return render(request, "matricula/desactivaradmin.html", {'admins': User.objects.all(), 'form':administrador})

@login_required(login_url='/login')
def crearAlumno(request):      
    if request.method == "POST":
        try:
            Alumno.objects.create(nombre = request.POST["nombre"], apellido = request.POST["apellido"], dni = request.POST["dni"])
        
            return HttpResponseRedirect("listaalumnos")
        except:
            errorCrear = "El dni utilizado ya se encuentra registrado."
            return render(request, "matricula/crearalumno.html", {'alumnos': Alumno.objects.all(), 'errorcrear': errorCrear})
        

    return render(request, "matricula/crearalumno.html", {'alumnos': Alumno.objects.all()})

@login_required(login_url='/login')
def editarAlumno(request, id):
    alumno = Alumno.objects.get(dni=id)
    if request.method == "POST":
        if request.POST["dni"] == str(alumno.dni):
            alumno.nombre = request.POST["nombre"]
            alumno.apellido = request.POST["apellido"]
            alumno.dni = request.POST["dni"]
            alumno.save()
            return HttpResponseRedirect("../listaalumnos")
        else:
            try:
                Alumno.objects.update(nombre = request.POST["nombre"], apellido = request.POST["apellido"], dni = request.POST["dni"])
                return HttpResponseRedirect("../listaalumnos")
            except:
                mensaje = "error"
                return render(request, "matricula/editaralumno.html", {'alumnos': Alumno.objects.all(), 'form':alumno, 'mensaje':mensaje})
            
    return render(request, "matricula/editaralumno.html", {'alumnos': Alumno.objects.all(), 'form':alumno,})
    

@login_required(login_url='/login')
def desactivarAlumno(request, id):
    alumno = Alumno.objects.get(dni=id)   
    if request.method == "POST":        
        if(alumno.activo):
            alumno.activo =  False    
        else:
            alumno.activo = True

        alumno.save()
        return HttpResponseRedirect("../listaalumnos")

    return render(request, "matricula/desactivaralumno.html", {'alumnos': Alumno.objects.all(), 'form':alumno})

@login_required(login_url='/login')
def listarAlumnos(request):
    return render(request, "matricula/listaalumnos.html", {'alumnos': Alumno.objects.all()})


@login_required(login_url='/login')
def crearProfesor(request):
    if request.method == "POST":
        try:
            Profesor.objects.create(nombre = request.POST["nombre"], apellido = request.POST["apellido"], dni = request.POST["dni"])
            return HttpResponseRedirect("listadocentes")
        except:
            errorCrear = "El dni utilizado ya se encuentra registrado."
            return render(request, "matricula/crearprofesor.html", {'docentes': Profesor.objects.all(), 'errorcrear': errorCrear})
        

    return render(request, "matricula/crearprofesor.html", {'docentes': Profesor.objects.all()})

@login_required(login_url='/login')
def editarDocente(request, id):
    docente = Profesor.objects.get(dni=id)   
    if request.method == "POST":
        if request.POST["dni"] == str(docente.dni):

            docente.id = id
            docente.nombre = request.POST["nombre"]
            docente.apellido = request.POST["apellido"]
            docente.dni = request.POST["dni"]   

            docente.save()
        else:
            try:
                Profesor.objects.update(nombre = request.POST["nombre"], apellido = request.POST["apellido"], dni = request.POST["dni"])
                return HttpResponseRedirect("../listadocentes")
            except:
                mensaje = "error"
                return render(request, "matricula/editardocente.html", {'docentes': Profesor.objects.all(), 'form':docente, 'mensaje':mensaje})

    return render(request, "matricula/editardocente.html", {'docentes': Profesor.objects.all(), 'form':docente})

@login_required(login_url='/login')
def desactivarDocente(request, id):
    docente = Profesor.objects.get(dni=id)   #switched dni
    if request.method == "POST":        
        if(docente.activo):
            docente.activo =  False    
        else:
            docente.activo = True

        docente.save()
        return HttpResponseRedirect("../listadocentes")

    return render(request, "matricula/desactivardocente.html", {'docentes': Profesor.objects.all(), 'form':docente})

@login_required(login_url='/login')
def listarDocentes(request):
    return render(request, "matricula/listadocentes.html", {'docentes': Profesor.objects.all()})

@login_required(login_url='/login')
def crearCurso(request):
    if request.method == "POST":
        try:
            Curso.objects.create(nombreCurso = request.POST["nombreCurso"], profesor = Profesor.objects.get(dni = int(request.POST["profesor"])), vacantes = request.POST["vacantes"], activo = True)  

            return HttpResponseRedirect("listacursos")
        except:
            errorCrear = "El curso ingresado ya se encuentra registrado."
            return render(request, "matricula/crearcurso.html", {
            'profesores': Profesor.objects.all(), 
            'cursos': Curso.objects.all(),
            'errorcrear': errorCrear
            })
    return render(request, "matricula/crearcurso.html", {
        'profesores': Profesor.objects.all(), 
        'cursos': Curso.objects.all()
        })

@login_required(login_url='/login')
def editarCurso(request, id):
    curso = Curso.objects.get(id=id)   
    if request.method == "POST":
        try:
            curso.nombreCurso = request.POST["nombreCurso"]
            curso.profesor = Profesor.objects.get(dni = int(request.POST["profesor"]))
            curso.vacantes = request.POST["vacantes"]   
            
            curso.save()
            return HttpResponseRedirect("../listacursos")
        except:
            mensaje: "error"
            return render(request, "matricula/editarcurso.html", {'profesores': Profesor.objects.all(), 'cursos': curso.objects.all(), 'form':curso, 'mensaje':mensaje})

    return render(request, "matricula/editarcurso.html", {'profesores': Profesor.objects.all(), 'cursos': Curso.objects.all(), 'form':curso})

@login_required(login_url='/login')
def desactivarCurso(request, id):
    curso = Curso.objects.get(id=id)   
    if request.method == "POST":        
        if(curso.activo):
            curso.activo =  False    
        else:
            curso.activo = True

        curso.save()
        return HttpResponseRedirect("../listacursos")

    return render(request, "matricula/desactivarcurso.html", {'cursos': Curso.objects.all(), 'form':curso})

@login_required(login_url='/login')
def listarCursos(request):
    return render(request, "matricula/listacursos.html", {'cursos': Curso.objects.all()})

@login_required(login_url='/login')
def matricularAlumno(request):
    if request.method == "POST":
        objCurso = Curso.objects.get(pk = int(request.POST["curso"]))
        semestre = request.POST["semestre"]
        matricula = DetalleMatricula.objects.all().filter(semestre = semestre, curso = objCurso)

        obj = str(dict.fromkeys(matricula))    

        listaalumnos = []
        for obj in matricula:
                listaalumnos.append(obj.alumno)
        
        print(len(listaalumnos))

        obj = DetalleMatricula()
        obj.curso = Curso.objects.get(id = int(request.POST["curso"]))
        obj.alumno = Alumno.objects.get(dni = int(request.POST["alumno"]))
        obj.semestre = request.POST["semestre"]

        try:
            if len(listaalumnos) < objCurso.vacantes :            
                obj.save()
                return HttpResponseRedirect("listamatriculas")
        #     return render(request, "matricula/matricularalumno.html", {
        #     'cursos': Curso.objects.all(),
        #     'alumnos': Alumno.objects.all()
        # })
            elif len(listaalumnos) == objCurso.vacantes:
                completo = "Ya no hay vacantes en este curso."
                return render(request, "matricula/matricularalumno.html", {
                'cursos': Curso.objects.all(),
                'alumnos': Alumno.objects.all(),
                'completo': completo
                })
        #     return render(request, "matricula/matricularalumno.html", {
        #     'cursos': Curso.objects.all(),
        #     'alumnos': Alumno.objects.all(),
        #     'mensaje':mensaje
        # })
        except:
            mensaje = f"Alumno {obj.alumno.nombre} {obj.alumno.apellido} ya se encuentra matriculado en el curso {obj.curso.nombreCurso} para el semestre {obj.semestre}."
            return render(request, "matricula/matricularalumno.html", {
            'cursos': Curso.objects.all(),
            'alumnos': Alumno.objects.all(),
            'mensaje': mensaje
            })


        
    return render(request, "matricula/matricularalumno.html", {
            'cursos': Curso.objects.all(),
            'alumnos': Alumno.objects.all()
        })        

@login_required(login_url='/login')
def listarMatriculas(request, semestre):
    matricula = DetalleMatricula.objects.all().filter(semestre=semestre)
    semestre = semestre
    listacurso = []
    for obj in matricula:
        listacurso.append(obj.curso)

    lista = {i:listacurso.count(i) for i in listacurso}
    listacurso = list(dict.fromkeys(listacurso))    
    return render(request, "matricula/listamatriculas.html", {'cursos': lista, 'semestre':semestre})


@login_required(login_url='/login')
def listarMatriculasTotales(request):
    matricula = DetalleMatricula.objects.all()
    listacurso = []
    for obj in matricula:
        listacurso.append(obj.curso)

    lista = {i:listacurso.count(i) for i in listacurso}
    listacurso = list(dict.fromkeys(listacurso))    
    return render(request, "matricula/listamatriculas.html", {'cursos': lista})

@login_required(login_url='/login')
def reporteMatricula(request,semestre, id):
    curso = Curso.objects.get(id=id)   
    matricula = DetalleMatricula.objects.all().filter(semestre = semestre, curso = curso)
    
    obj = str(dict.fromkeys(matricula))    

    listaalumnos = []
    for obj in matricula:
            listaalumnos.append(obj.alumno)

    return render(request, "matricula/reportematricula.html", {'matricula': obj, 'alumnos': listaalumnos})
    