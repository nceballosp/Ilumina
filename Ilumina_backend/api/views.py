from rest_framework import viewsets, permissions
from .serializers import *
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .utils.load import load_file
from .utils.budget import get_budget


# No protegido de csrf: arreglar
@csrf_exempt
@api_view(['POST'])
def read_file_test(request: HttpRequest):
    file = request.FILES.get('data')
    if not file:
        return Response({"detail": "No se recibió archivo"}, status=400)
    df = load_file(file)
    if df:
        return Response({"detail": f"Archivo '{file.name}' cargado correctamente ✅"})

@api_view(['GET'])
def show_file_test(request: HttpRequest):
    df = get_budget()
    if df:
        return Response(data=df, status=200)
