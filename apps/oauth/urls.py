# -*- coding: utf-8 -*-
from django.urls import path
from apps.oauth.views import profile_view, change_profile_view
from apps.oauth.views import account_logout

urlpatterns = [

    path('profile/', profile_view, name='profile'),
    path('profile/change/', change_profile_view, name='change_profile'),
    # path('account_logout/', account_logout, name='account_logout'),

]
