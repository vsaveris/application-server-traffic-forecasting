'''
File name: dataStatistics.py
    Data statistics representation, including graphs.
           
Author: Vasileios Saveris
email: vsaveris@gmail.com

License: MIT

Date last modified: 06.04.2020

Python Version: 3.8
'''

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


def comparisonGraph(type, data, color, save_file):
    '''
    Creates a 2x2 subplots comparison graph (hosts) for the input data.
    
    Args:
        type (string): The comparison type. String is appended in the suplots
            title.
            
        data (pandas DataFrame or Series): The data to be plotted. Only requests
            column is used.
            
        color (string): Color to be used in the graph.
        
        save_file (string): Relevant path and file to save the graph.

    Raises:
        -

    Returns:
        -
    '''
    
    fig, axs = plt.subplots(2, 2)
    fig.suptitle('Compare all hosts, ' + type, fontweight = 'bold')
    axs[0, 0].plot(data[data.host == 'as-01'].requests, color = color)
    axs[0, 0].set_title('as-01')
    axs[0, 1].plot(data[data.host == 'as-02'].requests, color = color)
    axs[0, 1].set_title('as-02')
    axs[1, 0].plot(data[data.host == 'as-03'].requests, color = color)
    axs[1, 0].set_title('as-03')
    axs[1, 1].plot(data[data.host == 'as-04'].requests, color = color)
    axs[1, 1].set_title('as-04')
    
    for ax in axs.flat:
        ax.set(xlabel = 'instances', ylabel = 'requests')
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
        
    plt.savefig(save_file)
    plt.show()
    print('- Graph saved in: ' + save_file)
    
    
def seasonalityHourly(data, start_day, save_file):
    '''
    Creates a 7x1 subplots for hourly seasonality of a week.
    
    Args:   
        data (pandas DataFrame or Series): The data to be plotted. Only hour and
            requests columns are used.
            
        start_day (integer): The start month day of the time period.
        
        save_file (string): Relevant path and file to save the graph.

    Raises:
        -

    Returns:
        -
    '''
    
    fig, axs = plt.subplots(7, gridspec_kw = {'hspace': 0})
    fig.suptitle('Seasonality, hourly basis, Monday to Sunday', fontweight = 'bold')
    
    labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    colors = ['navy', 'royalblue']*4
    
    for i in range(7):
        axs[i].bar(data[data.week_day == i].hour, data[data.week_day == i].
            requests, color = colors[i], label = labels[i])
        axs[i].set_yticklabels([])
        axs[i].legend(loc = 'upper left', fontsize = 8)

    fig.text(0.5, 0.04, 'time of the day', ha = 'center')
    fig.text(0.04, 0.5, 'requests', va = 'center', rotation = 'vertical')
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
        
    plt.savefig(save_file)
    plt.show()
    print('- Graph saved in: ' + save_file)
    
    
def seasonalityDaily(data, color, save_file):
    '''
    Creates a bar graph for daily seasonality of a week.
    
    Args:
        data (pandas DataFrame or Series): The data to be plotted. Only requests
            column is used.
            
        color (string): Color to be used in the graph.
        
        save_file (string): Relevant path and file to save the graph.

    Raises:
        -

    Returns:
        -
    '''
    
    plt.title('Seasonality, daily basis, Monday to Sunday', fontweight = 'bold')

    plt.bar(['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'], data.requests, 
        color = color, width = 0.4)
    
    plt.xlabel('day of the week')
    plt.ylabel('requests')
        
    plt.savefig(save_file)
    plt.show()
    print('- Graph saved in: ' + save_file)


def seasonalityMonthly(data, color, save_file):
    '''
    Creates a bar graph for monthly seasonality of a year.
    
    Args:
        data (pandas DataFrame or Series): The data to be plotted. Only requests
            column is used.
            
        color (string): Color to be used in the graph.
        
        save_file (string): Relevant path and file to save the graph.

    Raises:
        -

    Returns:
        -
    '''
    
    plt.title('Seasonality, monthly basis, for a year', fontweight = 'bold')

    plt.bar(['Ja', 'Fe', 'Ma', 'Ap', 'Ma', 'Jun', 'Jul', 'Au', 'Se', 'Oc', 'No', 
        'De'], data.requests, color = color, width = 0.4)
    
    plt.xlabel('months of the year')
    plt.ylabel('requests')
        
    plt.savefig(save_file)
    plt.show()
    print('- Graph saved in: ' + save_file)


def trendYearly(data, color, save_file):
    '''
    Creates a bar graph for yearly traffic trend.
    
    Args:
        data (pandas DataFrame or Series): The data to be plotted. Only requests
            column is used.
            
        color (string): Color to be used in the graph.
        
        save_file (string): Relevant path and file to save the graph.

    Raises:
        -

    Returns:
        -
    '''
    
    plt.title('Yearly traffic trend', fontweight = 'bold')

    plt.bar(data.year, data.requests, color = color, width = 0.4)
    
    plt.xlabel('years')
    plt.ylabel('requests')
        
    plt.savefig(save_file)
    plt.show()
    print('- Graph saved in: ' + save_file)
    

if __name__ == '__main__':
    
    # Unprocessed data information
    input_data = pd.read_csv('../data/input/traffic_stats.csv')
    
    print('\nUnprocessed data information:')
    print('- Number of instances: ', f"{input_data.shape[0]:,d}".
        replace(',', '\''), sep = '')
    print('- Number of features : ', input_data.shape[1], ', ', 
        input_data.columns.to_list(), sep = '')
    print('- First data instance: ', input_data.date.iloc[0], sep = '')
    print('- Last data instance : ', input_data.date.iloc[-1], sep = '')
    print('- Data time period   : ', 
        datetime.strptime(input_data.date.iloc[-1], '%Y-%m-%d %H:%M:%S') -\
        datetime.strptime(input_data.date.iloc[0], '%Y-%m-%d %H:%M:%S'),
        sep = '')
        
    # Comparing traffic distribution to all the application servers
    
    # Comparing traffic among all the application servers (hourly basis)
    print('\nComparing traffic among all the application servers (hourly basis)')
    hourly_data = pd.read_csv('../data/processed/traffic_stats_HOURLY.csv')
    
    comparisonGraph(type = 'hourly traffic', data = hourly_data, color = 'darkslateblue',
        save_file = '../graphs/data_statistics/compare_all_hosts_hourly.png')
    
    # Comparing traffic among all the application servers (daily basis)
    print('\nComparing traffic among all the application servers (daily basis)')
    daily_data = pd.read_csv('../data/processed/traffic_stats_DAILY.csv')
    
    comparisonGraph(type = 'daily traffic', data = daily_data, color = 'coral',
        save_file = '../graphs/data_statistics/compare_all_hosts_daily.png')

    # Comparing traffic among all the application servers (monthly basis)
    print('\nComparing traffic among all the application servers (monthly basis)')
    monthly_data = pd.read_csv('../data/processed/traffic_stats_MONTHLY.csv')
    
    comparisonGraph(type = 'monthly traffic', data = monthly_data, color = 'peru',
        save_file = '../graphs/data_statistics/compare_all_hosts_monthly.png')
        
    # Comparing traffic among all the application servers (yearly basis)
    print('\nComparing traffic among all the application servers (yearly basis)')
    yearly_data = pd.read_csv('../data/processed/traffic_stats_YEARLY.csv')
    
    comparisonGraph(type = 'yearly traffic', data = yearly_data, color = 'mediumseagreen',
        save_file = '../graphs/data_statistics/compare_all_hosts_yearly.png')
        
    
    # Seasonality analysis of the traffic (combined hosts)
    
    # Seasonality analysis on hourly basis for all days of the week
    print('\nSeasonality analysis on hourly basis for all days of the week')
    hourly_data_chs = pd.read_csv('../data/processed/traffic_stats_HOURLY_CHs.csv')

    seasonalityHourly(data = hourly_data_chs.query('year == 2016 and month == 2'+\
        ' and day >= 15 and day <= 21'), start_day = 15,
        save_file = '../graphs/data_statistics/seasonality_hourly_whole_week.png')
          
    # Seasonality analysis on daily basis for a week
    print('\nSeasonality analysis on daily basis for a week')
    daily_data_chs = pd.read_csv('../data/processed/traffic_stats_DAILY_CHs.csv')

    seasonalityDaily(data = daily_data_chs.query('year == 2016 and month == 2'+\
        ' and day >= 15 and day <= 21'), color = 'lightsalmon',
        save_file = '../graphs/data_statistics/seasonality_daily_whole_week.png')
        
    
    # Seasonality analysis on monthly basis for a year
    print('\nSeasonality analysis on monthly basis for a year')
    monthly_data_chs = pd.read_csv('../data/processed/traffic_stats_MONTHLY_CHs.csv')

    seasonalityMonthly(data = monthly_data_chs.query('year == 2016'), color = 'purple',
        save_file = '../graphs/data_statistics/seasonality_monthly_whole_year.png')
        
        
    # Trend of the traffic (yearly)
    print('\nYearly traffic trend')
    
    yearly_data_chs = pd.read_csv('../data/processed/traffic_stats_YEARLY_CHs.csv')
    
    trendYearly(data = yearly_data_chs, color = 'burlywood', 
        save_file = '../graphs/data_statistics/traffic_trend_yearly.png')
    