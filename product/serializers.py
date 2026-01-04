from rest_framework import serializers
from decimal import Decimal
from product.models import Category,Product,Review,ProductImage
from django.contrib.auth import get_user_model

class Category_serializer(serializers.ModelSerializer):
    product_count=serializers.IntegerField(read_only=True)
    class Meta:
        model=Category
        fields=['id','name','description','product_count']
    

        

    
    

'''class Product_serializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    unit_price=serializers.DecimalField(max_digits=10,decimal_places=2,source='price')
    
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    
    #category=serializers.PrimaryKeyRelatedField(
    #   queryset=Category.objects.all()
    #)
    #category=serializers.StringRelatedField()
    
    #category=Category_serializer()
    
    category=serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name='view_specific_category'
    )
    
    def calculate_tax(self,product):
        return round(product.price* Decimal(1.1),2)'''
  
  
class ProductImageSerializer(serializers.ModelSerializer):
    image=serializers.ImageField()
    class Meta:
        model=ProductImage
        fields=['id','image']
    
          
class Product_serializer(serializers.ModelSerializer):
    images=ProductImageSerializer(many=True,read_only=True)
    class Meta:
        model=Product
        fields=['id','name','description','price','stock','category','price_with_tax','images']
    
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax',)
    '''category=serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name='view_specific_category'
    )'''
    
    def calculate_tax(self,product):
        return round(product.price* Decimal(1.1),2)
        
    def validate_price(self,price):
        if price<0:
            raise serializers.ValidationError('Price could not be negative')
        return price
    '''def create(self, validated_data):
        product=Product(**validated_data)
        product.other=1
        product.save()
        return product'''
    
    # def validate(self, attrs):
    #     if attrs['password1'] != attrs['password2']:
    #         raise serializers.ValidationError("Password didn't pass")
    
    
class SimpleUserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(
        method_name='get_current_user_name')

    class Meta:
        model=get_user_model()
        fields=['id','name']
        
    def get_current_user_name(self,obj):
        return obj.get_full_name()
    
    
class Review_serializer(serializers.ModelSerializer):
    #user=SimpleUserSerializer()
    user=serializers.SerializerMethodField(
        method_name='get_user')
    class Meta:
        model=Review
        fields=['id','user','product','ratings','comment']
        read_only_fields=['user','product']
    
    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

        
    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)
    
    
