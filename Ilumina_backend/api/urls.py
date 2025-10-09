from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('load_file', LoadFileView.as_view(), name='load'),
    path('login', HomeView.as_view(), name='login'),
    path('budget', BudgetTableView.as_view(), name='budget'),
]
