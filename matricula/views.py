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
        else:
            return render(request, "matricula/login.html", {
                "message": "Invalid username and/or password."
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
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "matricula/register.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect(reverse("register"))
    else:
        return render(request, "matricula/register.html", {'admins': User.objects.all()})

@login_required(login_url='/login')
def listarAdmins(request):
    return render(request, "matricula/listaadmins.html", {'admins': User.objects.all()})

@login_required(login_url='/login')
def crearAlumno(request):      
    if request.method == "POST":
        obj = Alumno()
        obj.nombre = request.POST["nombre"]
        obj.apellido = request.POST["apellido"]
        obj.dni = request.POST["dni"]        

        obj.save()
        return HttpResponseRedirect("listaalumnos")

    return render(request, "matricula/crearalumno.html", {'alumnos': Alumno.objects.all()})

@login_required(login_url='/login')
def editarAlumno(request, id):
    alumno = Alumno.objects.get(id=id)   
    if request.method == "POST":
        alumno.id = id
        alumno.nombre = request.POST["nombre"]
        alumno.apellido = request.POST["apellido"]
        alumno.dni = request.POST["dni"]   

        alumno.save()
        return HttpResponseRedirect("../listaalumnos")

    return render(request, "matricula/editaralumno.html", {'alumnos': Alumno.objects.all(), 'form':alumno})

@login_required(login_url='/login')
def desactivarAlumno(request, id):
    alumno = Alumno.objects.get(id=id)   
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
        obj = Profesor()
        obj.nombre = request.POST["nombre"]
        obj.apellido = request.POST["apellido"]
        obj.dni = request.POST["dni"]

        obj.save()

    return render(request, "matricula/crearprofesor.html", {'docentes': Profesor.objects.all()})

@login_required(login_url='/login')
def listarDocentes(request):
    return render(request, "matricula/listadocentes.html", {'docentes': Profesor.objects.all()})

@login_required(login_url='/login')
def crearCurso(request):
    if request.method == "POST":
        obj = Curso()
        obj.nombreCurso = request.POST["nombre"]
        obj.profesor = Profesor.objects.get(id = int(request.POST["profesor"]))
        obj.activo = True        

        obj.save()

    return render(request, "matricula/crearcurso.html", {
        'profesores': Profesor.objects.all(), 
        'cursos': Curso.objects.all()
        })
    

@login_required(login_url='/login')
def listarCursos(request):
    return render(request, "matricula/listacursos.html", {'cursos': Curso.objects.all()})

@login_required(login_url='/login')
def matricularAlumno(request):
    if request.method == "POST":
        objCurso = Curso.objects.get(pk = int(request.POST["curso"]))
        obj = DetalleMatricula()
        if objCurso.matriculados < 10 :
            obj.curso = Curso.objects.get(id = int(request.POST["curso"]))
            obj.alumno = Alumno.objects.get(id = int(request.POST["alumno"]))
            obj.save()
            objCurso.matriculados += 1
            objCurso.save()
            return render(request, "matricula/matricularalumno.html", {
            'cursos': Curso.objects.all(),
            'alumnos': Alumno.objects.all()
        })
        elif objCurso.matriculados == 10:
            mensaje = "Ya no hay vacantes en este curso."
            return render(request, "matricula/matricularalumno.html", {
            'cursos': Curso.objects.all(),
            'alumnos': Alumno.objects.all(),
            'mensaje':mensaje
        })
    return render(request, "matricula/matricularalumno.html", {
            'cursos': Curso.objects.all(),
            'alumnos': Alumno.objects.all()
        })
    