# -*- coding: utf-8 -*-
from django.urls import path

from apps.resume.views import ResumeDetailView

urlpatterns = [
    path('<slug:slug>/', ResumeDetailView.as_view(), name='detail')
]
