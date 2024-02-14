"""cms_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from user_app import views as user_views
from api_app import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",user_views.home,name='home'),
    path("main/", user_views.main, name = 'main'), 
    path('signin/', user_views.signin, name='signin'),
    path('signout/', user_views.signout, name='signout'),
    path('register/', user_views.register, name='register'),
    path('create_policy/', user_views.create_policy, name='create_policy'),
    path('policy_detail/', user_views.read_policy, name='read_policy'),
    path('read_claim/', user_views.read_claim, name='read_claim'),
    path('create_claim/', user_views.create_claim, name='create_claim'),



    
    path('api/signup/', api_views.signup_api, name='signup_api'),
    path('api/login/', api_views.login_api, name='login_api'),
    path('api/user/claims/', api_views.user_claim_list, name='user_claim_list'),
    path('api/admin/claims/', api_views.admin_claim_list, name='admin_claim_list'),
    path('api/admin/claims/<uuid:claim_id>/', api_views.admin_claim_update, name='admin_claim_update'),
    path('api/admin/claims/<uuid:claim_id>/delete/', api_views.admin_claim_delete, name='admin_claim_delete'),
]
