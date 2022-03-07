from cgi import test
from django.test import TestCase
from os import walk
import cv2

from .helper.poly_solver import solve_polynomial_helper
from .helper.linear_solver import solve_2d, solve_3d
from .helper.poly_detector import get_poly_eqn_test
from .helper.linear_detector import get_lin_equation_test

from .test.polynomial_test_case import poly_test_eqn
from .test.two_d_linear_cases import two_d_linear_eqn
from .test.three_d_linear_cases import three_d_linear_eqn
from .test import linear_key
from .test import poly_key


class TestMajorProject(TestCase):

    def test_poly_detector(self):
        for (dirpath, dirnames, filenames) in walk('./majorProject/test/poly_images'):
            for filename in filenames:
                image = cv2.imread(f'{dirpath}/{filename}')
                eqn = get_poly_eqn_test(image)
                true_eqn = poly_key.eqns[filename]
                self.assertEqual(eqn, true_eqn)

    def test_linear_detector(self):
        for (dirpath, dirnames, filenames) in walk('./majorProject/test/linear_images'):
            for filename in filenames:
                image = cv2.imread(f'{dirpath}/{filename}')
                eqn = get_lin_equation_test(image)
                true_eqn = linear_key.eqns[filename]
                self.assertEqual(eqn, true_eqn)

    def test_poly_solver(self):
        for test_name, test_data in poly_test_eqn.items():
            eqn = test_data['eqn']
            true_soln = test_data['soln']
            soln = solve_polynomial_helper(eqn)[0]
            self.assertEqual(soln, true_soln)

    def test_2d_solver(self):
        for test_name, test_data in two_d_linear_eqn.items():
            eqns = test_data['eqns']
            true_soln_x = test_data['soln']['x']
            true_soln_y = test_data['soln']['y']
            soln_x, soln_y = solve_2d(eqns)[0]
            self.assertEqual(soln_x, true_soln_x)
            self.assertEqual(soln_y, true_soln_y)

    def test_3d_solver(self):
        for test_name, test_data in three_d_linear_eqn.items():
            eqns = test_data['eqns']
            true_soln_x = test_data['soln']['x']
            true_soln_y = test_data['soln']['y']
            true_soln_z = test_data['soln']['z']
            soln_x, soln_y, soln_z = solve_3d(eqns)[0]
            self.assertEqual(soln_x, true_soln_x)
            self.assertEqual(soln_y, true_soln_y)
            self.assertEqual(soln_z, true_soln_z)
