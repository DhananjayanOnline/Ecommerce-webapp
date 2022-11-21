from .models import Products, Carts, Reviews
from .serializers import ProductSerializer, ReviewSerializer, CartSerializer

from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework.views import APIView

# Create your views here.

class ProductsView(ModelViewSet):
    serializer_class=ProductSerializer
    queryset=Products.objects.all()

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["POST"], detail=True)
    def add_review(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ReviewSerializer(data=request.data, context={"user":request.user, "product":product})
        if serializer.is_valid():
            serializer.save()
            return Response("review added")
        else:
            return Response(data=serializer.errors)

    @action(methods=["GET"], detail=False)
    def catogories(self, request, *args, **kwargs):
        qs = Products.objects.values_list('category', flat=True).distinct()
        return Response(data=qs)

    
    def list(self, request, *args, **kwargs):
        qs = Products.objects.all()
        if "category" in request.query_params:
            qs=qs.filter(category=request.query_params.get("category"))
        serialiser = ProductSerializer(qs, many=True)
        return Response(data=serialiser.data)

    @action(methods=["POST"], detail=True)
    def addto_cart(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        serialier = CartSerializer(data=request.data, context={"user":user, "product":product})
        if serialier.is_valid():
            serialier.save()
            return Response(data=serialier.data)
        else:
            return Response(data=serialier.errors)


class CartView(ViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        qs = Carts.objects.filter(user=request.user)
        serializer = CartSerializer(qs, many=True)
        return Response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        object=Carts.objects.get(id=id)
        if object.user==request.user:
            object.delete()
            return Response(data="deleted")
        else:
            raise serializers.ValidationError("You have no permission to perform this operation")

# class ReviewDeleteView(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def delete(self, request, *args, **kwargs):
#         id = kwargs.get('pk')
#         user = request.user
#         print(user)
#         review = Reviews.objects.get(id=id)
#         if review.user == user:
#             review.delete()
#             return Response(data="deleted")
#         else:
#             raise serializers.ValidationError("You have no permission to perform this operation")


from rest_framework import mixins
from rest_framework import generics

class ReviewDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):

    serializer_class = ReviewSerializer
    queryset = Reviews.objects.all()

    def delete(self, request, *args, **kwargs):
        id=kwargs.get('id')
        review = Reviews.objects.get(id=id)
        if review.user == request.user:
            return self.destroy(request, *args, **kwargs)
        else:
            raise serializers.ValidationError('you have no permission to delete this operation')

