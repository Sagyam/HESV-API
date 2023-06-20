from django.contrib import admin
from django.urls import path
from majorProject import views

urlpatterns = [
    path('solve-3d-linear-equation',
         views.solve_3d_linear_equation),
    path('solve-2d-linear-equation', views.solve_2d_linear_equation),
    path('solve-polynomial-equation', views.solve_polynomial_equation),
    path('get-linear-equation', views.get_linear_equation),
    path('get-polynomial-equation', views.get_polynomial_equation),


]
