from django.contrib.auth.forms import  AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .forms import SignUpForm, UpdateProfileForm, UpdateUserForm
from .models import Profile

from posts.models import Question, Answer




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
                return redirect('profile', user)
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



def user_profile(request, username):
    user = User.objects.get(username=username)
    u_page = Profile.objects.get(user_id=user)
    questions = Question.objects.all()
    answer = Answer.objects.all()

    context = {
        'u_page' : u_page,
        'usr': user,
        'question' :questions,
        'ans':answer,
    }


    return render(request, 'accounts/profile.html', context)



@login_required(login_url='/login')
def edit_profile(request):
    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('edit-profile')
    
    else:
        p_form = UpdateProfileForm(instance=request.user.profile)
        
        u_form = UpdateUserForm(instance=request.user)
        

    context = {
        'p_form' : p_form,
        'u_form': u_form
    }

    return render(request, "accounts/edit-profile.html", context)



def landing_page(request):
    return render(request, "index.html")