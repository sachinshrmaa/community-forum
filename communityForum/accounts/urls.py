from django.urls import path
from .views import user_login, user_logout, SignUpView, home_view

urlpatterns = [
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('', home_view, name="landing-page"),
]