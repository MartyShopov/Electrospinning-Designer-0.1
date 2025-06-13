import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression

class PolynomialRegressionApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Polynomial Regression Formula")
        self.window.geometry("1000x750")
        self.font_style = ("Arial", 14)

        self.upload_button = tk.Button(window, text="Select CSV File", command=self.upload_and_calculate, font=self.font_style, width=20, height=2)
        self.upload_button.pack(pady=10)

        self.output_text = tk.Text(window, wrap=tk.WORD, font=("Courier New", 12), height=5)
        self.output_text.pack(padx=20, pady=10, fill=tk.X)

        self.plot_frame = tk.Frame(window)
        self.plot_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.navigation_frame = tk.Frame(window)

        self.prev_button = tk.Button(self.navigation_frame, text="Previous", command=self.show_prev_plot, font=self.font_style)
        self.next_button = tk.Button(self.navigation_frame, text="Next", command=self.show_next_plot, font=self.font_style)
        self.plot_label = tk.Label(self.navigation_frame, text="", font=self.font_style)

        self.prev_button.pack(side=tk.LEFT, padx=20)
        self.plot_label.pack(side=tk.LEFT, padx=20)
        self.next_button.pack(side=tk.LEFT, padx=20)

        self.navigation_frame.pack_forget()  # hide initially

        self.plots = []
        self.current_plot_index = 0
        self.canvas = None

    def upload_and_calculate(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            self.formula, self.plots = self.polynomial_regression_and_plots(file_path)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, self.formula)
            self.current_plot_index = 0
            self.show_current_plot()

            if len(self.plots) > 1:
                self.prev_button.config(state=tk.NORMAL)
                self.next_button.config(state=tk.NORMAL)
            else:
                self.prev_button.config(state=tk.DISABLED)
                self.next_button.config(state=tk.DISABLED)

            self.update_plot_label()
            self.navigation_frame.pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def polynomial_regression_and_plots(self, csv_file):
        df = pd.read_csv(csv_file)
        df.columns = [f"X{x}" for x in range(1, len(df.columns) + 1)]
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        feature_names = X.columns.tolist()

        stats = {
            feature: {
                "min": X[feature].min(),
                "max": X[feature].max(),
                "mean": X[feature].mean()
            } for feature in feature_names
        }

        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)

        poly = PolynomialFeatures(degree=2, include_bias=False)
        X_poly = poly.fit_transform(X_scaled)

        poly_feature_names = poly.get_feature_names_out(feature_names)

        model = LinearRegression()
        model.fit(X_poly, y)

        formula_terms = []
        for coef, name in zip(model.coef_, poly_feature_names):
            term = name.replace(" ", "*")
            if coef >= 0:
                formula_terms.append(f"+ {coef:.2f}*{term}")
            else:
                formula_terms.append(f"- {abs(coef):.2f}*{term}")

        intercept = f"{model.intercept_:.2f}"
        formula = f"y = {intercept} " + " ".join(formula_terms)

        plots = []
        for feature_pair in itertools.combinations(feature_names, 2):
            fig = self.generate_contour_plot(feature_pair, feature_names, stats, scaler, poly, model)
            plots.append(fig)

        return formula, plots

    def generate_contour_plot(self, feature_pair, feature_names, stats, scaler, poly, model):
        f1, f2 = feature_pair

        f1_vals = np.linspace(stats[f1]["min"], stats[f1]["max"], 50)
        f2_vals = np.linspace(stats[f2]["min"], stats[f2]["max"], 50)
        F1_grid, F2_grid = np.meshgrid(f1_vals, f2_vals)

        data = []
        for i in range(F1_grid.shape[0]):
            for j in range(F1_grid.shape[1]):
                row = []
                for feature in feature_names:
                    if feature == f1:
                        row.append(F1_grid[i, j])
                    elif feature == f2:
                        row.append(F2_grid[i, j])
                    else:
                        row.append(stats[feature]["mean"])
                data.append(row)

        data = pd.DataFrame(data, columns=feature_names)
        data_scaled = scaler.transform(data)
        data_poly = poly.transform(data_scaled)
        y_pred = model.predict(data_poly)
        Z = y_pred.reshape(F1_grid.shape)

        fig, ax = plt.subplots(figsize=(6, 5))
        contour = ax.contourf(F1_grid, F2_grid, Z, levels=20, cmap="viridis")
        plt.colorbar(contour, ax=ax, label="Predicted y")
        ax.set_xlabel(f1)
        ax.set_ylabel(f2)
        ax.set_title(f"Contour Plot: {f1} vs {f2}")
        plt.close(fig)
        return fig

    def show_current_plot(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig = self.plots[self.current_plot_index]
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_plot_label()

    def show_next_plot(self):
        if not self.plots:
            return
        self.current_plot_index = (self.current_plot_index + 1) % len(self.plots)
        self.show_current_plot()

    def show_prev_plot(self):
        if not self.plots:
            return
        self.current_plot_index = (self.current_plot_index - 1) % len(self.plots)
        self.show_current_plot()

    def update_plot_label(self):
        if self.plots:
            self.plot_label.config(text=f"Plot {self.current_plot_index + 1} of {len(self.plots)}")
        else:
            self.plot_label.config(text="")

def create_polynomial_regression_window():
    window = tk.Tk()
    app = PolynomialRegressionApp(window)
    window.mainloop()