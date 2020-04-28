# Traffic forecast 
The below models are implemented and evaluated:
- Deep Neural Network (DNN)
- Recurrent Neural Network (RNN), Not implemented yet.
- Long Short Term Memory Deep Neural Network (LSTM), Not implemented yet.

The scirpt used for the traffic forecast part can be found below:

```
$python runForecast.py -h
usage: runForecast.py [-h] -f file -m model -t test_data_portion

Run traffic forecast

optional arguments:
  -h, --help            show this help message and exit
  -f file               input data file
  -m model              model to be used for the traffic forecast, currently only 'DNN' has been implemented and supported
  -t test_data_portion  test data percentage

Usage Example:
Execute the forecast flow for the given input data file, using a DNN model and 0.2 of the input data as test data.

$python -W ignore runForecast.py -f ../data/processed/traffic_stats_DAILY_CHs.csv -m DNN -t 0.2

Note: The -W ignore option is used for avoiding Sklearn convergence warnings during the hyperparameters tunning step.
```

### Deep Neural Network

For the deep neural network study case, daily and hourly traffic forecasts have been evaluated. In both cases hyperparameters tunning applies.

#### Daily traffic forecast

For the daily forecast part, `20%` of the daily input data were kept as a test set. The data input file used was the `traffic_stats_DAILY_CHs.csv`. The script execution details can be found below:

```
$python -W ignore runForecast.py -f ../data/processed/traffic_stats_DAILY_CHs.csv -m DNN -t 0.2

Traffic Forecast initialization: input_file = ../data/processed/traffic_stats_DAILY_CHs.csv, test_split = 0.2, verbose = True
- Input data loaded, file = ../data/processed/traffic_stats_DAILY_CHs.csv
- Split input data to training and test set, test_size = 0.2
- Data sets prepared, training_size = 1468, test_size = 368

Evaluate model: normalize = True, standardize = True, model = DNN
- MLPRegressor initialization: model_params = None, verbose = True
Fitting 1 folds for each of 288 candidates, totalling 288 fits
[Parallel(n_jobs=-1)]: Using backend LokyBackend with 16 concurrent workers.
[Parallel(n_jobs=-1)]: Done  18 tasks      | elapsed:    5.3s
[Parallel(n_jobs=-1)]: Done 168 tasks      | elapsed:  1.4min
[Parallel(n_jobs=-1)]: Done 288 out of 288 | elapsed:  3.8min finished
- Evaluation Step 1: best_score = 0.14554332782280488
- Evaluation Step 1: best_params = {'activation': 'relu', 'hidden_layer_sizes': (100, 100), 'learning_rate': 'constant', 'learning_rate_init': 0.01, 'max_iter': 200, 'random_state': 1, 'shuffle': False, 'solver': 'lbfgs'}
- Multi Process Task initialization: task = <bound method DNN._calculateTestScore of <dnn.DNN object at 0x000001A2E9C99610>>, processes = None, number of tasks = 199, time elapsed: 174.506 seconds
- Evaluation Step 2: best_score = 0.1929492649842115
- Evaluation Step 2: best_params = {'activation': 'relu', 'hidden_layer_sizes': (75, 75), 'learning_rate': 'constant', 'learning_rate_init': 0.01, 'max_iter': 200, 'random_state': 1, 'shuffle': False, 'solver': 'lbfgs'}
- Multi Process Task initialization: task = <bound method DNN._calculateTrainTestScore of <dnn.DNN object at 0x000001A2E9C99610>>, processes = None, number of tasks = 401, time elapsed: 251.103 seconds
- Evaluation Step 3: best_score = 0.19553084596033266
- Evaluation Step 3: best_params = {'activation': 'relu', 'hidden_layer_sizes': (75, 75), 'learning_rate': 'constant', 'learning_rate_init': 0.01, 'max_iter': 193, 'random_state': 1, 'shuffle': False, 'solver': 'lbfgs'}
- Evaluation best score: 0.19553084596033266
- Evaluation best params: {'activation': 'relu', 'hidden_layer_sizes': (75, 75), 'learning_rate': 'constant', 'learning_rate_init': 0.01, 'max_iter': 193, 'random_state': 1, 'shuffle': False, 'solver': 'lbfgs'}
```

In the below graph, the performance of the model on the train and the test set per iteration is shown:

![](../../graphs/forecasts/evaluate_ETT_20200420205214.png?raw=true)

In the below graph the train data, test data and the forecast is shown:

![](../../graphs/forecasts/evaluate_TTF_20200420205214.png?raw=true)

In the below graph the test data and the forecast is shown:

![](../../graphs/forecasts/evaluate_TF_20200420205214.png?raw=true)



#### Hourly traffic forecast

For the hourly forecast part, `0.01%` of the hourly input data were kept as a test set. The data input file used was the `traffic_stats_HOURLY_CHs.csv`. The script execution details can be found below:

```
$python -W ignore runForecast.py -f ../data/processed/traffic_stats_HOURLY_CHs.csv -m DNN -t 0.01

Traffic Forecast initialization: input_file = ../data/processed/traffic_stats_HOURLY_CHs.csv, test_split = 0.01, verbose = True
- Input data loaded, file = ../data/processed/traffic_stats_HOURLY_CHs.csv
- Split input data to training and test set, test_size = 0.01
- Data sets prepared, training_size = 43585, test_size = 441

Evaluate model: normalize = True, standardize = True, model = DNN
- MLPRegressor initialization: model_params = None, verbose = True
Fitting 1 folds for each of 288 candidates, totalling 288 fits
[Parallel(n_jobs=-1)]: Using backend LokyBackend with 16 concurrent workers.
[Parallel(n_jobs=-1)]: Done  18 tasks      | elapsed:  1.5min
[Parallel(n_jobs=-1)]: Done 168 tasks      | elapsed: 46.3min
[Parallel(n_jobs=-1)]: Done 288 out of 288 | elapsed: 111.0min finished
- Evaluation Step 1: best_score = 0.6405633123530308
- Evaluation Step 1: best_params = {'activation': 'relu', 'hidden_layer_sizes': (100, 100, 100, 100, 100), 'learning_rate': 'constant', 'learning_rate_init': 0.01, 'max_iter': 200, 'random_state': 1, 'shuffle': False, 'solver': 'adam'}
- Multi Process Task initialization: task = <bound method DNN._calculateTestScore of <dnn.DNN object at 0x0000023B1D418640>>, processes = None, number of tasks = 199, time elapsed: 1539.689 seconds
- Evaluation Step 2: best_score = 0.7741202911740084
- Evaluation Step 2: best_params = {'activation': 'relu', 'hidden_layer_sizes': (111, 111, 111, 111, 111), 'learning_rate': 'constant', 'learning_rate_init': 0.01, 'max_iter': 200, 'random_state': 1, 'shuffle': False, 'solver': 'adam'}
- Multi Process Task initialization: task = <bound method DNN._calculateTrainTestScore of <dnn.DNN object at 0x0000023B1D418640>>, processes = None, number of tasks = 401, time elapsed: 3097.692 seconds
- Evaluation Step 3: best_score = 0.7741202911740084
- Evaluation Step 3: best_params = {'activation': 'relu', 'hidden_layer_sizes': (111, 111, 111, 111, 111), 'learning_rate': 'constant', 'learning_rate_init': 0.01, 'max_iter': 100, 'random_state': 1, 'shuffle': False, 'solver': 'adam'}
- Evaluation best score: 0.7741202911740084
- Evaluation best params: {'activation': 'relu', 'hidden_layer_sizes': (111, 111, 111, 111, 111), 'learning_rate': 'constant', 'learning_rate_init': 0.01, 'max_iter': 100, 'random_state': 1, 'shuffle': False, 'solver': 'adam'}
```

In the below graph, the performance of the model on the train and the test set per iteration is shown:

![](../../graphs/forecasts/evaluate_ETT_20200420211309.png?raw=true)

In the below graph the train data, test data and the forecast is shown:

![](../../graphs/forecasts/evaluate_TTF_20200420211309.png?raw=true)

In the below graph the test data and the forecast is shown:

![](../../graphs/forecasts/evaluate_TF_20200420211309.png?raw=true)