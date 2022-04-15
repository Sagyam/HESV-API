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
    try:
        image = request.data['image']
    except KeyError:
        data = {'error': 'No image provided'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    equation, desmos_eqn,DEBUG_LOGS = get_poly_equation(image)
    data = {
        'equation': equation,
        'desmos_eqn': desmos_eqn,
        'debug_logs': DEBUG_LOGS
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_linear_equation(request):
    try:
        image = request.data['image']
    except KeyError:
        data = {'error': 'No image provided'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    equation, DEBUG_LOGS = get_lin_equation(image)

    data = {
        'equation': equation,
        'debug_logs': DEBUG_LOGS,

    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def solve_3d_linear_equation(request):
    try:
        eq1 = request.data['equation1']
        eq2 = request.data['equation2']
        eq3 = request.data['equation3']
    except KeyError:
        data = {'error': 'Missing equation'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    soln, error, errorMessage, warningMessage, DEBUG_LOGS = solve_3d([eq1, eq2, eq3])

    data = {
        'x': soln[0] if soln is not None else None,
        'y': soln[1] if soln is not None else None,
        'z': soln[2] if soln is not None else None,
        'error': error,
        "errorMessage": errorMessage,
        "warningMessage": warningMessage,
        "debug_logs": DEBUG_LOGS,
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def solve_2d_linear_equation(request):
    try:
        eq1 = request.data['equation1']
        eq2 = request.data['equation2']
    except KeyError:
        data = {'error': 'Missing equation'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    soln, error, errorMessage, warningMessage, DEBUG_LOGS = solve_2d([eq1, eq2])

    data = {
        'x': soln[0] if soln is not None else None,
        'y': soln[1] if soln is not None else None,
        'error': error,
        "errorMessage": errorMessage,
        "warningMessage": warningMessage,
        "debug_logs": DEBUG_LOGS,
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def solve_polynomial_equation(request):
    try:
        equation = request.data['equation']
    except KeyError:
        data = {'error': 'No equation provided'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    solutions, soln_type, DEBUG_LOGS = solve_polynomial_helper(equation)

    data = {
        'solutions': solutions,
        'solution_type': soln_type,
        "debug_logs": DEBUG_LOGS
    }
    return Response(data, status=status.HTTP_200_OK)
