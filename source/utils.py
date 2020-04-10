'''
File name: utils.py
    Utilities script for the traffic forecast flow.
           
Author: Vasileios Saveris
email: vsaveris@gmail.com

License: MIT

Date last modified: 10.04.2020

Python Version: 3.8
'''

# Python packages
from joblib import dump, load

# SjLearn packages
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.model_selection import TimeSeriesSplit, train_test_split


def formatArguments(args, exclude = None):
    '''
    Prepares a formatted string of the input arguments dictionary.
    
    Args:
        args (dictionary): A dictionary with arguments: values pairs.
        
        exclude (list of strings, default is None): Arguments to be excluded
            from the formatted string.
        
    Raises:
        -

    Returns:
        string: A formatted string of the input arguments in the form of
            argument = value, ...
    '''
    
    if not isinstance(exclude, list):
        exclude = [exclude]
        
    av_pairs = [k + ' = ' + str(v) for k, v in args if k not in exclude]
        
    return ', '.join(av_pairs)
    
        
def splitData(data, split_size):
    '''
    Splits data in two chunks.
    
    Args:
        data (DataFrame): The input data to be splitted.
        
        split_size (float): Percentage of split. First chunk contains 1-x portion
            of the input data and the second chunk contains x portion of the
            input data.
        
    Raises:
        -

    Returns:
        DataFrame: First chunk of the data (1-x portion)
        DataFrame: Secind chunk of the data (x portion)
    '''
    
    return train_test_split(data, test_size = test_size, shuffle = False)


def normalizeData(data):
    '''
    Scaling data to have unit norm. 
    
    Args:
        data (DataFrame): The input data to be normalized.
        
    Raises:
        -

    Returns:
        DataFrame: Nomralized data.
    '''
    
    return Normalizer().transform(data)


def standardizeData(data, save_scaler_file = None, load_scaler_file = None):
    '''
    Scaling data to have zero mean and unit variance.
    
    Args:
        data (DataFrame): The input data to be standardized.
        
        save_scaler_file (string): The file to dump the scaler, for later use.
        
        load_scaler_file (string): Load dumped scaler instead of creating a new
            one.
        
    Raises:
        -

    Returns:
        DataFrame: Standardized data.
    '''
    
    if load_scaler_file is None:
        scaler = StandardScaler().fit(data)     
    else:
        scaler = load(load_scaler_file)
        
    if save_scaler_file is not None:
        dump(scaler, save_scaler_file)
    
    return scaler.transform(data)
  

def timeSeriesCV(data, splits = 5):
    '''
    Create Time Series Cross Validation indices for the input data.
    
    Args:
        data (DataFrame): The input data.
        
        splits (integer >= 2): The number of folds to be used.
        
    Raises:
        -

    Returns:
        generator: Indices of train and test data for each fold.
    '''
    
    return TimeSeriesSplit(n_splits = splits).split(data)