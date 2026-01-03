from rest_framework import serializers
from order.models import Cart,CartItem,Order,OrderItem
from product.models import Product
from order.services import OrderServices



class EmptySerializer(serializers.Serializer):
    pass

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','price']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']
        
    def save(self, **kwargs):
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']
        
        try:
          cart_item= CartItem.objects.get(cart_id=cart_id,product_id=product_id)
          cart_item.quantity+=quantity
          self.instance=cart_item.save()
        except CartItem.DoesNotExist:
            self.instance=CartItem.objects.create(cart_id=cart_id,**self.validated_data)
        return self.instance
    
    def validate_product_id(self,valu):
        if not Product.objects.filter(pk=valu).exists():
            raise serializers.ValidationError(f'This Product id {valu} not available')
        return valu
            
class UpddateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']   
        
class CartItemsSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model=CartItem
        fields=['id','product','quantity','total_price']
        
    def get_total_price(self,cart=CartItem):
        return cart.quantity*cart.product.price
    
        
        

class CartSerializer(serializers.ModelSerializer):
    items=CartItemsSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model=Cart
        fields=['id','user','items','total_price']
        read_only_fields = ['user']
        
    def get_total_price(self,cart):
        return sum(
            [item.product.price*item.quantity for item in cart.items.all()]
        )
  
class CreateOrderSerializer(serializers.Serializer):
    cart_id=serializers.UUIDField()
    
    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError("Cart Is Not Found")
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart Is Empty')
        return cart_id
    
    def create(self,validated_data):
        user_id=self.context['user_id']
        cart_id=validated_data['cart_id']
        
        try:
          order=OrderServices.create_order(user_id=user_id,cart_id=cart_id)
          return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        
    def to_representation(self,instance):
        return OrderSerializer(instance).data
        
           
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=['id','product','price','quantity','total_price']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['status']
        
        
        # this method replace action method
        
    ''' def update(self, instance, validated_data):
       user=self.context['user']
       new_status=validated_data['status']
       
       if new_status==Order.CANCELED:
           return OrderServices.cancel_order(order=instance,user=user)
       
       if not user.is_staff:
           raise serializers.ValidationError({'detail':'You are not allowed to update this order'})
       
       return super().update(instance,validated_data)'''
        
        
class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)
    class Meta:
        model=Order
        fields=['id','user','status','total_price','created_at','items']