import re
import numpy as np


DEBUG_LOGS = []


def contains_nums(string):
    return any(i.isdigit() for i in string)


def standardize_eqn(equation):
    """
    Standardizes an equation by removing = and shift intercept to left.
    :param equation: equation to standardize eg 2x+3y=7
    :return: standardized equation eg 2x+3y-7
    """
    left, right = equation.split('=')[0], equation.split('=')[1]

    left_sub = re.sub("[+-]?\d+[XxYyZz]|[+-]?\d+\.\d+[XxYyZz]", "", left)

    if left_sub == '':
        intercept = -1 * float(right)
        if intercept > 0.0:
            intercept = '+' + str(intercept)
        equation = left + str(intercept)

    elif left_sub == left:
        intercept = -1 * float(right)
        if intercept > 0.0:
            intercept = '+' + str(intercept)
        equation = left + str(intercept)

    elif contains_nums(left_sub):
        equation = left

    elif not contains_nums(left_sub):
        intercept = -1 * float(right)
        if intercept > 0.0:
            intercept = '+' + str(intercept)
        equation = left + str(intercept)

    else:
        equation = left
 

    return equation


def get_coffecient_2d(equation):
    """
    Returns the coefficients and intercept of the 2nd degree term in an equation.
    :param : eg: 2x+3y=7
    :return: eg: (2,3,7)
    """
    try:
        coef_x = re.findall('-?[0-9.]*[Xx]', equation)[0][:-1]
    except:
        coef_x = 0.0

    try:
        coef_y = re.findall('-?[0-9.]*[Yy]', equation)[0][:-1]
    except:
        coef_y = 0.0

    intercept = re.sub("[+-]?\d+[XxYy]|[+-]?\d+\.\d+[XxYy]", "", equation)
    intercept = re.findall('[+-]+\d+', intercept)[0]

    if coef_x == '':
        coef_x = 1.0
    elif coef_x == '-':
        coef_x = -1.0

    if coef_y == '':
        coef_y = 1.0
    elif coef_y == '-':
        coef_y = -1.0

 
    return [float(coef_x), float(coef_y), float(intercept)]


def get_coffecient_3d(equation):
    """
    Returns the coefficients and intercept of the 2nd degree term in an equation.
    :param : eg: 2x+3y=7
    :return: eg: (2,3,7)
    """
    try:
        coef_x = re.findall('-?[0-9.]*[Xx]', equation)[0][:-1]
    except:
        coef_x = 0.0

    try:
        coef_y = re.findall('-?[0-9.]*[Yy]', equation)[0][:-1]
    except:
        coef_y = 0.0

    try:
        coef_z = re.findall('-?[0-9.]*[Zz]', equation)[0][:-1]
    except:
        coef_z = 0.0

    intercept = re.sub("[+-]?\d+[XxYyZz]|[+-]?\d+\.\d+[XxYyZz]", "", equation)
    intercept = re.findall('[+-]+\d+', intercept)[0]

    if coef_x == '':
        coef_x = 1.0
    elif coef_x == '-':
        coef_x = -1.0

    if coef_y == '':
        coef_y = 1.0
    elif coef_y == '-':
        coef_y = -1.0

    if coef_z == '':
        coef_z = 1.0
    elif coef_z == '-':
        coef_z = -1.0

    
    return [float(coef_x), float(coef_y), float(coef_z), float(intercept)]


def isOverDetermined(equations):
    '''
    Checks if the equations does not contain z or Z.
    '''
    for eq in equations:
        if 'z' in eq or 'Z' in eq:
            return False
    return True
      

def isUnderDetermined(equations):
    '''
    Checks if the equations contains z or Z.
    '''
    for eq in equations:
        if 'z' in eq or 'Z' in eq:
            return True
    return False

def solve_2d(equation):
    a = []
    b = []
    errorMessage = None
    warningMessage = None
    soln = None

    if isUnderDetermined(equation):
        errorMessage = "Under-Determined System"
        error = True
        return [soln, error, errorMessage, warningMessage, DEBUG_LOGS]

    for i, eqn in enumerate(equation):
        std_eqn = standardize_eqn(eqn)
        x, y, c = get_coffecient_2d(std_eqn)
        a.append([x, y])
        b.append(c)

    a, b = np.asanyarray(a), np.asanyarray(b)
    DEBUG_LOGS.append(f'std_eqn: {std_eqn}, a: {a}, b: {b}')

    try:
        soln = np.linalg.solve(a, b)
        soln = [round(x, 2) for x in soln]
        #Quick Hack
        soln = [-1 * x for x in soln]
        error = False
    except Exception as e:
        try:
            warningMessage = 'No exact solution.'
            soln = np.dot(np.linalg.pinv(a), b)
            soln = [round(x, 2) for x in soln]
            #Quick Hack
            soln = [-1 * x for x in soln]
            error = False
        except Exception as e:
            soln = None
            errorMessage = 'System is not Solvable.'
            error = True
    return [soln, error, errorMessage, warningMessage, DEBUG_LOGS]


def solve_3d(equation):
    a = []
    b = []
    errorMessage = None
    warningMessage = None
    soln = None

    if isOverDetermined(equation):
        warningMessage = "Over-Determined System"
        

    for i, eqn in enumerate(equation):
        std_eqn = standardize_eqn(eqn)
        x, y, z, c = get_coffecient_3d(std_eqn)
        a.append([x, y, z])
        b.append(c)

    a, b = np.asanyarray(a), np.asanyarray(b)
    DEBUG_LOGS.append(f'std_eqn: {std_eqn}, a: {a}, b: {b}')

    try:
        soln = np.linalg.solve(a, b)
        soln = [round(x, 2) for x in soln]
        #Quick Hack
        soln = [-1 * x for x in soln]
        error = False
    except Exception as e:
        try:
            errorMessage = 'No exact solution'
            soln = np.dot(np.linalg.pinv(a), b)
            #Quick Hack
            soln = [-1 * x for x in soln]
            soln = [round(x, 2) for x in soln]
            error = True
        except Exception as e:
            soln = None
            errorMessage = 'System is not Solvable.'
            error = True

    return [soln, error, errorMessage, warningMessage, DEBUG_LOGS]
