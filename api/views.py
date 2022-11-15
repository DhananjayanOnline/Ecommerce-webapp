from django.shortcuts import render
from .models import Products
from .serializers import ProductSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions

# Create your views here.

class ProductsView(ModelViewSet):
    serializer_class=ProductSerializer
    queryset=Products.objects.all()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


