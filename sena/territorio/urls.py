from django.urls import path
from . import views                 

app_name = "territorio"
urlpatterns = [
    path('', views.index, name="index"),
    path('aprendices/', views.listarAprendiz, name="aprendices"),
    path('aprendicesAdd/', views.aprendicesFormulario, name="form-aprendiz"),
    path('aprendGuardar/', views.aprendicesGuardar, name="guardar-aprend"),
    path('eliminarApr/<int:id>', views.eliminarAprendiz, name="elim-aprend"),


    path('monitoria/', views.listarMonitorias, name="monitorias"),
    path('monitoriaAdd/', views.monitoriaFormulario, name="form-monitoria"),
    path('monitGuardar/', views.monitoriaGuardar, name="guardar-monit"),
    path('eliminarMon/<int:id>', views.eliminarMonitoria, name="elim-monit"),


    path('actividades/', views.listarActividades, name="actividades"),
]