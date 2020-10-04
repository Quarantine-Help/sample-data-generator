from django.urls import path

from pacifier.views import DataPacifierAPIView

urlpatterns = [
    path('', DataPacifierAPIView.as_view()),
]
