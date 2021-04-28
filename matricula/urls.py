from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),

    path('listaadmins', views.listarAdmins, name='listaadmins'),

    path('crearalumno', views.crearAlumno, name='crearalumno'),
    path('listaalumnos', views.listarAlumnos, name='listaalumnos'),
    path('editaralumno/<int:id>', views.editarAlumno, name='editaralumno'),
    path('desactivaralumno/<int:id>', views.desactivarAlumno, name='desactivaralumno'),

    path('crearprofesor', views.crearProfesor, name='crearprofesor'),
    path('listadocentes', views.listarDocentes, name='listadocentes'),
    path('editardocente/<int:id>', views.editarDocente, name='editardocente'),
    path('desactivardocente/<int:id>', views.desactivarDocente, name='desactivardocente'),

    path('crearcurso', views.crearCurso, name='crearcurso'),
    path('listacursos', views.listarCursos, name='listacursos'),
    path('editarcurso/<int:id>', views.editarCurso, name='editarcurso'),
    path('desactivarcurso/<int:id>', views.desactivarCurso, name='desactivarcurso'),

    path('matricularalumno', views.matricularAlumno, name='matricularalumno'),
    path('listamatriculas', views.listarMatriculas, name='listamatriculas'),
    path('listamatriculas/<str:semestre>', views.listarMatriculas, name='listamatriculas')


]