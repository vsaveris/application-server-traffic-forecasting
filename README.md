# application-server-traffic-forecasting
Traffic forecasting study case of an application server (cluster, servers x4) using Machine Learning.
The project consists of three parts, all presented in this README file:
- Data Preprocessing: Preprocessing of the input data (different levels of aggregation)
- Data Statistics: Statistical analysis of the input and preprocessed data (seasonality, trends)
- Traffic forecast using Machine Learning algorithms (time series forecasting)

## Input Data File
The input data file contains traffic data per minute, on four application servers which they consist a single cluster. The traffic is disctributed to these four application servers in a load balanced way. The format of the input data is:

```
date	        host	requests
15/03/26 14:00	as-01	316
15/03/26 14:00	as-02	285
15/03/26 14:00	as-03	306
15/03/26 14:00	as-04	286
15/03/26 14:01	as-01	268
15/03/26 14:01	as-02	303
15/03/26 14:01	as-03	266
15/03/26 14:01	as-04	290
...
```

The available data are from `2015-03-26 14:00:00` till `2020-04-03 19:59:00`.

## Source Code
to be filled at the end

### Input Data Preprocessing
In this step, the input data file `./data/input/traffic_stats.csv` is loaded and processed. The processing steps are implemented in the `dataFactory.py` and they are:
- Tokenize the date column of the input data and create the following additional columns: `year`, `month`, `day`, `week_day` and `hour`.
- Aggregate the data (sum() applied on the request column) with the following granularities: `YEARLY`, `MONTHLY`, `DAILY` and `HOURLY`. Data aggregation is permormed for each host separated but also as all hosts they were just one.

```
$python dataFactory.py

Data Factory initialization: file_name = ../data/input/traffic_stats.csv, process_date_time = True, save_file = ../data/processed/traffic_stats_tokenized_date.csv, verbose = True
- Reading input file
- Date Time processing (split in to tokens)
- Enchanced (tokenized date) input file saved as: ../data/processed/traffic_stats_tokenized_date.csv

Data Aggregation: granularity = HOURLY, combine_hosts = False, save_file = ../data/processed/traffic_stats_HOURLY.csv
- Filter Columns: ['year', 'month', 'day', 'week_day', 'hour', 'host', 'requests']
- Group Columns : ['year', 'month', 'day', 'week_day', 'hour', 'host']
- Aggregated data saved as: ../data/processed/traffic_stats_HOURLY.csv

Data Aggregation: granularity = HOURLY, combine_hosts = True, save_file = ../data/processed/traffic_stats_HOURLY_CHs.csv
- Filter Columns: ['year', 'month', 'day', 'week_day', 'hour', 'requests']
- Group Columns : ['year', 'month', 'day', 'week_day', 'hour']
- Aggregated data saved as: ../data/processed/traffic_stats_HOURLY_CHs.csv

Data Aggregation: granularity = DAILY, combine_hosts = False, save_file = ../data/processed/traffic_stats_DAILY.csv
- Filter Columns: ['year', 'month', 'day', 'week_day', 'host', 'requests']
- Group Columns : ['year', 'month', 'day', 'week_day', 'host']
- Aggregated data saved as: ../data/processed/traffic_stats_DAILY.csv

Data Aggregation: granularity = DAILY, combine_hosts = True, save_file = ../data/processed/traffic_stats_DAILY_CHs.csv
- Filter Columns: ['year', 'month', 'day', 'week_day', 'requests']
- Group Columns : ['year', 'month', 'day', 'week_day']
- Aggregated data saved as: ../data/processed/traffic_stats_DAILY_CHs.csv

Data Aggregation: granularity = MONTHLY, combine_hosts = False, save_file = ../data/processed/traffic_stats_MONTHLY.csv
- Filter Columns: ['year', 'month', 'host', 'requests']
- Group Columns : ['year', 'month', 'host']
- Aggregated data saved as: ../data/processed/traffic_stats_MONTHLY.csv

Data Aggregation: granularity = MONTHLY, combine_hosts = True, save_file = ../data/processed/traffic_stats_MONTHLY_CHs.csv
- Filter Columns: ['year', 'month', 'requests']
- Group Columns : ['year', 'month']
- Aggregated data saved as: ../data/processed/traffic_stats_MONTHLY_CHs.csv

Data Aggregation: granularity = YEARLY, combine_hosts = False, save_file = ../data/processed/traffic_stats_YEARLY.csv
- Filter Columns: ['year', 'host', 'requests']
- Group Columns : ['year', 'host']
- Aggregated data saved as: ../data/processed/traffic_stats_YEARLY.csv

Data Aggregation: granularity = YEARLY, combine_hosts = True, save_file = ../data/processed/traffic_stats_YEARLY_CHs.csv
- Filter Columns: ['year', 'requests']
- Group Columns : ['year']
- Aggregated data saved as: ../data/processed/traffic_stats_YEARLY_CHs.csv
```

The data format of each produced file can be found below:

#### Tokenized Date of input data file (./data/processed/traffic_stats_tokenized_date.csv)
```
date	        year	month   day	week_day	hour	host	requests
15/03/26 14:00	2015	3	    26	3	        14	    as-01	316
15/03/26 14:00	2015	3	    26	3	        14	    as-02	285
15/03/26 14:00	2015	3	    26	3	        14	    as-03	306
15/03/26 14:00	2015	3	    26	3	        14	    as-04	286
15/03/26 14:01	2015	3	    26	3	        14	    as-01	268
15/03/26 14:01	2015	3	    26	3	        14	    as-02	303
15/03/26 14:01	2015	3	    26	3	        14	    as-03	266
15/03/26 14:01	2015	3	    26	3	        14	    as-04	290
...
```

#### `YEARLY` data aggregation without combining the hosts (./data/processed/traffic_stats_YEARLY.csv)
```
year	host	requests
2015	as-01	105487150
2015	as-02	107122538
2015	as-03	109152541
2015	as-04	107571586
2016	as-01	442256819
2016	as-02	442244400
2016	as-03	443141710
2016	as-04	443166195
...
```

#### `YEARLY` data aggregation with combining the hosts (./data/processed/traffic_stats_YEARLY_CHs.csv)
```
year	requests
2015	429333815
2016	1770809124
2017	1623434234
2018	1490622486
2019	1458040162
2020	311183306
```

#### `MONTHLY` data aggregation without combining the hosts (./data/processed/traffic_stats_MONTHLY.csv)
```
year	month   host	requests
2015	3	    as-01	895369
2015	3	    as-02	972804
2015	3	    as-03	969290
2015	3	    as-04	894936
2015	4	    as-01	4848222
2015	4	    as-02	5275880
2015	4	    as-03	5265163
2015	4	    as-04	4853454
...
```

#### `MONTHLY` data aggregation with combining the hosts (./data/processed/traffic_stats_MONTHLY_CHs.csv)
```
year	month   requests
2015	3	    3732399
2015	4	    20242719
2015	5	    19479111
2015	6	    28505426
...
```

#### `DAILY` data aggregation without combining the hosts (./data/processed/traffic_stats_DAILY.csv)
```
year	month   day	week_day	host	requests
2015	3	    26	3	        as-01	92558
2015	3	    26	3	        as-02	100167
2015	3	    26	3	        as-03	99569
2015	3	    26	3	        as-04	93092
2015	3	    27	4	        as-01	191122
2015	3	    27	4	        as-02	206725
2015	3	    27	4	        as-03	205785
2015	3	    27	4	        as-04	191377
2015	3	    28	5	        as-01	96609
2015	3	    28	5	        as-02	107580
2015	3	    28	5	        as-03	106837
...
```

#### `DAILY` data aggregation with combining the hosts (./data/processed/traffic_stats_DAILY_CHs.csv)
```
year	month   day	week_day	requests
2015	3	    26	3	        385386
2015	3	    27	4	        795009
2015	3	    28	5	        406355
2015	3	    29	6	        310390
2015	3	    30	0	        929001
2015	3	    31	1	        906258
...
```

#### `HOURLY` data aggregation without combining the hosts (./data/processed/traffic_stats_HOURLY.csv)
```
year	month   day	week_day	hour	host	requests
2015	3	    26	3	        14	    as-01	17083
2015	3	    26	3	        14	    as-02	18356
2015	3	    26	3	        14	    as-03	18034
2015	3	    26	3	        14	    as-04	17440
2015	3	    26	3	        15	    as-01	16759
2015	3	    26	3	        15	    as-02	18055
2015	3	    26	3	        15	    as-03	17972
2015	3	    26	3	        15	    as-04	17057
2015	3	    26	3	        16	    as-01	16876
2015	3	    26	3	        16	    as-02	17951
2015	3	    26	3	        16	    as-03	17996
2015	3	    26	3	        16	    as-04	16986
...
```

#### `HOURLY` data aggregation with combining the hosts (./data/processed/traffic_stats_HOURLY_CHs.csv)
```
year	month   day	week_day	hour	requests
2015	3	    26	3	        14	    70913
2015	3	    26	3	        15	    69843
2015	3	    26	3	        16	    69809
2015	3	    26	3	        17	    54620
2015	3	    26	3	        18	    40256
2015	3	    26	3	        19	    31337
2015	3	    26	3	        20	    23894
2015	3	    26	3	        21	    13236
2015	3	    26	3	        22	    7183
...
```

### Data Statistics
In this step a statistical analysis on the input and on the preprocessed data is applied. The code executed for this step can be found below:

```
$python dataStatistics.py

Unprocessed data information:
- Number of instances: 10'557'976
- Number of features : 3, ['date', 'host', 'requests']
- First data instance: 2015-03-26 14:00:00
- Last data instance : 2020-04-03 19:59:00
- Data time period   : 1835 days, 5:59:00

Comparing traffic among all the application servers (hourly basis)
- Graph saved in: ../graphs/data_statistics/compare_all_hosts_hourly.png

Comparing traffic among all the application servers (daily basis)
- Graph saved in: ../graphs/data_statistics/compare_all_hosts_daily.png

Comparing traffic among all the application servers (monthly basis)
- Graph saved in: ../graphs/data_statistics/compare_all_hosts_monthly.png

Comparing traffic among all the application servers (yearly basis)
- Graph saved in: ../graphs/data_statistics/compare_all_hosts_yearly.png

Seasonality analysis on hourly basis for all days of the week
- Graph saved in: ../graphs/data_statistics/seasonality_hourly_whole_week.png

Seasonality analysis on daily basis for a week
- Graph saved in: ../graphs/data_statistics/seasonality_daily_whole_week.png

Seasonality analysis on monthly basis for a year
- Graph saved in: ../graphs/data_statistics/seasonality_monthly_whole_year.png

Yearly traffic trend
- Graph saved in: ../graphs/data_statistics/traffic_trend_yearly.png
```

#### Comparing traffic among all the application servers (hourly basis)
It confirms that the traffic is distributed equally to all the four application servers (hourly basis), so there is no need for individual host traffic forecast.

![](./graphs/data_statistics/compare_all_hosts_hourly.png?raw=true)

#### Comparing traffic among all the application servers (daily basis)
It confirms that the traffic is distributed equally to all the four application servers (daily basis), so there is no need for individual host traffic forecast. Additionally it can be noted that in around the 3000th instance, as-01 and as-02 were offload from traffic (posibble reason a planned maintenance or an outage) and at the same time this traffic distributed equally to the other two hosts.

![](./graphs/data_statistics/compare_all_hosts_daily.png?raw=true)

#### Comparing traffic among all the application servers (monthly basis)
It confirms that the traffic is distributed equally to all the four application servers (monthly basis), so there is no need for individual host traffic forecast.

![](./graphs/data_statistics/compare_all_hosts_monthly.png?raw=true)

#### Comparing traffic among all the application servers (yearly basis)
It confirms that the traffic is distributed equally to all the four application servers (yearly basis), so there is no need for individual host traffic forecast.

![](./graphs/data_statistics/compare_all_hosts_yearly.png?raw=true)

#### Seasonality analysis on hourly basis for all days of the week
It shows the total traffic level for each day of the week (hourly basis).

![](./graphs/data_statistics/seasonality_hourly_whole_week.png?raw=true)

#### Seasonality analysis on daily basis for a week
It shows the total daily traffic for each day of the week.

![](./graphs/data_statistics/seasonality_daily_whole_week.png?raw=true)

#### Seasonality analysis on monthly basis for a year
It shows the total monthly traffic for each month of the year.

![](./graphs/data_statistics/seasonality_monthly_whole_year.png?raw=true)

#### Yearly traffic trend
It shows the yearly traffic trend. It is confirmed that the trend is declining, considering only the years where full data are available (2016 till 2019).

![](./graphs/data_statistics/traffic_trend_yearly.png?raw=true)


### Traffic forecast 
to be filled