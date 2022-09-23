from email.policy import default
from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=254)
    usuario = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=254)
    ROLES = (
        ("R", "Administrador"),
        ("I", "Instructor"),
        ("A", "Aprendiz"),
    )
    #enumerate mysql
    rol = models.CharField(choices = ROLES, max_length=1, default="A")
    foto = models.ImageField(upload_to = '', default = 'perfil.png')

    def __str__(self):
        return self.nombre


class Aprendiz(models.Model):
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return self.nombre


class Monitoria(models.Model):
    cat = models.CharField(max_length=100)
    aprendiz = models.ForeignKey(Aprendiz, on_delete = models.DO_NOTHING)
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()

    def __str__(self):
        return f"{self.aprendiz.nombre} {self.aprendiz.apellido} - {self.cat}"


class Actividades(models.Model):
    monitoria = models.ForeignKey(Monitoria, on_delete=models.DO_NOTHING)
    actividad_realizada = models.CharField(max_length=254)
    obs = models.TextField()                                                                                                                                                                                                       
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.actividad_realizada
