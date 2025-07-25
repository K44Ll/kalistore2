# 💼 Kali's Store 2

**Kali's Store 2** é uma plataforma de e-commerce simples e funcional, desenvolvida em Django, voltada para a venda dos meus próprios projetos. O objetivo é oferecer um ambiente direto, seguro e bonito para que qualquer usuário possa navegar, interagir e adquirir conteúdo.

---

Disponível [aqui](https://kalistore2.onrender.com)

## 🚀 Funcionalidades

- ✅ Sistema de autenticação (login, logout, registro)
- 💬 Chat entre usuário e administrador
- 📂 Painel de administração com upload de arquivos
- 🪟 Interface com efeito *glassmorphism* estilizada com CSS
- 📜 Página de Ajuda integrada
- 🔐 Sistema básico de permissões e acesso
- 📦 Upload de arquivos com retorno de link
- 🖼️ Integração com arquivos estáticos


---

## 🧠 Tecnologias utilizadas

- **Backend:** Django 5+
- **Frontend:** HTML5, CSS3 (customizado), Google Fonts
- **Banco de dados:** SQLite (desenvolvimento)
- **Outros:** Template engine Django, sistema de URLs, CSRF protection

---

## 🛠️ Como rodar localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/kalistore2.git
   cd kalistore2
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou .\venv\Scripts\activate no Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Aplique as migrações:
   ```bash
   python manage.py migrate
   ```

5. Crie um superusuário (opcional):
   ```bash
   python manage.py createsuperuser
   ```

6. Rode o servidor:
   ```bash
   python manage.py runserver
   ```

---

## 🧪 Teste rápido

Acesse `http://127.0.0.1:8000/` no navegador.  
Entre com sua conta ou crie uma.  
Acesse `/admin/` para o painel de administração.  
Use o chat para enviar mensagens e testar a interface.

---

## 📁 Estrutura do projeto (resumida)

```bash
kalistore2/
├── loja/                 # App principal (views, models, urls)
├── static/               # CSS, imagens, JS
├── templates/            # Templates HTML
├── media/                # Arquivos enviados (upload)
├── db.sqlite3            # Banco de dados local
└── manage.py
```

---

## 🢨 Estilo visual

O visual foi inspirado em **Glassmorphism**, com paleta escura e efeitos suaves.  
O foco é tornar a experiência de navegação moderna e intuitiva.

---

## 💡 Planos futuros

- 🛒 Carrinho de compras
- 💳 Integração com pagamentos
- 📊 Painel com estatísticas
- 🔔 Notificações no painel admin

---

## 📞 Contato

Caso tenha interesse em meus projetos ou deseje contratar serviços personalizados:

📧 Email: [wolfcookie20009@gmail.com]  
🐙 GitHub: [github.com/K4LL](https://github.com/K44Ll)

---
