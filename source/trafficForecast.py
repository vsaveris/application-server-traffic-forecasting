'''
File name: trafficForecast.py
    Traffic Forecast class implementation.
           
Author: Vasileios Saveris
email: vsaveris@gmail.com

License: MIT

Date last modified: 10.04.2020

Python Version: 3.8
'''

# My packages
import utils as ut
import lstm, rnn, dnn

# Python packages imports
from joblib import dump, load
from datetime import datetime

# Matplotlib for graphs
import matplotlib.pyplot as plt

# Sklearn imports
from sklearn.metrics import r2_score

# Pandas imports
import pandas as pd


'''
Constants
'''
C_SUPPORTED_MODELS = {'LSTM': lstm.LSTM, 'RNN': rnn.RNN, 'DNN': dnn.DNN}


class TF():
    '''
    Traffic forecast class implementation.

    Args:
        model_params (dictionary): The parameters of the sklearn MLPRegressor.
            Keys are ('hidden_layer_sizes', 'activation', 'solver', 
            'learning_rate', 'learning_rate_init', 'max_iter', 'shuffle')        
        
        verbose (boolean, default is False): If True print services are enabled.

    Public Attributes:
        -
        
    Private Attributes:
        See constructor (self._*)
                                
    Public Methods:
        
        train (args) -> None: Trains the model with the input data.
            
        predict (args) -> Numpy Array: Returns predictions for the input data.
            
        explore (args) -> float, dictionary: Performs model selections with
            hyperparameters tunning and return the best score and a dictionary
            with the best performing parameters.
        
    Private Methods:
        -
        
    Raises:
        -
        
    '''
    
    def __init__(self, input_file, test_split, verbose = False):
        
        self._verbose = verbose
        
        if self._verbose:
            print('\nTraffic Forecast initialization: ', 
                ut.formatArguments(locals().items(), 'self'), sep = '')
                        
        # Read input file
        input_data = pd.read_csv(input_file)
        
        if self._verbose:
            print('- Input data loaded, file = ', input_file, sep = '')
            
        # Create data sets from the input data
        self._train_data, self._test_data = \
            self._createDataSets(input_data, test_split)

        
    def _createDataSets(self, input_data, test_split):
        '''
        Split the input data to train and test sets.
    
        Args:
            input_data (pandas DataFrame): The input data.
            
            test_split (float): The percentage of the input data that should be 
                used as test data. The rest of the data (1. - test_split) will 
                be used as train data.
            
        Raises:
            -

        Returns:
            DataFrame: The train data.
            
            DataFrame: The test data.
        '''
        
        train_data, test_data = ut.splitData(input_data, test_split)
        
        if self._verbose:
            print('- Split input data to training and test set, test_size = ', 
                    test_split, sep = '')
            
        # Print details of data split
        if self._verbose:
            print('- Data sets prepared, training_size = ', len(train_data.index), 
                ', test_size = ', len(test_data.index), sep = '')
                
        return train_data, test_data
           
        
    def evaluate(self, normalize = False, standardize = False, model = None):
        '''
        Executes the evaluation flow for the given model family. The evaluation 
        flow is defined in detail in the class implementation of the model 
        family passed in the function (see C_SUPPORTED_MODELS.values()). In 
        general it is a hyperparameters tunning flow in which the best 
        performing set is returned.
    
        Args:
            normalize (boolean): Data normalization flag.
            
            standardize (boolean): Data standardization flag.
            
            model (string): The model family to be evaluated. One of the 
                C_SUPPORTED_MODELS.keys().
            
        Raises:
            -

        Returns:
            -
        '''

        if self._verbose:
            print('\nEvaluate model: ', ut.formatArguments(locals().items(), 
                'self'), sep = '')
                
        # Signature for the dumped files
        exec_time_stamp =  datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Validate inputs
        if model not in C_SUPPORTED_MODELS.keys():
            print('- Model \'', model, '\' is not supported. Supported models ',
                'are: ', C_SUPPORTED_MODELS, sep = '')
            return None
            
        if self._test_data is None:
            print('- Evaluation requires test data, currently test data set is ',
                self._test_data, sep = '')
            return None
        
        # Normalize data sets
        if normalize:
            self._train_data.iloc[:, :-1] = \
                ut.normalizeData(self._train_data.iloc[:, :-1])
        
            self._test_data.iloc[:, :-1] = \
                ut.normalizeData(self._test_data.iloc[:, :-1])

        # Standardize data sets
        if standardize:
            self._train_data.iloc[:, :-1] = \
                ut.standardizeData(self._train_data.iloc[:, :-1], 
                save_scaler_file = '../dumps/evaluate_scaler_' + 
                    exec_time_stamp + '.dump')
        
            self._test_data.iloc[:, :-1] = \
                ut.standardizeData(self._test_data.iloc[:, :-1], 
                load_scaler_file = '../dumps/evaluate_scaler_' + 
                    exec_time_stamp + '.dump')

        # Run evaluation (grid search)
        model = C_SUPPORTED_MODELS[model](verbose = self._verbose)
        best_score, best_params = model.explore(self._train_data, 
            self._test_data, exec_time_stamp)

            
        print('- Evaluation best score: ', best_score, sep = '')
        print('- Evaluation best params: ', best_params, sep = '')
        
        # Plot training, test and forecast data
        forecast = self._test_data.copy()
        forecast.iloc[:, -1] = model.predict(self._test_data)
        
        plt.clf()
        plt.plot(self._train_data.iloc[:, -1], color = 'midnightblue', 
            label = 'train data')
        plt.plot(self._test_data.iloc[:, -1], color = 'orangered', 
            label = 'test data')
        plt.plot(forecast.iloc[:, -1], color = 'black', label = 'forecast', 
            linewidth = 0.5 )
        plt.legend(loc = 'best', fontsize = 8)
        plt.title('Evaluation Train/Test/Forecast score: ' +\
            str(round(r2_score(self._test_data.iloc[:, -1], 
            forecast.iloc[:, -1]), 3)))
        plt.savefig('../graphs/forecasts/evaluate_TTF_' + exec_time_stamp + '.png')     
        
        plt.clf()
        plt.plot(self._test_data.iloc[:, -1], color = 'orangered', 
            label = 'test data')
        plt.plot(forecast.iloc[:, -1], color = 'black', label = 'forecast', 
            linewidth = 0.5 )
        plt.legend(loc = 'best', fontsize = 8)
        plt.title('Evaluation Test/Forecast score: ' +\
            str(round(r2_score(self._test_data.iloc[:, -1], 
            forecast.iloc[:, -1]), 3)))
        plt.savefig('../graphs/forecasts/evaluate_TF_' + exec_time_stamp + '.png') 