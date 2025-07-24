# loja/urls.py
from django.urls import path
from .views import home
from .views import login_view
from .views import logout_view
from .views import cadastro_view
from django.urls import path, include
from .views import pedido
from . import views
from .views import painel_admin
from django.conf import settings
from django.conf.urls.static import static
from .views import painel_admin, upload
from .views import Ajuda
from .views import Chat

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cadastro/', cadastro_view, name='register'),
    path('pedir/', pedido, name='pedir'),
    path('ativar-conta/<uidb64>/<token>/', views.ativar_conta, name='ativar_conta'),
    path('adm/', painel_admin, name='adm'),  # ← aqui
    path('upload/', upload, name='upload'),
    path('Ajuda/', Ajuda, name='Ajuda'),
    path ('Ajuda/chat/', Chat, name='chat'),
    path('Ajuda/chat/enviar-mensagem/', views.enviar_mensagem, name='enviar_mensagem'),
]
