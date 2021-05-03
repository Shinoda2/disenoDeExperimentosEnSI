from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),

    path('listaadmins', views.listarAdmins, name='listaadmins'),
    path('editaradmin/<int:id>', views.editarAdmin, name='editaradmin'),
    path('desactivaradmin/<int:id>', views.desactivarAdmin, name='desactivaradmin'),

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
    path('listamatriculas', views.listarMatriculasTotales, name='listamatriculas'),
    path('listamatriculas/<str:semestre>', views.listarMatriculas, name='listamatriculas'),

    path('reportematricula/<str:semestre>/<int:id>', views.reporteMatricula, name='reportematricula'),

    path('createsuccess/curso', views.successCurso, name='createsucesscurso'),
    path('createsuccess/docente', views.successDocente, name='createsucessdocente'),
    path('createsuccess/alumno', views.successAlumno, name='createsucessalumno'),
    path('createsuccess/admin', views.successAdmin, name='createsucessadmin'),

    path('editsuccess/curso', views.editsuccessCurso, name='editsucesscurso'),
    path('editsuccess/docente', views.editsuccessDocente, name='editsucessdocente'),
    path('editsuccess/alumno', views.editsuccessAlumno, name='editsucessalumno'),
    path('editsuccess/admin', views.editsuccessAdmin, name='editsucessadmin')
]