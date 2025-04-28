from rest_framework import serializers
from .models import product, category, review
from rest_framework import serializers
from .models import User, UserConfirmation

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        UserConfirmation.objects.create(user=user)
        #Здесь можно добавить отправку кода на emailили sms
        return user

class ConfirmationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = review
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    class Meta:
        model = product
        fields = '__all__'

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.stars for review in reviews) / len(reviews), 2)
        return 0


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = category
        fields = ('id', 'name', 'products_count')

    def get_products_count(self, obj):
        return obj.product_set.count()



class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = '__all__'



class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = review
        fields = '__all__'