import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# Original function
def uc(gamma, H, R, h):
    Uc_squared = (4 * H**2 / h**2) * math.log((2 * h / R) - 1.5) * (0.117 * math.pi * gamma * R)
    return Uc_squared ** 0.5

# Modified function (returns the figure)
def create_contour_figure(X_var, Y_var, const_1, const_2):
    units = {
        "Surface Tension" : "dyn/cm",
        "H" : "cm",
        "R" : "cm",
        "h" : "cm"
    }

    value_ranges = {
        "Surface Tension_min" : 20,
        "Surface Tension_max" : 80,
        "H_min" : 10,
        "H_max" : 30, 
        "R_min" : 0.007,
        "R_max" : 0.05,
        "h_min" : 0.5,
        "h_max" : 6
    }
    
    values = {
        "Surface Tension" : None,
        "H" : None,
        "R" : None,
        "h" : None
    }
    
    X_range = np.linspace(value_ranges[f"{X_var}_min"], value_ranges[f"{X_var}_max"], 500)
    Y_range = np.linspace(value_ranges[f"{Y_var}_min"], value_ranges[f"{Y_var}_max"], 500)
    
    X_mesh, Y_mesh = np.meshgrid(X_range, Y_range)

    values[X_var] = X_mesh
    values[Y_var] = Y_mesh

    fill = const_1
    assigned = []
    for key in values:
        if values[key] is None:
            values[key] = fill
            assigned.append((key, fill))
            fill = const_2

    uc_values = np.vectorize(uc)(values["Surface Tension"], values["H"], values["R"], values["h"])
    uc_values = np.clip(uc_values, 10, 30)
    
    fig, ax = plt.subplots(figsize=(6, 5))
    c = ax.contourf(X_mesh, Y_mesh, uc_values, levels=20, cmap="viridis")
    fig.colorbar(c, label="$U_c$, kV", ax=ax)
    ax.set_xlabel(f"{X_var}, {units[X_var]}")
    ax.set_ylabel(f"{Y_var}, {units[Y_var]}")
    
    # Build the title string
    const_info = ", ".join([f"{var} = {val} {units[var]}" for var, val in assigned])
    ax.set_title(const_info, fontsize=12)
    
    fig.tight_layout()
    
    return fig

# GUI Part
def create_window():
    window = tk.Tk()
    window.title("Contour Plot Generator")

    variables = ["Surface Tension", "H", "R", "h"]

    font_style = ("Arial", 14)
    entry_width = 15
    padding = 10

    # Input frame
    input_frame = tk.Frame(window)
    input_frame.pack(side=tk.TOP, pady=padding)

    tk.Label(input_frame, text="Select X variable:", font=font_style).grid(row=0, column=0, padx=padding, pady=padding)
    x_var = ttk.Combobox(input_frame, values=variables, font=font_style, width=entry_width)
    x_var.grid(row=0, column=1, padx=padding, pady=padding)

    tk.Label(input_frame, text="Select Y variable:", font=font_style).grid(row=1, column=0, padx=padding, pady=padding)
    y_var = ttk.Combobox(input_frame, values=variables, font=font_style, width=entry_width)
    y_var.grid(row=1, column=1, padx=padding, pady=padding)

    tk.Label(input_frame, text="Enter const_1:", font=font_style).grid(row=2, column=0, padx=padding, pady=padding)
    const1_entry = tk.Entry(input_frame, font=font_style, width=entry_width)
    const1_entry.grid(row=2, column=1, padx=padding, pady=padding)

    tk.Label(input_frame, text="Enter const_2:", font=font_style).grid(row=3, column=0, padx=padding, pady=padding)
    const2_entry = tk.Entry(input_frame, font=font_style, width=entry_width)
    const2_entry.grid(row=3, column=1, padx=padding, pady=padding)

    # Plot frame
    plot_frame = tk.Frame(window)
    plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    canvas = None  # Canvas placeholder

    def submit():
        nonlocal canvas

        X = x_var.get()
        Y = y_var.get()
        try:
            c1 = float(const1_entry.get())
            c2 = float(const2_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numeric values for const_1 and const_2.")
            return

        if X == Y or X == "" or Y == "":
            messagebox.showerror("Error", "X and Y variables must be different and selected.")
            return

        fig = create_contour_figure(X, Y, c1, c2)

        if canvas:
            canvas.get_tk_widget().destroy()

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    submit_btn = tk.Button(input_frame, text="Generate Plot", command=submit, font=font_style)
    submit_btn.grid(row=4, column=0, columnspan=2, padx=padding, pady=padding)

    window.mainloop()