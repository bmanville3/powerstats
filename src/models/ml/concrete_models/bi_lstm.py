from typing import override

import torch
import torch.nn as nn
from torch import Tensor
from torch.nn.utils.rnn import pack_padded_sequence

from src.models.ml.base import BaseNetwork


class LifterBiLSTM(BaseNetwork):
    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        num_layers: int = 1,
        dropout: float = 0.1,
        device: str | None = None,
    ) -> None:
        super().__init__(device)
        self.hidden_size = hidden_size
        self.num_directions = 2  # because it's bidirectional

        self.lstm: nn.LSTM = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
            bidirectional=True,
        )
        # Output from LSTM will be (batch, hidden_size * 2)
        self.classifier: nn.Linear = nn.Linear(hidden_size * self.num_directions, 1)

    @override
    def forward(self, x: Tensor) -> Tensor:
        # x: (batch, seq_len, input_size)

        # Infer lengths by assuming rows with all 0s are padding
        with torch.no_grad():
            mask = x.abs().sum(dim=2) > 0  # (batch, seq_len)
            lengths = mask.sum(dim=1)  # (batch,)

        packed = pack_padded_sequence(
            x, lengths.cpu(), batch_first=True, enforce_sorted=False
        )
        _, (hn, _) = self.lstm(packed)
        # hn shape: (num_layers * num_directions, batch, hidden_size)

        # Concatenate last layer's forward and backward hidden states
        forward_last = hn[-2]
        backward_last = hn[-1]
        out = torch.cat(
            (forward_last, backward_last), dim=1
        )  # (batch, hidden_size * 2)

        logits: Tensor = self.classifier(out).squeeze(1)  # (batch,)
        return torch.sigmoid(logits)

    @override
    def get_optimizer(self) -> torch.optim.Optimizer:
        return torch.optim.SGD(self.parameters(), lr=0.001)

    @override
    def get_loss_fn(self) -> nn.Module:
        return nn.BCELoss()
