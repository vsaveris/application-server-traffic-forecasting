'''
File name: dataFactory.py
    Data Factory class implementation. The class provides an interface for data
    preprocessing.
           
Author: Vasileios Saveris
email: vsaveris@gmail.com

License: MIT

Date last modified: 05.04.2020

Python Version: 3.8
'''

import pandas as pd
from datetime import datetime


class DataFactory():
    '''
    Data Factory class implementation.

    Args:
        file_name (string): The input file name holding the data.
        
        process_date_time (boolean, default is False): Wether the Date column
            should be processed (see _processDateTime())
            
        save_file (string, default is None): The file in which the modifications
            in the input file should be stored. Makes sense when process_date_time
            is True.
        
        verbose (boolean, default is False): If True print services are enabled.

    Public Attributes:
        -
        
    Private Attributes:
        See constructor (self._*)
                                
    Public Methods:
        
        aggregateData (args) -> DataFrame: Aggregates the data of the input file
            according a selected granularity.
        
    Private Methods:
        See methods docstring (def _*)
        
    Raises:
        -
        
    '''

    def __init__(self, file_name, process_date_time = False, save_file = None, 
        verbose = False):
        
        self._verbose = verbose
        
        if self._verbose:
            print('\nData Factory initialization:', self._printProcArgs(locals()
                , 'self'))
            print('- Reading input file')
        
        # Read input data file
        self._data_file = pd.read_csv(file_name)

        if process_date_time:
            self._processDateTime()
            
        if save_file is not None:
            self._data_file.to_csv(save_file, index = False)
            
            if self._verbose:
                print('- Enchanced (tokenized date) input file saved as:', 
                    save_file)
        
    
    def _printProcArgs(self, arguments, exclude = None):
        '''
        Prepares a formatted string of the input arguments dictionary.
    
        Args:
            arguments (dictionary): A dictionary with arguments: values pairs.
            
            exclude (list of strings, default is None): Arguments to be excluded
                from the formatted string.
            
        Raises:
            -

        Returns:
            string: A formatted string of the input arguments in the form of
                argument = value, ...
        '''
        
        return ', '.join('{} = {}'.format(k, v) for k, v in arguments.items() if
            k not in exclude)
        
    
    def _tokenizeDateTime(self, date_time_str, format = '%Y-%m-%d %H:%M:%S'):
        '''
        Tokenizes an input Date Time string.
    
        Args:
            date_time_str (string): A Date Time string.
            
            format (string, default is '%Y-%m-%d %H:%M:%S'): The format of the
                input date time string.

        Raises:
            -

        Returns:
            dictionary: A dictionary with the Date Time tokens, keys are: 'year'
            'month', 'day', 'week_day', 'hour'. Year is in XXXX format, week day
            starts from 0 for Monday, hour is 24h format.
        '''
        
        date_time = datetime.strptime(date_time_str, format)
        
        return {'year': date_time.year, 'month': date_time.month, 
            'day': date_time.day, 'week_day': date_time.weekday(),
            'hour': date_time.hour}
            
    
    def _processDateTime(self):
        '''
        Adds in the self._data_file dataframe the contents of the tokenized date
        time as columns.
    
        Args:
            -

        Raises:
            -

        Returns:
            -
        '''
    
        if self._verbose:
            print('- Date Time processing (split in to tokens)')
        
        # Tokenize date column
        t_dt = [self._tokenizeDateTime(x)for x in self._data_file.date.to_list()]

        # Create new columns with tokenized date-time data
        self._data_file['year'] = [x['year'] for x in t_dt]
        self._data_file['month'] = [x['month'] for x in t_dt]
        self._data_file['day'] = [x['day'] for x in t_dt]
        self._data_file['week_day'] = [x['week_day'] for x in t_dt]
        self._data_file['hour'] = [x['hour'] for x in t_dt]
        
        # Rearange columns
        self._data_file = self._data_file[[self._data_file.columns[0], 'year', 
            'month', 'day', 'week_day', 'hour'] + 
            self._data_file.columns[1:3].to_list()]
    
    
    def aggregateData(self, granularity, combine_hosts = False, save_file = None):     
        '''
        Aggregates the data (sum(), on the requests column) of the self._data_file
        according the selected granularity.
    
        Args:
            granularity (string): The granularity to be used for the data 
                aggregation. Supported values are: 'HOURLY', 'DAILY', 'MONTHLY'
                and 'YEARLY'.
            
            combine_hosts (boolean, default is False): If True, aggregation is
                applied as all the hosts they were one. The host column is 
                dropped.
                
            save_file (string, default is None): The csv file in which the 
                aggregated data should be stored.
                
        Raises:
            ValueError: When granularity given value is not supported.

        Returns:
            DataFrame: The aggregated data.
        '''
        
        if self._verbose:
            print('\nData Aggregation:', self._printProcArgs(locals(), 'self'))
        
        # Validate the value of the granularity argument
        if granularity not in ['HOURLY', 'DAILY', 'MONTHLY', 'YEARLY']:
            raise ValueError('granularity argument error. Value given is \''  +\
                str(granularity) + '\', where supported values are: \'HOULRY' +\
                '\', \'DAILY\', \'MONTHLY\', \'YEARLY\'')
                
        # Define filter and group columns based on the granularity value
        if granularity == 'HOURLY':
            filter_columns = ['year', 'month', 'day', 'week_day', 'hour']
            
        elif granularity == 'DAILY':
            filter_columns = ['year', 'month', 'day', 'week_day']
            
        elif granularity == 'MONTHLY':
            filter_columns = ['year', 'month']
            
        elif granularity == 'YEARLY':
            filter_columns = ['year']

        if not combine_hosts:
            filter_columns += ['host']
            
        group_columns = filter_columns.copy()
        
        filter_columns += ['requests']
        
        if self._verbose:
            print('- Filter Columns:', filter_columns)
            print('- Group Columns :', group_columns)

        # Aggregate data
        data = self._data_file.filter(filter_columns, axis = 1)
        data = data.groupby(group_columns, as_index = False)['requests'].sum()
        
        if save_file is not None:
            data.to_csv(save_file, index = False)
        
            if self._verbose:
                print('- Aggregated data saved as:', save_file)
                
        return data


if __name__ == '__main__':
    
    # Read input data file and process the date column
    df = DataFactory(file_name = '../data/input/traffic_stats.csv', 
        process_date_time = True, 
        save_file = '../data/processed/traffic_stats_tokenized_date.csv', 
        verbose = True)

    # Create all the types of data aggregation
    for g in ['HOURLY', 'DAILY', 'MONTHLY', 'YEARLY']:
        df.aggregateData(granularity = g, combine_hosts = False, 
            save_file = '../data/processed/traffic_stats_' + g + '.csv')
            
        df.aggregateData(granularity = g, combine_hosts = True, 
            save_file = '../data/processed/traffic_stats_' + g + '_CHs.csv')
