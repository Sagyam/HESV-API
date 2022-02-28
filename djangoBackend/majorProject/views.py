from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['POST'])
def get_polynomial_equation(request):
    image = request.data['image']
    data = {
        'eqn': 'x3+y3+z3',
        'image_name': image.name
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_linear_equation(request):
    image = request.data['image']
    data = {
        'equation': 'x2+y2',
        'name': image.name
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def solve_3d_linear_equation(request):
    eq1 = request.data['equation1']
    eq2 = request.data['equation2']
    eq3 = request.data['equation3']
    data = {
        'x': 1,
        'y': 2,
        'z': 3,
        'solution_found': True
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def solve_2d_linear_equation(request):
    eq1 = request.data['equation1']
    eq2 = request.data['equation2']
    data = {
        'x': 1,
        'y': 2,
        'solution_found': True
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def solve_polynomial_equation(request):
    equation = request.data['equation']
    data = {
        'solution': [1, 2],
        'solution_type': 'linear'
    }
    return Response(data, status=status.HTTP_200_OK)
