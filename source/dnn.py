'''
File name: dnn.py
    Deep Neural Network (DNN) traffic forecast implementation.
           
Author: Vasileios Saveris
email: vsaveris@gmail.com

License: MIT

Date last modified: 11.04.2020

Python Version: 3.8
'''

# My packages
import utils as ut
from model import MODEL
from mpt import MPT

# Sklearn imports
from sklearn.metrics import r2_score
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV, PredefinedSplit
from sklearn.model_selection import PredefinedSplit

# Matplotlib for graphs
import matplotlib.pyplot as plt


class DNN(MODEL):
    '''
    DNN class implementation.

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
    
    def __init__(self, model_params = None, verbose = False):
    
        self._verbose = verbose
        
        if self._verbose:
            print('- MLPRegressor initialization: ', 
                ut.formatArguments(locals().items(), 'self'), sep = '')
        
        if model_params is None:
            self._model = MLPRegressor()
            
        else:
            self._model = MLPRegressor(
                hidden_layer_sizes = model_params['hidden_layer_sizes'],
                activation = model_params['activation'],
                solver = model_params['solver'],
                learning_rate = model_params['learning_rate'],
                learning_rate_init = model_params['learning_rate_init'],
                max_iter = model_params['max_iter'],
                shuffle = model_params['shuffle'])
        
        
    def train(self, data):
        '''
        Trains the model with the input data.
    
        Args:
            data (pandas DataFrame): The training data.
            
        Raises:
            -

        Returns:
            -
        '''
        
        self._model.fit(data.iloc[:, :-1].values, data.iloc[:, -1].values)
        
        
    def predict(self, data):
        '''
        Returns predictions for the input data.
    
        Args:
            data (Numpy Array): The input features for which a prediction is 
                requested.
            
        Raises:
            -

        Returns:
            Numpy Array: Predictions for the input data.
        '''
        
        return self._model.predict(data.iloc[:, :-1].values)
        
    
    def _calculateTestScore(self, model, data):
        '''
        Returns the r2 score for the test data, after fitting the model with the
        train data.
    
        Args:
            model (MLPRegressor): The MLPRegressor object to be used.
            
            data (dictionary): Contains the train_data and test_data, as keys
                of the dictionary. Their values are pandas DataFrames.
            
        Raises:
            -

        Returns:
            float: r2 score for the prediction of the test data.
        '''
        
        train_data = data['train_data']
        test_data = data['test_data']
        
        model.fit(train_data.iloc[:, :-1], train_data.iloc[:,-1])
        
        return r2_score(test_data.iloc[:, -1], 
            model.predict(test_data.iloc[:, :-1]))
            
            
    def _calculateTrainTestScore(self, model, data):
        '''
        Returns the r2 score for the train and the test data, after fitting the 
        model with the train data.
    
        Args:
            model (MLPRegressor): The MLPRegressor object to be used.
            
            data (dictionary): Contains the train_data and test_data, as keys
                of the dictionary. Their values are pandas DataFrames.
            
        Raises:
            -

        Returns:
            float: r2 score for the prediction of the train data.
            
            float: r2 score for the prediction of the test data.
        '''
        
        train_data = data['train_data']
        test_data = data['test_data']
        
        model.fit(train_data.iloc[:, :-1], train_data.iloc[:,-1])
            
        return r2_score(train_data.iloc[:, -1], 
            model.predict(train_data.iloc[:, :-1])),\
            r2_score(test_data.iloc[:, -1],
            model.predict(test_data.iloc[:, :-1]))

    
    def explore(self, train_data, test_data, exec_time_stamp):
        '''
        Performs model selections with hyperparameters tunning.
    
        Args:
            train_data (pandas DataFrame): The training data.
            
            test_data (pandas DataFrame): The test data.
            
            exec_time_stamp (string): Signature for the saved graph.
            
        Raises:
            -

        Returns:
            float: The best score
            
            dictionary: Best performing parameters. Keys are 
                ('hidden_layer_sizes', 'activation', 'solver', 'learning_rate', 
                'learning_rate_init', 'max_iter', 'shuffle') 
        '''

        # Prepare train/test folds for GridSearchCV
        data = train_data.copy()
        data = data.append(test_data)
        
        # Use a single test fold
        test_fold = [-1]*len(train_data.index) + [1]*len(test_data.index)
        ps = PredefinedSplit(test_fold)

        # Grid search to some of the model's parameters
        params = {
            'hidden_layer_sizes': [(100,)*i for i in range(2, 8)],
            'activation': ['identity', 'logistic', 'tanh', 'relu'],
            'solver': ['lbfgs', 'adam'],
            'learning_rate': ['constant', 'adaptive'],
            'learning_rate_init': [0.01, 0.001, 0.0001],
            'max_iter': [200],
            'shuffle': [False], 'random_state': [1]}
             
        gs = GridSearchCV(estimator = MLPRegressor(), param_grid = params, 
            scoring = 'r2', n_jobs = -1, refit = True, cv = ps, verbose = 1)
         
        gs.fit(data.iloc[:, :-1], data.iloc[:,-1])
            
        best_score = gs.best_score_
        best_params = gs.best_params_
        
        print('- Evaluation Step 1: best_score = ', best_score, sep = '')
        print('- Evaluation Step 1: best_params = ', best_params, sep = '')

        # Explore different sizes of hidden layers
        models = []
        scores = []
        hidden_layer_sizes = []

        for i in range(2, 201):  
            hidden_layer_sizes.append((i,)*len(best_params['hidden_layer_sizes']))
            
            models.append(MLPRegressor(
                hidden_layer_sizes = hidden_layer_sizes[-1], 
                activation = best_params['activation'], 
                solver = best_params['solver'],
                learning_rate = best_params['learning_rate'], 
                learning_rate_init = best_params['learning_rate_init'],
                max_iter = best_params['max_iter'], 
                shuffle = best_params['shuffle'], random_state=1))
        
        # Use multi process class for parallel executing of the tasks
        scores = MPT(iteratable = models, task = self._calculateTestScore, 
            processes = None, verbose = True, train_data = train_data, 
            test_data = test_data).execute()
        
        best_score = max(scores)
        best_params['hidden_layer_sizes'] = \
            hidden_layer_sizes[scores.index(best_score)]
        
        print('- Evaluation Step 2: best_score = ', best_score, sep = '')
        print('- Evaluation Step 2: best_params = ', best_params, sep = '')

        # Explore number of iterations
        models = []
        train_scores = []
        test_scores = []

        for i in range(100, 501):
            models.append(MLPRegressor(
                hidden_layer_sizes = best_params['hidden_layer_sizes'], 
                activation = best_params['activation'], 
                solver = best_params['solver'],
                learning_rate = best_params['learning_rate'], 
                learning_rate_init = best_params['learning_rate_init'],
                max_iter = i, 
                shuffle = best_params['shuffle'], random_state=1))
        
        # Use multi process class for parallel executing of the tasks
        scores = MPT(iteratable = models, task = self._calculateTrainTestScore, 
            processes = None, verbose = True, train_data = train_data, 
            test_data = test_data).execute()
        
        train_scores = [s[0] for s in scores]
        test_scores  = [s[1] for s in scores]
        
        best_score = max(test_scores)
        best_params['max_iter'] = test_scores.index(best_score) + 100
        
        plt.clf()
        plt.plot(list(range(100, 501)), train_scores, color = 'green', 
            label = 'train score')
        plt.plot(list(range(100, 501)), test_scores, color = 'red', 
            label = 'test score')
        
        plt.legend(loc = 'best', fontsize = 8)
        plt.title('Train and Test score per iteration: score = ' +\
            str(round(best_score, 3)) + ', iter = ' +\
            str(best_params['max_iter']))
        plt.savefig('../graphs/forecasts/evaluate_ETT_' +\
            exec_time_stamp + '.png')
        
        print('- Evaluation Step 3: best_score = ', best_score, sep = '')
        print('- Evaluation Step 3: best_params = ', best_params, sep = '')

        # Train the model with the best set of hyperparameters
        self._model = models[test_scores.index(best_score)]
        self._model.fit(train_data.iloc[:, :-1], train_data.iloc[:,-1])
        
        return best_score, best_params