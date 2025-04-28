"""
URL configuration for shop_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from products import views

urlpatterns = [
    # User Auth Endpoints
    path('register/', views.RegisterUserView.as_view()),
    path('confirm/', views.ConfirmUserView.as_view()),
    path('login/', views.LoginUserView.as_view()),

    # Product Endpoints
    path('products/', views.ProductListView.as_view()),
    path('products/<int:pk>/', views.ProductDetailView.as_view()),
    path('products/reviews/', views.ProductReviewsWithRatingView.as_view()),

    # Category Endpoints
    path('categories/', views.CategoryListView.as_view()),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view()),

    # Review Endpoints
    path('reviews/', views.ReviewListView.as_view()),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view()),
]