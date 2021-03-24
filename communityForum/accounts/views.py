from django.contrib.auth.forms import  AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .forms import SignUpForm



class SignUpView(View):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, ('Your account has been created.'))
            return redirect('login')

        return render(request, self.template_name, {'form': form})




def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/', user)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})




@login_required(login_url='/login')
def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")


@login_required(login_url='/login')
def home_view(request):
    return render(request, "index.html")