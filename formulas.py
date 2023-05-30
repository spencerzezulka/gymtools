import streamlit as st
import numpy as np
import pandas as pd
# import astropy.units as u
# import astropy.constants as c
import altair as alt

class GymBro():
    def __init__(self, weight, reps, metric=True):
        self.weight = weight
        self.reps = reps
        self.metric = metric

class GymBroStats(GymBro):
    def __init__(self, weight, reps, metric=True, formula='Epley', max_reps_shown=30, rounded=False, round_down=True):
        super().__init__(weight=weight, reps=reps, metric=metric)
        self.formula = formula
        self.rep_array = self.create_rep_array(max_reps_shown)
        self.max = self.calculate_1rm()
        self.round_down=round_down
        self.weight_array = self.calculate_weights(formula=formula, rounded=rounded, round_down=self.round_down)
        self.reps_to_weight = dict(zip(self.rep_array, self.weight_array))

    def create_rep_array(self, max_reps_shown: int):
        return np.arange(start=1, stop=max_reps_shown+1, step=1, dtype=int)

    def epley(self):
        '''
        Return Epley Formula 1RM.
        Pros: Commonly-used formula.
        Cons: Fails if inputting 1RM trivially (slight offset for low reps)
        '''
        if self.reps == 1:
            return self.weight
        return np.multiply(self.weight, np.add(1, np.true_divide(self.reps, 30)))

    def brzycki(self):
        '''
        Return Brzycki Formula 1RM.
        Pros: Commonly-used formula.
        Cons: Approximation poor for high reps (reps approaching 37).
        '''
        if self.reps >= 37:
            raise Exception("Brzycki Formula fails for reps over 37.")
        return np.true_divide(np.multiply(self.weight, 36), np.subtract(37, self.reps))

    def kemmler(self):
        '''
        Return Kemmler Formula 1RM.
        Pros: Polynomial terms make robust to low and high reps.
        Cons: Approximation poor for high reps (reps approaching 37).
        '''
        return np.multiply(self.weight, (0.988+0.0104*self.reps+0.00190*self.reps**2-0.0000584*self.reps**3))

    def calculate_1rm(self):
        if self.formula == 'Epley':
            return self.epley()
        elif self.formula == 'Brzycki':
            return self.brzycki()
        elif self.formula == 'Kemmler':
            return self.kemmler()
        else:
            raise ValueError(f"Invalid formula: {self.formula}")
    
    def rounding_function(self, result, rounding_increment, round_down=True):
        return rounding_increment*np.floor(result/rounding_increment) if round_down else rounding_increment*np.round(result/rounding_increment)

    def reverse_epley(self, max: int, desired_reps: int, rounded=False, rounding_increment=5, round_down=True):
        '''
        Return weight and rep pairing given by Epley formula.
        Pros: Commonly-used formula.
        Cons: Fails if inputting 1RM trivially (slight offset for low reps)
        '''
        if desired_reps <= 0:
            raise Exception("Rep count must be 1 or greater.")
        if desired_reps == 1:
            return self.rounding_function(max, rounding_increment, round_down) if rounded else max
        else:
            result = max / (1 + desired_reps / 30)
            return self.rounding_function(result, rounding_increment, round_down) if rounded else result
            
    def reverse_brzycki(self, max: int, desired_reps: int, rounded=False, rounding_increment=5, round_down=True):
        '''
        Return weight and rep pairing given by Brzycki formula.
        Pros: Commonly-used formula. 
        Cons: Approximation poor for high reps (reps approaching 37).
        '''
        if desired_reps <= 0:
            raise Exception("Rep count must be 1 or greater.")
        if desired_reps >= 37:
            raise Exception("Brzycki Formula fails for reps over 37.")
        else:
            result = max * ((37 - desired_reps) / 36)
            return self.rounding_function(result, rounding_increment, round_down) if rounded else result


    def reverse_kemmler(self, max: int, desired_reps: int, rounded=False, rounding_increment=5, round_down=True):
        '''
        Return weight and rep pairing given by Kemmler formula.
        Pros: Polynomial terms make robust to low and high reps.
        Cons: Approximation poor for high reps (reps approaching 37).
        '''
        if desired_reps <= 0:
            raise Exception("Rep count must be 1 or greater.")
        else:
            result = max / (0.988 + 0.0104 * desired_reps + 0.00190 * desired_reps ** 2 - 0.0000584 * desired_reps ** 3)
            return self.rounding_function(result, rounding_increment, round_down) if rounded else result

    # def plates_calculator(weight, available_plate_weights=[2.5, 5, 10, 25, 45], bar_weight=45, unit='lbs') -> defaultdict:
    #     weight = weight-bar_weight
    #     available_plate_weights.sort(reverse=True)
    #     plate_map = defaultdict(int)
    #     for plate_weight in available_plate_weights:
    #         while weight-2*plate_weight>=0:
    #             plate_map[plate_weight]+=2
    #             weight-=2*plate_weight
    #     if weight!=0:
    #         print(f'missing {weight} {unit}')
    #     return plate_map


    def calculate_weights(self, round_down=True, formula: str='Epley', rounded=False):
        """
        Generate an array of weights for each rep count based on the selected formula.
        """
        if formula == 'Epley':
            return [self.reverse_epley(self.max, rep_count, round_down=round_down, rounded=rounded) for rep_count in self.rep_array]
        elif formula == 'Brzycki':
            return [self.reverse_brzycki(self.max, rep_count, round_down=round_down, rounded=rounded) for rep_count in self.rep_array]
        elif formula == 'Kemmler':
            return [self.reverse_kemmler(self.max, rep_count, round_down=round_down, rounded=rounded) for rep_count in self.rep_array]
        else:
            raise ValueError("Invalid formula. Choose either 'Epley', 'Brzycki' or 'Kemmler'.")
