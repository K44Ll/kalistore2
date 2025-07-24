from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
import requests

def home(request):
    return render(request, "home.html") 


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # cria a sessão do usuário
            return redirect('home')  # redireciona para alguma página, ex: "home"
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos.'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect("login")

from django.contrib.auth.models import User

def cadastro_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmar = request.POST.get("confirm_password")

        if not username or not password:
            return render(request, 'cadastro.html', {"error": "Preencha todos os campos."})
        
        if password != confirmar:
            return render(request, 'cadastro.html', {"error": "As senhas não coincidem."})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro.html', {"error": "Nome de usuário já existe."})

        # Cria o usuário
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect("login")

    return render(request, 'cadastro.html')

@login_required(login_url='login')
def pedido(request):
    TOKEN = os.getenv("TG_API_KEY")
    ID = os.getenv("TG_CHAT_ID")
    

    if request.method == "POST":
        categoria = request.POST.get('tipo', '')
        email = request.POST.get('email', '')
        contato = request.POST.get('telefone', '')
        outroctt = request.POST.get('contatoalt', '')
        tipooutroctt = request.POST.get('tipoctt', '')

        # Escapar texto para evitar erro com Markdown (se quiser usar HTML, mudo o parse_mode e formatação)
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
        else:
            messages.error(request, "Erro ao enviar pedido. Tente novamente mais tarde.")

        return render(request, "pedido.html")

    # GET
    return render(request, "pedido.html")
