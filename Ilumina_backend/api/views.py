from typing import Any
from django.http import JsonResponse
from .models import *
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from django.views.generic import TemplateView,View
from .utils.load import load_file
from .utils.budget import get_budget
import json


class HomeView(TemplateView):
    template_name = 'home.html'

class LoadFileView(TemplateView): 
    template_name = 'load.html'
    def post(self,request: HttpRequest):
        print(request.POST)
        file = request.FILES.get('data')
        if not file:
            return JsonResponse({"detail": "No se recibió archivo"}, status=400)
        df = load_file(file)
        if df:
            return JsonResponse({"detail": f"Archivo '{file.name}' cargado correctamente ✅"})


class UpdateRowView(View):
    def put(self):
        pass
class BudgetTableView(TemplateView):
    template_name = 'budget.html'
    def post(self,request:HttpRequest):
        ipc: float = float(request.GET.get('ipc',0))
        df:list = get_budget(ipc)
        if df:
            return JsonResponse(data=df, status=200, safe=False)