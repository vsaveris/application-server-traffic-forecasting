'''
File name: runForecast.py
    Run traffic forecast script.
           
Author: Vasileios Saveris
email: vsaveris@gmail.com

License: MIT

Date last modified: 10.04.2020

Python Version: 3.8
'''

import sys, argparse
import trafficForecast as tf

'''
Constants
'''
# Examples text to be shown with the -h input option 
C_EXAMPLES = 'Usage Examples:\n\n1. Hyperparameters selection for DNN model ' +\
    '(20% of the data used as test set)\n$python runForecast.py -t '          +\
    'evaluate -f ../data/processed/traffic_stats_HOURLY_CHs.csv -m DNN\n'     +\
    '\n2. Train a DNN model for the input data and save the trained model on' +\
    ' disk\n$python runForecast.py -t train -f ../data/processed/traffic_'    +\
    'stats_HOURLY_CHs.csv -m DNN\n\n3. Make a forecast using a trained model' +\
    ' model for some time intervals\n$python runForecast.py -t forecast -d '  +\
    '../dumps/RNN_20200410193302.dump -i 240\n'

# Type of data preprocessing per model
C_MODEL_PREPROCESSING = {'DNN': {'NORMALIZATION': True, 'STANDARDIZATION': True},
    'RNN':  {'NORMALIZATION': False, 'STANDARDIZATION': False},
    'LSTM': {'NORMALIZATION': False, 'STANDARDIZATION': False}}


def parseInputArguments():
    '''
    Parses the input arguments.
    
    Args:
        -
        
    Raises:
        -

    Returns:
        namespace: The input arguments passed.
    '''

    args_parser = argparse.ArgumentParser(description = 'Run traffic forecast', 
        epilog = C_EXAMPLES, formatter_class = argparse.RawTextHelpFormatter)
    
    args_parser.add_argument('-t', action = 'store', required = True, 
        help = 'execution type, one of \'evaluate\', \'train\', \'forecast\'',
        choices = ('evaluate', 'train', 'forecast'), metavar = 'type')
    
    args_parser.add_argument('-f', action = 'store', required = False, 
        help = 'input data file', metavar = 'file')

    args_parser.add_argument('-m', action = 'store', required = False, 
        #help = 'model to be used for the traffic forecast, one of \'RNN\', '+\
        #'\'LSTM\', required when type (-t) is \'train\' or \'evaluate\'',
        help = 'model to be used for the traffic forecast, currently only '  +\
        '\'DNN\' has been implemented and supported, argument is required '  +\
        'when type (-t) is \'train\' or \'evaluate\'',
        choices = ('DNN'), metavar = 'model')
                            
    args_parser.add_argument('-d', action = 'store', required = False, 
        help = 'saved trained model to be loaded, required when type (-t) is '+\
        '\'forecast\'', metavar = 'dump')
                            
    args_parser.add_argument('-i', action = 'store', required = False, 
        help = 'prediction time intervals, required when type (-t) is '+\
        '\'forecast\'', metavar = 'intervals')

    return args_parser.parse_args()
    

def validateInputArguments(input_arguments):
    '''
    Validates the input arguments.
    
    Args:
        input_arguments (namespace): The given input arguments.
        
    Raises:
        ValueError: When dependencies are not staisfied.

    Returns:
        -
    '''
    
    if input_arguments.t in ['train', 'evaluate']:
        if input_arguments.f is None:
            raise ValueError('Input data file (-f) should be given for ' +\
                'execution type \'' + input_arguments.t + '\'')
        
        if input_arguments.m is None:
            raise ValueError('Model (-m) should be given for ' +\
                'execution type \'' + input_arguments.t + '\'')
                   
    if input_arguments.t == 'forecast':
        if input_arguments.d is None or input_arguments.i is None:
            raise ValueError('Saved trained model to be loaded (-d) and '+\
                'Prediction time intervals (-i) should be given for '    +\
                'execution type \'' + input_arguments.t + '\'')\
                

if __name__ == '__main__':
    
    # Read and validate input arguments
    input_arguments = parseInputArguments()   
    validateInputArguments(input_arguments)
    
    # Execute the requested flow
    if input_arguments.t == 'train':
        traffic_forecast = tf.TF(input_file = input_arguments.f, verbose = True)
        
        traffic_forecast.train(
            normalize = C_MODEL_PREPROCESSING[input_arguments.m]['NORMALIZATION'], 
            standardize = C_MODEL_PREPROCESSING[input_arguments.m]['STANDARDIZATION'], 
            model = input_arguments.m)
            
    elif input_arguments.t == 'evaluate':
        traffic_forecast = tf.TF(input_file = input_arguments.f, 
            test_split = (True, 0.20), verbose = True)
        
        traffic_forecast.evaluate(
            normalize = C_MODEL_PREPROCESSING[input_arguments.m]['NORMALIZATION'], 
            standardize = C_MODEL_PREPROCESSING[input_arguments.m]['STANDARDIZATION'], 
            model = input_arguments.m)
            
    elif input_arguments.t == 'forecast':
        traffic_forecast = tf.TF(model_dump = input_arguments.d, verbose = True)
        
        traffic_forecast.forecast(forecast_intervals = input_arguments.i)
    