from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = router.urls
urlpatterns += [
    path('read_file', ReadFileView.as_view(), name='prueba'),
    path('show_file', ShowTableView.as_view(), name='prueba2'),
]
