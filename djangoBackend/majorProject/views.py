from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['POST'])
def three_degree_linear_equation(request):
    eq1 = request.data['eq1']
    eq2 = request.data['eq2']
    eq3 = request.data['eq3']
    data = {
        'x': 1,
        'y': 2,
        'z': 3,
        'solution_found': True
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def two_degree_linear_equation(request):
    eq1 = request.data['eq1']
    eq2 = request.data['eq2']
    data = {
        'x': 1,
        'y': 2,
        'solution_found': True
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_equation_polynomial(request):
    image = request.data['image']
    data = {
        'eqn': 'x3+y3+z3',
        'image_name': image.name
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def solve_the_equation_polynomial(request):
    equation = request.data['eq']
    data = {
        'solution': [1, 2],
        'solution_type': 'linear'
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_two_degree_equation(request):
    image = request.data['image']
    data = {
        'eq': 'x2+y2',
        'name': image.name
    }
    return Response(data, status=status.HTTP_200_OK)
