'''
File name: model.py
    Abstract class for models implementation.
           
Author: Vasileios Saveris
email: vsaveris@gmail.com

License: MIT

Date last modified: 10.04.2020

Python Version: 3.8
'''

from abc import ABC, abstractmethod

class MODEL(ABC):

    def __init__(self):
        pass
        
        
    @abstractmethod 
    def train(self):
        '''
        Method for training the model.
        '''
        pass
        
    
    @abstractmethod 
    def predict(self):
        '''
        Method for returning predictions using the trained model.
        '''
        pass
        
    
    @abstractmethod 
    def explore(self):
        '''
        Method for hyperparameters auto-tunning of the model.
        '''
        pass