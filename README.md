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
- `runForecast.py`: Main script for the Traffic Forecast part. Use `python runForecast.py -h` for available options.
- `utils.py`: Utilities script for the Traffic Forecast part.
- `dataFactory.py`: Main script for the Data Preprocessing part.
- `dataStatistics.py`: Main script for the Data Statistics part.
- `trafficForecast.py`: Interface for the Traffic Forecast part.
- `model.py`: Abstract class for each model implementation.
- `dnn.py`: Deep Neural Network implementation.
- `rnn.py`: Recurrent Neural Network implementation. Not added to the repository yet.
- `lstm.py`: Long Short Term Memory Neural Network implementation. Not added to the repository yet.


## Documentation for each Part
- [Data Preprocessing](https://github.com/vsaveris/application-server-traffic-forecasting/tree/master/docs/data_preprocessing)
- [Data Statistics](https://github.com/vsaveris/application-server-traffic-forecasting/tree/master/docs/data_statistics)
- [Traffic Forecast](https://github.com/vsaveris/application-server-traffic-forecasting/tree/master/docs/traffic_forecast)