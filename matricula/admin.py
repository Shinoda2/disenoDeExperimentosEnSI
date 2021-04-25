  
from django.contrib import admin

from .models import *
# Register your models here.
class alumnoadmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "apellido", "dni")
admin.site.register(User)
admin.site.register(Alumno, alumnoadmin)
admin.site.register(Profesor)
admin.site.register(Curso)
admin.site.register(DetalleMatricula)