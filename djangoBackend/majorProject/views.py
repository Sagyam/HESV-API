from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view

from .helper.linear_solver import *
from .helper.linear_detector import *
from .helper.poly_solver import *
from .helper.poly_detector import *


@api_view(['POST'])
def get_polynomial_equation(request):
    image = request.data['image']

    data = {
        'equation': 'x3+y3+z3',
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
    try:
        eq1 = request.data['equation1']
        eq2 = request.data['equation2']
        eq3 = request.data['equation3']
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    soln, error, errorMessage, warningMessage = solve_3d([eq1, eq2, eq3])

    data = {
        'x': soln[0],
        'y': soln[1],
        'z': soln[2],
        'error': error,
        "errorMessage": errorMessage,
        "warningMessage": warningMessage
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def solve_2d_linear_equation(request):
    try:
        eq1 = request.data['equation1']
        eq2 = request.data['equation2']
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    soln, error, errorMessage, warningMessage = solve_2d([eq1, eq2])

    data = {
        'x': soln[0],
        'y': soln[1],
        'error': error,
        "errorMessage": errorMessage,
        "warningMessage": warningMessage
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def solve_polynomial_equation(request):
    try:
        equation = request.data['equation']
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    solutions, soln_type = solve_polynomial_helper(equation)

    data = {
        'solutions': solutions,
        'solution_type': soln_type
    }
    return Response(data, status=status.HTTP_200_OK)
