import tkinter as tk
from tkinter import ttk
import Window_Uc
import Window_BBD
import Window_PolyRegression

def open_uc_window():
    Window_Uc.create_window()

def open_bbd_window():
    Window_BBD.create_box_behnken_window()

def open_poly_regression_window():
    Window_PolyRegression.create_polynomial_regression_window()

def main():
    root = tk.Tk()
    root.title("Main Menu")

    root.geometry("400x400")
    root.resizable(False, False)

    font_style = ("Arial", 16)
    padding = 20

    title_label = tk.Label(root, text="Electrospinning Designer 1.0", font=("Arial", 18, "bold"))
    title_label.pack(pady=padding)

    uc_button = tk.Button(root, text="Uc Calculation", command=open_uc_window, font=font_style, width=25, height=2)
    uc_button.pack(pady=padding)

    bbd_button = tk.Button(root, text="Box-Behnken Design", command=open_bbd_window, font=font_style, width=25, height=2)
    bbd_button.pack(pady=padding)

    poly_button = tk.Button(root, text="Polynomial Regression", command=open_poly_regression_window, font=font_style, width=25, height=2)
    poly_button.pack(pady=padding)

    root.mainloop()

if __name__ == "__main__":
    main()