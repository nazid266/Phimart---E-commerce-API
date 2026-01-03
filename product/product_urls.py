from django.urls import path
from product import views

urlpatterns = [
    path('',views.product_view.as_view()),
    path('<int:id>',views.view_specific_product.as_view(),name='product')
]
