import tkinter as tk
from tkinter import ttk, messagebox
import itertools
import pandas as pd

# The Box-Behnken function
def generate_box_behnken(num_factors, num_center_points=3):
    if num_factors < 3:
        raise ValueError("Box-Behnken design requires at least 3 factors.")
    
    design = []
    
    factor_pairs = list(itertools.combinations(range(num_factors), 2))
    
    for i, j in factor_pairs:
        for level_i in [-1, 1]:
            for level_j in [-1, 1]:
                run = [0] * num_factors
                run[i] = level_i
                run[j] = level_j
                design.append(run)
    
    center_point = [0] * num_factors
    for _ in range(num_center_points):
        design.append(center_point)
    
    columns = [f"X{i+1}" for i in range(num_factors)]
    df = pd.DataFrame(design, columns=columns)

    # Add index column
    df.insert(0, "Run", range(1, len(df)+1))

    return df

# GUI Function
def create_box_behnken_window():
    window = tk.Tk()
    window.title("Box-Behnken Design Generator")

    font_style = ("Arial", 14)
    entry_width = 15
    padding = 10

    input_frame = tk.Frame(window)
    input_frame.pack(side=tk.TOP, pady=padding)

    tk.Label(input_frame, text="Number of Factors:", font=font_style).grid(row=0, column=0, padx=padding, pady=padding)
    factors_entry = tk.Entry(input_frame, font=font_style, width=entry_width)
    factors_entry.grid(row=0, column=1, padx=padding, pady=padding)

    tk.Label(input_frame, text="Number of Center Points:", font=font_style).grid(row=1, column=0, padx=padding, pady=padding)
    centers_entry = tk.Entry(input_frame, font=font_style, width=entry_width)
    centers_entry.grid(row=1, column=1, padx=padding, pady=padding)

    # Output frame
    output_frame = tk.Frame(window)
    output_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    text_box = tk.Text(output_frame, wrap=tk.NONE, font=("Courier New", 12))
    text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add scrollbars
    y_scroll = tk.Scrollbar(output_frame, orient=tk.VERTICAL, command=text_box.yview)
    y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    text_box.configure(yscrollcommand=y_scroll.set)

    x_scroll = tk.Scrollbar(output_frame, orient=tk.HORIZONTAL, command=text_box.xview)
    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    text_box.configure(xscrollcommand=x_scroll.set)

    def generate():
        try:
            num_factors = int(factors_entry.get())
            num_centers = int(centers_entry.get())
            df = generate_box_behnken(num_factors, num_centers)
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))
            return

        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, df.to_string(index=False))

    submit_btn = tk.Button(input_frame, text="Generate Design", command=generate, font=font_style)
    submit_btn.grid(row=2, column=0, columnspan=2, padx=padding, pady=padding)

    window.mainloop()