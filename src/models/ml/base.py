import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable

import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from torch.utils.data import DataLoader

logger = logging.getLogger(__name__)


class BaseNetwork(ABC, nn.Module):  # type: ignore
    def __init__(self, device: str | None = None):
        super().__init__()
        if device:
            self.device = device
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info("Using device %s", self.device)
        self.to(device=self.device)

    @abstractmethod
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        pass

    def load_from(self, file: str | Path) -> None:
        if isinstance(file, str):
            file = Path(file)
        file = file.absolute()
        if not file.exists():
            raise ValueError(f"File {file} does not exist")
        checkpoint = torch.load(file, map_location=self.device)
        self.load_state_dict(checkpoint["model_state_dict"])
        logger.info("Loaded model from %s", file)

    def save_to(self, file: str | Path, allow_override: bool = False) -> None:
        if isinstance(file, str):
            file = Path(file)
        file = file.absolute()
        if file.exists() and not allow_override:
            raise ValueError(
                f"Tried to save to file {file} but already exists and override turned off"
            )
        torch.save({"model_state_dict": self.state_dict()}, file)
        logger.info("Saved model to %s", file)

    def train_model(
        self,
        dataloader: DataLoader,
        optimizer: torch.optim.Optimizer,
        loss_fn: nn.Module,
        epochs: int = 10,
        scheduler: torch.optim.lr_scheduler.LRScheduler | None = None,
        verbose: bool = True,
        save_loc: str | Path | None = None,
        val_dataloader: DataLoader | None = None,
    ) -> tuple[list[float], list[float] | None]:
        self.train()
        best = float("inf")
        losses_training: list[float] = []
        loss_validation: list[float] = []

        for epoch in range(epochs):
            logger.info("Starting epoch %d/%d", epoch + 1, epochs)
            total_loss = 0.0
            correct = 0
            total = 0

            for batch in dataloader:
                inputs, labels = batch
                inputs = inputs.to(self.device).float()
                labels = labels.to(self.device).float()

                optimizer.zero_grad()
                outputs = self(inputs)
                loss = loss_fn(outputs, labels)
                loss.backward()
                optimizer.step()

                total_loss += loss.item()

                if verbose:
                    preds = (outputs > 0.5).float()
                    correct += (preds == labels).sum().item()
                    total += labels.size(0)

            if scheduler:
                scheduler.step()

            avg_loss = total_loss / len(dataloader)
            losses_training.append(avg_loss)
            accuracy = correct / total if total > 0 else 0.0

            if verbose:
                logger.info(
                    f"Epoch {epoch + 1}/{epochs}, Train Loss: {avg_loss:.4f}, Train Accuracy: {accuracy:.4f}"
                )

            # Validation phase (if applicable)
            val_loss = None
            if val_dataloader:
                self.eval()
                with torch.no_grad():
                    val_total_loss = 0.0
                    for batch in val_dataloader:
                        inputs, labels = batch
                        inputs = inputs.to(self.device).float()
                        labels = labels.to(self.device).float()
                        outputs = self(inputs)
                        loss = loss_fn(outputs, labels)
                        val_total_loss += loss.item()
                    val_loss = val_total_loss / len(val_dataloader)
                loss_validation.append(val_loss)
                if verbose:
                    logger.info(
                        f"Epoch {epoch + 1}/{epochs}, Validation Loss: {val_loss:.4f}"
                    )

                self.train()

            # Determine best loss for saving
            current_loss = val_loss if val_loss is not None else avg_loss
            if save_loc and current_loss < best:
                best = current_loss
                logger.info("Saving new best model to %s", save_loc)
                self.save_to(save_loc, True)

        return (losses_training, None) if val_dataloader is None else (losses_training, loss_validation)

    def evaluate(
        self,
        dataloader: DataLoader,
        loss_fn: Callable[[torch.Tensor, torch.Tensor], torch.Tensor] | None = None,
        metric_fn: Callable[[torch.Tensor, torch.Tensor], float] | None = None,
    ) -> dict[str, float | torch.Tensor]:
        self.eval()
        total_loss = 0.0
        all_preds = []
        all_labels = []

        with torch.no_grad():
            for batch in dataloader:
                inputs, labels, *extra = batch
                inputs = inputs.to(self.device).float()
                labels = labels.to(self.device).float()

                outputs = self(inputs, *extra) if extra else self(inputs)
                if loss_fn:
                    loss = loss_fn(outputs, labels)
                    total_loss += loss.item()
                all_preds.append(outputs.cpu())
                all_labels.append(labels.cpu())

        preds_tensor = torch.cat(all_preds)
        labels_tensor = torch.cat(all_labels)

        preds_bin = (preds_tensor > 0.5).int().numpy()
        labels_np = labels_tensor.int().numpy()

        results: dict[str, float | torch.Tensor] = {
            "accuracy": accuracy_score(labels_np, preds_bin),
            "precision": precision_score(labels_np, preds_bin, zero_division=0),
            "recall": recall_score(labels_np, preds_bin, zero_division=0),
            "f1": f1_score(labels_np, preds_bin, zero_division=0),
            "predictions": preds_tensor,
            "labels": labels_tensor,
        }

        if loss_fn:
            results["loss"] = total_loss / len(dataloader)
        if metric_fn:
            results["metric"] = metric_fn(preds_tensor, labels_tensor)
        return results

    def train_model_auto(
        self,
        dataloader: DataLoader,
        epochs: int = 10,
        verbose: bool = True,
        save_loc: str | Path | None = None,
    ) -> tuple[list[float], list[float] | None]:
        optimizer = self.get_optimizer()
        return self.train_model(
            dataloader,
            self.get_optimizer(),
            self.get_loss_fn(),
            epochs,
            self.get_scheduler(optimizer),
            verbose,
            save_loc,
        )

    @abstractmethod
    def get_optimizer(self) -> torch.optim.Optimizer:
        pass

    @abstractmethod
    def get_loss_fn(self) -> Callable[[torch.Tensor, torch.Tensor], torch.Tensor]:
        pass

    def get_scheduler(
        self, _optimizer: torch.optim.Optimizer
    ) -> torch.optim.lr_scheduler.LRScheduler | None:
        return None
