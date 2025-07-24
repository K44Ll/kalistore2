# loja/urls.py
from django.urls import path
from .views import home
from .views import login_view
from .views import logout_view
from .views import cadastro_view
from django.urls import path, include
from .views import pedido

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cadastro/', cadastro_view, name='register'),
    path('pedir/', pedido, name='pedir'),
]
