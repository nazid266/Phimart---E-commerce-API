from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Product,Category,Review,ProductImage
from product.serializers import Product_serializer,Category_serializer,Review_serializer,ProductImageSerializer
from django.db.models import Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from product.pagination import DefaultPagination
from api.permissions import IsAdminUserOrReadOnly,FullDjangoModelPermissions
from .permissions import IsReviewAuthorOrReadonly
from rest_framework.permissions import DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

'''@api_view(['GET','POST'])# Function based view
def view_product(request):
    if request.method=='GET':
        product=Product.objects.select_related('category').all()
        serializer=Product_serializer(product,many=True)
        return Response(serializer.data)
    if request.method=='POST':
        #desirilizer
        serializer=Product_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()                                                                   
        return Response(serializer.data,status=status.HTTP_201_CREATED)'''  


'''@api_view(['GET','PUT','DELETE'])
def view_specific_product(request,id):
    if request.method=='GET':
        product=get_object_or_404(Product,pk=id)
        serializer=Product_serializer(product)
        return Response(serializer.data)
    if request.method=='PUT':
        product=get_object_or_404(Product,pk=id)
        serializer=Product_serializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method=='DELETE':
        product=get_object_or_404(Product,pk=id)
        copy_product=product
        product.delete()
        serializer=Product_serializer(copy_product)
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)'''


class ProductViewSet(ModelViewSet):
    """
    API endpoint for managing products in the e-commerce store
     - Allows authenticated admin to create, update, and delete products
     - Allows users to browse and filter product
     - Support searching by name, description, and category
     - Support ordering by price and updated_at
    """
    
    
    serializer_class=Product_serializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    #filterset_fields=['category_id','price','stock']
    filterset_class=ProductFilter
    #permission_classes=[IsAdminUser]
    #permission_classes=[IsAdminUserOrReadOnly]
    #permission_classes=[DjangoModelPermissions]
    permission_classes=[FullDjangoModelPermissions]
    #permission_classes=[DjangoModelPermissionsOrAnonReadOnly]
    search_fields=['name','description']
    ordering_fields=['price','stock']
    pagination_class=DefaultPagination
    
    def get_queryset(self):
        return Product.objects.prefetch_related("images").all()
    
    #def get_permissions(self):
    #    if self.request.method=='GET':
    #        return [AllowAny()]
    #   return [IsAdminUser()]
    
    
    #def get_queryset(self):
    #   queryset=Product.objects.all()
    #    category_id=self.request.query_params.get('category_id')
    #    
    #    if category_id is not None:
    #        queryset=Product.objects.filter(category_id=category_id)
    #    return queryset

    
    #def destroy(self, request, *args, **kwargs):
    #    product=self.get_object()
    #   if product.stock>10:
    #        return Response({'message':'product with stock more than 10 could not be deleted'})
    #    self.perform_destroy(product)
    #    return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    @swagger_auto_schema(
        operation_summary='Retrive a list of products'
    )
    def list(self, request, *args, **kwargs):
        """Retrive all the products"""
        return super().list(request, *args, **kwargs)
    
    
    @swagger_auto_schema(
        operation_summary='Only authenticated admin can create product',
        operation_description="This allow an admin to create a product",
        request_body=Product_serializer,
        responses={
            201: Product_serializer,
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create product"""
        return super().create(request, *args, **kwargs)
 
 

class ProductImageViewset(ModelViewSet):
    serializer_class=ProductImageSerializer
    
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))
    
    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get('product_pk'))
 
 
 
 
 
        
        


'''@api_view(['GET','POST'])
def view_categories(request):
    if request.method=='GET':
        category=Category.objects.annotate(product_count=Count('products')).all()
        serializer=Category_serializer(category,many=True)
        return Response(serializer.data)
    if request.method=='POST':
        serializer=Category_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)'''



'''@api_view(['GET','PUT','DELETE'])
def view_specific_category(request,pk):
   if request.method=='GET':
        category=get_object_or_404(Category,pk=pk)
        serializer=Category_serializer(category)
        return Response(serializer.data)
   if request.method=='PUT':
        category=get_object_or_404(Category,pk=pk)
        serializer=Category_serializer(category,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
   if request.method=='DELETE':
       category=get_object_or_404(Category,pk=pk)
       copy_category=category
       category.delete()
       serializer=Category_serializer(copy_category)
       return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)'''
       

   

    
class CategoryViewSet(ModelViewSet):
    permission_classes=[IsAdminUserOrReadOnly]
    queryset=Category.objects.annotate(product_count=Count('products')).all()
    serializer_class=Category_serializer
        
        
        
class ReviewViewSet(ModelViewSet):
    serializer_class=Review_serializer
    permission_classes=[IsReviewAuthorOrReadonly]
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
    def perform_update(self,serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return Review.objects.none
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))
    
    def get_serializer_context(self):
        if getattr(self,'swagger_fake_view',False):
            return super().get_serializer_context()
            
        return {'product_id':self.kwargs.get('product_pk')}
    
      

   
