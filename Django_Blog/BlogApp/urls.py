"""Django_Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

urlpatterns = [
    path('', views.IndexView, name='home'),
    path('profile/<name>', views.ProfileView, name="profile"),
    #path('single/<int:id>', views.SingleView.as_view(), name="single"),
    path('single/<int:id>', views.SingleView, name='single'),
    path('topic/<name>', views.CategoryView, name="topic"),
    path('login', views.loginView, name="login"),
    path('logout', views.logoutView, name="logout"),
    path('create', views.createView, name="create"),
    path('user', views.userView, name="user"),
    path('update/<int:id>', views.updateView, name="update"),
    path('delete/<int:id>', views.deleteView, name="delete"),
    path('register', views.registerView, name="register"),
    path('topics', views.topicsView, name="topics"),
    path('createTopics', views.createTopicsView, name="createTopics"),
    path('pdf/<int:id>',views.pdf.as_view(), name="pdf"),
    path('json',views.getJson.as_view(), name="json"),
    path('xml',views.getXml.as_view(), name="xml"),
    # Account confirmations
    path('activate/<uid>/<token>', views.activate, name="activate"),
]