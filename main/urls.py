from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="Home"),
    path('about', views.about, name="about"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
]