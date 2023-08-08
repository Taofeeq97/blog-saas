from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('articles/', views.home, name='home'),
    path('create_tenant/', views.create_tenant, name='create_tenant'),
    path('register/', views.register_user, name='register'),
    path('<slug:article>/', views.article, name='article'),
    path('', views.login_view, name='login'),
]
