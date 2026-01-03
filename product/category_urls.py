from django.urls import path
from product import views

urlpatterns = [
    path('',views.view_categories.as_view(),name='category'),
    path('<int:pk>/',views.view_specific_category.as_view(),name='view_specific_category')
]
