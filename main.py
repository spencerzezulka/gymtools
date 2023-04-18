import streamlit as st
import numpy as np
import pandas as pd
import astropy.units as u
import astropy.constants as c
import altair as alt

class GymBro():
    def __init__(self, weight, reps):
        self.weight = weight
        self.reps = reps

    def epley(self, weight: float, reps: int) -> np.float32: 
        '''
        Return Epley Formula 1RM.
        Pros: Commonly-used formula.
        Cons: Fails if inputting 1RM trivially (slight offset for low reps)
        '''
        if reps==1:
            return weight
        return np.multiply(weight, np.add(1, np.true_divide(reps, 30)))


    def brzycki(self, weight: float, reps: int) -> np.float32: 
        '''
        Return Brzycki Formula 1RM.
        Pros: Commonly-used formula.
        Cons: Approximation poor for high reps (reps approaching 37).
        '''
        if reps>=37:
            raise Exception("Brzycki Formula fails for reps over 37.")
        return np.true_divide(np.multiply(weight, 36), np.subtract(37, reps))

    def kemmler(self, weight: float, reps: int) -> np.float32: 
        '''
        Return Kemmler Formula 1RM.
        Pros: Polynomial terms make robust to low and high reps.
        Cons: Approximation poor for high reps (reps approaching 37).
        '''
        return np.multiply(weight, (0.988+0.0104*reps+0.00190*reps**2-0.0000584*reps**3))