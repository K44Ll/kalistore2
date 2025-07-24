from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect
from .models import Mensagem
import os
import requests


@login_required
def enviar_mensagem(request):
    if request.method == "POST":
        texto = request.POST.get("message", "").strip()
        if texto:
            Mensagem.objects.create(user=request.user, texto=texto)
    return redirect('chat')  # 'chat' é o nome da url da página do chat



def enviar_e_mail(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Confirmação de cadastro'
    message = render_to_string('cadastro_confirmado.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = 'html'
    email.send()


def home(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos.'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect("login")


def cadastro_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmar = request.POST.get("confirm_password")
        email = request.POST.get("email")

        if not username or not password or not email:
            return render(request, 'cadastro.html', {"error": "Preencha todos os campos."})

        if password != confirmar:
            return render(request, 'cadastro.html', {"error": "As senhas não coincidem."})

        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro.html', {"error": "Nome de usuário já existe."})

        if User.objects.filter(email=email).exists():
            return render(request, 'cadastro.html', {"error": "Esse e-mail já está em uso."})

        user = User.objects.create_user(username=username, password=password, email=email)
        user.is_active = False
        user.save()

        enviar_e_mail(request, user)

        return render(request, 'cadastro.html', {"success": "Verifique seu e-mail para ativar sua conta."})

    return render(request, 'cadastro.html')


def ativar_conta(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Conta ativada com sucesso! Faça login.")
        return redirect('login')
    else:
        return render(request, 'ativacao_invalida.html')


@login_required(login_url='login')
def pedido(request):
    TOKEN = os.getenv("TG_API_KEY")
    ID = os.getenv("TG_CHAT_ID")

    user_id = request.user.id
    cooldown_key = f'pedido_cooldown_user_{user_id}'
    cooldown_segundos = 120

    # Verifica cooldown no cache
    last_time = cache.get(cooldown_key)
    now = timezone.now()

    if last_time and (now - last_time).total_seconds() < cooldown_segundos:
        wait = cooldown_segundos - (now - last_time).total_seconds()
        messages.error(request, f"Espere {int(wait)} segundos antes de enviar outro pedido.")
        return render(request, "pedido.html")

    if request.method == "POST":
        categoria = request.POST.get('tipo', '')
        email = request.POST.get('email', '')
        contato = request.POST.get('telefone', '')
        outroctt = request.POST.get('contatoalt', '')
        tipooutroctt = request.POST.get('tipoctt', '')

        def escape_markdown(text):
            import re
            escape_chars = r'_*[]()~`>#+-=|{}.!'
            return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text or '')

        categoria_esc = escape_markdown(categoria)
        email_esc = escape_markdown(email)
        contato_esc = escape_markdown(contato) or "Não informado"
        outroctt_esc = escape_markdown(outroctt) or "Não informado"
        tipooutroctt_esc = escape_markdown(tipooutroctt) or "Não informado"

        msg = (
            f"📦 *Novo Pedido* 📦\n\n"
            f"*Produto:* {categoria_esc}\n"
            f"*E-mail:* {email_esc}\n"
            f"*Contato WhatsApp:* {contato_esc}\n"
            f"*Outro contato:* {outroctt_esc}\n"
            f"*Tipo de contato:* {tipooutroctt_esc}"
        )

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            'chat_id': ID,
            'text': msg,
            'parse_mode': 'Markdown'
        }

        response = requests.post(url, data=payload)

        if response.status_code == 200:
            messages.success(request, "Pedido enviado com sucesso! Em breve entraremos em contato.")
            # Atualiza o cache com o horário do pedido atual
            cache.set(cooldown_key, now, timeout=cooldown_segundos)
        else:
            messages.error(request, "Erro ao enviar pedido. Tente novamente mais tarde.")

        return render(request, "pedido.html")

    return render(request, "pedido.html")

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def painel_admin(request):
    return render(request, "admin.html")

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        arquivo = request.FILES['file']
        fs = FileSystemStorage()
        nome_arquivo = fs.save(arquivo.name, arquivo)
        url = fs.url(nome_arquivo)
        return render(request, 'admin.html', {'url': url})
    return render(request, 'admin.html')

def Ajuda(request):
    return render(request, "Ajuda.html")

@login_required
def Chat(request):
    if request.method == "POST":
        texto = request.POST.get("message", "").strip()
        if texto:
            Mensagem.objects.create(user=request.user, texto=texto)
        return redirect('chat')

    mensagens = Mensagem.objects.order_by('criado_em')  # busca todas mensagens ordenadas pelo tempo
    return render(request, "chat.html", {"mensagens": mensagens})
