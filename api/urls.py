from django.urls import path,include
from rest_framework.routers import SimpleRouter,DefaultRouter
from product.views import ProductViewSet,CategoryViewSet,ReviewViewSet,ProductImageViewset
from order.views import CartViewSet,CartItemViewSet,OrderViewSet
from rest_framework_nested import routers

router=routers.DefaultRouter()
router.register('products',ProductViewSet,basename='products')
router.register('categories',CategoryViewSet)
router.register('carts',CartViewSet,basename='carts')
router.register('orders',OrderViewSet,basename='orders')

product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('reviews',ReviewViewSet,basename='product_review')
product_router.register('images',ProductImageViewset,basename='product_image')

cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',CartItemViewSet,basename='cart_items')

#urlpatterns=router.urls

urlpatterns = [
    path('',include(router.urls)),
    path('',include(product_router.urls)),
    path('',include(cart_router.urls))
]
