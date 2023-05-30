import sys
sys.path.append('..')
from .. import formulas

import unittest

class TestFormulas(unittest.TestCase):
    def setUp(self):
        self.lifter = formulas.GymBroStats(135, 5)

    def test_epley(self):
        self.lifter.epley() == 157.5

if __name__ == '__main__':
    unittest.main()

    
    # def test_reverse_epley(self):
        # self.lifter.reverse_epley()[0] == self.lifter.epley()
    
    # def test_kemmler(self):


# print('GymBro Test is Working!')
# winston_stats = formulas.GymBroStats(135, 5)
# print(f'Max: {winston_stats.max}')
# print(f'Weight Array: {winston_stats.weight_array}')
# print(f'Rep Array: {winston_stats.rep_array}')
# print(f'Reps and Corresponding Weights: {dict(zip(winston_stats.rep_array, winston_stats.weight_array))}')