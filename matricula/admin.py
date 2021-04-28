  
from django.contrib import admin

from .models import *
# Register your models here.
class alumnoadmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "apellido", "dni")
class docenteadmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "apellido", "dni")
class cursoadmin(admin.ModelAdmin):
    list_display = ("id", "nombreCurso", "profesor" , "vacantes") 
admin.site.register(User)
admin.site.register(Alumno, alumnoadmin)
admin.site.register(Profesor, docenteadmin)
admin.site.register(Curso, cursoadmin)
admin.site.register(DetalleMatricula)