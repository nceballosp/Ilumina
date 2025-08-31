from rest_framework import viewsets, permissions
from .serializers import *
from rest_framework.response import Response
from .models import *

# Viewset CRUD del modelo documento
class DocumentViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def list (self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create (self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def retrieve (self, request, pk=None):
        document = self.queryset.get(pk=pk)
        serializer = self. serializer_class(document)
        return Response(serializer.data)

    def update (self, request, pk=None):
        document = self.queryset.get(pk=pk)
        serializer = self.serializer_class(document, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)        

    def destroy (self, request, pk=None):
        document = self.queryset.get(pk=pk)
        document.delete()
        return Response(status = 204)