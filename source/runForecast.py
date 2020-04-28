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
C_EXAMPLES = 'Usage Example:\nExecute the forecast flow for the given input'     +\
    ' data file, using a DNN model and 0.2 of the input data as test data.\n\n'  +\
    '$python -W ignore runForecast.py -f ../data/processed/traffic_stats_DAIL'   +\
    'Y_CHs.csv -m DNN -t 0.2\n\nNote: The -W ignore option is used for avoiding '+\
    'Sklearn convergence warnings during the hyperparameters tunning step.\n'

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

    args_parser.add_argument('-f', action = 'store', required = True, 
        help = 'input data file', metavar = 'file')

    args_parser.add_argument('-m', action = 'store', required = True, 
        #help = 'model to be used for the traffic forecast, one of \'RNN\', '+\
        #'\'LSTM\', required when type (-t) is \'train\' or \'evaluate\'',
        help = 'model to be used for the traffic forecast, currently only '  +\
        '\'DNN\' has been implemented and supported',
        choices = ('DNN'), metavar = 'model')
                            
    args_parser.add_argument('-t', action = 'store', type = float, required = True, 
        help = 'test data percentage', metavar = 'test_data_portion')

    return args_parser.parse_args()
                  

if __name__ == '__main__':
    
    # Read input arguments
    input_arguments = parseInputArguments()   
    
    # Execute the forecast flow
    traffic_forecast = tf.TF(input_file = input_arguments.f, 
        test_split = input_arguments.t, verbose = True)
    
    traffic_forecast.evaluate(
        normalize = C_MODEL_PREPROCESSING[input_arguments.m]['NORMALIZATION'], 
        standardize = C_MODEL_PREPROCESSING[input_arguments.m]['STANDARDIZATION'], 
        model = input_arguments.m)
