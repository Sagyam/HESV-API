from django.contrib import admin
from django.urls import path
from majorProject import views

urlpatterns = [
    path('/solveThreeDegreeLinearEquation/',
         views.three_degree_linear_equation),
    path('/solveTwoDegreeLinearEquation/', views.two_degree_linear_equation),
    path('/getTheImageForPolynomial/', views.get_equation_polynomial),
    path('/solveTheEquationPolynomial/', views.solve_the_equation_polynomial),
    path('/twoDegreeLinerEquation/', views.two_degree_linear_equation)
]
