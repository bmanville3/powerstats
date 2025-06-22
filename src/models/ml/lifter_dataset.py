import logging
from typing import Sequence

import torch
from torch import Tensor
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset

from src.database.database import Database
from src.database.tables.dto_table.result import ResultTable
from src.models.dto.result import Result

logger = logging.getLogger(__name__)


class LifterDataset(Dataset[tuple[Tensor, float]]): # type: ignore
    def __init__(self, sequences: list[Tensor], labels: list[float]) -> None:
        self.sequences: list[Tensor] = sequences
        self.labels: list[float] = labels

    def __len__(self) -> int:
        return len(self.sequences)

    def __getitem__(self, idx: int) -> tuple[Tensor, float]:
        return self.sequences[idx], self.labels[idx]


def collate_fn(
    batch: Sequence[tuple[Tensor, float]],
) -> tuple[Tensor, Tensor]:
    sequences, labels = zip(*batch)
    padded_seqs: Tensor = pad_sequence(sequences, batch_first=True)
    label_tensor: Tensor = torch.tensor(labels, dtype=torch.float32)
    return padded_seqs, label_tensor


def get_train_test_data_from_extracted(
    data: list[list[Result]],
) -> tuple[DataLoader, DataLoader]:
    sequences = []
    labels = []
    num_1s = 0
    for list_results in data:
        for i in range(len(list_results)):
            new_sequence = []
            for j in range(i + 1):
                result = list_results[j]
                new_sequence.append(
                    [
                        result.best3_bench_kg,
                        result.best3_deadlift_kg,
                        result.best3_squat_kg,
                        result.total_kg,
                        result.bodyweight_kg,
                        result.age,
                        1 if result.sex == "M" else 0,
                    ]
                )
            sequences.append(torch.tensor(new_sequence, dtype=torch.float32))
            if list_results[i].tested == "yes":
                num_1s += 1
                labels.append(1.0)
            else:
                labels.append(0.0)
    logger.info(
        "Created %d sequences from %d result entries. Percent tested: %.2f%%", len(sequences), len(data), num_1s * 100 / len(sequences)
    )
    dataset = LifterDataset(sequences, labels)
    train, test = torch.utils.data.random_split(dataset, [0.8, 0.2])
    logger.info(
        "Training dataset size: %d Testing dataset size: %d", len(train), len(test)
    )
    return DataLoader(
        train, shuffle=True, batch_size=128, collate_fn=collate_fn
    ), DataLoader(test, collate_fn=collate_fn)


def get_train_test_data_from_db() -> tuple[DataLoader, DataLoader]:
    database = Database()
    result_table = ResultTable(database)
    all_results = result_table.get_all()

    lifters_to_results: dict[str, list[Result]] = {}
    for result in all_results:
        if result.sex == "Mx":
            continue
        lifters_to_results.setdefault(result.name, []).append(result)
    list_saved = [
        sorted(result_list, key=lambda res: res.date)
        for result_list in lifters_to_results.values()
    ]
    return get_train_test_data_from_extracted(
        [
            res
            for res in list_saved
            if len(res) > 0
        ]
    )
