from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Alumno(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.IntegerField()
    activo = models.BooleanField(default=1)
    # email = models.EmailField(max_length=255)
    # fechaNacimiento = models.DateField()

class Profesor(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.IntegerField()
    activo = models.BooleanField(default=1)
    # email = models.EmailField(max_length=255)

class Curso(models.Model):
    nombreCurso = models.CharField(max_length=255)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name="profesor")
    activo = models.BooleanField()
    vacantes = models.IntegerField(default=0)

class DetalleMatricula(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="alumno")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="curso")

class Semestre(models.Model):
    nombreSemestre = models.CharField(max_length=255)

class semestreCurso(models.Model):
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name="semestre")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="subject")
    vacantes = models.IntegerField()
    