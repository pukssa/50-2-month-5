from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import product, category, review
from .serializer import ProductSerializer, ProductDetailSerializer, CategoryDetailSerializer, CategorySerializer,ReviewSerializer,ReviewDetailSerializer



@api_view(['GET'])
def product_detail_api_view(request,id):
    products = product.objects.get(id=id)
    data = ProductSerializer(products).data
    return Response(data)




@api_view(['GET'])
def product_list_api_view(request):
    products = product.objects.all()

    data = ProductSerializer(products, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_list_api_view(request):
    categories = category.objects.all()
    data = CategorySerializer(categories, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def category_detail_api_view(request, id):
    categories = category.objects.get(id=id)
    data = CategorySerializer(categories).data
    return Response(data)


@api_view(['GET'])
def review_list_api_view(request):
    reviews = review.objects.all()
    data = ReviewSerializer(reviews, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def review_detail_api_view(request, id):
    reviews = review.objects.get(id=id)
    data = ReviewSerializer(reviews).data
    return Response(data)


@api_view(['GET'])
def product_reviews_with_rating(request):
    products = product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
