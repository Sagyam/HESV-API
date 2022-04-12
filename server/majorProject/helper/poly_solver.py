import re
import numpy as np

DEBUG_LOGS = []


def add_leading_ones(eqn):
    '''
    This function takes add leading 1 to x
    Input: +x^3+x^2+x
    Output: +1x^3+1x^2+1x
    '''
    position_table = {}
    count = 0

    for i, char in enumerate(eqn):
        if char in ['x', 'X'] and eqn[i-1] in ['+', '-']:
            count += 1
            position_table[count] = i

    for key, value in position_table.items():
        eqn = eqn[:value+key-1] + '1' + eqn[value+key-1:]

    return eqn


def standardize_eqn(eqn):
    '''
    Standardizes an equation by removing = and shift's lone coeff to left
    and adds ^1 to the end of last term
    :param eqn: equation in the form of ax^b+cx^d+...+ex
    :return: equation in the form of ax^b+cx^d+...+ex^1
    :param equation: equation to standardize eg 2x^2+3x=7
    :return: standardized equation eg 2x^2+3x-7
    '''

    # Add a ^1 to the end of the last x
    for i, char in enumerate(eqn):
        if char in ['x', 'X'] and eqn[i+1] != '^':
            eqn = eqn[:i+1] + '^1' + eqn[i+1:]

    # Add a leading + at very beginning
    if eqn[0] != '-':
        eqn = '+'+eqn

    # add a leading 1 where necessary
    eqn = add_leading_ones(eqn)

    try:
        left, right = eqn.split('=')[0], eqn.split('=')[1]
    except IndexError:
        return eqn

    # remove = sign
    if right == '':
        return left
    elif right == '0':
        return left
    else:
        coeff = str(-1*float(right))
        if coeff[0] != '-':
            coeff = '+'+coeff
        eqn = left + coeff
        return eqn


def get_sorted_eqn(eqn):
    '''
    This function takes a unsorted polynomial equation and returns a sorted polynomial equation
    Note: If the sign of first term is postive, then it must be specified as +
    Eg: '2x+3=0' should be given as '+2x+3=0'
    '''
    # get the constant in the eqn
    try:
        number = re.findall(r'[+,-]\d\.\d$|[+,-]\d$', eqn)[0]
    except IndexError:
        number = ''

    # get all the terms in the equation
    terms = re.findall(r'[+,-]\d[x,X]\^\d|[+,-]\d\.\d[x,X]\^\d', eqn)
    # save the sign of the term in dictinary
    signs = {term[1:]: term[0] for term in terms}
    # remove first character from each term
    terms = [term[1:] for term in terms]
    # reverse the terms so power sorting is based on power
    terms = [term[::-1] for term in terms]
    # sort terms alphabetically
    terms = sorted(terms, reverse=True)
    # undo the reversing
    terms = [term[::-1] for term in terms]
    # now add the signs back to terms
    terms = [signs[term] + term for term in terms]
    sorted_eqn = ''.join(terms) + number
    return sorted_eqn


def get_visible_coeff(eqn):
    '''
    This function returns the coefficient of x in the equation
    The equation should be in the form of ax^b+cx^d+...+ex
    Notice that the last term need not contain '^'
    Eg. 5x will be treated as 5x^1
    The equation cannot contain '=' sign
    This function will not work for zero coefficients
    '''

    # remove all powers
    no_carets = re.sub(r"(\^\d+)", "", eqn)
    # get numeric coefficients
    raw_coeffs = re.findall(r'[\d\.\-\+]+', no_carets)
    # add a 1 to lone signs and convert coefficients to float
    coeffs = [float(x) for x in raw_coeffs]
    return coeffs


def get_powers(eqn):
    '''
    Returns all powers from eqn
    Eg: '2x^2+3x^2' will return [2,2]
    '''
    powers = []
    for x in re.findall(r'(\^\d+)', eqn):
        powers.append(int(x[1:]))
    return powers


def get_all_coeffs(eqn):
    '''
    Input: Polynomial equation in the form of ax^b+cx^d+...+ex
    Output: List of all coefficients (Even if they are zero)
    '''
    coeffs = get_visible_coeff(eqn)
    powers = get_powers(eqn)
    degree = max(powers)

    for i in range(degree, 0, -1):
        if i not in powers:
            coeffs.insert((degree-i), 0.0)
    return coeffs


def solve_polynomial_helper(equation):
    DEBUG_LOGS = []

    standardized_eqn = standardize_eqn(equation)
    DEBUG_LOGS.append(f'Standardized equation: {standardized_eqn}')

    sorted_eqn = get_sorted_eqn(standardized_eqn)
    DEBUG_LOGS.append(f'Sorted equation: {sorted_eqn}')

    coefficents = get_all_coeffs(sorted_eqn)
    DEBUG_LOGS.append(f'Coefficients: {coefficents}')

    solutions = np.roots(coefficents)
    solutions = [round(x, 2) for x in solutions]

    DEBUG_LOGS.append(f'Solutions: {solutions}')

    soln_type = 'real' if np.isreal(solutions).all() else 'complex'
    if soln_type == 'complex':
        solutions = [str(solution.real) + '+i' + str(solution.imag)
                     for solution in solutions]
    return solutions, soln_type, DEBUG_LOGS
