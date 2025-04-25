import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.path import Path

diameters = np.arange(0.1, 0.4, 0.025)  # [m]

# include diameter name in file

def plot_pile_data(diameters, column_name):
    
    # Create the subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 6), sharex=True)

    for select in range(len(diameters)):
        # Load the CSV file
        csv_filename = f"pile_D{diameters[select]}.csv" # Replace with your actual file name
        data = pd.read_csv(csv_filename)

        # Filter data based on pile_number
        pile_1_data = data[data["pile_number"] == 1]
        pile_2_data = data[data["pile_number"] == 2]
        pile_3_data = data[data["pile_number"] == 3]

        # Plot data for pile 1
        axes[0].plot(pile_1_data[column_name], pile_1_data["y"], label=f"D = {diameters[select]:.3f} m")
        axes[0].set_title("Pile 1: Bending Moment over Depth")
        axes[0].set_xlabel(f"{column_name} [kNm]")
        axes[0].set_ylabel("Depth [m]")
        axes[0].legend()
        axes[0].grid()

        # Plot data for pile 2
        axes[1].plot(pile_2_data[column_name], pile_2_data["y"], label=f"D = {diameters[select]:.3f} m")
        axes[1].set_title("Pile 2: Bending Moment over Depth")
        axes[1].set_xlabel(f"{column_name} [kNm]")
        axes[1].set_ylabel("Depth [m]")
        axes[1].legend()
        axes[1].grid()

        # Plot data for pile 3
        axes[2].plot(pile_3_data[column_name], pile_3_data["y"], label=f"D = {diameters[select]:.3f} m")
        axes[2].set_title("Pile 3: Bending Moment over Depth")
        axes[2].set_xlabel(f"{column_name} [kNm]")
        axes[2].set_ylabel("Depth [m]")
        axes[2].legend()
        axes[2].grid()

    # Adjust layout
    plt.tight_layout()
    plt.show()

# Example usage
x = "x"
y = "y"
Ux = "Ux"
Uy = "Uy"
N = "N"
Q = "Q"
M = "M"
plot_pile_data(diameters, M)
