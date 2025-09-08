from rest_framework import viewsets, permissions
from .serializers import *
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .utils import load_table


# No protegido de csrf: arreglar
@csrf_exempt
@api_view(['POST'])
def read_file_test(request: HttpRequest):
    file = request.FILES.get('data')
    df = load_table(file)
    return Response(data=df, status=200)
