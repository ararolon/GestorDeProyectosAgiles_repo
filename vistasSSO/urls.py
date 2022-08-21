
from django.urls import path, include
from vistasSSO import views
from django.views.generic import TemplateView


urlpatterns = [
    #path('',views.configuraciones_iniciales,name='confinicial'),
    path('', views.home, name='home'),
    #path('login/', views.login, name='login'),
    #path('logout/', views.logout, name='logout'),
]
