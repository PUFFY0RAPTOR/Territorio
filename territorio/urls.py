from django.urls import path
from . import views                 

app_name = "territorio"
urlpatterns = [
    path('', views.index, name="index"),
    path('loginFormulario/', views.loginFormulario, name="loginForm"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

    path('aprendices/', views.listarAprendiz, name="aprendices"),
    path('aprendicesAdd/', views.aprendicesFormulario, name="form-aprendiz"),
    path('aprendGuardar/', views.aprendicesGuardar, name="guardar-aprend"),
    path('eliminarApr/<int:id>', views.eliminarAprendiz, name="elim-aprend"),
    path('editarApr/<int:id>', views.aprendizFormularioEditar, name="edit-aprend"),
    path('actualizarAprendices/', views.actualizarAprendiz, name="actual_aprend"),
    path("/aprendicesBuscar", views.listarAprendizBuscar, name="buscar_aprend"),


    path('monitoria/', views.listarMonitorias, name="monitorias"),
    path('monitoriaAdd/', views.monitoriaFormulario, name="form-monitoria"),
    path('monitGuardar/', views.monitoriaGuardar, name="guardar-monit"),
    path('eliminarMon/<int:id>', views.eliminarMonitoria, name="elim-monit"),
    path('editarMon/<int:id>', views.monitoriaFormularioEditar, name="edit-monit"),
    path('actualizarMonitoria/', views.actualizarMonitoria, name="actual-monit"),

    path('actividades/', views.listarActividades, name="actividades"),

    path('listarUsuario/', views.listarUsuario, name="usuarios"),
    path('eliminarUsu/<int:id>', views.eliminarUsuario, name="elim-usu"),
    path('usuEditForm/<int:id>', views.usuFormularioEditar, name="form-usu"),
    path('usuEdit/', views.actualizarUsuario, name="actual_usu"),
    path('usuForm/', views.usuFormulario, name="usu_form"),
    path('usuGuardar/', views.usuGuardar, name="usu_guardar"),
    
] 