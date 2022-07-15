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
from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='blogHome'),
    path('contact', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('signup/', views.signup, name='signUp'),
    path('addpost/', views.addPost, name='addPost'),
    path('blogpost/<str:slug>/', views.blogPost, name='blogPost'),
    path('deletePost/', views.deletePost, name='deletePost'),
    path('hidePost/', views.hidePost, name='hidePost'),
    path('unHidePost/', views.unHidePost, name='unHidePost'),
    path('editPost/', views.editPost, name='editPost'),
    path('postcomment/', views.post_comment, name='postcomment'),
    path('commentreply/', views.comment_reply, name='commentreply'),
    path('category/<str:category>', views.category, name='category'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('subscribe/', views.subscribe, name='subscribe'),
    # path('login/', views.loginHandle, name='login'),
]
