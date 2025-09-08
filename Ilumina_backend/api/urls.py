from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = router.urls
urlpatterns += [
    path('read_file', read_file_test, name='prueba'),
    path('show_file', show_file_test, name='prueba2'),
]
