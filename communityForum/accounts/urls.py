from django.urls import path
from .views import user_login, user_logout, SignUpView, user_profile, edit_profile, landing_page


urlpatterns = [
    path('get-started/', landing_page, name="landing-page" ),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('edit-profile/', edit_profile, name="edit-profile"),
    path('profile/<username>/', user_profile, name="profile"),
]