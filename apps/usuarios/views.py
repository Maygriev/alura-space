from django.shortcuts import render, redirect

from apps.usuarios.forms import LoginForms, CadastroForms

from django.contrib import auth, messages
from django.contrib.auth.models import User 

def login(request):
        form = LoginForms()

        if request.method == 'POST':
                form = LoginForms(request.POST)

                if form.is_valid():
                        nomeLogin = form["nome_login"].value()
                        senhaLogin = form["senha"].value()

                        usuario = auth.authenticate(
                                request,
                                username=nomeLogin,
                                password=senhaLogin
                        )

                        if usuario is not None:
                                auth.login(request, usuario)
                                messages.success(request, f"{nomeLogin} logado com sucesso!")
                                return redirect("index")
                        else:
                                messages.error(request, "Erro ao efetuar login")
                                return redirect("login")

        return render(request, "usuarios/login.html", {"form": form})

def cadastro(request):

        form = CadastroForms()

        if request.method == 'POST':
                form = CadastroForms(request.POST)

                if form.is_valid():
                        if form["senha_1"].value() != form["senha_2"].value():
                                messages.error(request, "Senhas não são iguais")
                                return redirect("cadastro")
                        
                        nomeCadastro = form["nome_cadastro"].value()
                        emailCadastro = form["email"].value()
                        senhaCadastro = form["senha_1"].value()

                        if User.objects.filter(username=nomeCadastro).exists():
                                messages.error(request, f"Usuário {nomeCadastro} já existe")
                                return redirect("cadastro")
                        
                        usuario = User.objects.create_user(
                                username=nomeCadastro,
                                email=emailCadastro,
                                password=senhaCadastro
                        )

                        usuario.save()
                        messages.success(request, f"Cadastro de {nomeCadastro} efetuado com sucesso!")
                        return redirect("login")
                
        return render(request, "usuarios/cadastro.html", {"form": form})

def logout(request):
        auth.logout(request)
        messages.success(request, "Logout efetuado com sucesso!")
        return redirect("login")