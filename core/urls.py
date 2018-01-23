from django.urls import path
from core import views

urlpatterns = [
    path(r'', views.upload, name='upload'),
    path(r'results/', views.results_list, name='results_list'),
    path(r'results/<str:apk_hash>', views.results, name='results')
]
