from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('load_file', LoadFileView.as_view(), name='load'),
    path('generate_budget', BudgetTableView.as_view(), name='budget'),
    path('current_budget', LastBudgetTableView.as_view(), name='last_budget'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginUserView.as_view(), name='login'),
    path('logout', LogoutUserView.as_view(), name='logout'),
]
