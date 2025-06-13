# Electrospinning Designer 1.0

A Python-based GUI application for scientific modeling, regression analysis, and experimental design, with a focus on electrospinning research.

---

## Overview

**Electrospinning Designer 1.0** is designed for researchers and engineers working in electrospinning, nanomaterials, and materials science. It integrates several tools into a single desktop application:

- 📊 **Polynomial Regression**: Import CSV data, fit 2nd-degree polynomial regression models, extract formulas, and generate 2D contour plots for pairwise variables.
- 🔬 **Uc Calculation Module**: Compute and visualize the critical voltage (Uc) based on surface tension, geometry, and distance parameters, with interactive contour plotting.
- 🧪 **Box-Behnken Design Generator**: Generate Box-Behnken experimental designs for multiple factors with user-defined center points.

---

## Features

### 1️⃣ Main Menu  
A simple launcher that allows you to choose between the modules:

- **Uc Calculation**
- **Box-Behnken Design**
- **Polynomial Regression**

### 2️⃣ Polynomial Regression

- Load CSV datasets with multiple input variables and a target response.
- Fit a second-degree polynomial regression model using scikit-learn.
- Extract symbolic formula for the model.
- Visualize pairwise variable contour plots automatically.

### 3️⃣ Uc (Critical Voltage) Calculation

- Calculates the critical voltage using a provided electrospinning formula.
- Visualize contour plots for any two selected variables while keeping the others constant.
- Customizable input ranges.

### 4️⃣ Box-Behnken Design

- Generate experimental designs for any number of factors (≥3).
- Supports flexible center point specification.
- Displays results in a scrollable table for easy export.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/MartyShopov/Electrospinning-Designer-0.1.git
cd Electrospinning-Designer

