from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import product, category, review
from .serializer import ProductSerializer, ProductDetailSerializer, CategoryDetailSerializer, CategorySerializer,ReviewSerializer,ReviewDetailSerializer
from django.contrib.auth import authenticate
from .models import User, UserConfirmation
from .serializer import (
    UserRegistrationSerializer,
    ConfirmationSerializer,)

@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail": "Код подтверждения отправлен."},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def confirm_user(request):
    serializer = ConfirmationSerializer(data=request.data)
    if serializer.is_valid():
        code = serializer.validated_data['code']
        try:
            confirmation = UserConfirmation.objects.get(code=code)
            user = confirmation.user
            user.is_active = True
            user.save()
            confirmation.delete()  #Код больше не нужен
            return Response({"detail": "Пользователь подтвержден."})
        except UserConfirmation.DoesNotExist:
            return Response(
                {"error": "Неверный код."},
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user and user.is_active:

        return Response({"detail": "Успешный вход."})
    return Response(
        {"error": "Неверные данные или пользователь не подтвержден."},
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    obj = get_object_or_404(product, id=id)
    if request.method == 'GET':
        data = ProductSerializer(obj).data
        return Response(data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    obj = get_object_or_404(category, id=id)
    if request.method == 'GET':
        data = CategorySerializer(obj).data
        return Response(data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    obj = get_object_or_404(review, id=id)
    if request.method == 'GET':
        data = ReviewSerializer(obj).data
        return Response(data)
    elif request.method == 'PUT':
        serializer = ReviewSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def product_reviews_with_rating(request):
    products = product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
