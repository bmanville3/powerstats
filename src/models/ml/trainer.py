import logging

from src.models.ml.base import BaseNetwork
from src.models.ml.lifter_dataset import get_train_test_data_from_db
from src.models.ml.lstm import LifterLSTM
from src.utils import find_dir

logger = logging.getLogger(__name__)


def train_models(model_names: set[str]) -> dict[str, BaseNetwork]:
    trained_models: dict[str, BaseNetwork] = {}
    powerstats_dir = find_dir("trained_models")
    train, test = get_train_test_data_from_db()

    if "LSTM" in model_names:
        model_names.remove("LSTM")
        trained_models["LSTM"] = LifterLSTM(7, 100)

    if len(model_names) != 0:
        logger.error("Unknown models to train: %s", model_names)

    for name, model in trained_models.items():
        logger.info("Training model: %s", name)
        save_path = powerstats_dir / f"{name}_lifter_model"
        if save_path.exists():
            model.load_from(powerstats_dir / f"{name}_lifter_model")
        model.train_model_auto(train, save_loc=powerstats_dir / f"{name}_lifter_model")
        model.load_from(powerstats_dir / f"{name}_lifter_model")
        logger.info("Evaluating model: %s", name)
        model.evaluate(test)
        trained_models[name] = model
    return trained_models
