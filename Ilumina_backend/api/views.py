from typing import Any
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, TemplateView, CreateView, View
from .forms import RegisterForm
from django.contrib import messages

from .models import *
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .utils.load import load_file
from .utils.budget import get_budget
from django.contrib.auth.models import User


class HomeView(TemplateView):
    template_name = 'home.html'


class LoadFileView(LoginRequiredMixin,TemplateView):
    template_name = 'load.html'

    def post(self, request: HttpRequest):
        file = request.FILES.get('data')
        if str(file).split('.')[1] != 'xlsx':
            return JsonResponse({"detail": "El archivo tiene que ser un xlsx"}, status=400)
        if not file:
            return JsonResponse({"detail": "No se recibió archivo"}, status=400)
        df = load_file(file)
        if df:
            return JsonResponse({"detail": f"Archivo '{file.name}' cargado correctamente ✅"})
        elif not df:
            return JsonResponse({"detail": f"Algo salio mal cargando los datos, revisar formato del archivo"})

class UpdateRowView(View):
    def put(self):
        pass


class LastBudgetTableView(LoginRequiredMixin,ListView):
    template_name = 'last_budget.html'
    context_object_name = 'data'

    def get_queryset(self):
        queryset = AnnualBudget.objects.all().values()
        return list(queryset)


class BudgetTableView(LoginRequiredMixin,TemplateView):
    template_name = 'budget.html'

    def post(self, request: HttpRequest):
        ipc: float = float(request.GET.get('ipc', 0))
        df: list = get_budget(ipc)
        if df:
            return JsonResponse(data=df, status=200, safe=False)


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginUserView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class LogoutUserView(LogoutView):
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Has cerrado sesión correctamente.")
        return super().dispatch(request, *args, **kwargs)
