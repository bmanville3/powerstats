# Overview
This directory contains results from hyperparameter tuning in cross-validation using the validation set, the best trained model, and results of the best trained model on the validation set.

## The data used
The data in the sql database was used to train and validate the hyerparameters. The goal was to predict if a lifter competed in a drug tested competition or not (the best proxy we have in the data for true drug use).

## Hyperparameter tuning - Initial LSTM Run
Initially, only the LSTM was ran using a hyperparameter grid constructed from
```
param_grid: dict[str, list[float | int]] = {
    "hidden_size": [32, 64, 128, 200],
    "num_layers": [1, 2, 3],
    "dropout": [0.0, 0.1, 0.3],
    "lr": [0.0001, 0.0005, 0.001, 0.01],
}
```
This took around 6 hours to run and the results can be found at [`full_initial_LSTM_tuning_results.csv`](./full_initial_LSTM_tuning_results.csv).

From these results, I manually selected ones by F1 score > ~0.6 and accuracy > 0.56 leading to the following hyperparameter selection:
```
hidden_size,num_layers,dropout,lr,f1,accuracy,precision,recall
200,1,0.0,0.001,0.6174961593089655,0.5721973675679181,0.5575971731448763,0.6918130744000259
128,1,0.0,0.001,0.618791449634247,0.565810802048888,0.5507562131076938,0.7060046114376644
200,2,0.1,0.001,0.6037984507475362,0.5614180120599105,0.5498159901861432,0.6695352839931153
200,2,0.0,0.01,0.5969201413216857,0.5617097840886986,0.5517250881834215,0.6501802357678693
```
While not perfect, we will extrapolate these results for regular training (due to resource limitations in testing). That is, instead of running the full param_grid sweep again for every model, we will only run
```
param_grid: dict[str, list[float | int]] = {
    "hidden_size": [128, 200, 256],
    "num_layers": [1, 2],
    "dropout": [0.0],
    "lr": [0.001],
}
```
Additionally, the original optimizer used was SGD, but the new optimizer used will be Adam.
### Justification for the new param grid
* The better models tend to have higher complexity ($\text{size}\geq 128$).
* Having more than 2 layers led to bad results.
* The dropout parameter did not change much.
* Setting the learning rate lower/higher tended to not make results better
* While SGD was used at first, playing around with Adam instantly spiked the accuracy by 2-3%. Changing the optimizer does draw question to if the results are valid, but we will have to live with it as rerunning the full sweep would take too long.
