from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('crearalumno', views.crearAlumno, name='crearalumno'),
    path('crearprofesor', views.crearProfesor, name='crearprofesor'),
    path('crearcurso', views.crearCurso, name='crearcurso'),
    path('matricularalumno', views.matricularAlumno, name='matricularalumno')
]