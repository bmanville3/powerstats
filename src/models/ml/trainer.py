import itertools
import logging

import matplotlib.pyplot as plt
import pandas as pd
import torch
from torch.utils.data import DataLoader

from src.models.ml.base import BaseNetwork
from src.models.ml.concrete_models.bi_lstm import LifterBiLSTM
from src.models.ml.concrete_models.lstm import LifterLSTM
from src.models.ml.concrete_models.rnn import LifterRNN
from src.models.ml.lifter_dataset import (
    IS_USING_LABEL,
    LifterDataset,
    collate_fn,
    get_point_from_result,
    get_train_test_data_from_db,
)
from src.utils.known_ped_users import get_known_users
from src.utils.utils import POWERSTATS

logger = logging.getLogger(__name__)


def train_models(model_names: set[str]) -> dict[str, BaseNetwork]:
    graph_loc = POWERSTATS / "graphs/models/val_set/"
    graph_loc.mkdir(exist_ok=True, parents=True)
    trained_models_dir = POWERSTATS / "trained_models"
    trained_models_dir.mkdir(exist_ok=True)

    train, test = get_train_test_data_from_db()
    tuned_models: dict[str, BaseNetwork] = {}

    # Hyperparameter grids
    # for the initial LSTM using SGD optimizer and
    # param_grid: dict[str, list[float | int]] = {
    #     "hidden_size": [32, 64, 128, 200],
    #     "num_layers": [1, 2, 3],
    #     "dropout": [0.0, 0.1, 0.3],
    #     "lr": [0.0001, 0.0005, 0.001, 0.01],
    # }
    # the best models on the full dataset (80/20 split) are (that I manually selected by F1 score > ~0.6 and accuracy > 0.56):
    #
    # hidden_size,num_layers,dropout,lr,f1,accuracy,precision,recall
    # 200,1,0.0,0.001,0.6174961593089655,0.5721973675679181,0.5575971731448763,0.6918130744000259
    # 128,1,0.0,0.001,0.618791449634247,0.565810802048888,0.5507562131076938,0.7060046114376644
    # 200,2,0.1,0.001,0.6037984507475362,0.5614180120599105,0.5498159901861432,0.6695352839931153
    # 200,2,0.0,0.01,0.5969201413216857,0.5617097840886986,0.5517250881834215,0.6501802357678693
    #
    # while not perfect, we will extrapolate these results for regular training (due to resource limitations in testing)
    param_grid: dict[str, list[float | int]] = {
        "hidden_size": [128, 200, 256, 384],
        "num_layers": [1, 2],
        "dropout": [0.0, 0.1],
        "lr": [0.001, 0.0005],
    }
    param_combinations = list(
            itertools.product(
                param_grid["hidden_size"],
                param_grid["num_layers"],
                param_grid["dropout"],
                param_grid["lr"],
            )
        )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info("Using device %s", device)
    classes = {
            "LSTM": LifterLSTM,
            "RNN": LifterRNN,
            "Bidirectional_LSTM": LifterBiLSTM,
    }

    for model_name in list(model_names):  # copy to mutate safely
        logger.info("Hyperparameter tuning for model: %s", model_name)
        model_class = classes.get(model_name)

        if model_class is None:
            logger.error("Unknown model: %s", model_name)
            model_names.remove(model_name)
            continue

        results = []

        for hidden_size, num_layers, dropout, lr in param_combinations:
            if num_layers <= 1 and dropout > 0.0:
                logger.debug("Skipping param combo because num_layers=%s and dropout=%s", num_layers, dropout)
                continue
            hidden_size = int(hidden_size)
            num_layers = int(num_layers)
            logger.info(
                "Testing: hidden=%d, layers=%d, dropout=%.2f, lr=%.4f",
                hidden_size,
                num_layers,
                dropout,
                lr,
            )
            model: BaseNetwork = model_class(
                input_size=7,
                hidden_size=hidden_size,
                num_layers=num_layers,
                dropout=dropout,
                device=device,
            )
            model.to(device)
            optimizer = torch.optim.Adam(model.parameters(), lr=lr)

            # Train model temporarily
            model.train_model(
                train, optimizer, model.get_loss_fn(), epochs=10, save_loc=None
            )
            # Evaluate
            metrics = model.evaluate(test)
            results.append(
                {
                    "hidden_size": hidden_size,
                    "num_layers": num_layers,
                    "dropout": dropout,
                    "lr": lr,
                    "f1":  metrics["f1"],
                    "accuracy": metrics["accuracy"],
                    "precision": metrics["precision"],
                    "recall": metrics["recall"],
                }
            )

        # Find best configuration
        df = pd.DataFrame(results)
        df.to_csv(trained_models_dir / f"{model_name}_tuning_results.csv", index=False)

        best_row = df.sort_values("accuracy", ascending=False).iloc[0]
        logger.info("Best hyperparameters for %s: %s", model_name, best_row)

        # Retrain final model with best params
        best_model: BaseNetwork = model_class(
            input_size=7,
            hidden_size=int(best_row["hidden_size"]),
            num_layers=int(best_row["num_layers"]),
            dropout=float(best_row["dropout"]),
            device=device,
        )
        best_model.to(device)
        best_optimizer = torch.optim.Adam(best_model.parameters(), lr=best_row["lr"])
        best_model.train_model(
            train,
            best_optimizer,
            best_model.get_loss_fn(),
            epochs=20,
            save_loc=trained_models_dir / f"{model_name}_lifter_model",
        )
        best_model.load_from(trained_models_dir / f"{model_name}_lifter_model")
        tuned_models[model_name] = best_model

        # Final test set evaluation after full retraining
        final_metrics = best_model.evaluate(test)

        # Save best hyperparameters and final evaluation to a .txt file
        hyperparam_file = trained_models_dir / f"{model_name}_hyperparameters.txt"
        with open(hyperparam_file, "w") as f:
            f.write(f"Best Hyperparameters for {model_name}:\n")
            f.write(f"Hidden Size: {int(best_row['hidden_size'])}\n")
            f.write(f"Num Layers: {int(best_row['num_layers'])}\n")
            f.write(f"Dropout: {float(best_row['dropout'])}\n")
            f.write(f"Learning Rate: {best_row['lr']:.4f}\n\n")

            f.write("Final Evaluation on Validation Set:\n")
            for metric, value in final_metrics.items():
                if isinstance(value, torch.Tensor):
                    continue  # skip tensors like predictions/labels
                f.write(f"{metric.capitalize()}: {value:.4f}\n")

        # Filter only scalar numeric metrics for plotting
        plot_metrics = {
            k: v for k, v in final_metrics.items() if isinstance(v, (float, int))
        }

        # Optionally, ensure these keys are present and order them
        metrics_to_plot = ["f1", "accuracy", "precision", "recall"]
        plot_metrics_ordered = {
            k.capitalize(): plot_metrics[k]
            for k in metrics_to_plot
            if k in plot_metrics
        }

        plt.figure(figsize=(8, 5))
        plt.bar(
            plot_metrics_ordered.keys(),
            plot_metrics_ordered.values(),
            color=["#4CAF50", "#2196F3", "#FFC107", "#FF5722"],
        )
        plt.ylim(0, 1.1)
        plt.title(f"{model_name} - Best Metric Scores on Validation Set")
        for i, (k, v) in enumerate(plot_metrics_ordered.items()):
            plt.text(i, v + 0.01, f"{v:.2f}", ha="center", va="bottom")
        plt.ylabel("Score")
        plt.xlabel(f"(Using drugs = class {IS_USING_LABEL})")
        plt.savefig(graph_loc / f"{model_name}_val_metrics_bar.png")
        plt.close()

    return tuned_models


def test_models(model_names: set[str]) -> None:
    graph_loc = POWERSTATS / "graphs/models/test_set/"
    graph_loc.mkdir(exist_ok=True, parents=True)
    trained_models_dir = POWERSTATS / "trained_models"
    trained_models_dir.mkdir(exist_ok=True)
    users = get_known_users()

    sequences = []
    labels = []
    for user, label in users:
        sequences.append(
            torch.tensor(
                [get_point_from_result(result) for result in user],
                dtype=torch.float32,
            )
        )
        labels.append(label)

    dataset = LifterDataset(sequences, labels)
    dataloader = DataLoader(dataset, collate_fn=collate_fn)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info("Using device %s", device)

    for name in model_names:
        hyperparam_path = trained_models_dir / f"{name}_hyperparameters.txt"
        if not hyperparam_path.exists():
            logger.error("Missing hyperparameter file for model %s", name)
            continue

        # Read hyperparameters from the text file
        with open(hyperparam_path, "r") as f:
            lines = f.readlines()

        try:
            hidden_size = int(lines[1].split(":")[1].strip())
            num_layers = int(lines[2].split(":")[1].strip())
            dropout = float(lines[3].split(":")[1].strip())
            _lr = float(lines[4].split(":")[1].strip())
        except (IndexError, ValueError) as e:
            logger.error("Could not parse hyperparameters for model %s: %s", name, e)
            continue

        model_class = {
            "LSTM": LifterLSTM,
            "RNN": LifterRNN,
            "Bidirectional_LSTM": LifterBiLSTM,
        }.get(name)

        if model_class is None:
            logger.error("Unknown model name: %s", name)
            continue

        model: BaseNetwork = model_class(
            input_size=7,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
            device=device,
        )
        model.to(device)

        save_path = trained_models_dir / f"{name}_lifter_model"
        if save_path.exists():
            model.load_from(save_path)
        else:
            logger.error(
                "Could not find saved model weights at %s for %s. Skipping evaluation.",
                save_path,
                name,
            )
            continue

        logger.info("Evaluating model: %s", name)
        metrics = model.evaluate(dataloader)
        logger.info(
            "%s evaluation on golden labels (drug use = %s): %s",
            name,
            IS_USING_LABEL,
            metrics,
        )

        # Filter metrics to plot (exclude tensors like predictions/labels)
        metrics_to_plot = {
            k.capitalize(): v for k, v in metrics.items() if isinstance(v, (float, int))
        }
        ordered_keys = ["F1", "Accuracy", "Precision", "Recall"]
        plot_metrics = {
            k: metrics_to_plot[k] for k in ordered_keys if k in metrics_to_plot
        }

        plt.figure(figsize=(8, 5))
        plt.bar(
            plot_metrics.keys(),
            plot_metrics.values(),
            color=["#4CAF50", "#2196F3", "#FFC107", "#FF5722"],
        )
        plt.ylim(0, 1.1)
        plt.title(f"{name} - Best Metric Scores on True Test Set")
        for i, (k, v) in enumerate(plot_metrics.items()):
            plt.text(i, v + 0.01, f"{v:.2f}", ha="center", va="bottom")
        plt.ylabel("Score")
        plt.savefig(graph_loc / f"{name}_test_metrics_bar.png")
        plt.close()
