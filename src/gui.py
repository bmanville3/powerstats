import tkinter as tk
from dataclasses import dataclass
from datetime import datetime
from tkinter import messagebox, simpledialog, ttk

import torch

from src.models.dto.result import Result
from src.models.ml.base import BaseNetwork
from src.models.ml.lifter_dataset import get_point_from_result
from src.models.ml.trainer import load_best_model
from src.utils.utils import POWERSTATS


@dataclass
class ResultSubset:
    best3_bench_kg: float
    best3_deadlift_kg: float
    best3_squat_kg: float
    total_kg: float
    bodyweight_kg: float
    age: float
    sex: str
    date: str

    def to_partial_result(self) -> Result:
        return Result(
            result_id=None, # type: ignore
            name=None, # type: ignore
            sex=self.sex,
            age=self.age,
            bodyweight_kg=self.bodyweight_kg,
            best3_bench_kg=self.best3_bench_kg,
            best3_deadlift_kg=self.best3_deadlift_kg,
            best3_squat_kg=self.best3_squat_kg,
            wilks=None, # type: ignore
            dots=None, # type: ignore
            federation=None, # type: ignore
            place=None, # type: ignore
            tested=None, # type: ignore
            total_kg=self.total_kg,
            date=self.date,
            sanctioned=None, # type: ignore
        )


class ResultEntryApp:
    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.title("Result Entry")
        self.results: list[ResultSubset] = []
        self.all_dates: set[str] = set()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        rnn = load_best_model(
            "RNN", POWERSTATS / "trained_models", self.device
        )
        if rnn is None:
            raise ValueError("Could not load rnn")
        self.rnn: BaseNetwork = rnn
        lstm = load_best_model(
            "LSTM", POWERSTATS / "trained_models", self.device
        )
        if lstm is None:
            raise ValueError("Could not load lstm")
        self.lstm: BaseNetwork = lstm
        bi_lstm = load_best_model(
            "Bidirectional_LSTM", POWERSTATS / "trained_models", self.device
        )
        if bi_lstm is None:
            raise ValueError("Could not load bi_lstm")
        self.bi_lstm: BaseNetwork = bi_lstm
        self.fields = {}

        labels = [
            ("Bench (kg)", "best3_bench_kg"),
            ("Deadlift (kg)", "best3_deadlift_kg"),
            ("Squat (kg)", "best3_squat_kg"),
            ("Bodyweight (kg)", "bodyweight_kg"),
            ("Age", "age"),
            ("Sex (M/F)", "sex"),
            ("Date (YYYY-MM-DD) *", "date"),
        ]

        for idx, (label_text, field_name) in enumerate(labels):
            label = tk.Label(root, text=label_text)
            entry = tk.Entry(root)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.fields[field_name] = entry

        # Model Selection Dropdown
        model_label = tk.Label(root, text="Select Model:")
        model_label.grid(row=len(labels), column=0, sticky="e", padx=5)

        self.model_var = tk.StringVar(value="Bidirectional_LSTM")
        model_dropdown = ttk.Combobox(
            root,
            textvariable=self.model_var,
            values=["RNN", "LSTM", "Bidirectional_LSTM"],
            state="readonly",
            width=20,
        )
        model_dropdown.grid(row=len(labels), column=1, sticky="w", padx=5, pady=5)

        # Buttons side by side
        button_row = len(labels) + 1
        submit_button = tk.Button(root, text="Add Result", command=self.submit)
        submit_button.grid(row=button_row, column=0, padx=5, pady=5)

        delete_button = tk.Button(
            root, text="Delete by Date", command=self.delete_by_date
        )
        delete_button.grid(row=button_row, column=1, padx=5, pady=5)

        delete_all_button = tk.Button(root, text="Delete All", command=self.delete_all)
        delete_all_button.grid(row=button_row, column=2, padx=5, pady=5)

        calculate_button = tk.Button(root, text="Calculate", command=self.calculate)
        calculate_button.grid(row=button_row, column=3, padx=5, pady=5)

        # Prediction output
        self.prediction_output = tk.Text(root, height=4, width=120)
        self.prediction_output.config(state=tk.DISABLED)
        self.prediction_output.grid(
            row=button_row + 1, column=0, columnspan=4, padx=5, pady=5
        )

        # Results display
        self.results_display = tk.Text(root, height=10, width=120)
        self.results_display.config(state=tk.DISABLED)
        self.results_display.grid(
            row=button_row + 2, column=0, columnspan=4, padx=5, pady=5
        )

        # Disclaimer text
        disclaimer = (
            "* Note: The dates entered are not used by the model. They are only used to keep relative order of entries.\n\n"
            "Disclaimer: This prediction is made by a machine learning model trained on historical data.\n"
            "The model is a proof of concept and its ability to handle outliers is likely insufficient.\n"
            "It may not be fully accurate or generalizable. Do not use it for medical or legal decisions.\n"
        )
        disclaimer_label = tk.Label(
            root, text=disclaimer, fg="gray", justify="left", wraplength=700
        )
        disclaimer_label.grid(
            row=button_row + 3, column=0, columnspan=4, padx=5, pady=(0, 10)
        )

    def validate_and_parse(self) -> None | ResultSubset:
        try:
            bench = float(self.fields["best3_bench_kg"].get())
            deadlift = float(self.fields["best3_deadlift_kg"].get())
            squat = float(self.fields["best3_squat_kg"].get())
            bw = float(self.fields["bodyweight_kg"].get())
            age = float(self.fields["age"].get())
            sex = self.fields["sex"].get().strip().upper()
            date_str = self.fields["date"].get().strip()

            if not all(val > 0 for val in [bench, deadlift, squat, bw]):
                raise ValueError("All weight values must be > 0.")

            if not (13 <= age <= 120):
                raise ValueError("Age must be between 13 and 120.")

            if not (20 <= bw <= 400):
                raise ValueError("Bodyweight must be between 20kg and 400kg")

            if sex not in ("M", "F"):
                raise ValueError("Sex must be 'M' or 'F'.")

            datetime.strptime(date_str, "%Y-%m-%d")
            if date_str in self.all_dates:
                raise ValueError(
                    f"{date_str} already in use. Only one entry per date allowed"
                )
            self.all_dates.add(date_str)

            return ResultSubset(
                best3_bench_kg=bench,
                best3_deadlift_kg=deadlift,
                best3_squat_kg=squat,
                total_kg=bench + squat + deadlift,
                bodyweight_kg=bw,
                age=age,
                sex=sex,
                date=date_str,
            )
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return None

    def submit(self) -> None:
        result = self.validate_and_parse()
        if result:
            self.results.append(result)
            self.refresh_display()
            for entry in self.fields.values():
                entry.delete(0, tk.END)

    def delete_by_date(self) -> None:
        date_to_delete = simpledialog.askstring(
            "Delete by Date", "Enter date to delete (YYYY-MM-DD):"
        )
        if not date_to_delete:
            return
        try:
            datetime.strptime(date_to_delete, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Date format must be YYYY-MM-DD.")
            return
        if date_to_delete not in self.all_dates:
            messagebox.showinfo(
                "Not Found", f"No results found for date {date_to_delete}."
            )

        self.results = [r for r in self.results if r.date != date_to_delete]
        self.all_dates.remove(date_to_delete)
        self.refresh_display()

    def delete_all(self) -> None:
        self.results = []
        self.all_dates = set()
        self.refresh_display()
        self.prediction_output.config(state=tk.NORMAL)
        self.prediction_output.delete("1.0", tk.END)
        self.prediction_output.config(state=tk.DISABLED)

    def calculate(self) -> None:
        if not self.results:
            messagebox.showinfo("No Data", "No results to calculate.")
            return

        self.refresh_display()

        try:
            sequence = [
                get_point_from_result(result.to_partial_result())
                for result in self.results
            ]
            model_name = self.model_var.get()
            model = {
                "RNN": self.rnn,
                "LSTM": self.lstm,
                "Bidirectional_LSTM": self.bi_lstm,
            }[model_name]

            model.eval()
            with torch.no_grad():
                prediction = model(
                    torch.tensor(sequence).unsqueeze(0).to(self.device)
                ).item()

            label = "Using Drugs" if prediction >= 0.5 else "Not Using Drugs"

            # Display prediction
            self.prediction_output.config(state=tk.NORMAL)
            self.prediction_output.delete("1.0", tk.END)
            self.prediction_output.insert(
                tk.END,
                f"Prediction: {label}\nProbability of Using Drugs = {prediction}\nDone with {model_name} model",
            )
            self.prediction_output.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))

    def refresh_display(self) -> None:
        self.results = list(sorted(self.results, key=lambda r: r.date))
        self.results_display.config(state=tk.NORMAL)
        self.results_display.delete("1.0", tk.END)
        for result in self.results:
            self.results_display.insert(tk.END, f"{result}\n")
        self.results_display.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = ResultEntryApp(root)
    root.mainloop()
