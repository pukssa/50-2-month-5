from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import product, category, review, User, UserConfirmation
from .serializer import (
    UserRegistrationSerializer,
    ConfirmationSerializer,
    ProductSerializer,
    ProductDetailSerializer,
    CategorySerializer,
    CategoryDetailSerializer,
    ReviewSerializer,
    ReviewDetailSerializer
)
from django.contrib.auth import authenticate

class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Код подтверждения отправлен."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmUserView(APIView):
    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            try:
                confirmation = UserConfirmation.objects.get(code=code)
                user = confirmation.user
                user.is_active = True
                user.save()
                confirmation.delete()
                return Response({"detail": "Пользователь подтвержден."})
            except UserConfirmation.DoesNotExist:
                return Response(
                    {"error": "Неверный код."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            return Response({"detail": "Успешный вход."})
        return Response(
            {"error": "Неверные данные или пользователь не подтвержден."},
            status=status.HTTP_401_UNAUTHORIZED
        )

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_url_kwarg = 'id'

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_url_kwarg = 'id'

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = review.objects.all()
    serializer_class = ReviewSerializer

class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = review.objects.all()
    serializer_class = ReviewDetailSerializer
    lookup_url_kwarg = 'id'

class ProductReviewsWithRatingView(generics.ListAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer