from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('load_file/', LoadFileView.as_view(), name='load'),
    path('generate_budget/', BudgetTableView.as_view(), name='budget'),
    path('adjust_budget/', BudgetAdjustmentView.as_view(), name='adjust_budget'),
    path("adjust_budget/save/", SaveBudgetAdjustmentView.as_view(),
         name="save_adjust_budget"),
    path("adjust_budget/table/", BudgetAdjustmentTableView.as_view(),
         name="table_adjust_budget"),
    path("adjust_budget/update/", UpdateBudgetAdjustmentView.as_view(),
         name="update_adjust_budget"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('report/', NegativeAccountReportView.as_view(), name='report'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('portal/', CoordinatorPortalView.as_view(), name='portal'),
]
