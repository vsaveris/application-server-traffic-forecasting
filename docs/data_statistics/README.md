# Data Statistics
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

![](../../graphs/data_statistics/compare_all_hosts_hourly.png?raw=true)

#### Comparing traffic among all the application servers (daily basis)
It confirms that the traffic is distributed equally to all the four application servers (daily basis), so there is no need for individual host traffic forecast. Additionally it can be noted that in around the 3000th instance, as-01 and as-02 were offload from traffic (posibble reason a planned maintenance or an outage) and at the same time this traffic distributed equally to the other two hosts.

![](../../graphs/data_statistics/compare_all_hosts_daily.png?raw=true)

#### Comparing traffic among all the application servers (monthly basis)
It confirms that the traffic is distributed equally to all the four application servers (monthly basis), so there is no need for individual host traffic forecast.

![](../../graphs/data_statistics/compare_all_hosts_monthly.png?raw=true)

#### Comparing traffic among all the application servers (yearly basis)
It confirms that the traffic is distributed equally to all the four application servers (yearly basis), so there is no need for individual host traffic forecast.

![](../../graphs/data_statistics/compare_all_hosts_yearly.png?raw=true)

#### Seasonality analysis on hourly basis for all days of the week
It shows the total traffic level for each day of the week (hourly basis).

![](../../graphs/data_statistics/seasonality_hourly_whole_week.png?raw=true)

#### Seasonality analysis on daily basis for a week
It shows the total daily traffic for each day of the week.

![](../../graphs/data_statistics/seasonality_daily_whole_week.png?raw=true)

#### Seasonality analysis on monthly basis for a year
It shows the total monthly traffic for each month of the year.

![](../../graphs/data_statistics/seasonality_monthly_whole_year.png?raw=true)

#### Yearly traffic trend
It shows the yearly traffic trend. It is confirmed that the trend is declining, considering only the years where full data are available (2016 till 2019).

![](../../graphs/data_statistics/traffic_trend_yearly.png?raw=true)
