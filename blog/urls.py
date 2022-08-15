"""iBlogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='blogHome'),
    path('contact', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('signup/', views.signup, name='signUp'),
    path('addpost/', views.add_post, name='add_post'),
    path('blogpost/<str:slug>/', views.blog_post, name='blog_post'),
    path('delete_post/', views.delete_post, name='delete_post'),
    path('hide_post/', views.hide_post, name='hide_post'),
    path('un_hide_post/', views.un_hide_post, name='un_hide_post'),
    path('editPost/', views.edit_post, name='editPost'),
    path('postcomment/', views.post_comment, name='postcomment'),
    path('commentreply/', views.comment_reply, name='commentreply'),
    path('category/<str:category>', views.category, name='category'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('login/', views.login_handle, name='login'),
    path('verification/<str:username>/<str:verification_code>', views.verify_email, name='verify_email'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:username>/<str:password_reset_code>', views.reset_password, name='reset_password'),
    path('change_password/', views.change_password, name='change_password'),
]
