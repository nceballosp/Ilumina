from .serializers import *
from rest_framework.response import Response
from .models import *
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .utils.load import load_file
from .utils.budget import get_budget
from rest_framework.views import APIView


class ReadFileView(APIView):
    # No protegido de csrf: arreglar
    @csrf_exempt
    def post(self, request: HttpRequest):
        file = request.FILES.get('data')
        if not file:
            return Response({"detail": "No se recibió archivo"}, status=400)
        df = load_file(file)
        if df:
            return Response(
                {"detail": f"Archivo '{file.name}' cargado correctamente ✅"})


class ShowTableView(APIView):
    def get(self, request: HttpRequest):
        ipc: float = float(request.GET.get('ipc'))
        df = get_budget(ipc)
        if df:
            return Response(data=df, status=200)


class UpdateRowView(APIView):
    @csrf_exempt
    def put():
        pass
